package com.anish.taskprocessor;

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
