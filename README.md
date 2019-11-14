# msr4flakiness

Obs. if you need to run any of the python scripts listed in this repo, please run first the script "createvenv". It will load all necessary dependencies.

* The file /output/issues.txt lists the GitHub issues related to flaky tests downloaded with the script mine.py. You don't need to run this script again unless you want to change the selection criterion.

* The files under the directory /data correspond to the body of the flaky tests for the issues from /output/issues.txt. These files were extracted manually.

* The script find_features.py processes the files under the directory data <b><i>to produce a list of words which are more common across tests</i></b>. 
