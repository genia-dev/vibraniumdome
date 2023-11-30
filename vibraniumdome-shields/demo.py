import openai
from vibraniumdome_sdk import VibraniumDome

VibraniumDome.init(app_name="your_app_name_here")

response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello World"},
    ],
    temperature=0,
    request_timeout=30,
    user="used_id",
    headers={"x-session-id": "session_id"},
)
