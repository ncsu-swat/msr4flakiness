The files with flaky tests are organized in three directories:

test_files: original source file containing flaky test
test_cases: flaky test method (check comment for MISSING_TEST_CASES below)
test_tokens: tokens for the corresponding test method

The data is in the repo, so you only need to run the scripts if you
want to change some part of the extraction process. Find instruction
on how to run the scripts below.

===== To generate the data ======

1. run the script below to save the test files containing flaky tests
in the directory **test_files**. The repository will be cloned/checked
out. Execution of this script should take around 5m on a good internet
connection. 

$> python mine_test_files.py

obs. there are a small number of cases for which we cannot find the
file in the repo

2. run the script below to extract the flaky test cases from each file
under directory "test_cases". The extracted test cases will be stored
in the directory **test_cases**

$> python extract_test_cases.py

obs. The file MISSING_TEST_CASES lists all test files for which we
could not **automatically** extract test cases. The idea is to extract
test cases manually for these files.

3. run the following script to extract the tokens from each test case
(from directory "test_cases") and store those tokens under directory
**test_tokens**

$> ./gentokens.sh