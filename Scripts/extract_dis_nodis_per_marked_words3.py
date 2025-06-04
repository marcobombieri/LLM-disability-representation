import csv

# Read the CSV file
file_paths=[
    ["../DatasetsGenerated/mistral8b_generated.csv", "../DatasetsGenerated/mistral8b_generated_no-dis.csv"],
    ["../DatasetsGenerated/gemini15flash_generated.csv", "../DatasetsGenerated/gemini15flash_generated_no-dis.csv"],
    ["../DatasetsGenerated/gpt4omini_generated.csv", "../DatasetsGenerated/gpt4omini_generated_no-dis.csv"],
]

columns=['dis', 'no-dis']

output_paths=[
    "../DatasetsCorpora/corpora_mixtral8b_dis_no-dis.csv",
    "../DatasetsCorpora/corpora_gemini15flash_dis_no-dis.csv",
    "../DatasetsCorpora/corpora_gpt4omini_dis_no-dis.csv"
]

for i, file_path in enumerate(file_paths):
    with open(file_path[0], mode='r', encoding='utf-8') as fdis, open(file_path[1], mode='r', encoding='utf-8') as fnodis, open(output_paths[i], mode='w', encoding='utf-8') as fout:
        writer = csv.writer(fout)
        writer.writerow(["disability", "text"])
        reader_dis = csv.reader(fdis)
        reader_nodis = csv.reader(fnodis)
        rows_dis = [row for row in reader_dis]  # List of rows
        rows_nodis = [row for row in reader_nodis]
        for row in rows_dis:        
            data=["dis", row[4]]
            writer.writerow(data)
        for row in rows_nodis:        
            data=["no-dis", row[4]]
            writer.writerow(data)

