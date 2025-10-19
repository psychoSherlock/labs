import json
import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import Flask, request, jsonify, send_file, send_from_directory, Blueprint
import jwt
from dotenv import load_dotenv
import uuid
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

app = Flask(__name__, static_folder='clientSide', static_url_path='')
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'change-this-secret')

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

api_blueprint = Blueprint('api', __name__)

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@neuralfluxcorp.com')

_current_admin_password = None

def get_admin_password():
    global _current_admin_password
    if _current_admin_password is None:
        _current_admin_password = ADMIN_PASSWORD
    return _current_admin_password

def set_admin_password(new_password):
    global _current_admin_password
    _current_admin_password = new_password

REQUIRED_HEADER_KEY = 'X-NEURALEND-KEY'
REQUIRED_HEADER_VALUE = '97b213d150a41128ae4123500d506d6422613feef8'

login_attempts = {}
LOCKOUT_DURATION = 60
MAX_ATTEMPTS = 3
MAX_LOGIN_ATTEMPTS_CACHE = 100

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'svg'}
MAX_FILE_SIZE = 5 * 1024 * 1024

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

_data_store = None
_swagger_cache = None

MAX_EMPLOYEES = 200
MAX_MESSAGES = 500
MAX_TRAINING_JOBS = 100
MAX_STRING_LENGTH = 500
MAX_BODY_LENGTH = 2000

def load_data():
    global _data_store
    if _data_store is None:
        with open('data.json', 'r') as f:
            _data_store = json.load(f)
    return _data_store

def get_next_id(collection):
    if not collection:
        return 1
    return max(item['id'] for item in collection) + 1

def validate_string(value, field_name, max_length=MAX_STRING_LENGTH):
    if not isinstance(value, str):
        return False, f"{field_name} must be a string"
    if len(value) > max_length:
        return False, f"{field_name} exceeds maximum length of {max_length} characters"
    if len(value.strip()) == 0:
        return False, f"{field_name} cannot be empty"
    return True, None

def validate_email(email):
    if '@' not in email or '.' not in email.split('@')[1]:
        return False, "Invalid email format"
    return validate_string(email, "email")

def sanitize_string(value, max_length=MAX_STRING_LENGTH):
    if not isinstance(value, str):
        return str(value)[:max_length]
    return value[:max_length]

