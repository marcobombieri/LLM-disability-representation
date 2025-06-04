from transformers import pipeline
import os
import pandas as pd

#rdisability_path = os.path.join("cl_dataset_rdisability_mistral_TOTAL.csv")
paths = ["../DatasetsGenerated/gemini15flash_generated_no-dis-360.csv",
"../DatasetsGenerated/gpt4omini_generated_no-dis-360.csv",
"../DatasetsGenerated/mistral_generated_no-dis_360.csv"
]

def preprocessing(text):
    words = text.split()
    # Join the words with a single space
    cleaned_text = ' '.join(words)
    if len(cleaned_text) > 1024:
        cleaned_text = cleaned_text[0:1024]
    return cleaned_text

def get_emotion(text):
    #print(text)
    #classifier = pipeline("text-classification", model="paulagarciaserrano/roberta-depression-detection", top_k=None)
    classifier = pipeline("text-classification", model="rafalposwiata/deproberta-large-depression", top_k=None, device="cuda")
    return classifier(text)



import csv

# Read the CSV file
for p in paths:
    c=1
    with open(p, mode='r', encoding='utf-8') as file:
        with open(p[:-4]+"_depression.csv", mode="w", encoding="utf-8") as output:
            reader = csv.reader(file)
            writer = csv.writer(output)
    
            # Convert to a list or process row by row
            rows = [row for row in reader]  # List of rows
            for row in rows:
                try:
                    post = row[4]
                    emotion = get_emotion(post)
                    data =[c, emotion]
                    writer.writerow(data)
                    c=c+1
                except RuntimeError as e:
                    try:
                        # Truncate text and retry
                        truncated_post = post[:1024]
                        emotion = get_emotion(truncated_post)
                        data = [c, "TRUNCATED"+str(emotion)]
                        writer.writerow(data)
                    except Exception as inner_e:
                        print(f"Failed to process truncated text for row {c}: {inner_e}")
                        writer.writerow([c, "Error: Failed after truncation"])
                    c=c+1    









