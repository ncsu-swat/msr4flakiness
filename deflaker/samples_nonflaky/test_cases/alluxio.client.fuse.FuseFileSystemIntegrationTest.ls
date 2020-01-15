@Test
public void ls() throws Exception {
    // ls -sh has different results in osx
    Assume.assumeTrue(OSUtils.isLinux());
    String testFile = "/lsTestFile";
    createFileInFuse(testFile);
    // Fuse getattr() will wait for file to be completed
    // when fuse release returns but does not finish
    String out = ShellUtils.execCommand("ls", "-sh", sMountPoint + testFile);
    Assert.assertFalse(out.isEmpty());
    Assert.assertEquals("40K", out.split("\\s+")[0]);
    Assert.assertTrue(sFileSystem.exists(new AlluxioURI(testFile)));
    Assert.assertEquals(40 * Constants.KB, sFileSystem.getStatus(new AlluxioURI(testFile)).getLength());
}
