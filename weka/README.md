# Machine Learning Classifiers

This document gives the step by step guidance to replicate ML classfier results through WEKA

## Arff Files

- Arff Files represent data sets used for ML Classfiers. They are all stored in arffiles folder
- tokenslockeywordskeywordcount.arff arfile contains the data to reproduce the results displayed in table 3
- Other arff files are used to generate the results reperesented in table 4

## How to Run Weka?

1. Download Weka version 3.8.3 from here: https://www.cs.waikato.ac.nz/ml/weka/
2. Open Weka
3. Click Explorer

## PreProcessing
4. Click PreProcess Tab
5. Click Open File-> select tokenslockeywordskeywordcount.arff
6. In Attributes section, click @@class@@
7. Under the filter section, click "Choose" -> Filters -> unsupervised -> attribute -> StringToWordVector
-click on the box where StringToWordVector features appear in order to modify the preprocessing steps (e.g.: stop-word removal, stemmer, tokenizers etc.
Click Apply

## Classifier
8. Click Classify tab
9. Click the drop down list under more options -> select (nom)@@class@@
9. Choose an algorithm (again algorithm attributes could be modified by clicking on the box where the algorithm name appears- number of iterations were changed in this manner (e.g. for RandomForest we ran iterations of 5, 10, 50, 100, 500 and 1000 and these results are availble in "Random Forest Iteration folder).
10. Under the Test Options, test options could be modified. In our experiments, we ran 80% split.
11. Click Start
12. The section "Classifier output" (==Run Information==) depicts the features of the classifier for replication purposes. Results for IBK, Random Forest, J48, Naive Bayes and SMO are available in the Machine Learning Classifiers Folder. Furthermore, the Random Forest and SMO  were rerun without certain tokens as it is depicted in table 4. Results for these classifiers are available in folders such as No Lower Case, No Stemmer, No Identifiers etc.

## Infomation Gained
13. Select Attribute Tab
14. Select (nom)@@class@@ from the drop down list above the start button
15. Click Choose under Attribute Evaluator -> Select the option InfoGainAttributeEval
16. Click Choose under Search Method -> Click Ranker -> Click on the Ranker box and change the threshold value to 0.02
17. Click Start
18. "Information Gained After Attribute Selection" file shows the results for this. These are the results depicted in table 5

## ML Models

19. ML Models folder contains Machine Learning models to recreate the results from 5 machine learning classifier algorithms. Click Classify Tab -> Right Click in Results List -> Load Model -> Browse to the required machine learning model.
