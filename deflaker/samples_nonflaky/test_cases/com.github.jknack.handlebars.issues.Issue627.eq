@Test
public void eq() throws Exception {
    shouldCompileTo("{{#eq 1 1}}yes{{/eq}}", $, "yes");
    shouldCompileTo("{{#eq 1 2}}yes{{else}}no{{/eq}}", $, "no");
    shouldCompileTo("{{#eq a b}}yes{{/eq}}", $("hash", $("a", "a", "b", "a")), "yes");
    // as expression
    shouldCompileTo("{{eq 1 1}}", $, "true");
    shouldCompileTo("{{eq 1 0}}", $, "false");
    shouldCompileTo("{{eq 1 1 yes='yes' no='no'}}", $, "yes");
    shouldCompileTo("{{eq 1 0 yes='yes' no='no'}}", $, "no");
    // as subexpression
    shouldCompileTo("{{#if (eq 1 1)}}yes{{/if}}", $, "yes");
}
