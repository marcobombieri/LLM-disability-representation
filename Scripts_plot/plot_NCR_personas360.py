import pandas as pd
import glob
import os
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

models = ['Gemini-1.5F', "GPT-4o-mini", "Mixtral-8B"]
disabs = ['LLM_D_GEM', 'LLM_D_GPT', 'LLM_D_MIX']
fontsize1=18
fontsize2=14


# File paths (couples of files)
file_paths = [
    ["../DatasetsGenerated/gemini15flash_generated_NCR.csv", "../DatasetsGenerated/gemini15flash_generated_no-dis-360_NCR.csv"],
    ["../DatasetsGenerated/gpt4omini_generated_NCR.csv", "../DatasetsGenerated/gpt4omini_generated_no-dis-360_NCR.csv"],
    ["../DatasetsGenerated/mistral8b_generated_NCR.csv", "../DatasetsGenerated/mistral_generated_no-dis_360_NCR.csv"]
]

# Emotions to compare
#emotions = ["anger", "anticipation", "disgust", "fear", "joy", "negative", "positive", "sadness", "surprise", "trust"]
emotions = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

# Function to calculate the average emotion values for a CSV file
def calculate_emotion_averages(file_path, emotions):
    df = pd.read_csv(file_path)
    return df[emotions].mean()

# Function to plot a comparison of two models for their emotion averages
def plot_emotion_comparison(emotion_averages_1, emotion_averages_2, file_pair, emotions):
    x = np.arange(len(emotions))  # x-axis positions
    width = 0.35  # Width of the bars
    patterns = ['...', '---']  # Finer patterns for better readability
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar plots for the two files
    ax.bar(x - width/2, emotion_averages_1, width, label='LLM_D_GEM', hatch='...')
    ax.bar(x + width/2, emotion_averages_2, width, label='LLM_ND_GEM',  hatch='---')
    
    # Add labels, title, and legend
    ax.set_xlabel('Emotions', fontsize=fontsize1)
    ax.set_ylabel('Emotion distribution (%)', fontsize=fontsize1)
    #ax.set_title(f'Emotion Comparison: {file_pair[0].split("/")[-1]} vs {file_pair[1].split("/")[-1]}')
    ax.set_xticks(x)
    #ax.set_yticks(x, fontsize=fontsize1)
    ax.set_xticklabels(emotions, rotation=0, fontsize=fontsize2)
    plt.yticks(fontsize=fontsize2)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend(fontsize=fontsize2-2)
    
    # Display the plot
    plt.tight_layout()
    plt.show()

def get_row_values(file_path, emotions):
    df = pd.read_csv(file_path)
    return df[emotions]




# Loop through each pair of file paths and process
for i, file_pair in enumerate(file_paths):
    # Calculate the averages for both files in the pair
    emotion_averages_1 = calculate_emotion_averages(file_pair[0], emotions) * 100
    emotion_averages_2 = calculate_emotion_averages(file_pair[1], emotions) * 100

    print(file_pair)
    print(emotion_averages_1)
    print(emotion_averages_2)

    row_values_1 = get_row_values(file_pair[0], emotions)
    row_values_2 = get_row_values(file_pair[1], emotions)


    for e in row_values_1.keys():
        # t_stat, p_value = stats.ttest_ind(row_values_1[e].values, row_values_2[e].values)
        t_stat, p_value = stats.ttest_ind(row_values_1[e].values, row_values_2[e].values)
        if p_value < 0.05:
            # Print the t-statistic and p-value
            print(models[i], "\n", e)
            print(f"T-statistic: {t_stat:.3f}")
            print(f"P-value: {p_value:.3f} \n")
            pass

    # Plot the comparison
    plot_emotion_comparison(emotion_averages_1, emotion_averages_2, file_pair, emotions)
    output_file = os.path.join("..", "Figures", "NCR", "emotions_NCR_personas_"+models[i]+"_360.png")
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0.01, dpi=300)
    print(f"Figure saved as {output_file}")

