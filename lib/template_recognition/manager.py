import multiprocessing
import cv2

from lib.template_recognition.methods import preliminary_operations as po
from lib.template_recognition.methods.templateMatching import globalMatching

from typing import Any, Tuple

from lib.global_var import fps


def worker(queue):
    """worker method passed to processes.
    It calls the globalMatching functions using queued tasks

    Args:
        queue (_type_): the multiprocess tasks queue
    """    
    while True:
        task = queue.get()
        if task is None:
            queue.task_done()
            break

        res = globalMatching(task["frame"], task["template"], task["template_name"], task.get("searchArea", [(0, 0), (0, 0)]), task.get("mask", None))
        print(res)
        queue.task_done()


class Manager():
    def __init__(self, res: Tuple[int, int] = (1920, 1080), camIndex: int = 0, processesNumber: int = 4):

        ## BASE SETTINGS
        self.camIndex = camIndex
        self.res = res

        self.processesNumber = processesNumber
        
        # Set Camera 
        self.create_cap()

        self.set_cap("CAP_PROP_FRAME_WIDTH", self.res[0])
        self.set_cap("CAP_PROP_FRAME_HEIGHT", self.res[1])


        ## VARIABLES
        self.queue = multiprocessing.JoinableQueue(maxsize=self.processesNumber+1)
        self.processes = []

        # Load all templates
        self.templates = po.load_all_templates()
        

    ######################################################
    ##      CAMERA METHODS      ##
    ######################################################        
    def create_cap(self):
        self.cap = cv2.VideoCapture(self.camIndex)  # 0 is usually the default webcam

        # Imposta l'autoesposizione a 0 (disattiva l'autoesposizione se supportato)
        self.cap.set(getattr(cv2, "CAP_PROP_AUTO_EXPOSURE"), 0.0)  # Nota: 0.25 in OpenCV disattiva l'autoesposizione su alcune webcam
        # Imposta l'esposizione a -7. Nota che il valore effettivo dipende dalla webcam e dal driver
        self.cap.set(getattr(cv2, "CAP_PROP_EXPOSURE"), -6.0)
        self.cap.set(getattr(cv2, "CAP_PROP_BRIGHTNESS"), -50)


    def set_cap(self, setting: str, value: Any):
        if getattr(cv2, setting, None):
            self.cap.set(getattr(cv2, setting), value)
    


    ######################################################
    ##      MULTIPROCESS METHODS      ##
    ######################################################

    def startProcesses(self):
        # Start worker processes
        self.processes = [multiprocessing.Process(target=worker, args=(self.queue,)) for _ in range(self.processesNumber)]
        for p in self.processes:
            p.daemon = True  # Optionally set as daemon if you want them to terminate with the main process
            p.start()


    @fps
    def start(self):
        if len(self.processes) == 0:
            self.startProcesses()
        try:
            if len(self.templates.keys()) == 0:
                raise ValueError("No Templates in the template folder!")
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                for template_name, template in self.templates.items():
                    task = {"frame": frame, "template": template["value"], "template_name": template_name, "mask": template["mask"]}
                    self.queue.put(task)
        finally:
            # Stop workers by sending a stop signal (None)
            print("Stopping workers")
            for _ in self.processes:
                self.queue.put(None)
            self.queue.join()  # Wait for all tasks to be processed
            print(self.processes)
        self.cap.release()
        

    

manager = Manager()



