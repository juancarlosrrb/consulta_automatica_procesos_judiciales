# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 12:14:22 2024

@author: USUARIO
"""

####sevidor local
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

@app.route('/correo_login', methods=['POST'])
def correo_login():
    data = request.json
    mail_username = data.get('mail_username')
    password_sfa = data.get('password_sfa')

    print('Correo recibido:', mail_username)
    print('Contraseña recibida:', password_sfa)
    
    
    

    return jsonify({'mensaje': 'Datos recibidos correctamente, se ha creado su usurario puede ingresar', 'mail_username': mail_username})



if __name__ == '__main__':
    app.run(debug=False)
