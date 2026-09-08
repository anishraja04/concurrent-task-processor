import os

files = {
    'pom.xml': '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.anish</groupId>
    <artifactId>concurrent-task-processor</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <!-- Logging -->
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>2.0.7</version>
        </dependency>
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>1.4.11</version>
        </dependency>
        <!-- Testing -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-engine</artifactId>
            <version>5.9.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
''',
    'src/main/java/com/anish/taskprocessor/Task.java': '''package com.anish.taskprocessor;

import java.util.concurrent.Callable;

public abstract class Task implements Callable<TaskResult> {
    protected final String taskId;

    public Task(String taskId) {
        this.taskId = taskId;
    }

    public String getTaskId() {
        return taskId;
    }
}
''',
    'src/main/java/com/anish/taskprocessor/TaskResult.java': '''package com.anish.taskprocessor;

public class TaskResult {
    private final String taskId;
    private final boolean success;
    private final String message;

    public TaskResult(String taskId, boolean success, String message) {
        this.taskId = taskId;
        this.success = success;
        this.message = message;
    }

    public String getTaskId() { return taskId; }
    public boolean isSuccess() { return success; }
    public String getMessage() { return message; }

    @Override
    public String toString() {
        return "TaskResult{taskId='" + taskId + "', success=" + success + ", message='" + message + "'}";
    }
}
''',
    'src/main/java/com/anish/taskprocessor/TaskFactory.java': '''package com.anish.taskprocessor;

public class TaskFactory {
    public static Task createTask(String type, String taskId, Object payload) {
        switch (type.toUpperCase()) {
            case "DOWNLOAD":
                return new DownloadTask(taskId, (String) payload);
            case "PROCESS":
                return new DataProcessTask(taskId, (Integer) payload);
            default:
                throw new IllegalArgumentException("Unknown task type: " + type);
        }
    }
}
''',
    'src/main/java/com/anish/taskprocessor/DownloadTask.java': '''package com.anish.taskprocessor;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DownloadTask extends Task {
    private static final Logger logger = LoggerFactory.getLogger(DownloadTask.class);
    private final String url;

    public DownloadTask(String taskId, String url) {
        super(taskId);
        this.url = url;
    }

    @Override
    public TaskResult call() throws Exception {
        logger.info("Task {} started: Downloading from {}", taskId, url);
        // Simulate network delay
        Thread.sleep((long) (Math.random() * 2000 + 500));
        
        if (Math.random() > 0.9) { // 10% chance to fail
            logger.error("Task {} failed during download", taskId);
            return new TaskResult(taskId, false, "Connection timeout");
        }
        
        logger.info("Task {} completed successfully.", taskId);
        return new TaskResult(taskId, true, "Downloaded successfully");
    }
}
''',
    'src/main/java/com/anish/taskprocessor/DataProcessTask.java': '''package com.anish.taskprocessor;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DataProcessTask extends Task {
    private static final Logger logger = LoggerFactory.getLogger(DataProcessTask.class);
    private final int dataSize;

    public DataProcessTask(String taskId, int dataSize) {
        super(taskId);
        this.dataSize = dataSize;
    }

    @Override
    public TaskResult call() throws Exception {
        logger.info("Task {} started: Processing {} records", taskId, dataSize);
        // Simulate heavy CPU processing
        Thread.sleep((long) (dataSize * 10));
        
        logger.info("Task {} completed successfully.", taskId);
        return new TaskResult(taskId, true, "Processed " + dataSize + " records");
    }
}
''',
    'src/main/java/com/anish/taskprocessor/TaskProcessor.java': '''package com.anish.taskprocessor;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

public class TaskProcessor {
    private static final Logger logger = LoggerFactory.getLogger(TaskProcessor.class);
    private final ExecutorService executorService;

    public TaskProcessor(int poolSize) {
        this.executorService = Executors.newFixedThreadPool(poolSize);
        logger.info("Initialized TaskProcessor with pool size: {}", poolSize);
    }

    public List<TaskResult> processTasks(List<Task> tasks) {
        List<Future<TaskResult>> futures = new ArrayList<>();
        List<TaskResult> results = new ArrayList<>();

        for (Task task : tasks) {
            futures.add(executorService.submit(task));
        }

        for (Future<TaskResult> future : futures) {
            try {
                results.add(future.get());
            } catch (InterruptedException | ExecutionException e) {
                logger.error("Error executing task: ", e);
            }
        }
        return results;
    }

    public void shutdown() {
        executorService.shutdown();
        try {
            if (!executorService.awaitTermination(5, TimeUnit.SECONDS)) {
                executorService.shutdownNow();
            }
        } catch (InterruptedException e) {
            executorService.shutdownNow();
        }
    }
}
''',
    'src/main/java/com/anish/taskprocessor/Main.java': '''package com.anish.taskprocessor;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.ArrayList;
import java.util.List;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);

    public static void main(String[] args) {
        logger.info("Starting Concurrent Task Processing System...");
        TaskProcessor processor = new TaskProcessor(4);

        List<Task> tasks = new ArrayList<>();
        for (int i = 1; i <= 5; i++) {
            tasks.add(TaskFactory.createTask("DOWNLOAD", "DL-TASK-" + i, "http://example.com/file" + i));
            tasks.add(TaskFactory.createTask("PROCESS", "PR-TASK-" + i, 100 * i));
        }

        List<TaskResult> results = processor.processTasks(tasks);
        
        long successCount = results.stream().filter(TaskResult::isSuccess).count();
        logger.info("Execution finished. {}/{} tasks successful.", successCount, tasks.size());

        processor.shutdown();
    }
}
''',
    'src/main/resources/logback.xml': '''<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <root level="info">
        <appender-ref ref="STDOUT" />
    </root>
</configuration>
''',
    'src/test/java/com/anish/taskprocessor/TaskProcessorTest.java': '''package com.anish.taskprocessor;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class TaskProcessorTest {
    private TaskProcessor taskProcessor;

    @BeforeEach
    public void setup() {
        taskProcessor = new TaskProcessor(2);
    }

    @AfterEach
    public void teardown() {
        taskProcessor.shutdown();
    }

    @Test
    public void testTaskProcessing() {
        Task t1 = TaskFactory.createTask("PROCESS", "T1", 50);
        Task t2 = TaskFactory.createTask("PROCESS", "T2", 50);

        List<TaskResult> results = taskProcessor.processTasks(Arrays.asList(t1, t2));
        
        assertEquals(2, results.size());
        assertTrue(results.get(0).isSuccess());
        assertTrue(results.get(1).isSuccess());
    }
}
''',
    'README.md': '''# Concurrent Task Processing System

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
''',
    '.gitignore': '''target/
*.class
.idea/
*.iml
'''
}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Files created.")
