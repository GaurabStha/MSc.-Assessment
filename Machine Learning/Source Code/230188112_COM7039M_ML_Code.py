import streamlit as st
import pickle
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import nltk
nltk.download('punkt')
nltk.download('stopwords')
stopword = set(stopwords.words('english'))
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

# Load the TF-IDF Vectorizer
with open("Model/tfidf_vectorizer.pkl", "rb") as tfidf_file:
    vectorizer = pickle.load(tfidf_file)

# Load the PCA Model
with open("Model/pca.pkl", "rb") as pca_file:
    pca = pickle.load(pca_file)

# Load the Machine Learning Model
with open("Model/lr_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Function to remove unwanted text and characters
def remove_unwanted_text(text):
    text = re.sub(r'\bRT\b', '', text)  # Remove 'RT'
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)  # Remove Twitter handles
    text = re.sub(r'&amp;', '', text)  # Remove '&amp;'
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)  # Remove non-alphabetic characters
    return text

# Function to clean, preprocess, and stem text
def clean_and_preprocess_text(text):
    text = remove_unwanted_text(text)
    text = text.lower()  # Convert to lowercase
    words = word_tokenize(text)  # Tokenize text
    words = [ps.stem(word) for word in words if word not in stopword]  # Remove stopwords and stem
    cleaned_text = ' '.join(words)  # Rejoin words
    return cleaned_text

# Streamlit app interface
st.title("Hate Speech, Offensive Language and Neutral Language Classification")
st.write("Enter a tweet, and the model will classify it as *Hate Speech*, *Offensive Language*, or *Neither*.")

# Input text from user
tweet_input = st.text_input("Enter your tweet:")

if st.button("Classify"):
    if tweet_input:
        try:
            # Step 1: Clean and preprocess the input
            cleaned_tweet = clean_and_preprocess_text(tweet_input)

            # Step 2: Transform the input using the TF-IDF vectorizer
            vectorized_tweet = vectorizer.transform([cleaned_tweet]).toarray()

            # Step 3: Apply PCA transformation
            pca_transformed_tweet = pca.transform(vectorized_tweet)

            # Step 4: Predict using the Logistic Regression model
            prediction = model.predict(pca_transformed_tweet)
            prediction_proba = model.predict_proba(pca_transformed_tweet)

            # Map prediction to labels
            labels = {0: "Hate Speech", 1: "Offensive Language", 2: "Neither"}
            result = labels[prediction[0]]

            # Display result
            st.success(f"Prediction: *{result}*")
            st.write(f"Prediction Confidence: {max(prediction_proba[0]) * 100:.2f}%")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a tweet to classify!")