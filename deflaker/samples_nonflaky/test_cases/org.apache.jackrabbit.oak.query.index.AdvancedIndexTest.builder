@Test
public void builder() {
    IndexPlan.Builder b = new IndexPlan.Builder();
    IndexPlan plan = b.setEstimatedEntryCount(10).build();
    assertEquals(10, plan.getEstimatedEntryCount());
    b.setEstimatedEntryCount(20);
    assertEquals(10, plan.getEstimatedEntryCount());
}
