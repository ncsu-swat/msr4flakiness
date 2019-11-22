1. run the script below to save the test files containing flaky tests
in the directory "test_files"

$> python mine_test_files.py

TODO: there are several cases for which we cannot find the
files. please check what is the problem

2. run this script to extract the flaky test cases from each file in
test_files and store these test cases under directory "test_cases".

$> ....

3. run the following script to extract the tokens from each test case
in "test_cases" and store those tokens under directory "test_tokens"

$> ./gentokens.sh