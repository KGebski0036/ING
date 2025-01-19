import torch
import torch.nn as nn
import pickle
from helper import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename",
                    help="read logs from FILE", metavar="FILE", required=True)
args = parser.parse_args()

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

with open('model_metadata.pkl', 'rb') as f:
    metadata = pickle.load(f)

num_classes = metadata["num_classes"]
input_dim = metadata["input_dim"]

model = MultiClassificationModel(input_dim=input_dim, num_classes=num_classes)
model.load_state_dict(torch.load('vulnerabilities_classification_model.pth', weights_only=True))
model.eval()

data, labels = read_form_csv_and_return_data_with_label(args.filename, 2, [9, 10])

new_features = vectorizer.transform(data).toarray()

new_features_tensor = torch.tensor(new_features, dtype=torch.float32)

with torch.no_grad():
    outputs = model(new_features_tensor)
    probabilities = nn.functional.softmax(outputs, dim=1)
    predicted_classes = torch.argmax(probabilities, dim=1)

class_counts = {i: 0 for i in range(num_classes)}

wrong_interpret_normal = 0
wrong_interpret_brute = 0

for i, predicted_class in enumerate(predicted_classes.tolist()):
    probabilities_for_element = probabilities[i].tolist()
    if (probabilities_for_element[2] > 0.99 and labels[i] != 2):
        wrong_interpret_normal += 1
    if (probabilities_for_element[2] < 0.99 and labels[i] == 2):
        print(probabilities_for_element[2])
        wrong_interpret_brute += 1
    if (probabilities_for_element[0] > 0.5):
        class_counts[0] += 1
    if (probabilities_for_element[1] > 0.5):
        # print("\033[31m" + f"Warning: possible SQL Injection attack attempt from IP: {labels[i]}" + "\033[0m")
        class_counts[1] += 1
        # print("\033[33m")
        # print(*data[i].split(), sep='\n')
        # print("\033[0m")
    if (probabilities_for_element[2] > 0.90):
        # print(data[i])
        # print("\033[31m" + f"Warning, probable bruteforce attack attempt from IP: {labels[i]}" + "\033[0m")
        # print("\033[33m" + f"POST Requests Number {len(data[i].split())} {probabilities_for_element[2]}" + "\033[0m")
        class_counts[2] += 1

print("\033[34m" + f"Summary: Normal activity: {class_counts[0]}, SQL Injection: {class_counts[1]}, brouteforce: {class_counts[2]}" + "\033[0m")
print(f"Zła interpretacja normalnych {wrong_interpret_normal} i brute {wrong_interpret_brute}")
