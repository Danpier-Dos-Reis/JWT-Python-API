from flask import Flask, jsonify, request
import jwt
import datetime
from functools import wraps
from dal import VentaDBManager

app = Flask(__name__)

# Clave secreta para firmar los tokens
app.config['SECRET_KEY'] = 'mysecretkey'

# Decorador para verificar el token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    return decorated

# Endpoint para generar un token JWT
@app.route('/login', methods=['POST'])
def login():
    auth = request.json

    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Username and password required!'}), 400

    if auth['username'] == 'admin' and auth['password'] == 'password':
        token = jwt.encode({
            'user': auth['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials!'}), 401

# Endpoint protegido para obtener ventas
@app.route('/ventas', methods=['GET'])
@token_required
def get_ventas():
    # Configuración de la base de datos
    db_manager = VentaDBManager(
        host="localhost",
        user="dorito",
        password="Dorit@Picant3",
        database="db_ventas"
    )

    try:
        db_manager.connect()
        ventas = db_manager.obtener_ventas()

        # Convertir las ventas en formato JSON
        ventas_json = []
        for venta in ventas:
            ventas_json.append({
                'id': venta.Id,
                'cliente': venta.Cliente,
                'producto': venta.Producto,
                'cantidad': venta.Cantidad,
                'precio': venta.Precio,
                'fecha': str(venta.Fecha)
            })

        return jsonify(ventas_json)
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    finally:
        db_manager.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)