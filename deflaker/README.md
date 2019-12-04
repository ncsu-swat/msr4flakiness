*** Description of files ***

Deflaker dataset
  historical_projects.csv - list of project's url

  historical_rerun_flaky_tests.csv - list of flaky tests with reruns
  (<~~ we use this)

  known_flakes_with_versions_run.csv - flaky tests observed through
  different revisions (<~~ we don't use this)

mine_test_files.py - script that processes the dataset. test files are
added to the test_files directory, test cases are added to test_cases
directory, and tokens for each corresponding test_case are added to
the test_tokens directory. files with the same name but different
content are present in each of these directories so one can find
correspondence.

find_potential_features.py - some NLP stuff (tokenization,
segmentation, stemming, stop word removal) to find potential
features. the intuition is that humans read the output to decide what
terms/features should be considered.

frequency_potential_features.py - script that generate coverage matrix
indicating which feature are covered by each document (i.e., file
under test_tokens)