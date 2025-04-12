from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twitter import agent, tools

app = Flask(__name__)

# Store the has_posted flag in a dictionary
posted_status = {}

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    # Assign the first tool from the tools list to twitter_tool
    twitter_tool = tools[0]
    
    # Get the user input from the message body
    user_input = request.form.get("Body")
    
    # Use a unique identifier for each user (e.g., user_input or phone number)
    user_id = user_input.strip()  # You can customize this based on how you want to identify users

    # Initialize the flag if not already set
    if user_id not in posted_status:
        posted_status[user_id] = False

    if not posted_status[user_id]:
        # Run the agent to post the tweet
        response = agent.run("Post only ONE tweet: " + user_input)
        posted_status[user_id] = True  # Mark as posted
    else:
        response = "You can only post one tweet."

    # Send the response back to WhatsApp
    reply = MessagingResponse()
    reply.message(str(response))
    return str(reply)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
