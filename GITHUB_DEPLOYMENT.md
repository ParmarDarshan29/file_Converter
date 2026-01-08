# GitHub Deployment Guide

## ⚠️ Important: GitHub Limitation

**GitHub Pages cannot run your Flask backend.** It only serves static HTML/CSS/JS files.

Your app requires:
- Python Flask server
- nbconvert library
- pandoc (system package)
- xelatex (system package)

**None of these can run on GitHub Pages.**

---

## Solution: Use GitHub + Free Backend Hosting

Your code stays on GitHub, but deploys to a service that supports Python:

### **Recommended: GitHub → Render (100% Free)**

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Connect Render to GitHub:**
   - Go to [render.com](https://render.com)
   - Click "Sign Up" → "GitHub" 
   - Authorize Render to access your repos
   - Click "New +" → "Web Service"
   - Select `ParmarDarshan29/file_Converter`
   - Click "Connect"

3. **Auto-Deploy Setup:**
   - Render detects `render.yaml` automatically
   - Every time you push to GitHub, Render rebuilds automatically
   - Your code stays on GitHub, runs on Render

4. **Your app will be live at:**
   ```
   https://file-converter-xxxx.onrender.com
   ```

**Benefits:**
- ✅ Free tier forever
- ✅ Auto-deploys from GitHub on every push
- ✅ Supports Python, pandoc, xelatex
- ✅ Automatic HTTPS
- ✅ No credit card required

---

## Alternative: GitHub Pages (UI Demo Only)

If you want to show just the UI on GitHub Pages:

1. **Enable GitHub Pages:**
   - Go to repository Settings
   - Click "Pages" (left sidebar)
   - Source: "GitHub Actions"

2. **Choose workflow:**
   - Use `.github/workflows/github-pages.yml`
   - Pushes to main will auto-deploy

3. **Access demo:**
   ```
   https://parmardarshan29.github.io/file_Converter/
   ```

**⚠️ Warning:** The UI will display but PDF conversion **will not work** (no backend).

---

## Recommended Workflow

**Best practice:** GitHub for code + Render for hosting

```bash
# 1. Make changes locally
git add .
git commit -m "Update feature"

# 2. Push to GitHub
git push origin main

# 3. Render automatically deploys (no extra steps!)
```

Your repository stays on GitHub, but the live app runs on Render with full functionality.

---

## Quick Start

```bash
# Push to GitHub
git add .
git commit -m "Initial deployment"
git push origin main

# Then go to render.com and connect this repo
# That's it! 🎉
```
