
from flask import Blueprint, request, jsonify
from models.task import TaskRepository
from datetime import datetime

task_bp = Blueprint('tasks', __name__)
task_repo = TaskRepository()

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        # Get query parameters
        completed = request.args.get('completed')
        priority = request.args.get('priority')
        
        if completed is not None:
            completed = completed.lower() == 'true'
            tasks = task_repo.get_tasks_by_status(completed)
        elif priority:
            tasks = task_repo.get_tasks_by_priority(priority)
        else:
            tasks = task_repo.get_all_tasks()
        
        return jsonify({
            'success': True,
            'data': tasks,
            'count': len(tasks)
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title'):
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400
        
        # Validate priority
        valid_priorities = ['low', 'medium', 'high']
        if data.get('priority') and data['priority'].lower() not in valid_priorities:
            return jsonify({
                'success': False,
                'error': 'Priority must be one of: low, medium, high'
            }), 400
        
        # Parse due_date if provided
        if data.get('due_date'):
            try:
                data['due_date'] = datetime.fromisoformat(data['due_date'])
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid due_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
                }), 400
        
        task_id = task_repo.create_task(data)
        created_task = task_repo.get_task_by_id(task_id)
        
        return jsonify({
            'success': True,
            'data': created_task,
            'message': 'Task created successfully'
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = task_repo.get_task_by_id(task_id)
        
        if not task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': task
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        
        # Check if task exists
        existing_task = task_repo.get_task_by_id(task_id)
        if not existing_task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        # Parse due_date if provided
        if data.get('due_date'):
            try:
                data['due_date'] = datetime.fromisoformat(data['due_date'])
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid due_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
                }), 400
        
        # Validate priority
        valid_priorities = ['low', 'medium', 'high']
        if data.get('priority') and data['priority'].lower() not in valid_priorities:
            return jsonify({
                'success': False,
                'error': 'Priority must be one of: low, medium, high'
            }), 400
        
        success = task_repo.update_task(task_id, data)
        
        if success:
            updated_task = task_repo.get_task_by_id(task_id)
            return jsonify({
                'success': True,
                'data': updated_task,
                'message': 'Task updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update task'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        # Check if task exists
        existing_task = task_repo.get_task_by_id(task_id)
        if not existing_task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        success = task_repo.delete_task(task_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Task deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete task'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@task_bp.route('/tasks/<task_id>/toggle', methods=['PATCH'])
def toggle_task_completion(task_id):
    try:
        task = task_repo.get_task_by_id(task_id)
        
        if not task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404
        
        new_status = not task['completed']
        success = task_repo.update_task(task_id, {'completed': new_status})
        
        if success:
            updated_task = task_repo.get_task_by_id(task_id)
            return jsonify({
                'success': True,
                'data': updated_task,
                'message': f'Task marked as {"completed" if new_status else "incomplete"}'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to toggle task completion'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500