from flask import Flask 
from flask_cors import CORS
from dotenv import load_dotenv
from routes.tasks import tasks_bp
from supabase import create_client, Client
from routes.ai import ai_bp

import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(ai_bp)


supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_ROLE_KEY')
)

app.register_blueprint(tasks_bp)

@app.route('/api/dashboard')
def dashboard():
    return {
        'status': 'success',
        'message': 'taskhub data retrieved successfully',
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)