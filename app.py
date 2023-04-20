from flask import redirect, Flask
import pathlib
from decouple import config
import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_migrate import Migrate
from flask import Flask
from config import db, ma, migrate,bcrypt

# Get the parent directory of the current file
basedir = pathlib.Path(__file__).parent.resolve()  
# Create a Connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)
# Add the Swagger YAML file to the Connexion app instance
connex_app.add_api(basedir / "swagger.yml")
app = connex_app.app
app.config.from_object(config("APP_SETTINGS"))


db.init_app(app)
ma.init_app(app)
migrate.init_app(app,db)
bcrypt.init_app(app)

@app.route('/')   # Create a route for the homepage of the application
def home():
    # Redirect the user to the Swagger UI page of the API
    return redirect('/api/ui/') 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
