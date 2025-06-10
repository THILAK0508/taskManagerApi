
## 7. README.md
```markdown
# Task Manager API

A RESTful API for managing tasks built with Flask and MongoDB.

## Features

- Create, read, update, and delete tasks
- Mark tasks as completed/incomplete
- Filter tasks by status and priority
- Object-oriented design with repository pattern
- Local MongoDB integration
- Comprehensive error handling
- Unit tests included

## Prerequisites

- Python 3.7+
- MongoDB installed and running locally
- pip (Python package manager)

## Installation

1. Clone the repository or create the project structure
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure MongoDB is running on localhost:27017

4. Run the application:
   ```bash
   python app.py
   ```

## API Endpoints

### Base URL: `http://localhost:5000/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | Get all tasks |
| POST | `/tasks` | Create a new task |
| GET | `/tasks/<id>` | Get a specific task |
| PUT | `/tasks/<id>` | Update a task |
| DELETE | `/tasks/<id>` | Delete a task |
| PATCH | `/tasks/<id>/toggle` | Toggle task completion |

### Query Parameters

- `GET /tasks?completed=true` - Filter by completion status
- `GET /tasks?priority=high` - Filter by priority

### Request/Response Examples

#### Create Task
```bash
POST /api/tasks
{
    "title": "Learn Flask",
    "description": "Build a task manager API",
    "priority": "high",
    "due_date": "2024-12-31T23:59:59"
}
```

#### Response
```json
{
    "success": true,
    "data": {
        "_id": "60d5ec9f2f8b8a1234567890",
        "title": "Learn Flask",
        "description": "Build a task manager API",
        "completed": false,
        "priority": "high",
        "due_date": "2024-12-31T23:59:59",
        "created_at": "2024-01-01T10:00:00",
        "updated_at": "2024-01-01T10:00:00"
    },
    "message": "Task created successfully"
}
```

## Testing

Run the tests:
```bash
python -m unittest tests.test_tasks
```

## MongoDB Setup

1. Install MongoDB Community Edition
2. Start MongoDB service:
   ```bash
   # On macOS
   brew services start mongodb-community
   
   # On Ubuntu
   sudo systemctl start mongod
   
   # On Windows
   net start MongoDB
   ```

3. Verify MongoDB is running:
   ```bash
   mongo --eval "db.runCommand({connectionStatus: 1})"
   ```

## Project Structure

```
task_manager_api/
├── app.py                 # Main application file
├── models/
│   ├── __init__.py
│   └── task.py           # Task model and repository
├── routes/
│   ├── __init__.py
│   └── task_routes.py    # API routes
├── config/
│   ├── __init__.py
│   └── database.py       # Database configuration
├── tests/
│   ├── __init__.py
│   └── test_tasks.py     # Unit tests
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation