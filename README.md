# msr4flakiness

Setup:

  $> ./createvenv

Steps:

1. The file /output/issues.txt lists the GitHub issues related to flaky tests that we downloaded with the script mine.py. 

2. The files under the directory /data correspond to the body of the flaky tests for the issues from /output/issues.txt. These files were extracted manually.

3. The script find_features.py processes the files under the directory data to produce a list of words which are more common across tests.
