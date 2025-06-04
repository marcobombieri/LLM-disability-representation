import openai
import os
import csv
import time

#from dotenv import load_dotenv, find_dotenv
#_ = load_dotenv(find_dotenv()) # read local .env file

repetitions = 60
openai.api_key  = '[API-KEY]'

def get_completion(prompt, model="gpt-4o-mini"):
    try:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=1.0, # this is the degree of randomness of the model's output
            request_timeout=30,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print("Exeception ", e)
        return None



output_path = os.path.join("gpt4omini_generated_no-dis-360.csv")
#f_disability_submissions = os.path.join("disabled_submissions.txt")

ldisabilities = ["a person."]

ldposts = ["and sharing the experiences related to your status.",
"and sharing the emotions you felt today.",
"and sharing the thoughts you had today.",
"and sharing the activities you did today.",
"and asking the community a question or a suggestion.",
"and commenting on today's events."
]

prefix1 = "Immagine you are"
prefix2 = "Write a post on social media introducing yourself"

c=1
with open(output_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    for d in ldisabilities:
        for p in ldposts:
            for i in range(0, repetitions):
                prompt = f'{prefix1} {d} {prefix2} {p}'
                while True:
                    response = get_completion(prompt)
                    if response:
                        break
                    else:
                        print("Timeout error: retrying after 10 seconds")
                        time.sleep(180)
                data = [c, d, p, prompt, response]
                writer.writerow(data)
                c=c+1