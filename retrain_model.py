import warnings 
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

print("Loading dataset...")
# Load the dataset
df = pd.read_csv('Data Source/SPAM.csv', encoding='latin-1')

print("Preprocessing data...")
# Drop unnecessary columns
df = df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1)

# Rename columns for clarity
df.columns = ['Category', 'Message']

# Convert categories to binary (0 for spam, 1 for ham)
df['Category'] = df['Category'].map({'spam': 0, 'ham': 1})

# Check for null values
print(f"Null values: {df.isnull().sum().sum()}")
print(f"Dataset shape: {df.shape}")
print(f"Category distribution:\n{df['Category'].value_counts()}")

# Prepare features and target
X = df['Message']
y = df['Category']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Extracting features with TF-IDF...")
# TF-IDF Vectorization
tfidf = TfidfVectorizer(min_df=1, stop_words='english', lowercase=True)
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# Convert target to integers
y_train = y_train.astype(int)
y_test = y_test.astype(int)

print("Training models...")
# Define base models
base_models = [
    ('lr', LogisticRegression(random_state=42, max_iter=1000)),
    ('dt', DecisionTreeClassifier(random_state=42)),
    ('knn', KNeighborsClassifier()),
    ('rf', RandomForestClassifier(random_state=42, n_estimators=100))
]

# Create stacking classifier
stacking_model = StackingClassifier(
    estimators=base_models,
    final_estimator=LogisticRegression(random_state=42, max_iter=1000),
    cv=5
)

# Train the stacking model
stacking_model.fit(X_train_tfidf, y_train)

# Make predictions
y_pred = stacking_model.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"\nModel Performance:")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-score: {f1:.4f}")

print("\nSaving model and vectorizer...")
# Save the trained model and vectorizer
with open('Pickle Files/model.pkl', 'wb') as f:
    pickle.dump(stacking_model, f)

with open('Pickle Files/feature.pkl', 'wb') as f:
    pickle.dump(tfidf, f)

print("Model and vectorizer saved successfully!")
print("You can now run the Streamlit app with: streamlit run 'Spam Classification Deployment.py'")