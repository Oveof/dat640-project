import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from accelerate import Accelerator, load_checkpoint_and_dispatch

import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv('HF_TOKEN')

from huggingface_hub import login

login(token=HF_TOKEN)

model_name = "mistralai/Mistral-7B-Instruct-v0.3"


from transformers import AutoModelForCausalLM, AutoTokenizer


local_cache_dir = "./local_model_cache"

model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", cache_dir=local_cache_dir)
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=local_cache_dir)


messages = [

    {"role": "user", "content": "What is your favourite condiment?"},

    {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},

    {"role": "user", "content": "Do you have mayonnaise recipes?"}

]

model_inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
generated_ids = model.generate(model_inputs, max_new_tokens=100, do_sample=True)
print(tokenizer.batch_decode(generated_ids)[0])
