import openai
import os

from dotenv import load_dotenv, find_dotenv

def reload_env_and_api_key():
    load_dotenv(find_dotenv(), override=True)  # override=True ensures updated values
    openai.api_key = os.getenv('OPENAI_API_KEY')

# Initial load
reload_env_and_api_key()


client = openai.OpenAI()

def get_completion(prompt, model="gpt-4o"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


text = f"""
In a charming village, siblings Jack and Jill set out on 
a quest to fetch water from a hilltop 
well. As they climbed, singing joyfully, misfortune 
struck—Jack tripped on a stone and tumbled 
down the hill, with Jill following suit. 
Though slightly battered, the pair returned home to 
comforting embraces. Despite the mishap, 
their adventurous spirits remained undimmed, and they 
continued exploring with delight.
"""
# example 1
prompt_1 = f"""
Perform the following actions: 
1 - Summarize the following text delimited by triple 
backticks with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the following 
keys: french_summary, num_names.

Separate your answers with line breaks.

Text:
```{text}```
"""
response = get_completion(prompt_1)
print("Completion for prompt 1:")
print(response)


prompt = f"""
Your task is to determine if the student's solution 
is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem including the final total. 
- Then compare your solution to the student's solution 
and evaluate if the student's solution is correct or not. 
Don't decide if the student's solution is correct until 
you have done the problem yourself.

Use the following format:
Question:
```
question here
```
Student's solution:
```
student's solution here
```
Actual solution:
```
steps to work out the solution and your solution here
```
Is the student's solution the same as actual solution 
just calculated:
```
yes or no
```
Student grade:
```
correct or incorrect
```

Question:
```
I'm building a solar power installation and I need help 
working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost 
me a flat $100k per year, and an additional $10 / square 
foot
What is the total cost for the first year of operations 
as a function of the number of square feet.
``` 
Student's solution:
```
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
```
Actual solution:
"""
response = get_completion(prompt)
print(response)

# Give the model time to “think”