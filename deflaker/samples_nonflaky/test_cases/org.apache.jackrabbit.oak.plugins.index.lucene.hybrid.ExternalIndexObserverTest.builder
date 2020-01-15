@Test
public void builder() throws Exception {
    ExternalObserverBuilder builder = new ExternalObserverBuilder(queue, tracker, NOOP, MoreExecutors.sameThreadExecutor(), 10);
    Observer o = builder.build();
    o.contentChanged(INITIAL_CONTENT, CommitInfo.EMPTY_EXTERNAL);
    verifyZeroInteractions(queue);
}
