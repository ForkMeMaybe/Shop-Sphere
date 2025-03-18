import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression

# Training data with only website interactions
X_train = np.array(
    [
        [1, 0, 0, 0],  # Website visit
        [0, 1, 0, 0],  # Product search
        [0, 0, 1, 0],  # Adding to cart
        [0, 0, 0, 1],  # Reaching payment page
    ]
)

y_train = np.array([10, 40, 70, 90])  # Lead scores based on engagement level

# Train the Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "lead_model.pkl")
print("Model trained and saved with updated lead detection criteria!")
