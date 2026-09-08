# Concurrent Task Processing System

A high-performance, multithreaded task processing engine built in Java. It executes multiple jobs concurrently using thread pools, demonstrating core Object-Oriented Programming (OOP) and Design Pattern concepts.

## Features
- **Concurrency:** Uses Java's `ExecutorService`, `Callable`, and `Future` to run and manage multiple tasks concurrently.
- **Design Patterns:** Implements the Factory pattern (`TaskFactory`) to cleanly instantiate different types of workloads.
- **Thread Safety:** Designed to prevent race conditions during task execution and result collection.
- **Graceful Shutdown:** Ensures all tasks complete or are safely interrupted on shutdown.
- **Robust Logging:** Uses SLF4J and Logback to track thread execution and task failures in real-time.

## Architecture
- `TaskProcessor`: Manages the thread pool and dispatches tasks.
- `Task`: Abstract base class implementing `Callable`.
- `TaskResult`: Immutable record holding the result of a task.
- `DownloadTask` / `DataProcessTask`: Concrete implementations of tasks with distinct workloads.

## Technologies
- **Java 17**
- **Maven**
- **SLF4J / Logback**
- **JUnit 5**

## How to Run

1. Clone the repository.
2. Build the project using Maven:
   ```bash
   mvn clean package
   ```
3. Run the main class:
   ```bash
   mvn exec:java -Dexec.mainClass="com.anish.taskprocessor.Main"
   ```


## Community
Contributions are always welcome. See CONTRIBUTING.md for details.
