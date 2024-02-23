import multiprocessing
import cv2
import numpy as np

from lib.template_recognition.methods import preliminary_operations as po
from lib.template_recognition.methods.templateMatching import globalMathing


def worker(queue):
    while True:
        task = queue.get()
        if task is None:
            queue.task_done()
            break

        res = globalMathing(task["frame"], task["template"], task["template_name"], task.get("searchArea", None))
        
        print(res)
        queue.task_done()


class Manager():
    def __init__(self):
        self.templates = po.load_all_templates()
        self.cap = cv2.VideoCapture(0)  # 0 is usually the default webcam
        # Imposta l'autoesposizione a 0 (disattiva l'autoesposizione se supportato)
        self.cap.set(getattr(cv2, "CAP_PROP_AUTO_EXPOSURE"), 0.0)  # Nota: 0.25 in OpenCV disattiva l'autoesposizione su alcune webcam
        # Imposta l'esposizione a -7. Nota che il valore effettivo dipende dalla webcam e dal driver
        self.cap.set(getattr(cv2, "CAP_PROP_EXPOSURE"), -6.0)
        self.cap.set(getattr(cv2, "CAP_PROP_BRIGHTNESS"), -50)
        # Set the resolution to 1920x1080
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    


    def main(self):
        num_processes = 4  # Adjust based on your system and requirements
        queue = multiprocessing.JoinableQueue(maxsize=10)  # Adjust size as needed

        # Start worker processes
        processes = [multiprocessing.Process(target=worker, args=(queue,)) for _ in range(num_processes)]
        for p in processes:
            p.daemon = True  # Optionally set as daemon if you want them to terminate with the main process
            p.start()

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Can't receive frame (stream end?). Exiting ...")
                    break
                task = {"frame": frame, "template": self.templates["template"], "template_name": "template"}
                print(task)
                queue.put(task)
        finally:
            # Stop workers by sending a stop signal (None)
            for _ in processes:
                queue.put(None)
            queue.join()  # Wait for all tasks to be processed

        self.cap.release()


manager = Manager()