def check_required_header(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        header_value = request.headers.get(REQUIRED_HEADER_KEY)
        if header_value != REQUIRED_HEADER_VALUE:
            return jsonify({'error': 'Unauthorized - Invalid or missing required header'}), 401
        return f(*args, **kwargs)
    return decorated_function

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        if token.startswith('Bearer '):
            token = token[7:]
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

def is_locked_out(ip_address):
    if ip_address in login_attempts:
        attempts, last_attempt = login_attempts[ip_address]
        if attempts >= MAX_ATTEMPTS:
            time_passed = (datetime.now() - last_attempt).total_seconds()
            if time_passed < LOCKOUT_DURATION:
                return True, int(LOCKOUT_DURATION - time_passed)
            else:
                del login_attempts[ip_address]
    return False, 0

def record_failed_attempt(ip_address):
    if len(login_attempts) > MAX_LOGIN_ATTEMPTS_CACHE:
        current_time = datetime.now()
        expired_ips = [ip for ip, (_, last_attempt) in login_attempts.items() if (current_time - last_attempt).total_seconds() > LOCKOUT_DURATION]
        for ip in expired_ips[:len(expired_ips)//2]:
            del login_attempts[ip]
    if ip_address in login_attempts:
        attempts, _ = login_attempts[ip_address]
        login_attempts[ip_address] = (attempts + 1, datetime.now())
    else:
        login_attempts[ip_address] = (1, datetime.now())

def reset_attempts(ip_address):
    if ip_address in login_attempts:
        del login_attempts[ip_address]

@app.route('/', methods=['GET'])
def home():
    return send_from_directory('clientSide', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join('clientSide', path)):
        return send_from_directory('clientSide', path)
    return send_from_directory('clientSide', 'index.html')

@api_blueprint.route('/api/contract', methods=['GET'])
@check_required_header
def api_contract():
    global _swagger_cache
    if _swagger_cache is not None:
        return jsonify(_swagger_cache), 200
    swagger = {
        "openapi": "3.0.0",
        "info": {
            "title": "NeuralFlux Admin Panel API",
            "description": "AI-powered admin panel API for NeuralFlux Corporation",
            "version": "1.0.0",
            "contact": {
                "email": "admin@neuralfluxcorp.com"
            }
        },
        "servers": [
            {
                "url": request.host_url.rstrip('/'),
                "description": "NeuralFlux API Server"
            }
        ],
        "components": {
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-NEURALEND-KEY",
                    "description": "Required header for all requests"
                },
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "JWT token obtained from login"
                }
            },
            "schemas": {
                "LoginRequest": {
                    "type": "object",
                    "required": ["username", "password"],
                    "properties": {
                        "username": {"type": "string"},
                        "password": {"type": "string"}
                    }
                },
                "LoginResponse": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string"}
                    }
                },
                "Error": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"}
                    }
                }
            }
        },
        "security": [
            {"ApiKeyAuth": []}
        ],
        "paths": {
            "/": {
                "get": {
                    "summary": "API status",
                    "description": "Get API version and status information",
                    "responses": {
                        "200": {
                            "description": "Successful response"
                        }
                    }
                }
            },
            "/api/contract": {
                "get": {
                    "summary": "API documentation",
                    "description": "Get OpenAPI specification",
                    "responses": {
                        "200": {
                            "description": "OpenAPI specification"
                        }
                    }
                }
            },
            "/api/admin/login": {
                "post": {
                    "summary": "Admin login",
                    "description": "Authenticate and receive JWT token",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/LoginRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Login successful",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/LoginResponse"}
                                }
                            }
                        },
                        "401": {
                            "description": "Invalid credentials"
                        }
                    }
                }
            },
            "/api/admin/change-password": {
                "post": {
                    "summary": "Change password",
                    "description": "Change admin password",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "current_password": {"type": "string"},
                                        "new_password": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Password changed successfully"},
                        "401": {"description": "Unauthorized"}
                    }
                }
            },
            "/api/systems": {
                "get": {
                    "summary": "Get all systems",
                    "description": "Get all system status information",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "responses": {
                        "200": {"description": "List of systems"},
                        "401": {"description": "Unauthorized"}
                    }
                }
            },
            "/api/systems/{system_id}": {
                "get": {
                    "summary": "Get system by ID",
                    "description": "Get specific system details",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "system_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "System details"},
                        "404": {"description": "System not found"}
                    }
                },
                "patch": {
                    "summary": "Update system status",
                    "description": "Update system status (up, down, maintenance)",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "system_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["status"],
                                    "properties": {
                                        "status": {
                                            "type": "string",
                                            "enum": ["up", "down", "maintenance"]
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "System status updated"},
                        "400": {"description": "Invalid status"}
                    }
                }
            },
            "/api/employees": {
                "get": {
                    "summary": "Get all employees",
                    "description": "Get all employee information",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "responses": {
                        "200": {"description": "List of employees"},
                        "401": {"description": "Unauthorized"}
                    }
                },
                "post": {
                    "summary": "Create employee",
                    "description": "Create a new employee",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["name", "email", "department", "role"],
                                    "properties": {
                                        "name": {"type": "string"},
                                        "email": {"type": "string", "format": "email"},
                                        "department": {"type": "string"},
                                        "role": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Employee created successfully"},
                        "400": {"description": "Invalid request"}
                    }
                }
            },
            "/api/employees/{employee_id}": {
                "get": {
                    "summary": "Get employee by ID",
                    "description": "Get specific employee details",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "employee_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "Employee details"},
                        "404": {"description": "Employee not found"}
                    }
                },
                "put": {
                    "summary": "Update employee",
                    "description": "Update employee information",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "employee_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "email": {"type": "string"},
                                        "department": {"type": "string"},
                                        "role": {"type": "string"},
                                        "status": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Employee updated successfully"},
                        "400": {"description": "Invalid request"}
                    }
                },
                "delete": {
                    "summary": "Delete employee",
                    "description": "Delete an employee",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "employee_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "Employee deleted successfully"},
                        "404": {"description": "Employee not found"}
                    }
                }
            },
            "/api/messages": {
                "get": {
                    "summary": "Get all messages",
                    "description": "Get all messages",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "responses": {
                        "200": {"description": "List of messages"},
                        "401": {"description": "Unauthorized"}
                    }
                },
                "post": {
                    "summary": "Send message",
                    "description": "Send a new message",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["recipient", "subject", "body"],
                                    "properties": {
                                        "recipient": {"type": "string"},
                                        "subject": {"type": "string"},
                                        "body": {"type": "string"},
                                        "priority": {"type": "string", "enum": ["low", "normal", "high"]}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Message sent successfully"},
                        "400": {"description": "Invalid request"}
                    }
                }
            },
            "/api/messages/{message_id}": {
                "get": {
                    "summary": "Get message by ID",
                    "description": "Get specific message details",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "message_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "Message details"},
                        "404": {"description": "Message not found"}
                    }
                }
            },
            "/api/messages/{message_id}/read": {
                "post": {
                    "summary": "Mark message as read",
                    "description": "Mark a message as read",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "message_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {"description": "Message marked as read"},
                        "404": {"description": "Message not found"}
                    }
                }
            },
            "/api/models": {
                "get": {
                    "summary": "Get ML models",
                    "description": "Get all ML model deployments",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "responses": {
                        "200": {"description": "List of model deployments"},
                        "401": {"description": "Unauthorized"}
                    }
                }
            },
            "/api/models/deploy": {
                "post": {
                    "summary": "Deploy model",
                    "description": "Deploy a machine learning model",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["model_name", "version", "environment"],
                                    "properties": {
                                        "model_name": {"type": "string"},
                                        "version": {"type": "string"},
                                        "environment": {"type": "string", "enum": ["development", "staging", "production"]}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Model deployment initiated"},
                        "400": {"description": "Invalid request"}
                    }
                }
            },
            "/api/usage": {
                "get": {
                    "summary": "Get API usage",
                    "description": "Get API usage statistics",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "responses": {
                        "200": {"description": "Usage statistics"},
                        "401": {"description": "Unauthorized"}
                    }
                }
            },
            "/api/training-jobs": {
                "get": {
                    "summary": "Get training jobs",
                    "description": "Get ML training jobs",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "responses": {
                        "200": {"description": "List of training jobs"},
                        "401": {"description": "Unauthorized"}
                    }
                },
                "post": {
                    "summary": "Start training job",
                    "description": "Start a new ML training job",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["model_type", "dataset", "epochs"],
                                    "properties": {
                                        "model_type": {"type": "string"},
                                        "dataset": {"type": "string"},
                                        "epochs": {"type": "integer", "minimum": 1},
                                        "batch_size": {"type": "integer"},
                                        "learning_rate": {"type": "number"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Training job started successfully"},
                        "400": {"description": "Invalid request"}
                    }
                }
            },
            "/api/dashboard": {
                "get": {
                    "summary": "Get dashboard",
                    "description": "Get dashboard summary with all statistics",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "responses": {
                        "200": {"description": "Dashboard data"},
                        "401": {"description": "Unauthorized"}
                    }
                }
            },
            "/api/upload-image": {
                "post": {
                    "summary": "Upload image",
                    "description": "Upload an image file (max 5MB)",
                    "security": [{"ApiKeyAuth": [], "BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "image": {
                                            "type": "string",
                                            "format": "binary"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Image uploaded successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "image_id": {"type": "string"},
                                            "url": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        },
                        "400": {"description": "Invalid request"}
                    }
                }
            },
            "/api/images/{image_id}": {
                "get": {
                    "summary": "Get image",
                    "description": "Retrieve an uploaded image",
                    "parameters": [
                        {
                            "name": "image_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Image file",
                            "content": {
                                "image/svg+xml": {}
                            }
                        },
                        "404": {"description": "Image not found"}
                    }
                }
            }
        }
    }
    
    # Cache the swagger spec
    _swagger_cache = swagger
    return jsonify(swagger), 200

