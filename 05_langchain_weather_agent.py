from langchain_community.chat_models import ChatOllama
from langchain.agents import initialize_agent, AgentType, Tool
import requests

# Weather API setup
WEATHER_API_KEY = "your_openweathermap_api_key"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Define the tool function
def get_weather(location: str) -> str:
    """Fetches current weather for a given location."""
    params = {
        "q": location,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        return f"The current weather in {location} is {weather}, {temp}°C, humidity {humidity}%."
    else:
        return f"Could not fetch weather for {location}. Please check the location name."

# Register the tool with name and description
weather_tool = Tool(
    name="get_weather",
    func=get_weather,
    description="Use this tool to get the current weather for a given city."
)

# Initialize Ollama model
llm = ChatOllama(model="gemma3:1b")

# Create the agent
agent = initialize_agent(
    tools=[weather_tool],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# Main loop
def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.run(user_input)
        print("Assistant:", response)

if __name__ == "__main__":
    main()
