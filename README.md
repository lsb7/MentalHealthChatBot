# MentalHealthChatBot
Instruction-tuned Chatbot for Mental Health using Llama2

Our project trains models using Llama2.

We will train the following models with the following 3 datasets:

1) (PHR) phr_mental_therapy_dataset: https://huggingface.co/datasets/vibhorag101/phr_mental_therapy_dataset
2) (COUNSELING) mental_health_counseling_conversation: https://huggingface.co/datasets/Amod/mental_health_counseling_conversations
3) (REDDIT) Data scraped from subreddits (r/offmychest, r/advice, r/mentalhealth, r/confessions, r/self): web_scraper.py obtains this data

We will TRAIN 3 models on a mixture of data as follows: 
1) COUNSELING (first 1000 rows)
2) COUNSELING (first 1000 rows) and PHR (first 1000 rows)
3) COUNSELING (first 1000 rows) and REDDIT (1000)

And EVALUATE them together with a Vanilla model using BLEU score on UNSEEN counseling data (last 500 rows of COUNSELING dataset) that has professional responses.

The code we have provided below trains the models, evaluates the BLEU score of their responses, and runs on Google Co-lab.

llama_2_vanilla.py
finetuned_llama_2_v1.py
finetuned_llama_2_v2.py
finetuned_llama_2_v3.py
web_scraper.py (Gets data from reddit API)
