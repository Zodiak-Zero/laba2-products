from flask import Flask, render_template
from flask_restx import Api
from resources.products import api as products_api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

# Включите CORS для вашего приложения
CORS(app)

# Регистрация API ресурсов
api.add_namespace(products_api)

# Маршрут для обслуживания HTML страницы
@app.route('/index.html')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
