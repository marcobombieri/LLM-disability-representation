#!/bin/bash

python marked_words.py ../DatasetsCorpora/corpora_mixtral8b_dis_no-dis.csv --target_val 'dis' --target_col 'disability' --unmarked_val 'no-dis' > keywords_mixtral_dis_nodis.txt
python marked_words.py ../DatasetsCorpora/corpora_gemini15flash_dis_no-dis.csv --target_val 'dis' --target_col 'disability' --unmarked_val 'no-dis' > keywords_gemini_dis_nodis.txt
python marked_words.py ../DatasetsCorpora/corpora_gpt4omini_dis_no-dis.csv --target_val 'dis' --target_col 'disability' --unmarked_val 'no-dis' > keywords_gpt_dis_nodis.txt
