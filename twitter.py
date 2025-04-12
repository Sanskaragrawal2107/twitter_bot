import os
from dotenv import load_dotenv
import tweepy
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.tools import tool


load_dotenv()

def authenticate_twitter():
    """Authenticate with Twitter API v2"""
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    return client


@tool
def post_to_twitter(text: str) -> str:
    """ (max of 280 characters). If you are asked to post a tweet, use this tool."""
    client = authenticate_twitter()
    response = client.create_tweet(text=text)
    return f"Tweet posted successfully with ID: {response.data['id']}"
    


tools = [
    Tool.from_function(
        post_to_twitter,
        name="post_to_twitter",
        description="Post a short tweet to Twitter (max of  280 characters). If you are asked to post a tweet, use this tool."
    )
]


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7,api_key=os.getenv("GOOGLE_API_KEY"))


agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.run(user_input)
        print("Bot:", response)
