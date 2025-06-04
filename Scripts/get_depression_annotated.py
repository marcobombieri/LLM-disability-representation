from transformers import pipeline
import os
import pandas as pd
import csv


#rdisability_path = os.path.join("cl_dataset_rdisability_mistral_TOTAL.csv")
paths = ["../DatasetsAnnotated/1_ANN_csv.csv",
"../DatasetsAnnotated/2_ANN_csv.csv",
"../DatasetsAnnotated/3_ANN_csv.csv"
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




# Read the CSV file
for p in paths[0:]:
    with open(p, mode='r', encoding='utf-8') as file:
        with open(p[:-4]+"_depression.csv", mode="w", encoding="utf-8") as output:
            reader = csv.reader(file)
            writer = csv.writer(output)
    
            # Convert to a list or process row by row
            rows = [row for row in reader]  # List of rows
            for row in rows:
                if int(row[1])==1:
                    try:
                        post = row[3]
                        emotion = get_emotion(post)
                        data =[row[0], emotion]
                        writer.writerow(data)
                    except RuntimeError as e:
                        try:
                            # Truncate text and retry
                            truncated_post = post[:1024]
                            emotion = get_emotion(truncated_post)
                            data = [row[0], "TRUNCATED"+str(emotion)]
                            writer.writerow(data)
                        except Exception as inner_e:
                            print(f"Failed to process truncated text for row {c}: {inner_e}")
                            writer.writerow([c, "Error: Failed after truncation"])









