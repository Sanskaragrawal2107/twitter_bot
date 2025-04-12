from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    from twitter import agent, twitter_tool
    
    twitter_tool.has_posted = False
    user_input = request.form.get("Body")
    response = agent.run("post a tweet if asked otherwise respond to user" + user_input)

    reply = MessagingResponse()
    reply.message(str(response))
    return str(reply)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
