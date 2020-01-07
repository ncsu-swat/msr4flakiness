@Test
public void trigger() throws Exception {
    RunClassInSeparateJvmMachine machine = mock(RunClassInSeparateJvmMachine.class);
    DelayedRestartTrigger restartTrigger = new DelayedRestartTrigger(machine);
    // no settling
    restartTrigger.setSettleDownMillis(10);
    try {
        restartTrigger.start();
        assertEquals(0, restartTrigger.getRestartCount());
        assertEquals(0, restartTrigger.getAccumulatedTriggerCount());
        // thread needs to be waiting after start
        waitOrTimeout(Conditions.isWaiting(restartTrigger), Timeout.timeout(millis(10000)));
        restartTrigger.trigger();
        verify(machine, timeout(10000)).restart();
        // thread needs to be waiting after restart
        waitOrTimeout(Conditions.isWaiting(restartTrigger), Timeout.timeout(millis(10000)));
        assertEquals(1, restartTrigger.getRestartCount());
        assertEquals(0, restartTrigger.getAccumulatedTriggerCount());
    } finally {
        restartTrigger.shutdown();
    }
}
