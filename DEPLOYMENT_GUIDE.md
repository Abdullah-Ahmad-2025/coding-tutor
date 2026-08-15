# 🚀 Complete Deployment Guide - Coding Tutor AI

## 📋 Overview
This guide will help you deploy your **Coding Tutor AI** project completely **FREE** with no credit card required.

### Tech Stack
- **Frontend**: React (Vercel - Free)
- **Backend**: FastAPI/Python (Railway - Free)
- **Database**: SQLite (File-based - No external service needed)
- **AI API**: Groq (Free tier available)

---

## 🎯 Deployment Architecture

```
Frontend (React) → Backend (FastAPI) → SQLite Database
     ↓                  ↓                    ↓
   Vercel            Railway              File Storage
   (Free)           (Free)              (Free)
```

---

## 📝 Prerequisites

### 1. Required Accounts (All Free)
- [GitHub Account](https://github.com/signup) - For code hosting
- [Vercel Account](https://vercel.com/signup) - For frontend hosting
- [Railway Account](https://railway.app/) - For backend hosting
- [Groq Account](https://console.groq.com/) - For AI API (free tier)

### 2. Tools Needed
- Git installed on your computer
- Node.js installed (for frontend build)
- Python 3.9+ installed (for backend)

---

## 🚀 Step-by-Step Deployment

### Phase 1: Prepare Your Code for Deployment

#### Step 1.1: Clean Up Your Project
```bash
# Remove any local database files
cd backend
rm -f coding_tutor.db coding_tutor_local.db
cd ..
```

#### Step 1.2: Update Backend for Production
The backend is already configured for deployment with:
- Environment variable support (`DATABASE_URL`)
- CORS configuration
- Health check endpoint

#### Step 1.3: Update Frontend API URL
Edit `frontend/src/pages/ProblemPage.jsx`:
```javascript
// Change line 5 from:
const API = 'http://localhost:8000';

// To:
const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

---

### Phase 2: Push Code to GitHub

#### Step 2.1: Initialize Git (if not already done)
```bash
cd c:\Users\kingw\coding-tutor
git init
git add .
git commit -m "Initial commit"
```

#### Step 2.2: Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click "+" → "New repository"
3. Name it: `coding-tutor`
4. Make it **Public** (free hosting requires public repos)
5. Don't initialize with README
6. Click "Create repository"

#### Step 2.3: Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/coding-tutor.git
git branch -M main
git push -u origin main
```

---

### Phase 3: Deploy Backend to Railway

#### Step 3.1: Create Railway Account
1. Go to [Railway.app](https://railway.app/)
2. Sign up with GitHub
3. Verify your email
4. **Important**: Railway gives you $5 free credit/month (no credit card required)

#### Step 3.2: Create New Project
1. In Railway dashboard, click "New Project"
2. Click "Deploy from GitHub repo"
3. Select your `coding-tutor` repository
4. Click "Import"

#### Step 3.3: Configure Backend Service
1. Railway will detect your Python project automatically
2. Click on the service that was created (usually named after your repo)
3. Click the "Settings" tab
4. Configure the service:

   **Root Directory**: `backend`
   **Build Command**: `pip install -r ../requirements.txt`
   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. Click "Save Changes"

#### Step 3.4: Add Environment Variables
1. Click the "Variables" tab in your Railway service
2. Add the following environment variables:

   **If using SQLite (Recommended for beginners):**
   ```
   DATABASE_URL = sqlite:///coding_tutor.db
   GROQ_API_KEY = your_groq_api_key_here
   SECRET_KEY = your_random_secret_key_here
   CORS_ALLOWED_ORIGINS = https://your-frontend-url.vercel.app
   ```

   **If using PostgreSQL (Railway provides free PostgreSQL):**
   ```
   DATABASE_URL = ${RAILWAY_POSTGRES_CONNECTION_STRING}
   GROQ_API_KEY = your_groq_api_key_here
   SECRET_KEY = your_random_secret_key_here
   CORS_ALLOWED_ORIGINS = https://your-frontend-url.vercel.app
   ```

3. Click "Add Variable" for each one

#### Step 3.5: Deploy
1. Click the "Deployments" tab
2. Click "Redeploy" if it doesn't deploy automatically
3. Wait for deployment (1-3 minutes)
4. Click on your service domain to get the backend URL (e.g., `https://your-service.up.railway.app`)
5. Copy this URL

---

### Phase 4: Deploy Frontend to Vercel

#### Step 4.1: Create Vercel Account
1. Go to [Vercel.com](https://vercel.com/signup)
2. Sign up with GitHub
3. Verify your email

#### Step 4.2: Deploy Frontend
1. In Vercel dashboard, click "Add New Project"
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Environment Variables**:
   ```
   REACT_APP_API_URL = https://your-service.up.railway.app
   ```

5. Click "Deploy"
6. Wait for deployment (1-2 minutes)
7. Copy your frontend URL: `https://your-project.vercel.app`

---

### Phase 5: Update CORS Configuration

#### Step 5.1: Update Backend CORS
Go back to Railway → Your Backend Service → Variables tab:
```
CORS_ALLOWED_ORIGINS = https://your-frontend-url.vercel.app
```

#### Step 5.2: Redeploy Backend
In Railway, click the "Deployments" tab → Click "Redeploy"

---

### Phase 6: Get Groq API Key

#### Step 6.1: Create Groq Account
1. Go to [Groq Console](https://console.groq.com/)
2. Sign up (free)
3. Go to API Keys
4. Create new API key
5. Copy the key

#### Step 6.2: Add to Backend
Update the `GROQ_API_KEY` environment variable in Railway with your actual Groq API key.

---

### Phase 7: Test Your Deployment

#### Step 7.1: Test Backend Health
Visit: `https://your-service.up.railway.app/health`
Should return: `{"status":"ok","message":"Backend running"}`

#### Step 7.2: Test Frontend
Visit your Vercel URL and try:
1. Sign up/login
2. Solve a problem
3. Submit code

---

## 🔧 Troubleshooting

### Common Issues

**1. CORS Errors**
- Ensure `CORS_ALLOWED_ORIGINS` in backend matches your Vercel URL exactly
- Redeploy backend after updating CORS

**2. Database Connection Errors**
- If using SQLite: Ensure `DATABASE_URL` is set to `sqlite:///coding_tutor.db`
- If using PostgreSQL: Ensure the database URL is correct and includes SSL mode

**3. Build Failures**
- Check Railway logs for specific errors
- Ensure all dependencies are in `requirements.txt`
- For frontend: Ensure `npm install` runs successfully locally

**4. API Errors**
- Verify Groq API key is correct
- Check Groq API has free credits available

---

## 💡 Alternative Free Hosting Options

### Backend Alternatives
- **Render** (render.com) - Free tier available (requires credit card)
- **PythonAnywhere** - Free tier for Python web apps
- **Fly.io** - Free allowance for small apps

### Frontend Alternatives
- **Netlify** - Free hosting for React apps
- **GitHub Pages** - Free static hosting

### Database Alternatives
- **Supabase** - Free PostgreSQL database
- **Neon** - Free serverless PostgreSQL
- **Turso** - Free SQLite database in the cloud

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Deployment](https://create-react-app.dev/docs/deployment/)

---

## ✅ Deployment Checklist

- [ ] GitHub repository created and pushed
- [ ] Backend deployed to Railway
- [ ] Frontend deployed to Vercel
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] Groq API key added
- [ ] Backend health check passes
- [ ] Frontend loads successfully
- [ ] User authentication works
- [ ] Code submission works
- [ ] AI features work

---

## 🎉 You're Done!

Your Coding Tutor AI is now live and completely free! Users can:
- Sign up and log in
- Browse and solve coding problems
- Get AI-powered hints and explanations
- Track their progress and mistake patterns

**Your Live URLs:**
- Frontend: `https://your-project.vercel.app`
- Backend: `https://your-service.up.railway.app`
