@Test
public void move() {
    DocumentMK mk = createMK();
    String rev = mk.commit("/", "+\"test\":{\"x\":\"1\",\"child\": {}}", null, null);
    rev = mk.commit("/", ">\"test\": \"/test2\"", rev, null);
    String test = mk.getNodes("/test2", rev, 0, 0, Integer.MAX_VALUE, null);
    assertEquals("{\"x\":\"1\",\"child\":{},\":childNodeCount\":1}", test);
    test = mk.getNodes("/test", rev, 0, 0, Integer.MAX_VALUE, null);
    assertNull(test);
}
