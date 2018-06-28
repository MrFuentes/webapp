from wsgiref.handler import CGIHandler
from flask_app import app

CGIHandler().run(app)
