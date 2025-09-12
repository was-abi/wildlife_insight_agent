# 🚀 Render Deployment Guide for Wildlife Insight Agent

This guide will help you deploy the Wildlife Insight Agent to Render, a modern cloud platform perfect for Python web applications.

## 🌟 Why Render?

- **Easy Python deployment** with automatic builds
- **Free tier available** for testing and demos
- **Automatic HTTPS** and custom domains
- **Environment variable management** for secure API keys
- **Automatic deployments** from GitHub
- **Better than GitHub Pages** for dynamic applications

## 📋 Prerequisites

1. **GitHub account** with your code repository
2. **Render account** (free at [render.com](https://render.com))
3. **Gemini API key** (optional, app works in demo mode without it)

## 🚀 Quick Deployment Steps

### Step 1: Prepare Your Repository

Make sure your repository contains these files:
- ✅ `app_production.py` - Production-ready Streamlit app
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `Procfile` - Process configuration
- ✅ All supporting files (`streamlit_utils.py`, etc.)

### Step 2: Connect to Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your repository: `wildlife-insight-agent`

### Step 3: Configure the Service

**Basic Settings:**
- **Name**: `wildlife-insight-agent` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run app_production.py --server.port $PORT --server.address 0.0.0.0`

**Advanced Settings:**
- **Auto-Deploy**: `Yes` (deploys automatically on git push)

### Step 4: Environment Variables (Optional)

For full AI functionality, add this environment variable:

| Key | Value |
|-----|-------|
| `GEMINI_API_KEY` | `your_actual_api_key_here` |

**How to add:**
1. In your Render dashboard, go to your service
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Enter `GEMINI_API_KEY` as key and your API key as value

### Step 5: Deploy!

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start your Streamlit app
   - Provide you with a live URL

## 🎯 Deployment Files Explained

### `render.yaml`
```yaml
services:
  - type: web
    name: wildlife-insight-agent
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app_production.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

### `Procfile`
```
web: streamlit run app_production.py --server.port $PORT --server.address 0.0.0.0
```

### `app_production.py`
- Production-ready version of the Streamlit app
- Handles missing API keys gracefully (demo mode)
- Optimized for cloud deployment
- Environment variable support

## 🔧 Configuration Options

### Free Tier Limitations
- **750 hours/month** of runtime (enough for most demos)
- **Sleeps after 15 minutes** of inactivity
- **512MB RAM** (sufficient for this app)

### Paid Tier Benefits ($7/month)
- **Always-on** service (no sleeping)
- **More resources** for faster performance
- **Custom domains** support

## 🌐 Your Live App

Once deployed, you'll get a URL like:
```
https://wildlife-insight-agent.onrender.com
```

## 🔄 Automatic Updates

Every time you push to your GitHub repository:
1. Render automatically detects changes
2. Rebuilds your application
3. Deploys the new version
4. Your live app updates automatically!

## 🐛 Troubleshooting

### Common Issues

**1. Build Fails**
- Check `requirements.txt` for correct package versions
- Ensure all files are committed to GitHub
- Check build logs in Render dashboard

**2. App Won't Start**
- Verify `app_production.py` exists
- Check start command in Render settings
- Review application logs

**3. Import Errors**
- Ensure all dependencies are in `requirements.txt`
- Check Python version compatibility

### Debug Commands

View logs in Render dashboard:
- **Build logs**: Shows installation process
- **Deploy logs**: Shows startup process
- **Service logs**: Shows runtime errors

## 🎨 Customization

### Custom Domain
1. Go to your service settings
2. Click **"Custom Domains"**
3. Add your domain (requires paid plan)

### Environment Variables
Add any of these for customization:
- `STREAMLIT_THEME_PRIMARY_COLOR` - Change primary color
- `STREAMLIT_SERVER_PORT` - Custom port (usually not needed)
- `PYTHON_VERSION` - Specify Python version

## 📊 Monitoring

Render provides:
- **Uptime monitoring** - Track service availability
- **Resource usage** - Monitor CPU and memory
- **Request metrics** - See traffic patterns
- **Error tracking** - Catch and debug issues

## 🚀 Going Live Checklist

- [ ] Repository is public or Render has access
- [ ] All files are committed and pushed
- [ ] `requirements.txt` is complete
- [ ] `app_production.py` runs locally
- [ ] Environment variables are set (if needed)
- [ ] Service is created in Render
- [ ] Deployment is successful
- [ ] App loads at the provided URL
- [ ] All features work as expected

## 🎉 Success!

Your Wildlife Insight Agent is now live on the internet! 🌍

**Share your app:**
- Send the Render URL to friends and colleagues
- Add it to your portfolio or resume
- Use it for educational demonstrations
- Showcase your AI and web development skills

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [Python on Render](https://render.com/docs/deploy-python)

---

🌟 **Your Wildlife Insight Agent is ready to explore the world's biodiversity data!** 🌟