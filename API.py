import os
import config
from flask import Flask, request, send_file
from flask_restful import Resource, Api
from flask_cors import CORS
from twilio.rest import Client
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import db_connector as db
import time

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


class MESSAGE(Resource):

  def post(self):
        
    number = request.form['From']
    message_body = request.form['Body'].lower() # message enviado
    message = "No estas registrado en la base de datos."

                
    client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)
    ngrok_url = config.URL_NGROK

    exist, username = db.findUser(number) 

    if not exist:
        # El Paciente no esta registrado
        print(message_body)
        print(message_body.find("nombre"))
        if message_body.find("nombre") != -1:
            text = message_body.split()
            if db.AddUser(number, text[1]):
                message = "Fuiste registrado!"
                message = client.messages.create (
                                    from_='whatsapp:+14155238886',  
                                    body=message,
                                    to=number
                                    )
        else:
            message = "No estas registrado en la base de datos."
            message = client.messages.create(
                            from_='whatsapp:+14155238886',  
                            body=message,
                            to=number)
            message = "Para registrarte porfavor manda un mensaje con este formato.\nNombre: tunombre"
            message = client.messages.create(
                            from_='whatsapp:+14155238886',  
                            body=message,
                            to=number)
    else:
        if message_body == "hola":
            message = f"Hola, {username}!\nPara realizar una consulta de ritmo cardiaco escriba: 'Consulta pulso'"        
            message = client.messages.create (
                                    from_='whatsapp:+14155238886',  
                                    body=message,
                                    to=number
                                    )
            
        
        # El paciente si esta registrado                        
        if message_body.find("consulta") != -1:
            print("Se requiere una consulta.")
            # Si se requiere una consulta del pulso cardiaco
            if (message_body.find("heart rate") != -1) or (message_body.find("pulso cardiaco") != -1) or (message_body.find("pulso") != -1): 
                db.createImg(number, "HR")
                message = f"{username} esta es la información actual de tus registros de pulso cardiaco."        
                message = client.messages.create (
                                        from_='whatsapp:+14155238886',  
                                        body=message,
                                        media_url=[f'{ngrok_url}/image?number={number}'],
                                        to=number
                                    )
            # Si se requiere una consulta de concentracion de oxigeno
            if (message_body.find("concentracion oxigeno") != -1) or (message_body.find("oxigeno") != -1) or (message_body.find("spo2") != -1):
                db.createImg(number, "Spo2")
                message = f"{username} esta es la información actual de tus registros de concentracion de oxigeno."        
                message = client.messages.create (
                                        from_='whatsapp:+14155238886',  
                                        body=message,
                                        media_url=[f'{ngrok_url}/image?number={number}'],
                                        to=number
                                    )     

class IMAGE(Resource):
    def get(self):        
        number = request.args.get('number')
        number = number.replace(": ","_+")       
        print(number)
        filename = f"{number}.png"
        return send_file(filename, mimetype='image/png')

api.add_resource(MESSAGE, '/message')  # Route_1
api.add_resource(IMAGE, '/image')  # Route_2

if __name__ == '__main__':
    app.run(port='5013')
