import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
from get_group import *

if __name__ =="__main__":

    input_csv = "generated_logs.csv"

    payloads, labels = group_and_sort_within_group(input_csv, group_column_index=2, extract_columns=[9, 10])

    # Encode Payloads and Labels
    vectorizer = CountVectorizer()
    x_encoded = vectorizer.fit_transform(payloads).toarray()

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(labels)

    # Split Data into Training and Testing Sets
    X_train, X_test, y_train, y_test = train_test_split(
        x_encoded, y_encoded, test_size=0.2, random_state=42
    )

    # Convert to PyTorch Tensors
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    # Define the Binary Classification Model
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


    input_dim = X_train_tensor.shape[1]
    model = BinaryClassificationModel(input_dim)

    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    # Train the Model
    epochs = 100
    for epoch in range(epochs):
        model.train()

        outputs = model(X_train_tensor).squeeze()
        loss = criterion(outputs, y_train_tensor)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.4f}")

    # Evaluate the Model
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test_tensor).squeeze()
        predictions = (test_outputs >= 0.5).int()
        accuracy = (predictions == y_test_tensor.int()).float().mean()

    print(f"Test Accuracy: {accuracy:.4f}")

    # Save the vectorizer
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)

    # Save the Model
    torch.save(model.state_dict(), 'sql_classification_model.pth')
    print("Model state dictionary saved!")
