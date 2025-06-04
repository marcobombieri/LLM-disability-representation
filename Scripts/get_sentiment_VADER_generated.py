# Import necessary libraries
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv

#rdisability_path = os.path.join("cl_dataset_rdisability_mistral_TOTAL.csv")
'''
paths = ["../DatasetsGenerated/gemini15flash_generated.csv",
"../DatasetsGenerated/gpt4omini_generated.csv",
"../DatasetsGenerated/mistral8b_generated.csv",
"../DatasetsGenerated/gemini15flash_generated_no-dis.csv",
"../DatasetsGenerated/gpt4omini_generated_no-dis.csv",
"../DatasetsGenerated/mistral8b_generated_no-dis.csv",
]
'''

paths = ["../DatasetsGenerated/gemini15flash_generated_no-dis-360.csv",
"../DatasetsGenerated/gpt4omini_generated_no-dis-360.csv",
"../DatasetsGenerated/mistral_generated_no-dis_360.csv",
]


# Function to estimate sentiment
def estimate_sentiment(text):
    # Initialize the VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()
    # Analyze the sentiment of the text
    sentiment_scores = analyzer.polarity_scores(text)
    # Interpret the compound score
    compound_score = sentiment_scores['compound']
    if compound_score >= 0.05:
        sentiment = "Positive"
    elif compound_score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    # Print the results
    #print(f"Text: {text}")
    #print(f"Sentiment Scores: {sentiment_scores}")
    #print(f"Overall Sentiment: {sentiment}")
    return sentiment_scores, sentiment

# Main program
if __name__ == "__main__":
    #Read the CSV file    
    for p in paths[0:]:
        c=1
        output_file = p[:-4]+"_VADER.csv"
        with open(p, mode='r', encoding='utf-8') as file, open(output_file, mode="w", encoding="utf-8") as output:
            reader = csv.reader(file)
            writer = csv.writer(output)
            # Convert to a list or process row by row
            rows = [row for row in reader]  # List of rows
            results = []
            for row in rows:
                post = row[4]                    
                # Estimate emotions
                sentiment_scores, sentiment = estimate_sentiment(post)
                results.append((c, sentiment_scores, sentiment))
                data = [c, sentiment_scores, sentiment]
                c=c+1
                writer.writerow(data)
            