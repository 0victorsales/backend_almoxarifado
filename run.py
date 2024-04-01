from settings import app
from src.rotas import rotas


if __name__ == '__main__':
    with app.app_context():
        
        app.run(debug=True)