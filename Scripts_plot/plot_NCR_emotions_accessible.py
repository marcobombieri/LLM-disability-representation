import pandas as pd
import os
import matplotlib.pyplot as plt

# File paths for datasets
file_paths = [
    "../DatasetsAnnotated/csv_NCR.csv",
    "../DatasetsGenerated/gemini15flash_generated_NCR.csv",
    "../DatasetsGenerated/gpt4omini_generated_NCR.csv",
    "../DatasetsGenerated/mistral8b_generated_NCR.csv"
]

# Function to load the CSV files into DataFrames
def load_data(file_paths):
    dataframes = []
    for file in file_paths:
        df = pd.read_csv(file)
        dataframes.append(df)
    return dataframes

# Function to calculate the average value of each emotion across all models
def compare_emotions(dataframes):
    # Exclude 'positive' and 'negative' emotions from the comparison
    emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']
    models = ['r/disability', 'Gemini-1.5F', "GPT-4o-mini", "Mixtral-8B"]
    
    # Create a dictionary to store the comparison of emotions across models
    comparison = {}
    for emotion in emotions:
        # Calculate the mean for each emotion across all models
        comparison[emotion] = [df[emotion].mean() for df in dataframes]
    
    # Create a DataFrame with emotions as rows and models as columns
    comparison_df = pd.DataFrame(comparison, index=[models[i] for i in range(len(dataframes))])
    comparison_df = comparison_df * 100

    return comparison_df

def plot_comparison(comparison_df):
    # Define hatching patterns for each model
    patterns = ['...', '---', '////', 'xxx']  # Finer patterns for better readability
    models = comparison_df.index.tolist()
    emotions = comparison_df.columns.tolist()

    # Transpose for emotions on the x-axis
    ax = comparison_df.T.plot(kind='bar', figsize=(12, 6), width=0.8)

    # Explicitly apply patterns based on the model index
    bars = ax.patches  # Get all the bars
    num_models = len(models)  # Number of models
    num_emotions = len(emotions)  # Number of emotions

    # Group bars by emotions, ensuring same model uses the same pattern across emotions
    for emotion_idx in range(num_emotions):
        for model_idx in range(num_models):
            bar_idx = model_idx * num_emotions + emotion_idx
            print(patterns[model_idx])
            print(bar_idx)
            bars[bar_idx].set_hatch(patterns[model_idx])  # Match model to its pattern
            bars[bar_idx].set_edgecolor('black')          # Add a black edge for better visibility

    # Format the plot
    plt.xlabel('Emotion', fontsize=18)
    plt.ylabel('Emotion distribution (%)', fontsize=18)
    plt.xticks(rotation=0, ha='center', fontsize=18)
    plt.yticks(fontsize=18)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(models, fontsize=12, loc='upper left')  # Ensure legend reflects the models

    # Tight layout and save the figure
    plt.tight_layout()
    output_file = os.path.join("..", "Figures", "NCR", "emotions_NCR_accessible.png")
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0.03, dpi=300)
    print(f"Figure saved as {output_file}")
    plt.show()


# Example usage
if __name__ == "__main__":
    dataframes = load_data(file_paths)
    comparison_df = compare_emotions(dataframes)
    print(comparison_df)
    plot_comparison(comparison_df)
