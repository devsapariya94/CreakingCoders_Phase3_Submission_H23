
# Hackout 2023, DA-IICT

### Problem Statement:   
Create a technology to improve adoption by doctors, nurses and other health/administrative workers in state healthcare facilities to use the HMIS (Health Management Information System) software.

### Why are doctors not adopting such software?
1) Older age- Not knowing technology, can't adapt because of age.
2) Complex software- want to work with software, bcz of complex UI and working, can't give time to understand and use the software.
3) Transparency issue- doctors who know the technology but not using bcz they don't want anyone/other doctors to see their prescription.

## Steps for Server-setup
Commands:
git clone https://github.com/devsapariya94/CreakingCoders_Phase3_Submission_H23.git

cd CreakingCoders

pip install virtualenv

virtualenv virtualenv

virtualenv\Script\activate

pip install -r requirements.txt

python app.py
# Solution
1. Make Simple UI.
2. Implement AI model(RF/SVM)-for predict disease from the symptoms.
3. Implement mechanism- Optimal search for suggest the medicine to doctor. 
4. Apply Constraint so prescription of doctor is not see by the other doctor.
5. Smooth flow of patient's data:
Patient [Symptoms] 
-> 
Doctor(AI-predict disease+Optimal search of medicine) [Prescription]         
->
Pharmacist [Medicine] 
->
Patient 


## AI/ML Model
Artificial Intelligence (AI) and Machine Learning (ML) are technologies that enable computers to learn from data and perform tasks without explicit programming. ML models are algorithms that learn patterns and relationships from data, allowing them to make predictions, classifications, and decisions.

Here, we use the SVM(), Random Forest and Gaussian nb to predict the disease from symptoms provided by the patient.

1. Support Vector Machines (SVM):
SVM separates data points of different classes using a hyperplane. In disease prediction, SVM classifies patients into disease categories based on symptoms. It finds the decision boundary, maximizing the margin between classes.

2. Random Forest:
Random Forest is an ensemble technique combining decision trees. It predicts disease presence using majority votes of trees, each trained on a subset of data. It's used for disease prediction by training trees to predict diseases based on symptoms.

3. Gaussian Naive Bayes (NB):
Gaussian Naive Bayes is a probabilistic algorithm based on Bayes' theorem, assuming Gaussian-distributed features. In disease prediction, it estimates disease probabilities given symptoms. It calculates the likelihood of observing symptoms for each disease, predicting the highest probability.

## Currently Working On

1.  Refining the User Experience [Figma Link](https://www.figma.com/file/hncKZRmPf7TyfbGVGzhq0g/Hackout?type=design&node-id=0-1&mode=design&t=GLcxEuiqlTqRocqH-0)
2.  Integrating the ML Model into the main project ([ML model]))(https://github.com/devsapariya94/CreakingCoders_Phase3_Submission_H23/blob/main/ML%20Model%20to%20Predict%20the%20possible%20dicease.ipynb)

## Future Plans
