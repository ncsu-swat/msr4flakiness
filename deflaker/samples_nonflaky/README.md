* `test_files` contains all the .java files from which we extracted the test methods. 

* `test_cases` contains all the methods that could be extracted from the `test_files`. The script we used to extract test methods does not always find the target method (in case the test is defined in a superclass, for example). That is the reason why the number of files int the `test_files` and `test_cases` directories do not match.

* `test_cases_sampled` contains the non-flaky test cases that were sampled to build the balanced dataset used in our experiments.

* `test_tokens` contains the vocabulary of tokens we considered for each of the extracted test methods.
