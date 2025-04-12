from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    from twitter import agent
    
    user_input = request.form.get("Body")
    
    response = agent.invoke("post tweet if asked, otherwise just respond to the user: " + user_input)
    
    
    reply = MessagingResponse()
    reply.message(str(response))
    return str(reply)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
