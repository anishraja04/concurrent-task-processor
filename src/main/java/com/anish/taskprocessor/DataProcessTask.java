package com.anish.taskprocessor;

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
