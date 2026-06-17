import resend
import os
from dotenv import load_dotenv

load_dotenv()
resend_api_key = os.getenv('RESEND_API_KEY')


def send_task_assigned_email(user_email: str, task_title: str, task_id: str):
    resend.Emails.send({
        "from" : "TaskHub <onboarding@resend.dev>",
        "to" : user_email,  
        "subject" : f"New Task Assigned: {task_title}",
        "html" : f"""
<h1>New Task Assigned!</h1>
<p>You have been assigned a new task: <strong>{task_title}</strong></p>
<a href="http://localhost:3000/tasks">View Task</a>
"""
})
    
def send_task_submitted_email(admin_email: str, task_title: str, user_name: str, task_id: str):
    resend.Emails.send({
        "from": "TaskHub <onboarding@resend.dev>",
        "to": "priyanshisin477@gmail.com",
        "subject": f"Task Completed: {task_title} by {user_name}",
        "html": f"""
        <h1>Task Submitted!</h1>
        <p><strong>{user_name}</strong> has completed: <strong>{task_title}</strong></p>
        <a href="http://localhost:3000/tasks/{task_id}">Review Task</a>
        """
    })