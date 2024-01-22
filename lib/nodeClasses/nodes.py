import time
import threading

class Node:
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def execute(self):
        pass  # To be overridden by subclasses



class FunctionNode(Node):
    """A function Node extend the Node class as a type: "function"
    
    Define also function: function
    """    
    def __init__(self, id, function):
        super().__init__(id, "function")
        self.function = function

    def execute(self, *args):
        return self.function(*args)
    


class ComparatorNode(Node):
    def __init__(self, id, condition):
        super().__init__(id, "comparator")
        self.condition = condition

    def execute(self, *args):
        return self.condition(*args)



class TriggerNode(Node):
    def __init__(self, id, trigger_condition_func, polling):
        super().__init__(id, "trigger")
        self.trigger_condition_func = trigger_condition_func
        self.polling = polling
        self.triggered = False  # This flag will indicate whether the trigger condition has been met

    def check_trigger(self):
        """Check the trigger condition in a loop."""
        while not self.triggered:
            self.triggered = self.trigger_condition_func()
            if not self.triggered:
                time.sleep(self.polling)


    def execute(self):
        trigger_thread = threading.Thread(target=self.check_trigger)
        trigger_thread.start()
        trigger_thread.join()  # Wait for the trigger condition to be met
        return self.triggered