from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Newlife@localhost/GreekApartments'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if __name__ == "__main__":
    # Set up an application context
    with app.app_context():
        try:
            db.create_all()  # Creates tables if they don't exist
            print("Database connected successfully!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")