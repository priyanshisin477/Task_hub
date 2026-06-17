from flask import Blueprint, jsonify, request
from supabase import create_client
from dotenv import load_dotenv
from utils.email import send_task_assigned_email, send_task_submitted_email
load_dotenv()
import os

tasks_bp = Blueprint('tasks', __name__)

supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_ROLE_KEY')   
)

@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    response = supabase.table('tasks').select('*').execute()
    return jsonify({
        'status': 'success',
        'tasks': response.data
    })

@tasks_bp.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    response = supabase.table('tasks').insert([data]).execute()
    return jsonify({
        'status': 'success',
        'message': 'Task created successfully',
        'task': response.data[0]
    })

@tasks_bp.route('/api/tasks/<task_id>/assign', methods=['POST'])
def assign_task(task_id):
    data = request.get_json()
    user_id = data.get('user_id')

    # 1. Task update karo
    response = supabase.table('tasks')\
        .update({'assigned_by': user_id, 'status': 'assigned'})\
        .eq('id', task_id)\
        .execute()

    # 2. User details fetch karo
    user = supabase.table('users')\
        .select('email, name')\
        .eq('id', user_id)\
        .single()\
        .execute()

    # 3. Email bhejo
    task = response.data[0]
    send_task_assigned_email(
        user.data['email'],
        task['title'],
        task_id
    )

    return jsonify({
        'status': 'success',
        'message': 'Task assigned and email sent!'
    })

@tasks_bp.route('/api/tasks/<task_id>/submit', methods=['POST'])
def submit_task(task_id):

    # Task status update
    response = supabase.table('tasks') \
        .update({'status': 'submitted'}) \
        .eq('id', task_id) \
        .execute()

    task = response.data[0]

    # Admin email fetch karo
    admin = supabase.table('users') \
        .select('email') \
        .eq('role', 'admin') \
        .execute()

    admin_email = admin.data[0]['email']

    # Email bhejo
    send_task_submitted_email(
        admin_email,
        task['title'],
        'User',
        task_id
    )

    return jsonify({
        'status': 'success',
        'message': 'Task submitted successfully'
    })

@tasks_bp.route('/api/tasks/<task_id>/approve', methods=['POST'])
def approve_task(task_id):

    response = supabase.table('tasks') \
    .update({'status' : 'approved'}) \
    .eq('id', task_id) \
    .execute()

    return jsonify({
        'status' : 'success',
        'message' : 'Task approved successfully',
        'task' : response.data[0]
    })

@tasks_bp.route('/api/tasks/<task_id>/request-revison', methods=['PUT'])
def request_revison(task_id):
     
     response = supabase.table('tasks') \
    .update({'status' : 'revison_requested'}) \
    .eq('id', task_id) \
    .execute()
     
     return jsonify({
        'status' : 'success',
        'message' : 'Revison requested',
        'task' : response.data[0]
    })