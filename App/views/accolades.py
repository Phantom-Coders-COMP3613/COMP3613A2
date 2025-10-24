from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.models import Student, Accolades


from App.controllers import(
    view_accolades, login_required
    
)

accolades_views = Blueprint('accolades_views', __name__, template_folder='../templates')

@accolades_views.route('/api/view_accolade', methods=['GET'])
@login_required(Student)
def accolades_api():
    data = request.json

    try:
        student_id_int = int(data['student_id'])
    except (TypeError, ValueError):
        return jsonify({'message': f'Invalid Student ID format (must be integer)'}), 400 
    

    accolade = view_accolades(student_id_int) 
    if not accolade:
        return jsonify({'message': f'Invalid Student ID'}), 401
    elif accolade.milestone50:
           return jsonify({'message': f'Milestone 50 hours achieved!'}), 200
    elif accolade.milestone25:
            return jsonify({'message': f'Milestone 25 hours achieved!'}), 200
    elif accolade.milestone10:
            return jsonify({'message': f'Milestone 10 hours achieved!'}), 200
    else:
            return jsonify({'message': f'No milestones achieved yet.'}), 200
