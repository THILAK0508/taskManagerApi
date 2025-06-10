
from bson import ObjectId
from datetime import datetime
from config.database import db_instance

class Task:
    def __init__(self, title, description=None, completed=False, priority="medium", due_date=None):
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = priority
        self.due_date = due_date
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'due_date': self.due_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        task = Task(
            title=data.get('title'),
            description=data.get('description'),
            completed=data.get('completed', False),
            priority=data.get('priority', 'medium'),
            due_date=data.get('due_date')
        )
        return task

class TaskRepository:
    def __init__(self):
        self.collection = db_instance.get_collection('tasks')
    
    def create_task(self, task_data):
        task = Task.from_dict(task_data)
        result = self.collection.insert_one(task.to_dict())
        return str(result.inserted_id)
    
    def get_all_tasks(self, filters=None):
        query = filters or {}
        tasks = list(self.collection.find(query))
        for task in tasks:
            task['_id'] = str(task['_id'])
        return tasks
    
    def get_task_by_id(self, task_id):
        try:
            task = self.collection.find_one({'_id': ObjectId(task_id)})
            if task:
                task['_id'] = str(task['_id'])
            return task
        except:
            return None
    
    def update_task(self, task_id, update_data):
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(task_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except:
            return False
    
    def delete_task(self, task_id):
        try:
            result = self.collection.delete_one({'_id': ObjectId(task_id)})
            return result.deleted_count > 0
        except:
            return False
    
    def get_tasks_by_status(self, completed=None):
        if completed is not None:
            return self.get_all_tasks({'completed': completed})
        return self.get_all_tasks()
    
    def get_tasks_by_priority(self, priority):
        return self.get_all_tasks({'priority': priority})