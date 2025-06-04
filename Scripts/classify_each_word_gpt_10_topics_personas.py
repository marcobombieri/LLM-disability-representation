'''
'''
import openai
import pandas as pd
import os
import csv

path = os.path.join("..", "Results", "merged_dis_no-dis360_filtered.csv")
outp = os.path.join("..", "Results", "merged_dis_no-dis360_filtered_10_topics_personas.csv")

openai.api_key  = '[API-KEY]'

def get_completion(prompt, model="gpt-4o-mini"):
    try:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.0, # this is the degree of randomness of the model's output
            request_timeout=30,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print("Exeception ", e)
        return None

words = []
zscores = []

with open(path, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    

    for row in reader:
        if row[2] == 'True':
            words.append(row[0])
            zscores.append(row[1])

with open(outp, mode="w", encoding="utf-8") as fo:
    writer = csv.writer(fo)
    for word, zscore in zip(words,zscores):
        #print(word, zscore)
        prompt = f'''I have a list of words, and I would like you to classify them into the following topics:
            "1. Disability and Impairments"
            "2. Inclusion and Accessibility"
            "3. Emotions and Mental Health"
            "4. Support and Advocacy"
            "5. Independence and Autonomy"
            "6. Social Interactions and Communication"
            "7. Acceptance and Understanding"
            "8. Adaptation and Coping"
            "9. Isolation and Loneliness"
            "10. Strength and Resilience"
            Please carefully examine the meaning of each word and assign it to the most appropriate topic. 
            If a word could fit into multiple categories, choose the one where it is most relevant.
            In the answer do not add extra text or clarification, only report the topics.
            Classify this word: "{word}"
            '''
        while True:
            response = get_completion(prompt)
            if response:
                break
            else:
                print("Timeout error: retrying after 10 seconds")
                time.sleep(180)
        data = [word, zscore, response]
        writer.writerow(data)

        