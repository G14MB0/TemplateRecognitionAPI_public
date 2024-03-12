import multiprocessing
import queue
import cv2

from lib.template_recognition.methods import preliminary_operations as po
from lib.template_recognition.methods import aruco_operations as ao
from lib.template_recognition.methods.templateMatching import globalMatching
from lib.template_recognition.methods.file_operation import saveFrameWithTemplates
from lib import local_config
from lib.global_var import g_matching_threshold

from typing import Any, Tuple, List

import traceback
import time

from lib.global_var import fps, logFunctionDetail, logger




# @fps
def worker(task, calculate_fps=None):
    """worker method passed to processes.
    It calls the globalMatching functions using queued tasks

    Args:
        queue (_type_): the multiprocess tasks queue
    """    
    while True:
        
        res = globalMatching(task["frame"], task["template"], task["template_name"], search_area=task.get("searchArea", [(0, 0), (0, 0)]), mask=task.get("mask", None), threshold=task.get("threshold", None), isColored=task.get("isColored", False))
        if calculate_fps: calculate_fps()
        
        return {"presence": res[0], "position": res[1], "template_name": res[2], "confidence": res[3]}


def gui_process(frame_queue):
    print("START GUI PROCESS")
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            if frame is None:
                break
            elif isinstance(frame, str):
                cv2.destroyAllWindows()
                continue
            else:
                cv2.namedWindow('Frame', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    pass

class Manager():
    def __init__(self, 
                 res: Tuple[int, int] = (1920, 1080), 
                 camIndex: int = 0, 
                 processesNumber: int = 1, 
                 showImage: bool = True, 
                 showImageGray: bool = False, 
                 multiprocess: bool = False, 
                 **kwargs):
        
        """ Constructor of Manager class.

        Args:
            processNumber (int): number of processes for template matching
            resolution (Tuple[int, int], optional): camera resolution. Defaults to (1920, 1080).
            multiprocess (bool, optional): if true, activate the multiprocess. Defaults to True.
            camIndex (int, optional): index of the USB camera, depends on how Windows chose index for usb camera. Defaults to 1.
            showImage (bool, optional): If true, show a live video in proper methods. Defaults to False.
            showImageGray (bool, optional): if true, the image (showImage) is converted to gray. Defaults to False.
        """        
        
        #____________________________________________________#
        #-      ATTRIBUTE DEFINITIONS                       -#
        #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾#  

        if "saveFrame" in kwargs.keys():
            self.saveFrame = kwargs["saveFrame"]
            self.saving_folder = local_config.readLocalConfig().get("saving_folder", "")
        else:
            self.saveFrame = False

        ## BASE SETTINGS
        self.camIndex = camIndex
        self.res = res
        self.show = showImage
        self.showImageGray = showImageGray
        self.run = True
        self.isColored = local_config.readLocalConfig().get("is_colored", True)

        self.processesNumber = processesNumber
        self.multiprocess = multiprocess

        ## VARIABLES
        self.pool = None
        self.processes = []
        self.frame_queue = multiprocessing.Queue()
        self.gui_proc = None
        self.lastLiveValue = {}
        
        self.lastLiveValueQueue = queue.Queue()
        self.isLastLiveValueQueue = False

        self.liveTemplateList = []

        self.threshold = float(g_matching_threshold)

        #____________________________________________________#
        #-      PRELIMINARY OPERATIONS                      -#
        #‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾#
        
        print("Loading Templates")
        # Load all templates
        self.setupDistance = ao.calculateSetupDistance(self.res, self.camIndex)
        if self.setupDistance == -1:
            self.setupDistance = float(local_config.readLocalConfig().get("DEFAULT_DISTANCE", -1))
        
        self.templates = po.scale_all_templates(po.load_all_templates(), self.setupDistance, res)
        print("Templates Loaded")
        
        # for key, template in self.templates.items():
        #     cv2.imshow(key, template["value"])
        
        # # Wait for a key press and then destroy all windows
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # Set Camera 
        self.create_cap()

        self.set_cap("CAP_PROP_FRAME_WIDTH", self.res[0])
        self.set_cap("CAP_PROP_FRAME_HEIGHT", self.res[1])

    ######################################################
    ##      GENERIC METHODS      ##
    ######################################################
    def loadAllTemplates(self):
        self.templates = po.scale_all_templates(po.load_all_templates(), self.setupDistance, self.res)

    ######################################################
    ##      CAMERA METHODS      ##
    ######################################################        
    def create_cap(self):
        print("connecting to camera, please wait...")
        self.cap = cv2.VideoCapture(self.camIndex, cv2.CAP_DSHOW)  # 0 is usually the default webcam

        # Imposta l'autoesposizione a 0 (disattiva l'autoesposizione se supportato)
        self.cap.set(getattr(cv2, "CAP_PROP_AUTO_EXPOSURE"), 0.25)  # Nota: 0.25 in OpenCV disattiva l'autoesposizione su alcune webcam
        # Imposta l'esposizione a -7. Nota che il valore effettivo dipende dalla webcam e dal driver
        self.cap.set(getattr(cv2, "CAP_PROP_EXPOSURE"), -6.0)
        self.cap.set(getattr(cv2, "CAP_PROP_BRIGHTNESS"), -50)
        print("camera connected succesfully")



    def set_cap(self, setting: str, value: Any) -> bool:
        setting_id = getattr(cv2, setting, None)
        if setting_id:
            # Attempt to apply the setting
            success = self.cap.set(setting_id, value)
            # Check if the setting was applied successfully
            if success:
                print(f"Setting {setting} applied successfully.")
                return True
            else:
                print(f"Failed to apply setting {setting}.")
        else:
            print(f"Setting {setting} is not recognized.")
        return False

    


    ######################################################
    ##      MULTIPROCESS METHODS      ##
    ######################################################

    def startProcesses(self):
        """start the multiprocess execution pool.
        """        
        self.gui_proc = multiprocessing.Process(target=gui_process, args=(self.frame_queue, ))
        self.gui_proc.start()

        if self.multiprocess:
            start_time = time.time()  # Record the start time
            print("starting processes, please wait... ")
            
            # create process pool
            self.pool = multiprocessing.Pool(processes=self.processesNumber)

            time.sleep(1)
            end_time = time.time()  # Record the end time after all processes have started
            print(f"Time taken to start worker processes: {end_time - start_time} seconds")
            return
        else:
            return
        

    

    def startInstantTrigger(self, templates: List = [str]) -> dict:
        """This methods perform a template matching of templates (a list of template name)
        it repeat the process 3 times and if at least one time a template is found, it's appended to the results

        if self.saveFrame is True, save the current frame locally

        Args:
            templates (List, optional): List of templates name. Defaults to [].

        Returns:
            dict: dicitonary of results (keys -> position: tuple, confidence: float)
        """    
        if self.pool is None:
            print("multiprocess pool not initialized yet, please call startProcesses first")
            logger.warning("multiprocess pool not initialized yet, please call startProcesses first")
            if self.multiprocess:
                raise RuntimeError("multiprocess pool not initialized yet, please call startProcesses first")
        # Lista per tenere traccia dei template mancanti
        missing_templates = [template_name for template_name in templates if template_name not in self.templates]

        # Verifica se ci sono template mancanti e li logga
        if missing_templates:
            logger.debug(f"Passed wrong template name in InstantTrigger  {missing_templates}")

        frame = None
        globalResults = {}
        for _ in range(3):
            ret, frame = self.cap.read()
            current = time.time()
            # ret, frame = (True, cv2.imread("./image.jpg"))
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            results = {}
            tasks = []
            for template_name, template in self.templates.items():
                if template_name in templates:
                    task = {"frame": frame, "template": template["value"], "template_name": template_name, "mask": template["mask"], "threshold": self.threshold, "isColored": self.isColored}

                    if not self.multiprocess:
                        # do template matching and append to results the result
                        res = globalMatching(task["frame"], task["template"], task["template_name"], task.get("searchArea", [(0, 0), (0, 0)]), task.get("mask", None))
                        if res[0]:
                            results[template_name] = {"position": res[1], "confidence": res[3], "dimension": self.templates[template_name]["value"].shape}
                    else:
                        # send to the pool executor the task
                        async_result = self.pool.apply_async(worker, args=(task,))
                        tasks.append((template_name, async_result))

                if self.multiprocess:
                    # Collect results of tasks previously sent to pool executor
                    for template_name, async_result in tasks:
                        result = async_result.get()
                        if result["presence"]:
                            results[template_name] = {"position": result["position"], "confidence": result["confidence"], "dimension": self.templates[template_name]["value"].shape}

            print(f"inner instant check tooks: {time.time() - current}ms")
            self.setLastLiveValue(results)

            for key, item in results.items():
                if not key in globalResults.keys():
                    globalResults[key] = item

        if self.saveFrame and frame is not None: saveFrameWithTemplates(frame, globalResults, self.saving_folder)

        return globalResults


    def startLiveTrigger(self):
        """This methods start a live template matching using only templates in input

        Args:
            templates (List, optional): name list of all templates. Defaults to [].
        """     
        if self.pool is None:
            print("multiprocess pool not initialized yet, please call startProcesses first")
            logger.warning("multiprocess pool not initialized yet, please call startProcesses first")   
            if self.multiprocess:
                raise RuntimeError("multiprocess pool not initialized yet, please call startProcesses first")
        # Lista per tenere traccia dei template mancanti
        missing_templates = [template_name for template_name in self.liveTemplateList if template_name not in self.templates]

        # Verifica se ci sono template mancanti e li logga
        if missing_templates:
            logger.debug(f"Passed wrong template name in InstantTrigger  {missing_templates}")


        self.run = True
        while self.run:
            ret, frame = self.cap.read()
            # ret, frame = (True, cv2.imread("./image.jpg"))
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            results = {}
            tasks = []
            for template_name, template in self.templates.items():
                if template_name in self.liveTemplateList:
                    task = {"frame": frame, "template": template["value"], "template_name": template_name, "mask": template["mask"], "threshold": self.threshold, "isColored": self.isColored}

                    if not self.multiprocess:
                        # do template matching and append to results the result
                        res = globalMatching(task["frame"], task["template"], task["template_name"], task.get("searchArea", [(0, 0), (0, 0)]), task.get("mask", None))
                        if res[0]:
                            results[template_name] = {"position": res[1], "confidence": res[3], "dimension": self.templates[template_name]["value"].shape}
                    else:
                        # send to the pool executor the task
                        async_result = self.pool.apply_async(worker, args=(task,))
                        tasks.append((template_name, async_result))

            if self.multiprocess:
                # Collect results of tasks previously sent to pool executor
                for template_name, async_result in tasks:
                    result = async_result.get()
                    if result["presence"]:
                        results[template_name] = {"position": result["position"], "confidence": result["confidence"], "dimension": self.templates[template_name]["value"].shape}

            self.setLastLiveValue(results)

            if self.show:
                # Show results to a live video
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
                    cv2.putText(frame, f"{key} - conf: {round(value["confidence"], 2)}", textOrg, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
                if self.showImageGray: frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Send frame to GUI process for display
                self.frame_queue.put(frame)

        self.frame_queue.put("pause")

        


    def stopLiveTrigger(self):
        """Stop live matching
        """        
        self.run = False


    def startLiveVideo(self):
        """Start a live video of the camera input
        """     
        self.run = True   
        while self.run:
            ret, frame = self.cap.read()
            # ret, frame = (True, cv2.imread("./image.jpg"))
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                raise RuntimeError("Can't receive frame (stream end?). Exiting ...")
            
            if self.showImageGray: frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Matching Result', frame)
            # Break the loop on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


    def startLiveSearching(self):
        """This method start a live template matching on the camera input using all template in the template folder.

        Raises:
            ValueError: If no template in the template folder, break the loop
        """  
        self.run = True   
        if self.pool is None:
            print(f"starting {self.processesNumber} processes..")
            self.startProcesses()
        try:
            if len(self.templates.keys()) == 0:
                raise ValueError("No Templates in the template folder!")
            
            while self.run:
                ret, frame = self.cap.read()
                # ret, frame = (True, cv2.imread("./image.jpg"))
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                
                results = {}
                tasks = []
                for template_name, template in self.templates.items():
                    task = {"frame": frame, "template": template["value"], "template_name": template_name, "mask": template["mask"], "threshold": self.threshold, "isColored": self.isColored}

                    if not self.multiprocess:
                        # do template matching and append to results the result
                        res = globalMatching(task["frame"], task["template"], task["template_name"], task.get("searchArea", [(0, 0), (0, 0)]), task.get("mask", None))
                        if res[0]:
                            results[template_name] = {"position": res[1],
                                                                    "confidence": res[3],
                                                                    "dimension": self.templates[template_name]["value"].shape}
                    else:
                        # send to the pool executor the task
                        async_result = self.pool.apply_async(worker, args=(task,))
                        tasks.append((template_name, async_result))

                
                if self.multiprocess:
                    # Collect results of tasks previously sent to pool executor
                    for template_name, async_result in tasks:
                        result = async_result.get()
                        if result["presence"]:
                            results[template_name] = {"position": result["position"], "confidence": result["confidence"], "dimension": self.templates[template_name]["value"].shape}        
            
                if self.show:
                    # Show results to a live video
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
                    
                    if self.showImageGray: frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    cv2.imshow('Matching Result', frame)
                    # Break the loop on pressing 'q'
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                time.sleep(0.1)
                self.setLastLiveValue(results)
        
        except:
            self.run = False
            print(traceback.print_exc())
            if self.multiprocess and self.pool is not None:
                self.pool.close()  # Chiude il pool di processi
                self.pool.join()   # Attende che tutti i processi nel pool terminino

        finally:
            # Stop workers by sending a stop signal (None)
            self.run = False
            print("\nStopping workers")
            


    @logFunctionDetail
    def stop(self):
        print("Stopping manager operation ...")
        self.run = False
        self.frame_queue.put(None)
        if self.multiprocess and self.pool is not None:
            self.pool.close()  # Chiude il pool di processi
            self.pool.join()   # Attende che tutti i processi nel pool terminino

        cv2.destroyAllWindows()


    @logFunctionDetail
    def close(self):
        self.stop()
        self.cap.release()


    ######################################################
    ##    METODI GETTER SETTER PER TEMPLATE MATCHING    ##
    ######################################################
        
    def setLastLiveValue(self, value):
        self.lastLiveValue = value
        if self.isLastLiveValueQueue:
            self.lastLiveValueQueue.put(value)
        
    def getLastLiveValue(self):
        if self.isLastLiveValueQueue:
            return self.lastLiveValueQueue.get()
        return self.lastLiveValue


    def getInfo(self):
        """
        Gathers and returns information about the current configuration and state of the instance.

        Returns:
            dict: A dictionary containing key-value pairs of attributes and their current values.
        """
        info = {
            "saveFrame": self.saveFrame,
            "saving_folder": self.saving_folder if hasattr(self, 'saving_folder') else "Not Set",
            "camIndex": self.camIndex,
            "resolution": self.res,
            "showImage": self.show,
            "showImageGray": self.showImageGray,
            "run": self.run,
            "isColored": self.isColored,
            "processesNumber": self.processesNumber,
            "multiprocess": self.multiprocess,
            "threshold": self.threshold,
            "setupDistance": self.setupDistance,
            # Additional info about processes and templates might need a more complex representation
            "processes": len(self.processes),
            "templatesLoaded": len(self.templates) if hasattr(self, 'templates') else "Not Loaded",
        }

        return info


    def __str__(self):
        ### VA POPOLATA PER STAMPARE TUTTE LE INFO
        return str(self.getInfo())
    


    




