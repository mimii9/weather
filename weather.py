from flask import render_template
from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
swagger = Swagger(app) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Medicion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperatura = db.Column(db.Float, nullable=False)
    humedad = db.Column(db.Float, nullable=False)


@app.route('/api/clima', methods=['POST'])
def recibir_clima():
    """
    Enviar datos desde la Raspberry Pi
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            temp:
              type: number
              example: 25.5
            hum:
              type: number
              example: 60.0
    responses:
      201:
        description: Datos guardados con éxito
    """
    datos = request.get_json()
    nueva_medicion = Medicion(
        temperatura=datos.get('temp'),
        humedad=datos.get('hum')
    )
    db.session.add(nueva_medicion)
    db.session.commit()
    return jsonify({"mensaje": "Guardado en DB con éxito"}), 201

@app.route('/api/clima', methods=['GET'])
def obtener_clima():
    """
    Obtener la última medición guardada
    ---
    responses:
      200:
        description: Devuelve el último registro
    """
    ultima = Medicion.query.order_by(Medicion.id.desc()).first()
    if ultima:
        return jsonify({"temp": ultima.temperatura, "hum": ultima.humedad, "id": ultima.id}), 200
    return jsonify({"error": "No hay datos"}), 404

@app.route('/api/clima/historial', methods=['GET'])
def obtener_historial():
    """
    Obtener todas las mediciones guardadas
    ---
    responses:
      200:
        description: Lista completa de datos
    """
    todas = Medicion.query.all()
    resultado = [{"id": m.id, "temp": m.temperatura, "hum": m.humedad} for m in todas]
    return jsonify(resultado), 200

@app.route('/')
def index():
    totes = Medicion.query.order_by(Medicion.id.desc()).limit(10).all()
    resultat = [{"id": m.id, "temp": m.temperatura, "hum": m.humedad} for m in totes]
    return render_template('index.html', medicions=resultat)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Això crea la base de dades automàticament al arrencar.
    app.run(host='0.0.0.0', debug=True, port=5000)
