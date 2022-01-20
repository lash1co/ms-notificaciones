from flask import Flask
import os
import environment
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import request
from twilio.rest import Client

app = Flask(__name__)

@app.route("/send-sms")
def sms():
    cadenaHash = request.args.get("hash")
    if cadenaHash == os.environ.get("HASH"):
        destino = request.args.get("destinatario")
        mensaje = request.args.get("mensaje")
        try:
            account_sid = os.environ['TWILIO_ACCOUNT_SID']
            auth_token = os.environ['TWILIO_AUTH_TOKEN']
            client = Client(account_sid, auth_token)
            
            message = client.messages \
                            .create(
                                 body=mensaje,
                                 from_=os.environ.get("TWILIO_PHONE_NUMBER"),
                                 to='+'+destino
                             )
            
            print(message.sid)
            print("Enviado")
            return "OK"
        except Exception as e:
            print("No enviado")
            return "KO"
    else:
        print("No existe un hash o es incompatible")
        return "KO"

@app.route("/send-email")
def correo():
    cadenaHash = request.args.get("hash")
    #print(cadenaHash)
    #print(os.environ.get("HASH"))
    if cadenaHash == os.environ.get("HASH"):
        destino = request.args.get("destinatario")
        mensaje = request.args.get("mensaje")
        asunto = request.args.get("asunto")
        
        message = Mail(
        from_email=os.environ.get("EMAIL_FROM"),
        to_emails=destino,
        subject=asunto,
        html_content=mensaje)
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print("Enviado")
            return "Ok"
        except Exception as e:
            print("No enviado")
            return "KO"
    else:
        print("No existe un hash o es incompatible")
        return "KO"
if __name__ == '__main__':
    #environment.crearVariables()
    app.run()
