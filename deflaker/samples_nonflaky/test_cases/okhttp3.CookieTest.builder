@Test
public void builder() throws Exception {
    Cookie cookie = new Cookie.Builder().name("a").value("b").domain("example.com").build();
    assertThat(cookie.name()).isEqualTo("a");
    assertThat(cookie.value()).isEqualTo("b");
    assertThat(cookie.expiresAt()).isEqualTo(MAX_DATE);
    assertThat(cookie.domain()).isEqualTo("example.com");
    assertThat(cookie.path()).isEqualTo("/");
    assertThat(cookie.secure()).isFalse();
    assertThat(cookie.httpOnly()).isFalse();
    assertThat(cookie.persistent()).isFalse();
    assertThat(cookie.hostOnly()).isFalse();
}
