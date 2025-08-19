from ollama import chat
from ollama import ChatResponse

print("User: Why is the sky blue?")
response: ChatResponse = chat(model='gemma3:1b', messages=[
      {
              'role': 'user',
                  'content': 'Why is the sky blue?',
                    },
      ])
print("LLM: " + response['message']['content'])
# or access fields directly from the response object
#print(response.message.content)

