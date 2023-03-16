import os
import openai
import json
import tiktoken


# function to read secrets.json file
def read_secrets(file_name='secrets.json') -> dict:
    filename = os.path.join(file_name)
    try:
        with open(filename, mode="r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}


# function to calculate number of tokens in the prompt
def num_tokens_from_prompt(prompt, encoding) -> int:
    num_tokens = len(encoding.encode(prompt))
    return num_tokens


# function to call the gpt api
def GPT_Completion(prompt):
    openai.api_key = api_key
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        temperature=0.8,
        top_p=1,
        max_tokens=1024
    )
    return response.choices[0].text


secrets = read_secrets()
api_key = secrets['api_key']

# data in the sample.json file was generated from ChatGPT
info = read_secrets('sample.json')

commenter_prompt = "You are a person with the following background:"
commenter_background = info['commenter_background']
comment_prompt = '\n Write a comment for the LinkedIn post below and include a question:'
linkedin_post = info['linkedin_post']

# combine to form full prompt
prompt = commenter_prompt + commenter_background + comment_prompt + linkedin_post
encoding = tiktoken.encoding_for_model('text-davinci-003')

num_tokens = num_tokens_from_prompt(prompt, encoding)
print(num_tokens)

if num_tokens <= 4096:
    response = GPT_Completion(prompt)
    print(response)
else:
    print('Prompt is too long')
