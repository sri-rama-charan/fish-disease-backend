# Railway.app Deployment Guide

## Why Railway?

Railway offers **8GB RAM on their free tier** (with $5 credit/month), which is sufficient to run your ML model. Render's free tier only has 512MB RAM, which isn't enough.

## 🚀 Deployment Steps

### Step 1: Sign Up for Railway

1. Go to https://railway.app
2. Click **"Login"** or **"Start a New Project"**
3. Sign up with your **GitHub account**

### Step 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your `fish_disease_backend` repository
4. Railway will automatically detect it's a Python project

### Step 3: Configure Environment Variables

Railway needs your Hugging Face token to download the model:

1. In your Railway project dashboard, click **"Variables"** tab
2. Click **"New Variable"**
3. Add the following:
   - **Variable:** `HF_TOKEN`
   - **Value:** `your_huggingface_token_here`
4. Click **"Add"**

### Step 4: Deploy!

1. Railway will automatically start building and deploying
2. Wait for the build to complete (this may take 3-5 minutes due to ML dependencies)
3. Once deployed, Railway will provide you with a URL

### Step 5: Get Your Backend URL

1. In your Railway dashboard, click **"Settings"**
2. Under **"Domains"**, click **"Generate Domain"**
3. Copy your domain (e.g., `your-app.up.railway.app`)
4. Test it: `https://your-app.up.railway.app/docs`

## ✅ Verification

Once deployed, verify everything works:

1. **Health Check:** Visit `https://your-app.up.railway.app/health`
   - Should return: `{"status":"healthy","model_loaded":true}`

2. **API Docs:** Visit `https://your-app.up.railway.app/docs`
   - Try uploading a fish image to `/predict` endpoint

3. **Model Loading:** Check Railway logs
   - Should see: `INFO:main:Model loaded successfully`

## 📊 Monitoring

### Check Logs

1. Go to your Railway project dashboard
2. Click **"Deployments"** tab
3. Click on the latest deployment
4. View logs to see model loading and requests

### Monitor Usage

1. Click **"Metrics"** tab
2. Check RAM usage (should be under 8GB)
3. Monitor request counts

## 💰 Free Tier Limits

Railway's free tier includes:

- ✅ **$5 credit per month**
- ✅ **8GB RAM**
- ✅ **100GB bandwidth**
- ✅ **500 execution hours/month**

This is sufficient for development and testing!

## 🔧 Troubleshooting

### If deployment fails:

1. **Check Build Logs**
   - Go to Deployments → View logs
   - Look for errors during `pip install`

2. **Memory Issues**
   - If you see OOM (Out of Memory) errors
   - Upgrade to Railway's Pro plan ($5/month for 32GB RAM)

3. **Model Loading Timeout**
   - First deployment may take longer (downloading model)
   - Subsequent deploys will be faster (model cached)

## 🔄 Updating Your Deployment

After making code changes:

```bash
git add .
git commit -m "Your commit message"
git push
```

Railway will automatically detect changes and redeploy!

## 🌐 Connect Frontend

Once deployed, update your frontend's `.env.production`:

```bash
VITE_API_URL=https://your-app.up.railway.app
```

Then rebuild and redeploy your frontend on Vercel.

## 🎉 Done!

Your Fish Disease Detector backend is now live on Railway with full ML model support!
