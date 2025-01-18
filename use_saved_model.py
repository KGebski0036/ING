import torch
import torch.nn as nn
import pickle
from sklearn.feature_extraction.text import CountVectorizer

# Define the same model architecture as during training
class BinaryClassificationModel(nn.Module):
    def __init__(self, input_dim):
        super(BinaryClassificationModel, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)

# Load the saved vectorizer
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Load the model with the correct input dimension (should match training input size)
model = BinaryClassificationModel(input_dim=3929)  # Match the input size used during training
model.load_state_dict(torch.load('sql_classification_model.pth'))
model.eval()  # Set the model to evaluation mode

# Example new payloads for prediction
new_payloads = [
    "order_id=3' OR 1=1;--",
    "DROP TABLE users;--",
    "login=user1735&password=pass&action=login"
]

# Preprocess new payloads using the loaded vectorizer
new_features = vectorizer.transform(new_payloads).toarray()

# Convert to a PyTorch tensor
new_features_tensor = torch.tensor(new_features, dtype=torch.float32)

# Make predictions (probabilities)
with torch.no_grad():
    predictions = model(new_features_tensor).squeeze()  # Get predictions from the model

# Convert predictions to percentages (0 to 100)
predicted_percentages = predictions * 100

# Print the predicted percentages
for i, percent in enumerate(predicted_percentages.tolist()):
    print(f"Payload {i+1}: {percent:.2f}% probability of being: 1")
