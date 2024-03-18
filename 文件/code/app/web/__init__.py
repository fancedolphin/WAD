from flask import Blueprint

web = Blueprint('web', __package__)

from app.web import views
from app.web import student
from app.web import teacher
from app.web import manager