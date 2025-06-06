import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')


client = openai.OpenAI()

def get_completion(prompt, model="gpt-4o"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


prompt = f"""
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest 
valley flows from a modest spring; the 
grandest symphony originates from a single note; 
the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.
"""
response = get_completion(prompt)
print(response)

prompt = f"""
Task: Convert informal sentences to formal style.

Informal: “Need the docs ASAP, thx!”
Formal:   “Could you please send the documents as soon as possible? Thank you.”

Informal: “What’s up with the late delivery?”
Formal:   “Could you let me know the reason for the delay in delivery?”

Informal: “Catch you later.”
Formal:
"""

response = get_completion(prompt)
print(response)

# Pick highly representative demos
# • Cover edge cases the model often gets wrong.
# • Keep demos stylistically similar to the answer you hope to see.

# Use clear separators (\n\n, ---, or XML-like tags) to mark input vs. output.

# Keep it short—token budget is precious. A common sweet spot is 3 – 5 exemplars.

# Order matters: earlier examples can carry more weight, so place the closest analogy first.

# Try “format stacking”: add an instruction block before the demos

# "Few-shot" prompting