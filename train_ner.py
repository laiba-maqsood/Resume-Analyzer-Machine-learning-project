import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding
from spacy.scorer import Scorer
import random
import os
import sys
from sklearn.model_selection import train_test_split

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.skills_ner_dataset import TRAIN_DATA

def evaluate_model(nlp, examples):
    scorer = Scorer()
    predicted_examples = []
    for example in examples:
        pred_doc = nlp(example.reference.text)
        predicted = Example(pred_doc, example.reference)
        predicted_examples.append(predicted)
    scores = scorer.score(predicted_examples)  # Pass list of Examples here
    precision = scores.get("ents_p", 0.0)
    recall = scores.get("ents_r", 0.0)
    f1 = scores.get("ents_f", 0.0)
    return precision, recall, f1


def prepare_examples(nlp, data):
    examples = []
    for text, annotations in data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        examples.append(example)
    return examples

# Split data into training and validation sets
train_data, val_data = train_test_split(TRAIN_DATA, test_size=0.2, random_state=42)

# Initialize blank model
nlp = spacy.blank("en")

# Add NER pipeline
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Add label
ner.add_label("SKILL")

# Disable other pipes for training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.begin_training()

    train_examples = prepare_examples(nlp, train_data)
    val_examples = prepare_examples(nlp, val_data)

    for itn in range(60):  
        print(f"\nEpoch {itn + 1}/60")
        random.shuffle(train_examples)
        losses = {}
        batches = minibatch(train_examples, size=compounding(4.0, 32.0, 1.5))
        for batch in batches:
            nlp.update(batch, drop=0.2, losses=losses)
        print("Losses:", losses)

        # Evaluate on validation set
        precision, recall, f1 = evaluate_model(nlp, val_examples)
        print(f"Validation - Precision: {precision:.3f}, Recall: {recall:.3f}, F1: {f1:.3f}")

# Save model
output_dir = "models/skill_ner"
os.makedirs(output_dir, exist_ok=True)
nlp.to_disk(output_dir)
print(f"\nModel saved to {output_dir}")
