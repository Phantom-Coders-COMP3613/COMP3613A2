from flask import Blueprint, jsonify
from App.controllers.auth import login_required
from App.controllers.leaderboard import view_leaderboard
from App.models import Student


leaderboard_view = Blueprint('leaderboard_view', __name__)

@leaderboard_view.route('/api/view_leaderboard', methods=['GET'])
def leaderboard():
    data = view_leaderboard()
    return jsonify(data), 200