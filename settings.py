import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

chave_secreta = os.getenv("CHAVE_SECRETA")


app = Flask(__name__, static_folder='/root/frontend-BF/dist/frontend-bf')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = chave_secreta