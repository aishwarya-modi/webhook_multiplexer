from flask import Flask
from flasgger import Swagger
from controllers.webhook_controller import webhook_blueprint
from controllers.customer_controller import customer_blueprint
from config import mongo, MONGO_URI
from exceptions import handle_exception

app = Flask(__name__)

# Load configurations from config.py
app.config["MONGO_URI"] = MONGO_URI
# app.config["SECRET_KEY"] = SECRET_KEY

# Initialize Swagger
swagger = Swagger(app)

# Register Blueprints
app.register_blueprint(webhook_blueprint, url_prefix='/api')
app.register_blueprint(customer_blueprint, url_prefix='/api')

# Register error handler
app.register_error_handler(Exception, handle_exception)

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
