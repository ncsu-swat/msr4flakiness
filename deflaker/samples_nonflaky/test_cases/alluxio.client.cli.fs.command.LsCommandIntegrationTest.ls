/**
 * Tests ls command when security is enabled.
 */
@Test
@LocalAlluxioClusterResource.Config(confParams = { PropertyKey.Name.SECURITY_AUTHORIZATION_PERMISSION_ENABLED, "true", PropertyKey.Name.SECURITY_AUTHENTICATION_TYPE, "SIMPLE", PropertyKey.Name.SECURITY_GROUP_MAPPING_CLASS, "alluxio.security.group.provider.IdentityUserGroupsMapping", PropertyKey.Name.SECURITY_AUTHORIZATION_PERMISSION_SUPERGROUP, "test_user_ls" })
public void ls() throws Exception {
    createFiles("test_user_ls");
    mFsShell.run("ls", "/testRoot");
    // CHECKSTYLE.OFF: LineLengthExceed - Improve readability
    checkOutput("drwxr-xr-x  test_user_ls   test_user_ls                 1   NOT_PERSISTED .+ .+  DIR /testRoot/testDir", "-rw-r--r--  test_user_ls   test_user_ls                10   NOT_PERSISTED .+ .+ 100% /testRoot/testFileA", "-rw-r--r--  test_user_ls   test_user_ls                30       PERSISTED .+ .+   0% /testRoot/testFileC");
// CHECKSTYLE.ON: LineLengthExceed
}
