# TaskHub — AI-Powered Task Management Platform

## Live Demo
- Frontend: [Add Vercel URL after deployment]
- Backend: [Add Render URL after deployment]

## Tech Stack
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS
- **Backend**: Flask, Python
- **Database**: Supabase (PostgreSQL)
- **Auth**: Google OAuth
- **Email**: Resend
- **Storage**: Supabase Storage

## Local Setup

### Frontend:
cd frontend
npm install
npm run dev

### Backend:
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

## Migration Instructions
Run these SQL files in order in Supabase SQL Editor:
1. migrations/001_create_users.sql
2. migrations/002_create_tasks.sql
3. migrations/003_create_generated_images.sql
4. migrations/004_create_audit_logs.sql
5. migrations/005_add_rls_policies.sql

## AI Approach
1. Product image uploaded by admin
2. Background removed using remove.bg API
3. New backgrounds generated using HuggingFace Stable Diffusion
4. 8 variations generated per task
5. Product consistency maintained throughout

## Known Limitations
- AI generation uses HuggingFace free tier
- Email notifications on Resend free tier
- Supabase free plan (Seoul region)

## Assumptions Made
- Google OAuth only for authentication
- Emails sent to verified address for testing