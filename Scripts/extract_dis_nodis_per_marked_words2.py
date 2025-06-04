import csv

# Read the CSV file
file_paths=["../DatasetsAnnotated/ANN_csv.csv",
"../DatasetsGenerated/gemini15flash_generated.csv",
"../DatasetsGenerated/gpt4omini_generated.csv",
"../DatasetsGenerated/mistral8b_generated.csv",
]

columns=['reddit', 'gemini15f', 'gpt4omini', 'mistral8b']

output_path ="../DatasetsCorpora/corpora_rdisability_ai_2.csv"

with open(output_path, mode='w', encoding='utf-8') as o:
    writer = csv.writer(o)
    writer.writerow(["disability", "text"])
    for i, file_path in enumerate(file_paths):
        print(i, file_path)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Convert to a list or process row by row
            rows = [row for row in reader]  # List of rows
            for row in rows:
                if i==0:
                    if int(row[1])==1:
                        print(row[0])
                        data=["reddit", row[3]]
                        print(data)
                        writer.writerow(data)
                else:
                    data=[columns[i], row[4]]
                    writer.writerow(data)

