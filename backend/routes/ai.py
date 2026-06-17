from flask import Blueprint, jsonify, request
from supabase import create_client
from dotenv import load_dotenv
import os
import requests
import base64

load_dotenv()

ai_bp = Blueprint('ai', __name__)

supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_SERVICE_ROLE_KEY')
)

IMAGE_PROMPTS = {
    'white_background': 'product on pure white background, professional ecommerce photography, clean, high quality DSLR photo',
    'theme_luxury': 'product on luxury velvet background, professional photography, elegant, high quality',
    'theme_marble': 'product on marble surface, professional product photography, high quality DSLR',
    'creative_beach': 'product in beach sunset lifestyle scene, professional photography, photorealistic',
    'creative_forest': 'product in forest nature scene, professional photography, photorealistic',
    'model_front': 'person wearing the jewelry, front view, professional fashion photography, realistic',
    'model_side': 'person wearing the jewelry, 45 degree side angle, professional fashion photography',
    'model_closeup': 'close up of person wearing jewelry, professional fashion photography, detailed'
}

def remove_background(image_url: str) -> str:
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        data={
            'image_url': image_url,
            'size': 'auto'
        },
        headers={
            'X-Api-Key': os.getenv('REMOVEBG_API_KEY')
        }
    )
    img_base64 = base64.b64encode(response.content).decode('utf-8')
    return img_base64

def generate_with_huggingface(prompt: str, image_base64: str) -> str:
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
    }
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "num_inference_steps": 30,
            "guidance_scale": 7.5
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Response image bytes hoga
    img_base64 = base64.b64encode(response.content).decode('utf-8')
    return f"data:image/jpeg;base64,{img_base64}"    

@ai_bp.route('/api/tasks/<task_id>/generate', methods=['POST'])
def generate_image(task_id):
    data = request.get_json()
    image_type = data.get('image_type', 'white_background')

    # 1. Task details fetch karo
    task = supabase.table('tasks')\
        .select('product_img_url, title')\
        .eq('id', task_id)\
        .single()\
        .execute()

    product_image_url = task.data['product_img_url']

    # 2. Background remove karo
    img_base64 = remove_background(product_image_url)

    # 3. Prompt lo
    prompt = IMAGE_PROMPTS.get(image_type, IMAGE_PROMPTS['white_background'])


    generated_url = generate_with_huggingface(prompt, img_base64)

    # 5. Database mein save karo
    supabase.table('generated_image').insert({
        'task_id': task_id,
        'image_type': image_type,
        'image_url': generated_url,
        'prompt_used': prompt,
    }).execute()

    return jsonify({
        'status': 'success',
        'image_url': generated_url,
        'image_type': image_type
    })