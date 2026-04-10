package com.anish.taskprocessor;

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
