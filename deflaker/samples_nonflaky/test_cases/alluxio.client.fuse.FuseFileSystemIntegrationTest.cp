@Test
public void cp() throws Exception {
    String testFile = "/cpTestFile";
    String content = "Alluxio Cp Test File Content";
    File localFile = generateFileContent("/TestFileOnLocalPath", content.getBytes());
    ShellUtils.execCommand("cp", localFile.getPath(), sMountPoint + testFile);
    Assert.assertTrue(sFileSystem.exists(new AlluxioURI(testFile)));
    // Fuse release() is async
    // Cp again to make sure the first cp is completed
    String testFolder = "/cpTestFolder";
    ShellUtils.execCommand("mkdir", sMountPoint + testFolder);
    ShellUtils.execCommand("cp", sMountPoint + testFile, sMountPoint + testFolder + testFile);
    Assert.assertTrue(sFileSystem.exists(new AlluxioURI(testFolder + testFile)));
    byte[] read = new byte[content.length()];
    try (FileInStream is = sFileSystem.openFile(new AlluxioURI(testFile), OpenFilePOptions.newBuilder().setReadType(ReadPType.NO_CACHE).build())) {
        is.read(read);
    }
    Assert.assertEquals(content, new String(read, "UTF8"));
}
