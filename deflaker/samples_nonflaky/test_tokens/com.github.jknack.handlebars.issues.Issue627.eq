no
a
{{eq 1 1 yes='yes' no='no'}}
{{#eq a b}}yes{{/eq}}
b
$
yes
false
{{#if (eq 1 1)}}yes{{/if}}
eq
{{#eq 1 1}}yes{{/eq}}
{{#eq 1 2}}yes{{else}}no{{/eq}}
{{eq 1 1}}
{{eq 1 0}}
 as subexpression
true
shouldCompileTo
 as expression
{{eq 1 0 yes='yes' no='no'}}
hash
