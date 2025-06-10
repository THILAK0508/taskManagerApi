
from flask import Flask, jsonify
from flask_cors import CORS
from routes.task_routes import task_bp
from config.database import db_instance
import os

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for all domains
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(task_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'Task Manager API is running',
            'database': 'connected'
        })
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Welcome to Task Manager API',
            'version': '1.0.0',
            'endpoints': {
                'GET /api/tasks': 'Get all tasks',
                'POST /api/tasks': 'Create a new task',
                'GET /api/tasks/<id>': 'Get a specific task',
                'PUT /api/tasks/<id>': 'Update a task',
                'DELETE /api/tasks/<id>': 'Delete a task',
                'PATCH /api/tasks/<id>/toggle': 'Toggle task completion'
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)