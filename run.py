from app import create_app
from app.database import db
import os

app = create_app()

# Create database tables
with app.app_context():
    db.create_all()

    app.run(host='0.0.0.0', port=8000, debug=False) 