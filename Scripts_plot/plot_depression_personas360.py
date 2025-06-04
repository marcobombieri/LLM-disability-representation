import pandas as pd
import matplotlib.pyplot as plt
import re

# Models and file paths
models = ['Gemini-1.5F', "GPT-4o-mini", "Mixtral-8B"]
fontsize1 = 18
fontsize2 = 14

# File paths (pairs of files)
file_paths = [
    ["../DatasetsGenerated/gemini15flash_generated_depression.csv", "../DatasetsGenerated/gemini15flash_generated_no-dis-360_depression.csv"],
    ["../DatasetsGenerated/gpt4omini_generated_depression.csv", "../DatasetsGenerated/gpt4omini_generated_no-dis-360_depression.csv"],
    ["../DatasetsGenerated/mistral8b_generated_depression.csv", "../DatasetsGenerated/mistral_generated_no-dis_360_depression.csv"]
]

# Initialize a list to store results
comparison_results = []

# Regular expression to extract the first label
label_regex = r"\[\[\{'label': '([^']+)'"

# Process each pair of files
for pair in file_paths:
    file1, file2 = pair
    label_counts = {'Disability': {'not depression': 0, 'moderate': 0, 'severe': 0},
                    'Persona': {'not depression': 0, 'moderate': 0, 'severe': 0}}
    total_counts = {'Disability': 0, 'Persona': 0}  # Total rows for percentage calculation

    for i, file in enumerate([file1, file2]):
        label = 'Disability' if i == 0 else 'Persona'
        data = pd.read_csv(file, header=None)

        # Extract and count the first label
        for _, row in data.iterrows():
            match = re.search(label_regex, row[1])
            if match:
                extracted_label = match.group(1)
                if extracted_label in label_counts[label]:
                    label_counts[label][extracted_label] += 1
        total_counts[label] = sum(label_counts[label].values())  # Total valid rows for the file

    # Convert counts to percentages
    percentages = {
        'Disability': {key: (value / total_counts['Disability'] * 100) for key, value in label_counts['Disability'].items()},
        'Persona': {key: (value / total_counts['Persona']* 100) for key, value in label_counts['Persona'].items()}
    }
    comparison_results.append(percentages)

# Plotting the bar plots
for i, percentages in enumerate(comparison_results):
    labels = ['not depression', 'moderate', 'severe']
    file1_values = [percentages['Disability'][label] for label in labels]
    file2_values = [percentages['Persona'][label] for label in labels]
    
    x = range(len(labels))  # Number of depression categories
    
    plt.figure(figsize=(6, 4.5))
    plt.bar(x, file1_values, width=0.4, label='LLM_D_MIX', align='center', alpha=0.7, hatch='...')
    plt.bar([p + 0.4 for p in x], file2_values, width=0.4, label='LLM_ND_MIX', align='center', alpha=0.7, hatch='---')
    plt.xticks([p + 0.2 for p in x], labels, fontsize=fontsize1)
    plt.ylabel('Depression distribution (%)', fontsize=fontsize1)
    plt.yticks(fontsize=fontsize2)
    #plt.title(f'Depression Label Comparison: {models[i]}', fontsize=fontsize1)
    plt.legend(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'depression_label_comparison_pair_{models[i]}.png', bbox_inches='tight', pad_inches=0.01, dpi=300)
    plt.show()
