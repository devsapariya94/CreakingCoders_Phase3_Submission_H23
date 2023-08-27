
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

cd CreakingCoders_Phase3_Submission_H23

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

## Steps for creating the model
1. Importing neccesary libraries:
2.Loading and Preprocessing data:
-->Load the dataset from a CSV file, removing columns with missing values.
-->Visualize the distribution of disease occurrences using a bar plot.
3. Encoding the Target Labels:
-->Use LabelEncoder to convert disease names (categorical labels) into numerical values.
5. Splitting data:
-->Split the data into training and testing sets using train_test_split.
6. Defining Cross-Validation Scoring Metric:
-->Define a function to calculate accuracy score for cross-validation.
7. Initializing Models:
-->Create instances of Support Vector Classifier (SVC), Gaussian Naive Bayes, and Random Forest Classifier.
8. Cross-Validation:
-->Perform cross-validation for each model and print mean accuracy scores.
9. Training and Evaluating Individual Models:
-->Train an SVM model on the training data and evaluate its accuracy on both training and testing sets.
-->Display a confusion matrix for the SVM model's predictions.
10. Training Combined Models:
-->Train final models (SVM, Naive Bayes, Random Forest) on the entire dataset.
11. Making Predictions on Test Data:
-->Load the test dataset, preprocess it, and create input features (test_X) and target labels (test_Y).
-->Use the trained models to make individual predictions (SVM, Naive Bayes, Random Forest).
    1. Combining Predictions:
    -->Combine individual model predictions using mode voting to get the final combined prediction.
    2. Calculating Accuracy and Confusion matrix for Combined Model:
    -->Calculate accuracy on the test dataset using the combined model.
    -->Display a confusion matrix for the combined model's predictions.
    3. Creating symptom index:
    -->Create a dictionary to map symptom names to their indices in the input features.
    4. Defining Prediction Function:
    -->Create a function that takes a comma-separated list of symptoms as input and predicts the disease using the combined model.
    1. Testing the prediction Function  
    -->Test the prediction function with a sample symptom input.
## Currently Working On

1.  Refining the User Experience [Figma Link](https://www.figma.com/file/hncKZRmPf7TyfbGVGzhq0g/Hackout?type=design&node-id=0-1&mode=design&t=GLcxEuiqlTqRocqH-0)
2.  Integrating the ML Model into the main project ([ML model]))(https://github.com/devsapariya94/CreakingCoders_Phase3_Submission_H23/blob/main/ML%20Model%20to%20Predict%20the%20possible%20dicease.ipynb)

## Future Plans
