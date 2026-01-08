# Deployment Guide

## Option 1: Deploy to Render (Recommended - Free Tier Available)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account
   - Click "New +" → "Web Service"
   - Connect your `file_Converter` repository
   - Render will auto-detect the `render.yaml` file
   - Click "Create Web Service"
   - Wait for deployment (includes pandoc and xelatex installation)

3. **Access your app**
   - Your app will be live at: `https://your-app-name.onrender.com`

---

## Option 2: Deploy to Railway

1. **Push to GitHub** (same as above)

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variables if needed
   - Railway will build and deploy automatically

3. **Add build configuration**
   - Railway will detect Python automatically
   - Build command: `pip install -r requirements.txt && apt-get update && apt-get install -y pandoc texlive-xetex`
   - Start command: `python app.py`

---

## Option 3: GitHub Pages (Static Demo Only - No Backend)

**⚠️ Note:** GitHub Pages can only show the UI. PDF conversion won't work without a backend.

1. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Settings → Pages
   - Source: "GitHub Actions"
   - The workflow in `.github/workflows/deploy.yml` will auto-deploy

2. **Access demo**
   - Live at: `https://parmardarshan29.github.io/file_Converter/`

---

## Option 4: Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and create app**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Add buildpacks**
   ```bash
   heroku buildpacks:add --index 1 heroku/python
   heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-apt
   ```

4. **Create `Aptfile` for system dependencies**
   ```bash
   echo "pandoc" > Aptfile
   echo "texlive-xetex" >> Aptfile
   echo "texlive-fonts-recommended" >> Aptfile
   ```

5. **Deploy**
   ```bash
   git push heroku main
   heroku open
   ```

---

## Recommended: Render or Railway
- **Free tier available**
- **Automatic HTTPS**
- **Easy GitHub integration**
- **Supports system packages (pandoc, xelatex)**

Both platforms are perfect for Python/Flask apps and will handle your PDF conversion backend seamlessly.
