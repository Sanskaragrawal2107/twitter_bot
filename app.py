from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twitter import agent, tools

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    # Assign the first tool from the tools list to twitter_tool
    twitter_tool = tools[0]
    
    # Keep track of whether a tweet has been posted or not
    if not hasattr(twitter_tool, "has_posted"):
        twitter_tool.has_posted = False

    user_input = request.form.get("Body")
    
    if not twitter_tool.has_posted:
        response = agent.run("Post only ONE tweet: " + user_input)
        twitter_tool.has_posted = True  # Mark as posted
    else:
        response = "You can only post one tweet."

    reply = MessagingResponse()
    reply.message(str(response))
    return str(reply)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
