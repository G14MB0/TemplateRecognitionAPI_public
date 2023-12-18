import importlib
module = importlib.import_module("lib.global_var")

def createReport(info):
    print("**** GENERATING REPORT ****")
    print(info)

    if not hasattr(module, "962.CSM_BAT_CURRENT"):
        print(f"{module} has no attribute 962.CSM_BAT_CURRENT")
        return
    
    g_current = getattr(module, "962.CSM_BAT_CURRENT")
    
    if g_current.empty():
        print("Empty")
        return 0  # Return 0 or None if you prefer, for an empty queue

    total = 0
    count = 0

    while not g_current.empty():
        item = g_current.get()
        total += item
        count += 1

    average = total / count

    print(f"average current: {average}")

    if not hasattr(module, "g_q_Voltage"):
        print(f"{module} has no attribute g_q_Voltage")
        return
    
    g_batt = getattr(module, "g_q_Voltage")
    
    if g_batt.empty():
        print("Empty")
        return 0  # Return 0 or None if you prefer, for an empty queue

    total = 0
    count = 0

    while not g_batt.empty():
        item = g_batt.get()
        total += item
        count += 1

    average = total / count
    print(average)