package com.anish.taskprocessor;

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
