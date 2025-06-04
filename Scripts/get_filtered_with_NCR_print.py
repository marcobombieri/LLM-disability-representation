import csv
from collections import defaultdict


nrc_file = "../NRC/NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt" 
csv_file = "../Results/merged_dis_no-dis360_reversed.csv" 


# Function to load NRC Lexicon into a dictionary
def load_nrc_lexicon(nrc_file):
    nrc_dict = defaultdict(list)  # Use a dictionary to store emotions for each word
    with open(nrc_file, 'r') as file:
        for line in file:
            word, emotion, value = line.strip().split("\t")
            if int(value) == 1:  # Only include words/emotions with value 1
                nrc_dict[word.lower()].append(emotion)
    return nrc_dict

# Function to check CSV words, extract emotions, and save results
def check_words_and_save(csv_file, nrc_dict):
    with open(csv_file, 'r') as infile:
        reader = csv.reader(infile)
        
        
        # Process each word in the input file
        for row in reader:
            word, value = row
            emotions = nrc_dict.get(word.lower(), [])  # Get list of emotions or empty list
            #print(word, emotions)
            in_nrc = bool(emotions)  # True if emotions are found
            formatted_emotions = f"[{'|'.join(emotions)}]" if emotions else "[]"
            if emotions:
                print(word, f"({value}),", end=" ")



# Load NRC Lexicon
nrc_dict = load_nrc_lexicon(nrc_file)
# Check words and save results
check_words_and_save(csv_file, nrc_dict)

