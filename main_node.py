from lib.nodeClasses.nodes import *

# Define a global variable as a trigger condition
trigger_condition_met = False

# Define the trigger condition function for TriggerNode
def check_trigger_condition():
    return trigger_condition_met

# Define a simple function for FunctionNode
def sum_function(a, b):
    return a + b

# Define a condition for ComparatorNode
def is_greater_than_10(x):
    return x > 10

# Create nodes
trigger_node = TriggerNode("trigger1", check_trigger_condition, 0.5)  # Check every 0.5 seconds
function_node = FunctionNode("function1", sum_function)
comparator_node = ComparatorNode("comparator1", is_greater_than_10)

# Assuming you have a mechanism to run these nodes in order based on your workflow...
# For demonstration, we'll manually trigger the condition after a delay

def simulate_workflow():
    print("Workflow started. Waiting for trigger condition...")
    threading.Thread(target=trigger_node.execute).start()

    # Simulate other parts of the program that might eventually meet the trigger condition
    time.sleep(2)  # Wait for 2 seconds before meeting the condition
    global trigger_condition_met
    trigger_condition_met = True
    print("Trigger condition met.")

    # Proceed with function node execution after trigger
    result = function_node.execute(5, 7)  # Example sum function with inputs 5 and 7
    print(f"FunctionNode result: {result}")

    # Comparator node decides the flow based on the function result
    decision = comparator_node.execute(result)
    if decision:
        print("Result is greater than 10.")
    else:
        print("Result is not greater than 10.")

simulate_workflow()
