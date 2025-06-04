import pandas as pd
import matplotlib.pyplot as plt


models = ['Gemini-1.5F', "GPT-4o-mini", "Mixtral-8B"]
fontsize1=18
fontsize2=14


# File paths (pairs of files)
file_paths = [
    ["../DatasetsGenerated/gemini15flash_generated_VADER.csv", "../DatasetsGenerated/gemini15flash_generated_no-dis-360_VADER.csv"],
    ["../DatasetsGenerated/gpt4omini_generated_VADER.csv", "../DatasetsGenerated/gpt4omini_generated_no-dis-360_VADER.csv"],
    ["../DatasetsGenerated/mistral8b_generated_VADER.csv", "../DatasetsGenerated/mistral_generated_no-dis_360_VADER.csv"]
]

# Initialize a list to store the percentages for each pair
comparison_results = []

# Process each pair of files
for pair in file_paths:
    file1, file2 = pair
    sentiment_counts = {'Disability': {'Positive': 0, 'Negative': 0},
                        'Persona': {'Positive': 0, 'Negative': 0 }}
    total_counts = {'Disability': 0, 'Persona': 0}  # To store total counts for percentage calculation
    
    for i, file in enumerate([file1, file2]):
        label = 'Disability' if i == 0 else 'Persona'
        data = pd.read_csv(file, header=None)
        
        # Count the occurrences of each sentiment
        for _, row in data.iterrows():
            sentiment = row[2]  # Third element is the sentiment label
            sentiment_counts[label][sentiment] += 1
        total_counts[label] = len(data)  # Total rows in the file
    
    # Convert counts to percentages
    percentages = {
        'Disability': {key: (value / total_counts['Disability']* 100)  for key, value in sentiment_counts['Disability'].items()},
        'Persona': {key: (value / total_counts['Persona'] * 100)  for key, value in sentiment_counts['Persona'].items()}
    }
    comparison_results.append(percentages)

# Plotting the bar plots
for i, percentages in enumerate(comparison_results):
    labels = ['Positive', 'Negative']
    file1_values = [percentages['Disability'][label] for label in labels]
    file2_values = [percentages['Persona'][label] for label in labels]
    
    print(file1_values)
    print()
    print(file2_values)
    print("\n\n\n")
    
    x = range(len(labels))  # Number of sentiment categories
    
    plt.figure(figsize=(4.7, 4))
    plt.bar(x, file1_values, width=0.4, label='LLM_D_GPT', align='center', alpha=0.7, hatch='...')
    plt.bar([p + 0.4 for p in x], file2_values, width=0.4, label='LLM_ND_GPT', align='center', alpha=0.7, hatch='---')
    plt.xticks([p + 0.2 for p in x], labels, fontsize=fontsize1)
    plt.ylabel('Sentiment distribution (%)', fontsize=fontsize1)
    plt.yticks(fontsize=fontsize2)
    #plt.title(f'Sentiment Percentage Comparison: Pair {i+1}')
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'sentiment_percentage_comparison_pair_{models[i]}.png', bbox_inches='tight', pad_inches=0.01, dpi=300)
    plt.show()
