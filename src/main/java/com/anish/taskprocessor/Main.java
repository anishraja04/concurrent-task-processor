package com.anish.taskprocessor;

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
