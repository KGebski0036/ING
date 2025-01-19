import torch
import torch.nn as nn
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from get_group import *

# Define the same model architecture as during training
class MultiClassificationModel(nn.Module):
    def __init__(self, input_dim, num_classes):
        super(MultiClassificationModel, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, num_classes)
        )

    def forward(self, x):
        return self.network(x)

# Load the saved vectorizer
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

num_classes = 3
model = MultiClassificationModel(input_dim=19029, num_classes=num_classes)  # Match the input size used during training
model.load_state_dict(torch.load('vornabilities_classification_model.pth'))
model.eval()  # Set the model to evaluation mode

data, labels = group_and_sort_within_group("generated_logs_test.csv", 2, [9, 9])

# Preprocess new payloads using the loaded vectorizer
new_features = vectorizer.transform(data).toarray()

# Convert to a PyTorch tensor
new_features_tensor = torch.tensor(new_features, dtype=torch.float32)

# Make predictions (probabilities)
with torch.no_grad():
    outputs = model(new_features_tensor)  # Get raw outputs from the model
    probabilities = nn.functional.softmax(outputs, dim=1)  # Convert to probabilities
    predicted_classes = torch.argmax(probabilities, dim=1)  # Get the predicted class indices

# Print the predictions
for i, predicted_class in enumerate(predicted_classes.tolist()):
    print(f"Payload: {data[i]}")
    print(f"Predicted Class: {predicted_class}, Probability Distribution: {probabilities[i].tolist()}")

# Optional: Count occurrences of each class
class_counts = {i: 0 for i in range(num_classes)}
for cls in predicted_classes.tolist():
    class_counts[cls] += 1

print(f"Class Counts: {class_counts}")
