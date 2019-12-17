@Test
public void go() throws IOException, InterruptedException {
    if (!isConformingHost()) {
        return;
    }
    Process p = runLoopFSScript(LoopFSCommand.shake);
    for (int i = 0; i < NUM_STEPS; i++) {
        fa.append(String.valueOf(i) + LONG_STR);
        Thread.sleep(DELAY);
    }
    p.waitFor();
    // the extrernal script has the file system ready for IO 50% of the time
    double bestCase = 0.5;
    ResilienceUtil.verify(logfileStr, "^(\\d{1,3}) x*$", NUM_STEPS, bestCase * 0.6);
    System.out.println("Done go");
}
