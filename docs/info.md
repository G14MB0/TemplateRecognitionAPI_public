---
##### In this page you can find some info about the functionality of the app's methods
---
## "workers" parameter of uvicorn.run()

The workers parameter in the uvicorn.run method is used to specify the number of worker processes for handling requests. 

Here's a breakdown of what the workers parameter does:

- Multiprocess Handling: When you set the workers parameter, Uvicorn will spawn that number of worker processes. Each worker process runs its own independent instance of the application. This is a simple way to enable concurrent handling of requests and can increase the throughput of your application, especially on multi-core systems.

- Load Distribution: Each worker can handle requests independently. The operating system's process scheduler will distribute incoming requests among these workers. This helps in utilizing multiple CPU cores and managing a higher load, as each process can handle requests in parallel.

- Increased Reliability: Having multiple workers can also increase the reliability of the application. If one worker process encounters an issue and crashes, the other worker processes can continue to handle requests. This ensures that the application remains available even in the case of individual process failures.

- Use Case: The workers parameter is particularly useful when deploying production applications. In development, you usually don't need multiple workers, especially when the reload option is set to True for automatic reloading of code changes.

- Limitations: It's important to note that these workers do not share memory or state. If your application requires shared state or IPC (Inter-Process Communication), you'll need to implement an external system for that (like a database or a caching system).

- Choosing the Number of Workers: The optimal number of workers depends on the specifics of your application and your server's hardware. A common heuristic is to use 2-4 workers per CPU core.

---
