import multiprocessing
import cv2

from lib.template_recognition.methods import preliminary_operations as po
from lib.template_recognition.methods.templateMatching import globalMatching

from typing import Any, Tuple

import traceback
import time

from lib.global_var import fps


# @fps
def worker(task, calculate_fps=None):
    """worker method passed to processes.
    It calls the globalMatching functions using queued tasks

    Args:
        queue (_type_): the multiprocess tasks queue
    """    
    while True:
        # task = queue.get()
        # if task is None:
        #     print("Task queue is empty")
        #     queue.task_done()
        #     break
        
        res = globalMatching(task["frame"], task["template"], task["template_name"], task.get("searchArea", [(0, 0), (0, 0)]), task.get("mask", None))
        # Restituisce il risultato
        return {"presence": res[0], "position": res[1], "template_name": res[2], "confidence": res[3]}
        result_queue.put({"presence": res[0], "position": res[1], "template_name": res[2], "confidence": res[3]})
        # print(task["frame"].mean(), task["template"].mean(), task["template_name"], res[3])

        queue.task_done()

        # calculate_fps()


class Manager():
    def __init__(self, res: Tuple[int, int] = (1920, 1080), camIndex: int = 0, processesNumber: int = 1, showImage: bool = True, multiprocess: bool = False):

        ## BASE SETTINGS
        self.camIndex = camIndex
        self.res = res
        self.show = showImage
        self.run = True

        self.processesNumber = processesNumber

        self.multiprocess = multiprocess
        
        # Set Camera 
        self.create_cap()

        self.set_cap("CAP_PROP_FRAME_WIDTH", self.res[0])
        self.set_cap("CAP_PROP_FRAME_HEIGHT", self.res[1])


        ## VARIABLES
        self.queue = multiprocessing.JoinableQueue(maxsize=20)
        self.pool = None
        self.processes = []
        self.result_queue = multiprocessing.Queue()  # Queue for results

        # Load all templates
        self.templates = po.load_all_templates()
        

    ######################################################
    ##      CAMERA METHODS      ##
    ######################################################        
    def create_cap(self):
        print("connecting to camera, please wait...")
        self.cap = cv2.VideoCapture(self.camIndex)  # 0 is usually the default webcam

        # Imposta l'autoesposizione a 0 (disattiva l'autoesposizione se supportato)
        self.cap.set(getattr(cv2, "CAP_PROP_AUTO_EXPOSURE"), 0.0)  # Nota: 0.25 in OpenCV disattiva l'autoesposizione su alcune webcam
        # Imposta l'esposizione a -7. Nota che il valore effettivo dipende dalla webcam e dal driver
        self.cap.set(getattr(cv2, "CAP_PROP_EXPOSURE"), -6.0)
        self.cap.set(getattr(cv2, "CAP_PROP_BRIGHTNESS"), -50)
        print("camera connected succesfully")


    def set_cap(self, setting: str, value: Any):
        if getattr(cv2, setting, None):
            self.cap.set(getattr(cv2, setting), value)
    


    ######################################################
    ##      MULTIPROCESS METHODS      ##
    ######################################################

    def startProcesses(self):
        if self.multiprocess:
            start_time = time.time()  # Record the start time
            print("starting processes, please wait... ")
            # Start worker processes
            # self.processes = [multiprocessing.Process(target=worker, args=(self.queue, self.result_queue)) for _ in range(self.processesNumber)]
            # for p in self.processes:
            #     p.daemon = True
            #     p.start()
            
            # # Optionally, wait for the processes to become alive (not always necessary)
            # while not all(p.is_alive() for p in self.processes):
            #     time.sleep(0.1)  # Sleep briefly to avoid a busy wait

            # Creare un pool di processi
            self.pool = multiprocessing.Pool(processes=self.processesNumber)

            time.sleep(5)
            end_time = time.time()  # Record the end time after all processes have started
            print(f"Time taken to start worker processes: {end_time - start_time} seconds")
            time.sleep(1)


    def start(self):
        if len(self.processes) == 0 and self.multiprocess and not self.pool:
            print(f"starting {self.processesNumber} processes..")
            self.startProcesses()
        try:
            if len(self.templates.keys()) == 0:
                raise ValueError("No Templates in the template folder!")
            
            # Mostra il risultato del template matching
            while self.run:
                ret, frame = self.cap.read()
                # ret, frame = (True, cv2.imread("./image.jpg"))
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                
                results = {}
                tasks = []
                for template_name, template in self.templates.items():
                    task = {"frame": frame, "template": template["value"], "template_name": template_name, "mask": template["mask"]}

                    if not self.multiprocess:
                        res = globalMatching(task["frame"], task["template"], task["template_name"], task.get("searchArea", [(0, 0), (0, 0)]), task.get("mask", None))
                        if res[0]:
                            results[template_name] = {"position": res[1],
                                                                    "confidence": res[3],
                                                                    "dimension": self.templates[template_name]["value"].shape}
                    else:
                        # self.queue.put(task)
                        # Invia il task al pool di processi
                        async_result = self.pool.apply_async(worker, args=(task,))
                        tasks.append((template_name, async_result))

                
                if self.multiprocess:
                    # Collect results
                    # Raccogli i risultati dai task asincroni
                    for template_name, async_result in tasks:
                        result = async_result.get()
                        print(result["template_name"], result["confidence"])
                        if result["presence"]:
                            results[template_name] = {"position": result["position"], "confidence": result["confidence"], "dimension": self.templates[template_name]["value"].shape}
                    # while not self.result_queue.empty():
                    #     result = self.result_queue.get()
                    #     print(result["template_name"], result["confidence"])
                    #     if result["presence"] == True:
                    #         results[result["template_name"]] = {"position": result["position"],
                    #                                             "confidence": result["confidence"],
                    #                                             "dimension": self.templates[result["template_name"]]["value"].shape}
                        # Process the result as needed
                        
                if self.show:
                    for key, value in results.items():
                        top_left = (value["position"][0], value["position"][1])
                        bottom_right =  (top_left[0]+value["dimension"][1], top_left[1]+value["dimension"][0])
                        cv2.rectangle(frame, top_left, bottom_right, (0,255,0), 2)

                        # Determina se c'è spazio sopra il rettangolo per il testo
                        labelSize, baseLine = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                        if top_left[1] - labelSize[1] - baseLine >= 0:  # Se c'è spazio sopra
                            textOrg = (top_left[0], top_left[1] - baseLine)
                        else:  # Altrimenti, posiziona il testo sotto il rettangolo
                            textOrg = (top_left[0], bottom_right[1] + labelSize[1] + baseLine)

                        # Disegna il nome del template sopra o sotto il rettangolo
                        cv2.putText(frame, key, textOrg, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                    
                    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    cv2.imshow('Matching Result', frame)
                    # Break the loop on pressing 'q'
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                time.sleep(0.1)
                    
        
        except:
            self.run = False
            print(traceback.print_exc())
            if self.multiprocess:
                self.pool.close()  # Chiude il pool di processi
                self.pool.join()   # Attende che tutti i processi nel pool terminino

        finally:
            # Stop workers by sending a stop signal (None)
            self.cap.release()
            self.run = False
            print("\nStopping workers")
            for _ in self.processes:
                self.queue.put(None)
            self.queue.join()  # Wait for all tasks to be processed
            if self.multiprocess:
                self.pool.close()  # Chiude il pool di processi
                self.pool.join()   # Attende che tutti i processi nel pool terminino
        

    def __str__(self):
        return "questo è un oggetto della classe Manager()"

    




