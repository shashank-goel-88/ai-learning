import ollama

def chat_with_model(prompt, model='gemma3:1b'):
    stream = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
            )
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

if __name__ == "__main__":
    print("Welcome to the Ollama Chat App!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        chat_with_model(user_input)
        print("\n")

