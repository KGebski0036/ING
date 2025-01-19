import torch
import torch.optim as optim
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
from helper import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename",
                    help="read logs from FILE", metavar="FILE", required=True)
args = parser.parse_args()

input_csv = args.filename

if __name__ =="__main__":

    payloads, labels = read_form_csv_and_return_data_with_label(input_csv, group_column_index=2, extract_columns=[9, 10])


    vectorizer = CountVectorizer()
    x_encoded = vectorizer.fit_transform(payloads).toarray()

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(labels)

    X_train, X_test, y_train, y_test = train_test_split(
        x_encoded, y_encoded, test_size=0.2, random_state=42
    )

    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    num_classes = len(label_encoder.classes_)
    input_dim = X_train_tensor.shape[1]
    model = MultiClassificationModel(input_dim, num_classes)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    y_train_tensor = torch.tensor(y_train, dtype=torch.long)
    y_test_tensor = torch.tensor(y_test, dtype=torch.long)

    epochs = 100
    for epoch in range(epochs):
        model.train()

        outputs = model(X_train_tensor)
        loss = criterion(outputs, y_train_tensor)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.4f}")


    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test_tensor)
        predictions = torch.argmax(test_outputs, dim=1)
        accuracy = (predictions == y_test_tensor).float().mean()

    print(f"Test Accuracy: {accuracy:.4f}")

    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)

    torch.save(model.state_dict(), 'vulnerabilities_classification_model.pth')
    print("Model state dictionary saved!")

    metadata = {
        "num_classes": num_classes,
        "input_dim": input_dim,
    }

    with open('model_metadata.pkl', 'wb') as f:
        pickle.dump(metadata, f)
