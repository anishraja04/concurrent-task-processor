package com.anish.taskprocessor;

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
