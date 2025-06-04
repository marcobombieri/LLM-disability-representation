import openai
import os
import csv
import time
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


#from dotenv import load_dotenv, find_dotenv
#_ = load_dotenv(find_dotenv()) # read local .env file
API_KEY='[API-KEY]'

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
generation_config = genai.GenerationConfig(
  temperature=1.0
)

def get_completion(prompt):
    try:
        response = model.generate_content(
                prompt,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
                },
                generation_config = generation_config
        )
        return response.text
    except Exception as e:
        print("Exeception ", e)
        return None



output_path = os.path.join("gemini15flash_generated.csv")
#f_disability_submissions = os.path.join("disabled_submissions.txt")

ldisabilities = ["a person with a disability.", 
    "a person with autism.", 
    "a person with blindness.", 
    "a person with deafness.", 
    "a person with cerebral palsy.", 
    "a person with depression."]

ldposts = ["and sharing the experiences related to your disability.",
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
            for i in range(0, 10):
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