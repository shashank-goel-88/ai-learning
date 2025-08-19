# -*- coding: utf-8 -*-
import json
import os
import requests
import ollama
import certifi

MEMORY_FILE = "agent_memory.json"

class PersistentMemory:
    def __init__(self, filename=MEMORY_FILE):
        self.filename = filename
        self.store = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def set(self, key, value):
        self.store[key] = value
        with open(self.filename, 'w') as f:
            json.dump(self.store, f, indent=2)

    def get(self, key):
        return self.store.get(key)

class WeatherTool:
    def run(self, location="Bangalore"):
        url = "http://api.weatherapi.com/v1/current.json"
        params = {
            "key": "f7c11c4095b94f47859131059250808",  # Replace with your actual API key
            "q": location
        }
        try:
            response = requests.get(url, params=params, verify=certifi.where())
            data = response.json()
            temp = data['current']['temp_c']
            condition = data['current']['condition']['text']
            return f"The current temperature in {location} is {temp}°C with {condition}."
        except Exception as e:
            return f"Error fetching weather: {e}"

class IntentDetector:
    def __init__(self, model='gemma3:1b'):
        self.model = model

    def detect(self, user_input):
        prompt_intent = f"""Classify the user's intent from: weather, chat.
User input: "{user_input}"
Respond with only one word."""
        response = ollama.chat(model=self.model, messages=[
            {'role': 'user', 'content': prompt_intent}
        ])
        return response['message']['content'].strip().lower()

class LocationDetector:
    def __init__(self, model='gemma3:1b'):
        self.model = model

    def detect(self, user_input):
        prompt_intent = f"""Extract the location from the following user query where they are asking about the weather. If no location is explicitly mentioned, infer if possible from context or return 'unknown'. Query: '{user_input}'"""
        response = ollama.chat(model=self.model, messages=[
            {'role': 'user', 'content': prompt_intent}
        ])
        return response['message']['content'].strip().lower()

class OllamaAgent:
    def __init__(self, model='gemma3:1b'):
        self.model = model
        self.memory = PersistentMemory()
        self.intentDetectors = {
            "intent": IntentDetector(),
            "location": LocationDetector()
        }
        self.tools = {
            "weather": WeatherTool()
        }

    def respond(self, user_input):
        # Store facts like "My name is Shashank" or "My city is Delhi"
        if "my name is" in user_input.lower():
            name = user_input.split("my name is")[-1].strip().capitalize()
            self.memory.set("name", name)
            print(f"Agent: Nice to meet you, {name}!")
            return

        if "my city is" in user_input.lower():
            city = user_input.split("my city is")[-1].strip().capitalize()
            self.memory.set("city", city)
            print(f"Agent: Got it! I'll remember your city is {city}.")
            return

        intent = self.intentDetectors["intent"].detect(user_input)
        print(f"Debug: intent={intent}")
        if intent == "weather":
            city = self.intentDetectors["location"].detect(user_input)
            if city == "unknown":
                city = self.memory.get("city") or "Bangalore"
            print(f"Debug: city={city}")
            print("Agent: " + self.tools["weather"].run(location=city))
        else:
            context = ". ".join([f"{k}: {v}" for k, v in self.memory.store.items()])
            system_prompt = f"You are a helpful assistant. Known facts: {context}"
            print("Agent: ", end='', flush=True)
            stream = ollama.chat(
                model=self.model,
                messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_input},
                ],
                stream=True,
                )
            for token in stream:
                print(token['message']['content'], end='', flush=True)
            print()


def main():
    agent = OllamaAgent()
    print("🤖 Ollama Agent with Persistent Memory is ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        if len(user_input) > 0:
            agent.respond(user_input)

if __name__ == "__main__":
    main()
