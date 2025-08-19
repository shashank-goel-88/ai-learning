import requests
import ollama
import json

class StreamingOllamaChatbot:
    def __init__(self, model='gemma3:1b', history_limit=4):
        self.model = model
        self.chat_history = []
        self.system_prompt = {
                'role': 'system',
                'content': 'You are a helpful assistant. Keep responses concise and relevant.'
        }
        self.history_limit = history_limit

    def send_message(self, user_input):
        self.chat_history.append({'role': 'user', 'content': user_input})
        recent_history = [self.system_prompt] + self.chat_history[-self.history_limit:]

        print("Bot: ", end='', flush=True)
        response_stream = ollama.chat(model=self.model, messages=recent_history, stream=True)
        full_response = ''
        for chunk in response_stream:
            token = chunk['message']['content']
            print(token, end='', flush=True)
            full_response += token
        print()
        self.chat_history.append({'role': 'assistant', 'content': full_response})

def main():
        bot = StreamingOllamaChatbot()
        print("🤖 Streaming Ollama Chatbot with Weather is ready! Type 'exit' to quit.\n")

        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            bot.send_message(user_input)

if __name__ == "__main__":
        main()

