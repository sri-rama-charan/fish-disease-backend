# Complete Deployment Guide - Fish Disease Detector

## Overview

You have **TWO** separate repositories that need to be deployed:

1. **Backend** (FastAPI/Python) - `fish_disease_backend` folder
2. **Frontend** (React/Vite) - `aqua-health-pro` folder (current)

---

## STEP 1: Deploy Backend First

### What to Deploy

- Folder: `C:\projects\fish_disease_backend`
- Contains: FastAPI app, ML model, Python dependencies

### Best Free Options for Backend

#### Option A: Render.com (Recommended - Easy & Free)

1. **Prepare Backend for Deployment**
   - Go to backend folder: `cd C:\projects\fish_disease_backend`
   - Create `requirements.txt` if not exists:
     ```bash
     pip freeze > requirements.txt
     ```
   - Create `render.yaml`:
     ```yaml
     services:
       - type: web
         name: fish-disease-api
         runtime: python
         buildCommand: pip install -r requirements.txt
         startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

2. **Deploy to Render**
   - Go to https://render.com
   - Sign up/Login with GitHub
   - Click **New → Web Service**
   - Connect your GitHub repo (or upload backend folder)
   - Settings:
3. **Prepare Backend for Deployment**
   - Go to backend folder: `cd C:\projects\fish_disease_backend`
   - Create `requirements.txt` if not exists:
     ```bash
     pip freeze > requirements.txt
     ```
   - Create `render.yaml`:
     ```yaml
     services:
       - type: web
         name: fish-disease-api
         runtime: python
         buildCommand: pip install -r requirements.txt
         startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

4. **Deploy to Render**
   - Go to https://render.com
   - Sign up/Login with GitHub
   - Click **New → Web Service**
   - Connect your GitHub repo (or upload backend folder)
   - Settings:
     - **Runtime:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Environment Variables** (Important!):
       - Click **Add Environment Variable**
       - **Key:** `HF_TOKEN`
       - **Value:** Your Hugging Face token (starts with `hf_...`)
   - Click **Create Web Service**

5. **Get Your Backend URL**
   - After deployment: `https://fish-disease-api.onrender.com`
   - Test it: `https://fish-disease-api.onrender.com/docs`

### Running Locally

To run the backend locally, you need to set the HF_TOKEN environment variable:

**Windows (PowerShell):**

```powershell
$env:HF_TOKEN="your_token_here"
uvicorn main:app --reload
```

**Windows (Command Prompt):**

```cmd
set HF_TOKEN=your_token_here
uvicorn main:app --reload
```

**Linux/Mac:**

```bash
export HF_TOKEN=your_token_here
uvicorn main:app --reload
```

#### Option B: Railway.app

2. Click **Start a New Project → Deploy from GitHub**
3. Select backend repository
4. Railway auto-detects Python
5. Add environment variables if needed
6. Get URL: `https://fish-disease-api.railway.app`

#### Option C: Hugging Face Spaces

1. Go to https://huggingface.co/spaces
2. Create new Space
3. Choose **Gradio** or **Streamlit** SDK
4. Upload backend code
5. Get URL: `https://huggingface.co/spaces/yourusername/fish-disease`

---

## STEP 2: Deploy Frontend

### What to Deploy

- Folder: `C:\projects\aqua-health-pro` (current folder)
- Contains: React app built with Vite

### Prepare Frontend

1. **Update Backend URL**
   - Edit `.env.production` in this folder:
     ```bash
     VITE_API_URL=https://fish-disease-api.onrender.com
     ```
   - Replace with YOUR actual backend URL from Step 1

2. **Build the App**

   ```bash
   npm run build
   ```

   - This creates a `dist/` folder with optimized files

### Best Free Options for Frontend

#### Option A: Vercel (Recommended - Easiest)

1. Go to https://vercel.com
2. Sign up/Login with GitHub
3. Click **Add New → Project**
4. Import this repository (`aqua-health-pro`)
5. Configure:
   - **Framework:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Environment Variable:**
     - Name: `VITE_API_URL`
     - Value: `https://fish-disease-api.onrender.com` (your backend URL)
6. Click **Deploy**
7. Get URL: `https://aqua-health-pro.vercel.app`

#### Option B: Netlify

1. Go to https://netlify.com
2. Click **Add new site → Import from Git**
3. Select this repository
4. Settings:
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
5. Add environment variable:
   - `VITE_API_URL` = your backend URL
6. Deploy
7. Get URL: `https://aqua-health-pro.netlify.app`

#### Option C: GitHub Pages

1. Install gh-pages:

   ```bash
   npm install -D gh-pages
   ```

2. Add to `package.json`:

   ```json
   "scripts": {
     "predeploy": "npm run build",
     "deploy": "gh-pages -d dist"
   }
   ```

3. Deploy:

   ```bash
   npm run deploy
   ```

4. Get URL: `https://yourusername.github.io/aqua-health-pro`

---

## STEP 3: Update APK with Deployed URLs

After both are deployed:

1. **Update `.env.production`**

   ```bash
   VITE_API_URL=https://fish-disease-api.onrender.com
   ```

2. **Rebuild Everything**

   ```bash
   npm run build
   npx cap sync android
   ```

3. **Generate APK**

   ```bash
   npx cap open android
   ```

   - Build → Build APK

---

## Quick Summary

### What You Deploy:

| Component    | What                            | Where          | URL Example                     |
| ------------ | ------------------------------- | -------------- | ------------------------------- |
| **Backend**  | `fish_disease_backend` folder   | Render/Railway | `https://your-api.onrender.com` |
| **Frontend** | `aqua-health-pro` folder (this) | Vercel/Netlify | `https://your-app.vercel.app`   |

### Order of Operations:

1. ✅ Deploy **Backend** first → Get backend URL
2. ✅ Update **Frontend** `.env.production` with backend URL
3. ✅ Deploy **Frontend** → Get frontend URL
4. ✅ Rebuild **APK** with deployed backend URL
5. ✅ Install APK on phone → Works anywhere with internet!

---

## Testing After Deployment

1. **Test Backend:**
   - Visit: `https://your-backend-url.com/docs`
   - Should see FastAPI documentation

2. **Test Frontend:**
   - Visit: `https://your-frontend-url.com`
   - Upload a fish image
   - Should get disease detection results

3. **Test APK:**
   - Install on phone
   - Upload image
   - Should connect to deployed backend

---

## Recommended Combo (All Free):

- **Backend:** Render.com (500 hours/month free)
- **Frontend:** Vercel (unlimited free for personal projects)
- **Total Cost:** $0

---

## Need Help?

If you get stuck:

1. Check backend is deployed: Visit `your-backend-url.com/docs`
2. Check frontend env vars: `.env.production` has correct backend URL
3. Rebuild after changes: `npm run build && npx cap sync android`
