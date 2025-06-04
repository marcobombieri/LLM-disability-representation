import re
from collections import Counter, defaultdict
import csv
import numpy as np

#rdisability_path = os.path.join("cl_dataset_rdisability_mistral_TOTAL.csv")
paths = ["../DatasetsAnnotated/1_ANN_csv.csv",
"../DatasetsAnnotated/2_ANN_csv.csv",
"../DatasetsAnnotated/3_ANN_csv.csv"
]


lexicon_file = "../NRC/NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt" # Path to NRC Emotion Lexicon file

def save_to_csv(results, output_file):
    # Get a list of all possible emotions from the first entry in results
    emotions = set()
    
    for _, emotion_counts in results:
        emotions.update(emotion_counts.keys())
    emotions = sorted(emotions)
    
    # Write to CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["ID"] + emotions + ["total_emotions", "total_sentiments"])
        
        # Write each row
        for text, emotion_counts in results:
            total_sentiments = emotion_counts['positive'] + emotion_counts['negative']
            total_emotions = emotion_counts['anger'] + emotion_counts['anticipation'] + emotion_counts['disgust'] + emotion_counts['fear'] + emotion_counts['joy'] +emotion_counts['sadness'] +emotion_counts['surprise'] + emotion_counts['trust']
            row = [text]
            for emotion in emotions:
                if emotion == "positive" or emotion=="negative":
                    if total_sentiments > 0:
                        normalized_value = round(emotion_counts.get(emotion, 0) / total_sentiments, 4)
                    else:
                        normalized_value = 0
                else: 
                    if total_emotions > 0:
                        normalized_value = round(emotion_counts.get(emotion, 0) / total_emotions, 4)
                    else:
                        normalized_value = 0
                row.append(normalized_value)
            
            row += [total_emotions, total_sentiments]
            writer.writerow(row)


# Function to load NRC Emotion Lexicon
def load_nrc_lexicon(filepath):
    lexicon = defaultdict(list)  # A dictionary where keys are words and values are lists of emotions
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            word, emotion, association = line.strip().split("\t")
            if int(association) == 1:  # Only keep entries with association value 1
                lexicon[word].append(emotion)
    return lexicon

# Function to estimate emotion from text
def estimate_emotion(text, lexicon):
    # Tokenize and normalize the text
    words = re.findall(r"\w+", text.lower())
    # Count occurrences of emotions
    emotion_counts = Counter()
    for word in words:
        if word in lexicon:
            for emotion in lexicon[word]:
                emotion_counts[emotion] += 1
    return emotion_counts

# Main program
if __name__ == "__main__":
    nrc_lexicon = load_nrc_lexicon(lexicon_file) # Load the NRC Emotion Lexicon
    #Read the CSV file
    for p in paths[0:]:
        output_file = p[:-4]+"_NCR.csv"
        with open(p, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
        
            # Convert to a list or process row by row
            rows = [row for row in reader]  # List of rows
            results = []
            for row in rows:
                if(int(row[1])==1):
                    post = row[3]                    
                    # Estimate emotions
                    emotions = estimate_emotion(post, nrc_lexicon)
                    results.append((row[0], emotions))

            save_to_csv(results, output_file)