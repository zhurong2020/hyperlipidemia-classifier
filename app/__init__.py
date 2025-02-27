from flask import Flask
import os

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev_key'
)

from app import routes 