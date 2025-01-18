import torch
import torch.nn as nn
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from get_group import *

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
model = BinaryClassificationModel(input_dim=12934)  # Match the input size used during training
model.load_state_dict(torch.load('sql_classification_model.pth'))
model.eval()  # Set the model to evaluation mode

data, labels = group_and_sort_within_group("generated_logs_tests.csv", 2, [9, 9])
# data, labels = group_and_sort_within_group("data/logs.csv", 2, [9, 9])

# Preprocess new payloads using the loaded vectorizer
new_features = vectorizer.transform(data).toarray()

# Convert to a PyTorch tensor
new_features_tensor = torch.tensor(new_features, dtype=torch.float32)

# Make predictions (probabilities)
with torch.no_grad():
    predictions = model(new_features_tensor).squeeze()  # Get predictions from the model

# Convert predictions to percentages (0 to 100)
predicted_percentages = predictions * 100

detected_sql = 0
# Print the predicted percentages
for i, percent in enumerate(predicted_percentages.tolist()):
    if (percent > 50):
        detected_sql += 1
        print(data[i])
        print("Uwaga niebezpieczne zapytanie (SQL injection)!!! " + str(labels[i]) + " Prawdopodobieństwo " + str(percent) + "%" )

print("Dupsko: " + str(detected_sql))
