
from datasets import load_dataset

print("Downloading AI2 ARC dataset...")

dataset = load_dataset("allenai/ai2_arc", "ARC-Challenge")

print("\nDataset loaded successfully!")
print(dataset)

question = dataset["train"][0]

print("\nSample question:")
print(question["question"])

print("\nAnswer choices:")
for label, text in zip(
    question["choices"]["label"],
    question["choices"]["text"]
):
    print(f"{label}. {text}")

print("\nCorrect answer:", question["answerKey"])

print("\nTotal training questions:", len(dataset["train"]))
print("Total validation questions:", len(dataset["validation"]))
print("Total test questions:", len(dataset["test"]))
