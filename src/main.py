from flask import Flask
from infraestructure.db import Base, engine
from application.routes.commentaries_routes import commentaries_bp
from application.routes.delivery_routes import delivery_bp
from application.routes.offer_routes import offer_bp
from application.routes.status_routes import status_bp


app = Flask(__name__)


Base.metadata.create_all(bind=engine)

app.register_blueprint(commentaries_bp)
app.register_blueprint(delivery_bp)
app.register_blueprint(offer_bp)
app.register_blueprint(status_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)
