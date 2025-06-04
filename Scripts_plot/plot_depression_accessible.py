import pandas as pd
import matplotlib.pyplot as plt
import re
import os
import numpy as np


# File paths for datasets
file_paths = [
    "../DatasetsAnnotated/csv_depression.csv",
    "../DatasetsGenerated/gemini15flash_generated_depression.csv",
    "../DatasetsGenerated/gpt4omini_generated_depression.csv",
    "../DatasetsGenerated/mistral8b_generated_depression.csv",
]

fontsize1=18
fontsize2=14

# Function to extract the first label
def extract_label(text):
    match = re.search(r"\[\[\{'label': '([^']+)'", text)
    if match:
        return match.group(1)
    return None

# Initialize an empty dictionary to store percentages
label_percentages = {}

# Process each file
models = ['r/disability', 'Gemini-1.5F', "GPT-4o-mini", "Mixtral-8B"]
patterns = ['...', '---', '////', 'xxx']  # Finer patterns for better readability


for file in file_paths:
    # Load the CSV
    df = pd.read_csv(file, header=None, names=["id", "text"])
    
    # Extract the labels
    df["label"] = df["text"].apply(extract_label)
    
    # Count occurrences of each label
    label_counts = df["label"].value_counts()
    
    # Convert counts to percentages
    percentages = (label_counts / label_counts.sum()) 
    
    # Store percentages with the file name
    label_percentages[file] = percentages

# Combine percentages into a single DataFrame
comparison_df = pd.DataFrame(label_percentages).fillna(0) * 100
comparison_df = comparison_df.reindex(["severe", "moderate", "not depression"])

print(comparison_df.values)


# Generate x positions for the bars
num_categories = len(comparison_df.index)
num_models = len(comparison_df.columns)
bar_width = 0.2  # Adjust bar width
x_positions = np.arange(num_categories)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(6, 3.5))

# Plot each model's bars
for i in range(num_models):
    ax.bar(
        x_positions + i * bar_width, 
        comparison_df.iloc[:, i], 
        width=bar_width, 
        label=models[i],
        hatch=patterns[i], edgecolor='black'
    )

# Customize labels, ticks, and legend
ax.set_xlabel("Depression level", fontsize=fontsize2)
ax.set_ylabel("Depr. level distribution (%)", fontsize=fontsize2)
ax.set_xticks(x_positions + bar_width * (num_models - 1) / 2)
ax.set_xticklabels(comparison_df.index, fontsize=fontsize2)
plt.yticks(fontsize=fontsize2)
plt.legend(loc="upper left", fontsize=12)
ax.set_ylim(0, 105)


# Reduce whitespace
plt.tight_layout()

# Show the plot
plt.show()

# Add percentage values on top of the bars
'''
for container in ax.containers:
    for bar in container:
        height = bar.get_height()
        if height > 0:  # Display only non-zero values
            ax.text(
                bar.get_x() + bar.get_width() / 2, 
                height + 0.5, 
                f'{height:.2f}%', 
                ha='center', 
                va='bottom', 
                rotation=90  # Rotate the text
            )
'''
# Adjust layout and save the plot
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig(os.path.join("..", "Figures", "Depression", "depression_label_comparison_accessible.png"),  pad_inches=0.01, dpi=300, bbox_inches='tight')

plt.show()
