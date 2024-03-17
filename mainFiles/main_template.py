from lib.template_recognition.manager import Manager
import time



if __name__ == "__main__":
    manager = Manager(processesNumber=5, res=(1920, 1080), multiprocess=True)
    # print(manager)

    # manager.startProcesses()
    # print(manager.templates)
    # manager.startLiveSearching()


