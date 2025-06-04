import matplotlib.pyplot as plt
import numpy as np

fontsize1=18
fontsize2=14

# Data
categories = [
    "anger", "anticipation", "joy", "surprise", 
    "trust", "disgust", "sadness", "fear"
]
sv_path = "values-emotions-z-score.csv"  # Update the path if needed
data = pd.read_csv(csv_path)

# Access the columns as lists 
llms_values = data['llms_values'].tolist()
r_disabilities_values = data['r_disabilities_values'].tolist()

# Multiply by 100 to convert to percentages
llms_values = np.array(llms_values) * 100
r_disabilities_values = np.array(r_disabilities_values) * 100

# Bar width and positions
bar_width = 0.35
x = np.arange(len(categories))  # Position of each category on x-axis

# Create the plot
patterns = ['...', '---']  # Finer patterns for better readability
fig, ax = plt.subplots(figsize=(11, 5))
bars1 = ax.bar(x - bar_width/2, llms_values, bar_width, label='LLM_D versus RED_D',  hatch='...')
bars2 = ax.bar(x + bar_width/2, r_disabilities_values, bar_width, label='RED_D versus LLM_D', hatch='---')

# Add labels, title, and legend
ax.set_xlabel('Emotions', fontsize=fontsize1)
ax.set_ylabel('Emotion distribution (%)', fontsize=fontsize1)
#ax.set_title('Comparison of Emotional Distributions', fontsize=fontsize1)
ax.set_xticks(x)
plt.yticks(fontsize=fontsize1)
ax.set_xticklabels(categories, fontsize=fontsize1)
ax.legend(fontsize=fontsize2)

# Add gridlines
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Display values on top of bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        
        #ax.text(
        #    bar.get_x() + bar.get_width() / 2,
        #    height + 0.01,
        #    f'{height:.2f}',
        #    ha='center',
        #    fontsize=9
        #)

# Tight layout
plt.tight_layout()

# Save the plot as PNG
output_file = "emotional_distributions.png"
plt.savefig(output_file, bbox_inches='tight', pad_inches=0.03, dpi=300)
print(f"Plot saved as {output_file}")

# Show the plot
plt.show()
