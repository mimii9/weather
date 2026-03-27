
# 1. Importem les eines que acabem d'instalar
from flask import Flask, jsonify, request
from flasgger import Swagger

# 2. Inicialitzem la nostre aplicació Flask
app = Flask(__name__)

#Prova "base de dades" temporal a la memoria RAM
base_dades_provisional = []

# 3. Inicialitzem Swagger per a documentar la nostre app
swagger = Swagger(app)

# 4. Creaem el nostre primer Endpoint (una ruta a la que ens podem connectar)
# El mètode GET es fa servir per a demanar informació. La web o la App piden datos.
@app.route('/api/clima', methods=['GET'])
def obtener_clima():
    """
    Obtenir l'ultima dada real obtinguda guardada a la llista
    ---
    responses:
      200:
        description: Torna l'ultim registre de temperatura i humitat.
    responses:
      404:
        description: No es troben dades al server.
    """
    if len(base_dades_provisional) > 0:
        # Agafem l'ultim element de la llista
        ultimo_dato = base_dades_provisional[-1]
        return jsonify(ultimo_dato), 200
    else:
        return jsonify({"error": "No hi han dades encara"}), 404
#El mètode POST serveix per a que el sensor envii dades a la API.
@app.route('/api/clima', methods=['POST'])
def rebre_clima():
    """
    recibir datos desde la RaspberryPi
    ---
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Medicion
          propierties:
            temp:
              type: number
              example: 22.5
            hum: 
              type: number
              example: 60 
    responses:
      201: 
        Description: Datos recibidos correctamente
    """
    #Extraemos los datos que vienen en el JSON
    datos = request.get_json()
    #Guardem elpaquet a la nostra lista
    base_dades_provisional.append(datos)
    temperatura = datos.get('temp')
    humedad = datos.get('hum')
    #De momento solo los imprimimos para ver que llegan
    print(f"DEBUG: He rebut {temperatura}°C y {humedad}% de humedad.")
    return jsonify({"status": "ok", "mensaje": "Dades desades"}), 201
# 5. Aquesta línia li diu a Python que, si executem aquest arxiu, encienda el servidor
if __name__ == '__main__':
    # debug=True fa que el servidor es reinici només si deso canvis en el codi.
    app.run(debug=True, port=5000)