# Admin login endpoint
@api_blueprint.route('/api/admin/login', methods=['POST'])
@check_required_header
def admin_login():
    ip_address = request.remote_addr
    
    # Check if IP is locked out
    locked, remaining_time = is_locked_out(ip_address)
    if locked:
        return jsonify({
            'error': 'Account locked due to multiple failed attempts',
            'retry_after_seconds': remaining_time
        }), 429
    
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    
    # Validate credentials
    if username == ADMIN_USERNAME and password == get_admin_password():
        # Reset attempts on successful login
        reset_attempts(ip_address)
        
        # Create JWT token with 1 hour expiry
        token_payload = {
            'username': username,
            'email': ADMIN_EMAIL,
            'profile_picture': '/api/images/admin.svg',
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)
        }
        token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'token': token
        }), 200
    else:
        # Record failed attempt
        record_failed_attempt(ip_address)
        attempts, _ = login_attempts.get(ip_address, (0, None))
        remaining_attempts = MAX_ATTEMPTS - attempts
        
        if remaining_attempts <= 0:
            return jsonify({
                'error': 'Invalid credentials. Account locked for 1 minute.',
                'attempts_remaining': 0
            }), 401
        
        return jsonify({
            'error': 'Invalid credentials',
            'attempts_remaining': remaining_attempts
        }), 401

