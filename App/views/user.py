from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    jwt_required,
    login_required,
    create_staff,
    create_student
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/api/student', methods=['POST'])
def create_student_api():
    data = request.json
    student = create_student(data['username'], data['password'])
    if student:
        return jsonify({'message': f'Student created successfully with ID: {student.id}'}), 201
    return jsonify({'error': 'Failed to create student'}), 400

@user_views.route('/api/staff', methods=['POST'])
def create_staff_api():
    data = request.json
    staff = create_staff(data['username'], data['password'], data['staffId'])
    if staff:
        return jsonify({'message': f'Staff created successfully with ID: {staff.id}'}), 201
    return jsonify({'error': 'Failed to create staff'}), 400

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')