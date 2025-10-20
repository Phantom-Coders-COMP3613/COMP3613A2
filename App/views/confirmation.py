from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required

from App.controllers import (
    view_confirmations,
    log_hours
)

confirmation_views = Blueprint('confirmation_views', __name__, template_folder='../templates')

@confirmation_views.route('/confirmations', )