import networkx as nx
import matplotlib.pyplot as plt

trigger_condition_met = False


def task_1():
    print("checking trigger 1")
    # Imagine some useful work here
    return trigger_condition_met

def task_2():
    print("comparing 2")
    return

def task_3():
    print("Executing Task 3")
    # Imagine some useful work here
    return "Result 3"

def task_4():
    print("Executing Task 4")
    # Imagine some useful work here
    return "Result 4"

def task_5():
    print("Executing Task 5")
    # Imagine some useful work here
    return "Result 5"



# Create a directed graph of tasks
G = nx.DiGraph()

# Add tasks to the graph
G.add_node(1, func=task_1)
G.add_node(2, func=task_2, dependencies=[1])
G.add_node(3, func=task_3, dependencies=[2])
G.add_node(4, func=task_4, dependencies=[2])
G.add_node(5, func=task_5, dependencies=[4])


# Now, explicitly add edges to represent the dependencies
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(2, 4)
G.add_edge(4, 5)

# Draw the graph
# nx.draw(G, with_labels=True, node_size=2000, node_color="lightblue", font_weight="bold", arrows=True)
# plt.show()  # Display the plot
# Starting node
start_node = 2

# Find all endpoints (nodes with no outgoing edges)
endpoints = [node for node in G.nodes() if G.out_degree(node) == 0]

# Find and print all paths from the start node to each endpoint
all_paths = []
for target in endpoints:
    for path in nx.all_simple_paths(G, source=start_node, target=target):
        all_paths.append(path)

print(f"All paths starting from node {start_node}: {all_paths}")

print(f"successor of {start_node}: {list(G.successors(start_node))}")

qwee
def execute_graph(G):
    # Perform a topological sort to determine the execution order
    execution_order = list(nx.topological_sort(G))

    # This dictionary will store the results of each task
    results = {}

    for node in execution_order:
        node_data = G.nodes[node]
        func = node_data["func"]
        if "dependencies" in node_data:
            # If there are dependencies, pass their results as arguments
            args = [results[dep] for dep in node_data["dependencies"]]
            result = func(*args)
        else:
            # If there are no dependencies, just call the function
            result = func()
        results[node] = result
        print(f"Result of {node}: {result}")

# Execute the graph
execute_graph(G)