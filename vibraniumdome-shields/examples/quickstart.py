import os
from openai import OpenAI

from vibraniumdome_sdk import VibraniumDome

VibraniumDome.init(app_name="set_you_agent_name_here")

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Tell me a joke about opentelemetry"}],
    user="user-123456",
    extra_headers={"x-session-id": "abcd-1234-cdef"},
)

print(completion.choices[0].message.content)