# Change password endpoint
@api_blueprint.route('/api/admin/change-password', methods=['POST'])
@check_required_header
@token_required
def change_password(current_user):
    data = request.get_json()
    
    if not data or 'current_password' not in data or 'new_password' not in data:
        return jsonify({'error': 'Missing current_password or new_password'}), 400
    
    current_password = data['current_password']
    new_password = data['new_password']
    
    # Validate current password is a string
    if not isinstance(current_password, str):
        return jsonify({'error': 'Current password must be a string'}), 400
    
    # Validate new password is a string
    if not isinstance(new_password, str):
        return jsonify({'error': 'New password must be a string'}), 400
    
    # Validate new password length (min 8, max 128 characters)
    if len(new_password) < 8:
        return jsonify({'error': 'New password must be at least 8 characters long'}), 400
    
    if len(new_password) > 128:
        return jsonify({'error': 'New password cannot exceed 128 characters'}), 400
    
    # Check if new password is same as current
    if current_password == new_password:
        return jsonify({'error': 'New password must be different from current password'}), 400
    
    # Verify current password
    if current_password != get_admin_password():
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    # Update password in memory
    set_admin_password(new_password)
    
    return jsonify({
        'message': 'Password changed successfully'
    }), 200

# Get all systems (optimized - compute stats once)
@api_blueprint.route('/api/systems', methods=['GET'])
@check_required_header
@token_required
def get_systems(current_user):
    data = load_data()
    systems = data['systems']
    total = len(systems)
    up_count = 0
    down_count = 0
    
    # Single pass through systems
    for s in systems:
        if s['status'] == 'up':
            up_count += 1
        elif s['status'] == 'down':
            down_count += 1
    
    return jsonify({
        'systems': systems,
        'total': total,
        'up': up_count,
        'down': down_count
    }), 200

# Get specific system
@api_blueprint.route('/api/systems/<int:system_id>', methods=['GET'])
@check_required_header
@token_required
def get_system(current_user, system_id):
    data = load_data()
    system = next((s for s in data['systems'] if s['id'] == system_id), None)
    
    if system:
        return jsonify(system), 200
    return jsonify({'error': 'System not found'}), 404

# Get all employees (optimized - single pass)
@api_blueprint.route('/api/employees', methods=['GET'])
@check_required_header
@token_required
def get_employees(current_user):
    data = load_data()
    employees = data['employees']
    total = len(employees)
    active_count = sum(1 for e in employees if e.get('status') == 'active')
    
    return jsonify({
        'employees': employees,
        'total': total,
        'active': active_count
    }), 200

# Get specific employee
@api_blueprint.route('/api/employees/<int:employee_id>', methods=['GET'])
@check_required_header
@token_required
def get_employee(current_user, employee_id):
    data = load_data()
    employee = next((e for e in data['employees'] if e['id'] == employee_id), None)
    
    if employee:
        return jsonify(employee), 200
    return jsonify({'error': 'Employee not found'}), 404

# Get all messages (optimized - single pass)
@api_blueprint.route('/api/messages', methods=['GET'])
@check_required_header
@token_required
def get_messages(current_user):
    data = load_data()
    messages = data['messages']
    total = len(messages)
    unread_count = sum(1 for m in messages if not m.get('read', True))
    
    return jsonify({
        'messages': messages,
        'total': total,
        'unread': unread_count
    }), 200

# Get specific message
@api_blueprint.route('/api/messages/<int:message_id>', methods=['GET'])
@check_required_header
@token_required
def get_message(current_user, message_id):
    data = load_data()
    message = next((m for m in data['messages'] if m['id'] == message_id), None)
    
    if message:
        return jsonify(message), 200
    return jsonify({'error': 'Message not found'}), 404

# Get all ML model deployments (optimized - single pass)
@api_blueprint.route('/api/models', methods=['GET'])
@check_required_header
@token_required
def get_models(current_user):
    data = load_data()
    deployments = data['model_deployments']
    total = len(deployments)
    deployed_count = sum(1 for m in deployments if m.get('status') == 'deployed')
    
    return jsonify({
        'deployments': deployments,
        'total': total,
        'deployed': deployed_count
    }), 200

