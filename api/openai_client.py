import openai
from dotenv import load_dotenv
import os

load_dotenv()

def get_gpt_response(promt):
    api_key = os.getenv('GPT_API_KEY')

    client = openai.OpenAI(
        api_key=api_key,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": promt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    print(response)
    content = response.choices[0].message.content.strip()
    #print(str(content))
    return content
