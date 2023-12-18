import queue

# Create a FIFO queue
fifo_queue = queue.Queue()

# Add items to the queue
fifo_queue.put('item1')
fifo_queue.put('item2')
fifo_queue.put('item3')

# Retrieve items from the queue
while not fifo_queue.empty():
    item = fifo_queue.get()
    print(item)



