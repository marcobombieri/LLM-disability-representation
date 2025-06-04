# Import necessary libraries
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv

#rdisability_path = os.path.join("cl_dataset_rdisability_mistral_TOTAL.csv")
paths = ["../DatasetsAnnotated/1_ANN_csv.csv",
"../DatasetsAnnotated/2_ANN_csv.csv",
"../DatasetsAnnotated/3__ANN_csv.csv"
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

# Read the CSV file
for p in paths[0:]:
    with open(p, mode='r', encoding='utf-8') as file:
        with open(p[:-4]+"_VADER.csv", mode="w", encoding="utf-8") as output:
            reader = csv.reader(file)
            writer = csv.writer(output)
    
            # Convert to a list or process row by row
            rows = [row for row in reader]  # List of rows
            for row in rows:
                if(int(row[1])==1):
                    post = row[3]
                    sentiment_scores, sentiment = estimate_sentiment(post)
                    data =[row[0], sentiment_scores, sentiment]
                    writer.writerow(data)
 