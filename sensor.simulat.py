import requests
import time
import random

URL_API = "http://127.0.0.1:5000/api/clima"

print("Iniciant simulador de sensor... (Ctrl+C per parar)")

while True:
    #Inventem dades reals
    dades = {
        "temp": round(random.uniform(20.0, 30.0), 2),
        "hum": round(random.uniform(40.0, 70.0), 2)
    }

    try:
        resposta = requests.post(URL_API, json=dades)
        if resposta.status_code ==201:
            print(f"Enviat: {dades['temp']}°C, {dades['hum']}% - Éxit")
        else:
            print("Error al inviar")
    except:
        print("Server apagat... reintentant en 5 segons")

    time.sleep(5) #Espera 5 s abans d'enviar el següent