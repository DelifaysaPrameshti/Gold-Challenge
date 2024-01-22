from flask import Flask, jsonify
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import pandas as pd
import re

class CustomFlaskAppWithEncoder(Flask):
    json_provider_class = LazyJSONEncoder

app = CustomFlaskAppWithEncoder(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    json_response = { 
        'status_code':200, 
        'description':"untuk melakukan cleansing data tambahkan '/docs' di endpoint", 
        'data': "Welcome to API data cleansing"
        }

    response_data = jsonify(json_response)
    return response_data

#app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'API Data Cleansing'),
    'version': LazyString(lambda: '1.0.0'),
    'description': LazyString(lambda: 'Dokumentasi API untuk Membersihkan Data'),
    },
    host = LazyString(lambda: request.host)  
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs/Text-Cleansing',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,
                  config=swagger_config)

@swag_from("docs/Text_Cleansing.yml", methods=['POST'])
@app.route('/Text_Cleansing', methods=['POST'])
def text_cleansing():
    text = request.form.get('text')

    clean_text = cleansing_text(text)

    conn.execute("INSERT INTO data (text, text_clean) VALUES ('" + text + "', '" + clean_text + "')")
    conn.commit()

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah dibersihkan",
        'data': clean_text,
    }
    
    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run(debug=True)