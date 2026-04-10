package com.anish.taskprocessor;

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
