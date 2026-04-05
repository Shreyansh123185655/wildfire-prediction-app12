# WildFire Prediction App - Vercel Deployment

## 🚀 Deploy to Vercel

### Prerequisites
- Vercel account (free)
- GitHub account
- Git installed

### Step-by-Step Deployment

#### 1. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit - Wildfire Prediction App"
```

#### 2. Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `wildfire-prediction-app`
3. Don't initialize with README (we already have files)

#### 3. Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/wildfire-prediction-app.git
git branch -M main
git push -u origin main
```

#### 4. Deploy to Vercel
1. Go to [Vercel](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect it's a Python project
5. Configure settings:
   - **Framework Preset**: Python
   - **Root Directory**: ./
   - **Build Command**: `pip install -r requirements-vercel.txt`
   - **Output Directory**: ./
   - **Install Command**: `pip install -r requirements-vercel.txt`

#### 5. Environment Variables (if needed)
No additional environment variables required for this deployment.

#### 6. Deploy
Click "Deploy" and wait for the deployment to complete.

### 🌐 Access Your App
Once deployed, your app will be available at:
`https://your-project-name.vercel.app`

### 📱 Features
- **Responsive Design**: Works on mobile and desktop
- **Real-time Predictions**: Instant wildfire risk assessment
- **Interactive Interface**: Easy-to-use form with validation
- **Probability Scores**: Detailed risk percentages

### 🔧 Technical Details
- **Backend**: Python with scikit-learn model
- **Frontend**: HTML/CSS/JavaScript (no Streamlit on Vercel)
- **API**: RESTful endpoint for predictions
- **Model**: Pre-trained RandomForest classifier

### 🐛 Troubleshooting

#### Common Issues:
1. **Model Loading Error**: Ensure `wildfire_risk_model.pkl` is in the `notebooks/` directory
2. **Import Errors**: Check that all dependencies are in `requirements-vercel.txt`
3. **Build Failures**: Verify Python version compatibility (Python 3.9+)

#### Debug Steps:
1. Check Vercel deployment logs
2. Verify file paths in `api/index.py`
3. Test locally with `python api/index.py`

### 🔄 Updates
To update your app:
1. Make changes locally
2. Commit and push to GitHub
3. Vercel will automatically redeploy

### 📊 Monitoring
- Check Vercel Analytics for usage stats
- Monitor Vercel Logs for errors
- Set up Vercel Alerts for downtime

### 💡 Alternative Deployment Options
If Vercel doesn't work well, consider:
- **Heroku**: Better for Python apps
- **Railway**: Similar to Vercel but Python-friendly
- **Streamlit Cloud**: Native Streamlit hosting
- **AWS/GCP**: For production scaling

### 🎯 Success Criteria
✅ App loads without errors  
✅ Model predictions work correctly  
✅ Responsive design on mobile  
✅ Fast loading times (<3 seconds)  
✅ Error handling for invalid inputs  

---

**Happy Deploying! 🚀**
