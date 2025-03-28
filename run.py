from app import create_app
from app.database import db
import os

app = create_app()

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Obter a porta do ambiente (Azure App Service) ou usar 8000 como padrão
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False) 