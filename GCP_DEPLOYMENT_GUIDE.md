# GCP Cloud Run Deployment Guide

Complete step-by-step guide to deploy the Map Rendering API to Google Cloud Platform with CI/CD pipeline.

---

## 📋 Prerequisites

- Google Cloud Platform account
- GitHub repository with your code
- Project name: `garudx` (already created)
- OpenAI API Key
- Custom API Key for authentication

---

## 🚀 Part 1: Initial GCP Setup (Using UI)

### Step 1: Enable Required APIs

1. Go to **Google Cloud Console**: https://console.cloud.google.com
2. Select your project **garudx** from the top dropdown
3. Click on **Navigation Menu (☰)** → **APIs & Services** → **Library**
4. Search and enable the following APIs (click on each, then click **ENABLE**):
   - **Cloud Run API**
   - **Cloud Build API**
   - **Container Registry API**
   - **Artifact Registry API** (optional, for newer container storage)

### Step 2: Set Up Environment Variables in Cloud Build

You'll set your API keys as substitution variables in the Cloud Build trigger (we'll do this in Part 2, Step 2)

---

## 🔗 Part 2: Connect GitHub Repository (Using UI)

### Step 1: Connect GitHub to Cloud Build

1. Go to **Navigation Menu (☰)** → **Cloud Build** → **Triggers**
2. Click **CONNECT REPOSITORY**
3. Select source: **GitHub (Cloud Build GitHub App)**
4. Click **CONTINUE**
5. Click **Authenticate with GitHub**
6. Sign in to GitHub and authorize Google Cloud Build
7. Select your repository from the list
8. Click **CONNECT**
9. Click **DONE** (skip creating a trigger for now, we'll do it next)

### Step 2: Create Build Trigger

1. Still in **Cloud Build** → **Triggers**
2. Click **CREATE TRIGGER**
3. Configure the trigger:

   **Name**: `deploy-map-rendering-api`
   
   **Description**: `Deploy Map Rendering API to Cloud Run on push to main`
   
   **Event**: Select **Push to a branch**
   
   **Source**:
   - **Repository**: Select your connected GitHub repository
   - **Branch**: `^main$` (or `^master$` if you use master branch)
   
   **Configuration**:
   - **Type**: Select **Cloud Build configuration file (yaml or json)**
   - **Location**: `/map-rendering-api/cloudbuild.yaml`
     - ⚠️ Adjust this path based on your repo structure
     - If `map-rendering-api` is at the root, use `/cloudbuild.yaml`
   
   **Advanced** (expand this section):
   - **Service account**: Leave as default (Cloud Build service account)
   - **Substitution variables**: Click **ADD VARIABLE** twice:
     - Variable 1: `_OPENAI_API_KEY` = `your-openai-api-key-here`
     - Variable 2: `_API_KEY` = `your-custom-api-key-here`
   
4. Click **CREATE**

---

## 🔧 Part 3: Grant Cloud Build Permissions (Using UI)

### Step 1: Add Cloud Run Admin Role

1. Go to **Navigation Menu (☰)** → **IAM & Admin** → **IAM**
2. Find the principal that looks like:
   - `PROJECT_NUMBER@cloudbuild.gserviceaccount.com`
   - Example: `123456789@cloudbuild.gserviceaccount.com`
3. Click the **pencil icon (Edit)** next to it
4. Click **ADD ANOTHER ROLE**
5. Search and select: **Cloud Run Admin**
6. Click **ADD ANOTHER ROLE** again
7. Search and select: **Service Account User**
8. Click **SAVE**

---

## 🎯 Part 4: Deploy Your Application

### Option A: Automatic Deployment (Recommended)

1. Commit and push your code to GitHub:
   ```bash
   git add .
   git commit -m "Add GCP Cloud Run deployment configuration"
   git push origin main
   ```

2. Monitor the build:
   - Go to **Cloud Build** → **History**
   - You should see a build running
   - Click on it to see real-time logs
   - Wait for it to complete (takes 5-10 minutes first time)

3. Once complete, go to **Cloud Run** → **Services**
   - You should see `map-rendering-api` service
   - Click on it to see the URL

### Option B: Manual First Deployment (If trigger doesn't work)

1. Go to **Cloud Build** → **Triggers**
2. Find your trigger `deploy-map-rendering-api`
3. Click **RUN** button on the right
4. Click **RUN TRIGGER**
5. Monitor in **Cloud Build** → **History**

---

## 🌐 Part 5: Access Your API

### Get Your API URL

1. Go to **Navigation Menu (☰)** → **Cloud Run**
2. Click on **map-rendering-api** service
3. Copy the URL at the top (looks like: `https://map-rendering-api-xxxxx-uc.a.run.app`)

### Test Your API

1. Open the URL in browser and add `/docs`:
   ```
   https://map-rendering-api-xxxxx-uc.a.run.app/docs
   ```

2. You should see the FastAPI Swagger documentation

3. Test the health endpoint:
   ```
   https://map-rendering-api-xxxxx-uc.a.run.app/health
   ```

---

## 🔒 Part 6: Update Environment Variables (If Needed)

### Update API Keys or Other Variables

**Option 1: Update in Cloud Build Trigger (Recommended)**
1. Go to **Cloud Build** → **Triggers**
2. Click on **deploy-map-rendering-api**
3. Click **EDIT**
4. Scroll to **Substitution variables**
5. Update `_OPENAI_API_KEY` or `_API_KEY` values
6. Click **SAVE**
7. Next deployment will use new values

**Option 2: Update Directly in Cloud Run**
1. Go to **Cloud Run** → **map-rendering-api**
2. Click **EDIT & DEPLOY NEW REVISION**
3. Go to **Variables & Secrets** tab
4. Under **Environment variables**, you can add/edit:
   - `OPENAI_API_KEY` = your OpenAI key
   - `API_KEY` = your custom API key
   - `ENVIRONMENT` = production
   - `MODEL` = gpt-4o-mini
   - `LOG_LEVEL` = INFO
   - `MAX_PAGES` = 30
   - `DEFAULT_ZOOM` = 4.0
5. Click **DEPLOY**

⚠️ **Note**: Values set in Cloud Run UI will be overwritten on next Git push. Use Option 1 for permanent changes.

---

## 📊 Part 7: Monitor Your Application

### View Logs

1. Go to **Cloud Run** → **map-rendering-api**
2. Click **LOGS** tab
3. You'll see all application logs in real-time

### View Metrics

1. Go to **Cloud Run** → **map-rendering-api**
2. Click **METRICS** tab
3. View:
   - Request count
   - Request latency
   - Container instances
   - Memory/CPU usage

---

## 🔄 Part 8: CI/CD Pipeline Workflow

Now your CI/CD pipeline is complete! Here's what happens:

1. **You push code to GitHub** (main branch)
2. **Cloud Build trigger activates** automatically
3. **Cloud Build**:
   - Pulls your code
   - Builds Docker image
   - Pushes to Container Registry
   - Deploys to Cloud Run
4. **Cloud Run**:
   - Creates new revision
   - Gradually shifts traffic
   - Old revision removed after successful deployment
5. **Your API is live** with zero downtime!

---

## 🛠️ Troubleshooting

### Build Fails

1. Check **Cloud Build** → **History** → Click on failed build
2. Review logs for errors
3. Common issues:
   - Missing dependencies in `requirements.txt`
   - Dockerfile syntax errors
   - Permission issues (check IAM roles)

### Secrets Not Working

1. Verify secrets exist in **Secret Manager**
2. Check permissions for both:
   - Cloud Build service account
   - Compute Engine default service account
3. Ensure secret names match exactly in `cloudbuild.yaml`

### Cloud Run Service Not Starting

1. Go to **Cloud Run** → **map-rendering-api** → **LOGS**
2. Look for startup errors
3. Common issues:
   - Port mismatch (ensure app listens on port 8080)
   - Missing environment variables
   - Application crashes on startup

### Trigger Not Firing

1. Check **Cloud Build** → **Triggers**
2. Verify:
   - Repository is connected
   - Branch name matches (e.g., `^main$` vs `^master$`)
   - `cloudbuild.yaml` path is correct
3. Try manual trigger first

---

## 💰 Cost Optimization

### Free Tier Limits
- **Cloud Run**: 2 million requests/month free
- **Cloud Build**: 120 build-minutes/day free
- **Container Registry**: 0.5 GB storage free

### Tips to Reduce Costs
1. Set **max instances** to limit scaling
2. Use **minimum instances: 0** (default) to scale to zero
3. Set appropriate **CPU allocation**: Only during request processing
4. Monitor usage in **Billing** dashboard

---

## 🔐 Security Best Practices

1. ✅ **Never commit secrets** to Git
2. ✅ **Store API keys in Cloud Build substitution variables** (not in code)
3. ✅ **Enable HTTPS** (automatic with Cloud Run)
4. ✅ **Use API key authentication** (already implemented)
5. ✅ **Review IAM permissions** regularly
6. ✅ **Enable Cloud Armor** for DDoS protection (optional)
7. ⚠️ **Note**: For production, consider using Secret Manager for better security

---

## 📝 Quick Reference

### Important URLs
- **GCP Console**: https://console.cloud.google.com
- **Cloud Run**: https://console.cloud.google.com/run
- **Cloud Build**: https://console.cloud.google.com/cloud-build
- **Secret Manager**: https://console.cloud.google.com/security/secret-manager

### Key Files
- `Dockerfile` - Container configuration
- `cloudbuild.yaml` - CI/CD pipeline configuration
- `.dockerignore` - Files to exclude from Docker build
- `.gcloudignore` - Files to exclude from GCP deployment

### Useful Commands (Optional - for local testing)

```bash
# Build Docker image locally
docker build -t map-rendering-api .

# Run locally
docker run -p 8080:8080 --env-file .env map-rendering-api

# Test locally
curl http://localhost:8080/health
```

---

## ✅ Deployment Checklist

- [ ] Enable required GCP APIs
- [ ] Create secrets in Secret Manager
- [ ] Grant permissions to service accounts
- [ ] Connect GitHub repository
- [ ] Create Cloud Build trigger
- [ ] Push code to trigger deployment
- [ ] Verify deployment in Cloud Run
- [ ] Test API endpoints
- [ ] Monitor logs and metrics
- [ ] Set up billing alerts (recommended)

---

## 🎉 Success!

Your Map Rendering API is now deployed on GCP Cloud Run with automatic CI/CD!

Every time you push to the main branch, your application will automatically:
- Build
- Test
- Deploy
- Go live

**Your API URL**: Check Cloud Run console for the live URL

**API Documentation**: `https://YOUR-URL/docs`

**Health Check**: `https://YOUR-URL/health`