# Get API usage statistics
@api_blueprint.route('/api/usage', methods=['GET'])
@check_required_header
@token_required
def get_usage(current_user):
    data = load_data()
    return jsonify({
        'usage_statistics': data['api_usage'],
        'date': '2025-10-16'
    }), 200

# Get ML training jobs (optimized - single pass)
@api_blueprint.route('/api/training-jobs', methods=['GET'])
@check_required_header
@token_required
def get_training_jobs(current_user):
    data = load_data()
    jobs = data['training_jobs']
    total = len(jobs)
    running_count = 0
    queued_count = 0
    
    for j in jobs:
        status = j.get('status')
        if status == 'running':
            running_count += 1
        elif status == 'queued':
            queued_count += 1
    
    return jsonify({
        'training_jobs': jobs,
        'total': total,
        'running': running_count,
        'queued': queued_count
    }), 200

# Dashboard summary endpoint (optimized - single pass through all collections)
@api_blueprint.route('/api/dashboard', methods=['GET'])
@check_required_header
@token_required
def get_dashboard(current_user):
    data = load_data()
    
    # Systems summary (single pass)
    systems = data['systems']
    sys_total = len(systems)
    sys_up = sum(1 for s in systems if s.get('status') == 'up')
    sys_down = sum(1 for s in systems if s.get('status') == 'down')
    
    # Employees summary (single pass)
    employees = data['employees']
    emp_total = len(employees)
    emp_active = sum(1 for e in employees if e.get('status') == 'active')
    
    # Messages summary (single pass)
    messages = data['messages']
    msg_total = len(messages)
    msg_unread = 0
    msg_high_priority = 0
    for m in messages:
        is_read = m.get('read', True)
        if not is_read:
            msg_unread += 1
            if m.get('priority') == 'high':
                msg_high_priority += 1
    
    # Models summary (single pass)
    models = data['model_deployments']
    mod_total = len(models)
    mod_deployed = 0
    mod_testing = 0
    for m in models:
        status = m.get('status')
        if status == 'deployed':
            mod_deployed += 1
        elif status == 'testing':
            mod_testing += 1
    
    # Training jobs summary (single pass)
    jobs = data['training_jobs']
    job_total = len(jobs)
    job_running = 0
    job_queued = 0
    job_completed = 0
    for j in jobs:
        status = j.get('status')
        if status == 'running':
            job_running += 1
        elif status == 'queued':
            job_queued += 1
        elif status == 'completed':
            job_completed += 1
    
    dashboard_data = {
        'systems_summary': {'total': sys_total, 'up': sys_up, 'down': sys_down},
        'employees_summary': {'total': emp_total, 'active': emp_active},
        'messages_summary': {'total': msg_total, 'unread': msg_unread, 'high_priority': msg_high_priority},
        'models_summary': {'total': mod_total, 'deployed': mod_deployed, 'testing': mod_testing},
        'training_jobs_summary': {'total': job_total, 'running': job_running, 'queued': job_queued, 'completed': job_completed}
    }
    
    return jsonify(dashboard_data), 200

