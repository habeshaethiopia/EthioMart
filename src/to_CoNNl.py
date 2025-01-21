import re
import csv

def label_text_conll(text):
    """
    Label a single piece of text in CoNLL format based on simple patterns.
    """
    tokens = text.split()
    labeled_tokens = []

    for token in tokens:
        if re.match(r"^\d+ብር$", token) or re.match(r"^(ዋጋ|በ)\s*\d+\s*ብር$", text):
            label = "B-PRICE" if "ብር" in token else "I-PRICE"
        elif token in ["አዲስ", "አበባ", "ቦሌ", "ሾላ","ጀሞ","ፒያሳ","ገርጂ"]:  # Example locations
            label = "B-LOC" if token == "አዲስ" else "I-LOC"
        elif token in ["የቤት", "ብሪል", "ካሜራ"]:  # Example products
            label = "B-Product" if token in ["የቤት", "ብሪል"] else "I-Product"
        else:
            label = "O"
        
        labeled_tokens.append(f"{token}\t{label}")
    
    return "\n".join(labeled_tokens) + "\n"

def process_csv_to_conll(input_csv, output_txt):
    """
    Process a CSV file and save the labeled data in CoNLL format.
    """
    with open(input_csv, "r", encoding="utf-8") as csvfile, open(output_txt, "w", encoding="utf-8") as conllfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            message = row.get("Message", "").strip()
            if message:
                labeled_message = label_text_conll(message)
                conllfile.write(labeled_message + "\n")

# Input and output file paths
input_csv_path = "Data/telegram_data.csv"  # Replace with the path to your CSV file
output_txt_path = "labeled_dataset.conll"

# Run the conversion
process_csv_to_conll(input_csv_path, output_txt_path)

print(f"Labeled data has been saved to {output_txt_path}.")
