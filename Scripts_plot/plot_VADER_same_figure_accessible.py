import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

fontsize1 = 18
fontsize2 = 14

file_paths = [
    "../DatasetsAnnotated/csv_vader.csv",
    "../DatasetsGenerated/gemini15flash_generated_VADER.csv",
    "../DatasetsGenerated/gpt4omini_generated_VADER.csv",
    "../DatasetsGenerated/mistral8b_generated_VADER.csv"
]

data = list()
for file_path in file_paths:
    df = pd.read_csv(file_path, header=None, names=["ID", "Scores", "Sentiment"])
    sentiment_counts = df["Sentiment"].value_counts()

    # Ensure "Negative" is included even if it's 0
    sentiment_counts = sentiment_counts.reindex(["Positive", "Negative"], fill_value=0)

    # Calculate percentages
    total = sentiment_counts.sum()
    sentiment_percentages = (sentiment_counts / total) * 100
    data.append(list(sentiment_percentages))

# Convert the list into a NumPy array for easier manipulation
data_array = np.array(data)

# Define the sentiment categories
sentiments = ['positive', 'negative']

# Number of models and sentiments
num_models = len(data)
num_sentiments = len(sentiments)

# Create a bar plot
fig, ax = plt.subplots(figsize=(6, 3.5))

# Define the bar width and positions for each model
bar_width = 0.1
index = np.arange(num_sentiments)  # Positions for the bars

# Define the models and finer hatching patterns
models = ['r/disability', 'Gemini-1.5F', "GPT-4o-mini", "Mixtral-8B"]
patterns = ['...', '---', '////', 'xxx']  # Finer patterns for better readability

# Plot the data for each model with patterns
for i in range(num_models):
    ax.bar(index + i * bar_width, data_array[i], bar_width, label=models[i],
           hatch=patterns[i], edgecolor='black')  # Add finer hatching and edgecolor

# Add labels, title, and format the plot
ax.set_xlabel('Sentiment', fontsize=fontsize2)
ax.set_ylabel('Sentiment distribution (%)', fontsize=fontsize2)

# Set the x-axis labels to sentiment categories
ax.set_xticks(index + bar_width * (num_models - 1) / 2)  # Center the ticks
ax.set_xticklabels(sentiments, fontsize=fontsize2)
plt.yticks(fontsize=fontsize2)

# Add legend in the upper-right corner
ax.legend(fontsize=12, loc='upper right')

# Format the y-axis to display percentages (0 to 100%)
ax.set_ylim(0, 105)

# Show gridlines and improve layout
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()

# Save the plot to file
output_file = os.path.join("..", "Figures", "VADER", "sentiment_VADER_accessible.png")
plt.savefig(output_file, bbox_inches='tight', pad_inches=0.01, dpi=300)
print(f"Figure saved as {output_file}")
print(data)
