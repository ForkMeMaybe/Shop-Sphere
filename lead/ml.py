import numpy as np
import joblib
from textblob import TextBlob

# Load the trained model
MODEL_PATH = "lead_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise Exception(f"Model file '{MODEL_PATH}' not found. Train the model first!")


# Function to predict lead score
def predict_lead_score(engagement):
    """
    Predicts the lead score based on the engagement level.

    Parameters:
    - engagement (int): The engagement level
        0 = Website Visit
        1 = Product Search
        2 = Adding to Cart
        3 = Reaching Payment Page

    Returns:
    - float: The predicted lead score
    """
    engagement_mapping = {
        0: 10,  # Website Visit
        1: 40,  # Product Search
        2: 70,  # Adding to Cart
        3: 90,  # Reaching Payment Page
    }

    return float(
        engagement_mapping.get(engagement, 0)
    )  # Default to 0 if invalid engagement


# Function to analyze sentiment of a message
def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text message.

    Parameters:
    - text (str): The input text

    Returns:
    - str: "Positive", "Negative", or "Neutral"
    """
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