# Send message endpoint
@api_blueprint.route('/api/messages', methods=['POST'])
@check_required_header
@token_required
def send_message(current_user):
    req_data = request.get_json()
    
    if not req_data or 'recipient' not in req_data or 'subject' not in req_data or 'body' not in req_data:
        return jsonify({'error': 'Missing required fields: recipient, subject, body'}), 400
    
    data = load_data()
    
    # Check message limit
    if len(data['messages']) >= MAX_MESSAGES:
        return jsonify({'error': 'Message limit reached'}), 400
    
    # Validate fields
    valid, error = validate_string(req_data['recipient'], 'recipient')
    if not valid:
        return jsonify({'error': error}), 400
    
    valid, error = validate_string(req_data['subject'], 'subject')
    if not valid:
        return jsonify({'error': error}), 400
    
    valid, error = validate_string(req_data['body'], 'body', MAX_BODY_LENGTH)
    if not valid:
        return jsonify({'error': error}), 400
    
    priority = req_data.get('priority', 'normal')
    if priority not in ['low', 'normal', 'high']:
        priority = 'normal'
    
    # Create new message
    new_message = {
        'id': get_next_id(data['messages']),
        'sender': current_user,
        'recipient': sanitize_string(req_data['recipient']),
        'subject': sanitize_string(req_data['subject']),
        'body': sanitize_string(req_data['body'], MAX_BODY_LENGTH),
        'priority': priority,
        'read': False,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    data['messages'].append(new_message)
    
    return jsonify({
        'message': 'Message sent successfully',
        'message_id': new_message['id'],
        'recipient': new_message['recipient'],
        'subject': new_message['subject'],
        'status': 'sent'
    }), 201

# Create employee endpoint
@api_blueprint.route('/api/employees', methods=['POST'])
@check_required_header
@token_required
def create_employee(current_user):
    req_data = request.get_json()
    
    required_fields = ['name', 'email', 'department', 'role']
    if not req_data or not all(field in req_data for field in required_fields):
        return jsonify({'error': 'Missing required fields: name, email, department, role'}), 400
    
    data = load_data()
    
    # Check employee limit
    if len(data['employees']) >= MAX_EMPLOYEES:
        return jsonify({'error': 'Employee limit reached'}), 400
    
    # Validate fields
    valid, error = validate_string(req_data['name'], 'name')
    if not valid:
        return jsonify({'error': error}), 400
    
    valid, error = validate_email(req_data['email'])
    if not valid:
        return jsonify({'error': error}), 400
    
    valid, error = validate_string(req_data['department'], 'department')
    if not valid:
        return jsonify({'error': error}), 400
    
    valid, error = validate_string(req_data['role'], 'role')
    if not valid:
        return jsonify({'error': error}), 400
    
    # Check for duplicate email
    if any(e['email'] == req_data['email'] for e in data['employees']):
        return jsonify({'error': 'Employee with this email already exists'}), 400
    
    # Create new employee
    new_employee = {
        'id': get_next_id(data['employees']),
        'name': sanitize_string(req_data['name']),
        'email': sanitize_string(req_data['email']),
        'department': sanitize_string(req_data['department']),
        'role': sanitize_string(req_data['role']),
        'status': 'active',
        'hire_date': datetime.now().strftime('%Y-%m-%d'),
        'projects': []
    }
    
    data['employees'].append(new_employee)
    
    return jsonify({
        'message': 'Employee created successfully',
        'employee': new_employee
    }), 201

# Update employee endpoint
@api_blueprint.route('/api/employees/<int:employee_id>', methods=['PUT'])
@check_required_header
@token_required
def update_employee(current_user, employee_id):
    req_data = request.get_json()
    
    if not req_data:
        return jsonify({'error': 'No data provided'}), 400
    
    data = load_data()
    employee = next((e for e in data['employees'] if e['id'] == employee_id), None)
    
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    # Validate and update fields
    updated_fields = []
    
    if 'name' in req_data:
        valid, error = validate_string(req_data['name'], 'name')
        if not valid:
            return jsonify({'error': error}), 400
        employee['name'] = sanitize_string(req_data['name'])
        updated_fields.append('name')
    
    if 'email' in req_data:
        valid, error = validate_email(req_data['email'])
        if not valid:
            return jsonify({'error': error}), 400
        # Check for duplicate email (excluding current employee)
        if any(e['email'] == req_data['email'] and e['id'] != employee_id for e in data['employees']):
            return jsonify({'error': 'Employee with this email already exists'}), 400
        employee['email'] = sanitize_string(req_data['email'])
        updated_fields.append('email')
    
    if 'department' in req_data:
        valid, error = validate_string(req_data['department'], 'department')
        if not valid:
            return jsonify({'error': error}), 400
        employee['department'] = sanitize_string(req_data['department'])
        updated_fields.append('department')
    
    if 'role' in req_data:
        valid, error = validate_string(req_data['role'], 'role')
        if not valid:
            return jsonify({'error': error}), 400
        employee['role'] = sanitize_string(req_data['role'])
        updated_fields.append('role')
    
    if 'status' in req_data:
        if req_data['status'] not in ['active', 'inactive', 'on-leave']:
            return jsonify({'error': 'Invalid status. Allowed: active, inactive, on-leave'}), 400
        employee['status'] = req_data['status']
        updated_fields.append('status')
    
    return jsonify({
        'message': 'Employee updated successfully',
        'employee': employee,
        'updated_fields': updated_fields
    }), 200

# Delete employee endpoint
@api_blueprint.route('/api/employees/<int:employee_id>', methods=['DELETE'])
@check_required_header
@token_required
def delete_employee(current_user, employee_id):
    data = load_data()
    employee = next((e for e in data['employees'] if e['id'] == employee_id), None)
    
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    data['employees'].remove(employee)
    
    return jsonify({
        'message': 'Employee deleted successfully',
        'employee_id': employee_id
    }), 200

# Deploy model endpoint
@api_blueprint.route('/api/models/deploy', methods=['POST'])
@check_required_header
@token_required
def deploy_model(current_user):
    req_data = request.get_json()
    
    required_fields = ['model_name', 'version', 'environment']
    if not req_data or not all(field in req_data for field in required_fields):
        return jsonify({'error': 'Missing required fields: model_name, version, environment'}), 400
    
    data = load_data()
    
    # Validate fields
    valid, error = validate_string(req_data['model_name'], 'model_name')
    if not valid:
        return jsonify({'error': error}), 400
    
    valid, error = validate_string(req_data['version'], 'version', 50)
    if not valid:
        return jsonify({'error': error}), 400
    
    if req_data['environment'] not in ['development', 'staging', 'production']:
        return jsonify({'error': 'Invalid environment. Allowed: development, staging, production'}), 400
    
    # Create new deployment
    new_deployment = {
        'id': get_next_id(data['model_deployments']),
        'model_name': sanitize_string(req_data['model_name']),
        'version': sanitize_string(req_data['version'], 50),
        'environment': req_data['environment'],
        'status': 'deploying',
        'deployed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'accuracy': 0.0,
        'requests': 0
    }
    
    data['model_deployments'].append(new_deployment)
    
    return jsonify({
        'message': 'Model deployment initiated',
        'deployment': new_deployment,
        'estimated_time': '5-10 minutes'
    }), 201

# Start training job endpoint
@api_blueprint.route('/api/training-jobs', methods=['POST'])
@check_required_header
@token_required
def start_training_job(current_user):
    req_data = request.get_json()
    
    required_fields = ['model_type', 'dataset', 'epochs']
    if not req_data or not all(field in req_data for field in required_fields):
        return jsonify({'error': 'Missing required fields: model_type, dataset, epochs'}), 400
    
    data = load_data()
    
    # Check training job limit
    if len(data['training_jobs']) >= MAX_TRAINING_JOBS:
        return jsonify({'error': 'Training job limit reached'}), 400
    
    # Validate fields
    valid, error = validate_string(req_data['model_type'], 'model_type')
    if not valid:
        return jsonify({'error': error}), 400
    
    valid, error = validate_string(req_data['dataset'], 'dataset')
    if not valid:
        return jsonify({'error': error}), 400
    
    # Validate epochs
    try:
        epochs = int(req_data['epochs'])
        if epochs < 1 or epochs > 1000:
            return jsonify({'error': 'Epochs must be between 1 and 1000'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Epochs must be a valid integer'}), 400
    
    # Validate optional fields
    batch_size = 32
    if 'batch_size' in req_data:
        try:
            batch_size = int(req_data['batch_size'])
            if batch_size < 1 or batch_size > 512:
                batch_size = 32
        except (ValueError, TypeError):
            batch_size = 32
    
    learning_rate = 0.001
    if 'learning_rate' in req_data:
        try:
            learning_rate = float(req_data['learning_rate'])
            if learning_rate <= 0 or learning_rate > 1:
                learning_rate = 0.001
        except (ValueError, TypeError):
            learning_rate = 0.001
    
    # Create new training job
    new_job = {
        'id': get_next_id(data['training_jobs']),
        'model_type': sanitize_string(req_data['model_type']),
        'dataset': sanitize_string(req_data['dataset']),
        'epochs': epochs,
        'batch_size': batch_size,
        'learning_rate': learning_rate,
        'status': 'queued',
        'progress': 0,
        'started_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'current_epoch': 0,
        'loss': 0.0
    }
    
    data['training_jobs'].append(new_job)
    
    return jsonify({
        'message': 'Training job started successfully',
        'job': new_job,
        'estimated_duration': f"{epochs * 5} minutes"
    }), 201

# Update system status endpoint
@api_blueprint.route('/api/systems/<int:system_id>', methods=['PATCH'])
@check_required_header
@token_required
def update_system_status(current_user, system_id):
    req_data = request.get_json()
    
    if not req_data or 'status' not in req_data:
        return jsonify({'error': 'Missing required field: status'}), 400
    
    allowed_statuses = ['up', 'down', 'maintenance']
    if req_data['status'] not in allowed_statuses:
        return jsonify({'error': f'Invalid status. Allowed: {", ".join(allowed_statuses)}'}), 400
    
    data = load_data()
    system = next((s for s in data['systems'] if s['id'] == system_id), None)
    
    if not system:
        return jsonify({'error': 'System not found'}), 404
    
    system['status'] = req_data['status']
    system['last_checked'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify({
        'message': 'System status updated successfully',
        'system': system
    }), 200

# Mark message as read endpoint
@api_blueprint.route('/api/messages/<int:message_id>/read', methods=['POST'])
@check_required_header
@token_required
def mark_message_read(current_user, message_id):
    data = load_data()
    message = next((m for m in data['messages'] if m['id'] == message_id), None)
    
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    
    message['read'] = True
    
    return jsonify({
        'message': 'Message marked as read',
        'message_id': message_id,
        'read': True
    }), 200

# Image upload endpoint
@api_blueprint.route('/api/upload-image', methods=['POST'])
@check_required_header
@token_required
def upload_image(current_user):
    # Check if file is in request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({'error': 'No image file selected'}), 400
    
    # Get file extension
    original_filename = secure_filename(file.filename)
    if '.' not in original_filename:
        return jsonify({'error': 'Image format not supported'}), 400
    
    file_ext = original_filename.rsplit('.', 1)[1].lower()
    
    # Check if file type is allowed (only SVG, but don't reveal this)
    if file_ext not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Image format not supported'}), 400
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'Image file too large. Maximum size is 5MB'}), 400
    
    # Always save as 'admin.svg' to maintain a consistent filename (overwrites existing)
    admin_filename = 'admin.svg'
    file_path = os.path.join(UPLOAD_FOLDER, admin_filename)
    
    # Remove only the existing admin.svg file if it exists (more efficient than deleting all files)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass  # Continue even if deletion fails
    
    # Save file
    try:
        file.save(file_path)
        
        return jsonify({
            'message': 'Image uploaded successfully',
            'filename': admin_filename,
            'url': f"/api/images/admin.svg"
        }), 201
    except Exception as e:
        return jsonify({'error': f'Failed to upload image: {str(e)}'}), 500

# Serve image endpoint
@api_blueprint.route('/api/images/<image_id>', methods=['GET'])
def serve_image(image_id):
    # Sanitize image_id - remove any path components
    image_id = os.path.basename(image_id)
    
    # Additional validation - only allow alphanumeric, dash, underscore, and dot
    if not all(c.isalnum() or c in '.-_' for c in image_id):
        return jsonify({'error': 'Invalid image ID'}), 400
    
    # Prevent path traversal attacks
    if '..' in image_id or '/' in image_id or '\\' in image_id:
        return jsonify({'error': 'Invalid image ID'}), 400
    
    # If image_id already has .svg extension, use it as is, otherwise add .svg
    if image_id.endswith('.svg'):
        image_filename = image_id
    else:
        image_filename = f"{image_id}.svg"
    
    # Construct the full path
    image_path = os.path.join(UPLOAD_FOLDER, image_filename)
    
    # Get the absolute path and verify it's within the upload folder
    abs_image_path = os.path.abspath(image_path)
    abs_upload_folder = os.path.abspath(UPLOAD_FOLDER)
    
    # Ensure the resolved path is actually inside the upload folder
    if not abs_image_path.startswith(abs_upload_folder + os.sep):
        return jsonify({'error': 'Invalid image path'}), 400
    
    # Check if file exists and is actually a file (not directory)
    if not os.path.exists(abs_image_path) or not os.path.isfile(abs_image_path):
        return jsonify({'error': 'Image not found'}), 404
    
    # Verify file extension is .svg
    if not abs_image_path.lower().endswith('.svg'):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Parse and serve SVG (this enables XXE vulnerability)
    try:
        from lxml import etree
        from flask import Response
        
        parser = etree.XMLParser(resolve_entities=True, no_network=False)
        
        # Parse the SVG file (this triggers XXE if present)
        tree = etree.parse(abs_image_path, parser)
        
        # Convert back to string with resolved entities
        svg_content = etree.tostring(tree, encoding='unicode', method='xml')
        
        # Return the processed SVG
        return Response(svg_content, mimetype='image/svg+xml')
    except etree.XMLSyntaxError as e:
        return jsonify({'error': 'Invalid SVG file'}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to serve image: {str(e)}'}), 500

# Register the blueprint
app.register_blueprint(api_blueprint)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Production mode - no debug
    app.run(host='0.0.0.0', port=5000, debug=False)
