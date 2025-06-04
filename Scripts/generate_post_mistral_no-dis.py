from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from auto_gptq import exllama_set_max_input_length
import pandas as pd
import os
import csv

model_name_or_path = "TheBloke/Mixtral-8x7B-Instruct-v0.1-GPTQ"
#model_name_or_path = "TheBloke/Llama-2-13B-chat-GPTQ"
#model_name_or_path = "astronomer/Llama-3-8B-Instruct-GPTQ-8-Bit"
model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                             device_map="auto",
                                             trust_remote_code=False,
                                             revision="main")

#model = exllama_set_max_input_length(model, max_input_length=8192)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

repetitions=60

output_path = os.path.join("mistral_generated_no-dis_360.csv")
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

with open(output_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    count = 1
    for d in ldisabilities:
        for p in ldposts:
            for i in range(0, repetitions):
                prompt = f'{prefix1} {d} {prefix2} {p}'
                prompt_template=f'''[INST] <<SYS>>

                <</SYS>>
                {prompt}[/INST]'''
                
                pipe = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_new_tokens=1024,
                    do_sample=True,
                    temperature=1.0,
                    #top_p=0.95,
                    #top_k=40,
                    #repetition_penalty=1
                )

                model_answer = (pipe(prompt_template)[0]['generated_text'])
                start_index = model_answer.find("[/INST]")  # Find the index where "[/INST]" starts
                if start_index != -1:  # If "[/INST]" is found in the output
                    text_after_inst = model_answer[start_index + len("[/INST]"):].strip()  # Extract text after "[/INST]"
                    #print(text_after_inst)
                else:
                    print("ERROR")

                data = [count, d, p, prompt, text_after_inst]
                writer.writerow(data)
                count = count + 1