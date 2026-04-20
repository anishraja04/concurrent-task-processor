package com.anish.taskprocessor;

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
