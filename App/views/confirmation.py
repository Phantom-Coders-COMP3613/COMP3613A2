from flask import Blueprint, render_template, jsonify, request, send_from_directory
from App.models import Staff, Student, Confirmation, Staff
from flask_jwt_extended import jwt_required, current_user
from App.controllers import (
    staff_log_confirmation,
    login_required,
    student_request_confirmation
)

confirmation_views = Blueprint('confirmation_views', __name__, template_folder='../templates')

@confirmation_views.route('/api/confirmations/<int:confirmationId>', methods=['PUT'])
@login_required(Staff)
def log_confirmation_api(confirmationId):
    confirmation = staff_log_confirmation(staff_id=current_user.id, confirmation_id=confirmationId)
    if not confirmation:
        return jsonify({'message': f'Error returning confirmation'}), 400
    return jsonify({'status': 'success', 'message': f'Confirmation returned successfully with ID: {confirmation.confirmationId}'}), 200

@confirmation_views.route('/api/request', methods=['POST'])
@login_required(Student)
def request_confirm():
    data = request.json
    confirmation = student_request_confirmation(student_id=data['student_id'], hours=data['hours'])
    if not confirmation:
        return jsonify({'message': f'Error creating confirmation'}), 401
    return jsonify({'message': f'Confirmation pending'}), 202