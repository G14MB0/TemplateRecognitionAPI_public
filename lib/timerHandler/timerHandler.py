'''
This Module define a multithread method to define repetitive tasks
it uses schedule to define a repetitive tasks and wrap it in the "define_task" method

##USAGE:
print ciccio every 2 seconds:

def foo(ciccio):
    print(ciccio)

define_task(2, "s", foo, ciccio)

'''


import schedule
import threading
import time
import signal

# Flag to control the scheduler loop
stop_scheduler = False

def run_task(job_func):
    """this method encapsulate the job_func (the input method to be executed periodically)
    and send it in a separate thread
    is used by define_task

    Args:
        job_func (_type_): a function object

    Returns:
        _type_: the newly created thread
    """    
    job_thread = threading.Thread(target=job_func)
    job_thread.start()
    return job_thread

def run_scheduler():
    """this runs all the thread
    """    
    global stop_scheduler
    while not stop_scheduler:
        schedule.run_pending()
        time.sleep(1)

def define_task(interval: int, mu: str, function, *args):
    """this encapsulate the schedule module

    Args:
        interval (int): the interval
        mu (_type_): the measure unit (i.e. "s" for seconds, "m" for minutes ...)
        function (_type_): _description_

    Returns:
        _type_: the schedule object
    """    
    job = None
    if mu == "s":
        job = schedule.every(interval).seconds.do(lambda: run_task(function(*args)))
    elif mu == "m":
        job = schedule.every(interval).minutes.do(lambda: run_task(function(*args)))
    elif mu == "h":
        job = schedule.every(interval).hours.do(lambda: run_task(function(*args)))
    elif mu == "d":
        job = schedule.every(interval).days.do(lambda: run_task(function(*args)))
    return job


def stop_all_tasks():
    """simply cancel all the task
    """    
    # Cancel all scheduled jobs
    for job in schedule.jobs:
        schedule.cancel_job(job)


def destroy():
    """destroy the thread
    """    
    global stop_scheduler
    stop_scheduler = True


# Run the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

