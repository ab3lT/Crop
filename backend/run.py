from app import create_app
from flasgger import Swagger
from flask_cors import CORS

app = create_app()
swagger = Swagger(app)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
