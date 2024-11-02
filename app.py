from flask import Flask
from config import Config
from models import db, Folder, File
from routes import folder_routes

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Register routes
app.register_blueprint(folder_routes)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
