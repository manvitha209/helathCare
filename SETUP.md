# 🚀 Complete Setup & Installation Guide

**MedPredict AI** - Professional Disease Risk Assessment Platform

---

## 📋 System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **RAM**: 2 GB minimum
- **Disk Space**: ~500 MB
- **Internet**: Required for first setup (pip install)

### Check Your Python Version
```bash
python --version
```

If you don't have Python, download it from: https://www.python.org/downloads/

---

## ⚡ Quick Start (5 minutes)

### Windows Users
```bash
# 1. Open Command Prompt
cd path\to\health\ care

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train models
python train_models.py

# 5. Start application
python app.py

# 6. Open browser: http://127.0.0.1:5000
```

### macOS/Linux Users
```bash
# 1. Open Terminal
cd path/to/health\ care

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train models
python train_models.py

# 5. Start application
python app.py

# 6. Open browser: http://127.0.0.1:5000
```

---

## 📝 Detailed Setup Instructions

### Step 1: Download/Clone the Project

**Option A: Download ZIP**
1. Download the project as ZIP
2. Extract to a folder
3. Open terminal in that folder

**Option B: Clone with Git**
```bash
git clone <repository-url>
cd health\ care
```

### Step 2: Create Virtual Environment

**Why?** Isolates Python packages for this project only.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

✓ You'll see `(venv)` at the start of your terminal line when activated.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-2.3.3 numpy-1.24.3 pandas-2.0.3 ...
```

### Step 4: Train Machine Learning Models

```bash
python train_models.py
```

**Expected output:**
```
Training Diabetes Model...
[✓] Diabetes Model: 82.5% accuracy
[✓] Diabetes scaler saved

Training Heart Disease Model...
[✓] Heart Model: 84.2% accuracy
[✓] Heart scaler saved

[OK] All models trained successfully!
```

⚠️ **Note**: First run takes 2-5 minutes. This generates the `models/` folder.

### Step 5: Start the Application

```bash
python app.py
```

**Expected output:**
```
==================================================
   MedPredict AI - Disease Risk Prediction
==================================================
  Mode: 🚀 PRODUCTION
  URL:  http://127.0.0.1:5000
  Models: ✓ Ready
==================================================
```

### Step 6: Open in Browser

Visit: **http://127.0.0.1:5000**

✅ You're done! The application is running.

---

## 🔄 Regular Usage (After First Setup)

Once installed, run it anytime with:

**Windows:**
```bash
cd path\to\health\ care
venv\Scripts\activate
python app.py
```

**macOS/Linux:**
```bash
cd path/to/health\ care
source venv/bin/activate
python app.py
```

Then visit: http://127.0.0.1:5000

---

## 🌐 Access from Other Computers (Local Network)

To let other devices on your network access the app:

```bash
python app.py --host 0.0.0.0
```

Then from another computer, visit:
```
http://<your-computer-ip>:5000
```

**Find your IP:**
- **Windows**: `ipconfig` (look for "IPv4 Address")
- **macOS/Linux**: `ifconfig` (look for "inet")

---

## 🐳 Using Docker (Optional)

For production deployment or consistent environments:

### Build Docker Image
```bash
docker build -t medpredict-ai .
```

### Run Container
```bash
docker run -p 5000:5000 medpredict-ai
```

Then visit: http://127.0.0.1:5000

---

## ☁️ Cloud Deployment

### Heroku
```bash
# Install Heroku CLI
# Create Procfile with: web: gunicorn app:app

heroku login
heroku create medpredict-app
git push heroku main
```

### PythonAnywhere
1. Upload files to PythonAnywhere
2. Create web app
3. Configure Python version (3.9+)
4. Point to `app.py`
5. Enable HTTPS

### AWS/Azure/Google Cloud
- Use container services (ECS, App Service, Cloud Run)
- Set up load balancing for scaling
- Configure SSL certificates
- Enable auto-recovery

---

## 🛠️ Development Mode (Optional)

For developers who want debug output:

```bash
python app.py --debug
```

Or set environment variable:
```bash
set FLASK_DEBUG=True          # Windows
export FLASK_DEBUG=True       # macOS/Linux
python app.py
```

Features:
- Automatic code reloading
- Detailed error messages
- Debug toolbar (if enabled)

⚠️ **Never use debug mode in production!**

---

## 🔧 Common Issues & Solutions

### "Python command not found"
```bash
# Use full path or update PATH
# Or use: python3 instead of python
python3 --version
```

### "ModuleNotFoundError: No module named 'flask'"
```bash
# Activate virtual environment first
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Then reinstall
pip install -r requirements.txt
```

### "Port 5000 already in use"
```bash
# Kill the process using the port
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

### "Models not found" error
```bash
# Train models first
python train_models.py

# Wait for completion, then:
python app.py
```

### Application runs but page won't load
```bash
# Check if Flask is running
# Should show: WARNING in production mode

# Try clearing browser cache:
Ctrl+Shift+Delete (Chrome/Edge)
Cmd+Shift+Delete (Safari)

# Or use private/incognito window
```

### Slow predictions (first time)
```
Normal behavior - models load on first prediction (~500ms)
Subsequent predictions <100ms
```

---

## 📦 Project Structure After Setup

```
health-care/
├── venv/                   ← Virtual environment (created)
├── models/                 ← ML models (created by train_models.py)
│   ├── diabetes_model.pkl
│   ├── diabetes_scaler.pkl
│   ├── heart_model.pkl
│   └── heart_scaler.pkl
├── app.py                  ← Backend server
├── train_models.py         ← Model training script
├── index.html              ← Frontend UI
├── requirements.txt        ← Dependencies
├── .gitignore             ← Git config
├── .env.example           ← Environment template
├── README.md              ← Documentation
└── SETUP.md               ← This file
```

---

## 🔒 Production Checklist

Before deploying publicly:

- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use HTTPS/SSL certificates
- [ ] Implement API rate limiting
- [ ] Add input validation
- [ ] Set strong `SECRET_KEY`
- [ ] Configure proper CORS
- [ ] Enable logging
- [ ] Set up monitoring
- [ ] Regular backups of models
- [ ] Update dependencies regularly

---

## 📚 Additional Resources

- [Python Documentation](https://docs.python.org/3/)
- [Flask Guide](https://flask.palletsprojects.com/)
- [Virtual Environment Guide](https://docs.python.org/3/tutorial/venv.html)
- [scikit-learn Docs](https://scikit-learn.org/stable/)

---

## 💬 Getting Help

1. **Check terminal output** - Error messages are usually descriptive
2. **Read README.md** - Has troubleshooting section
3. **Check logs** - `app.log` file contains detailed logs
4. **Verify requirements** - Make sure all prerequisites are installed

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip list` shows Flask, numpy, pandas, etc.)
- [ ] Models trained successfully
- [ ] App runs without errors
- [ ] Browser shows the UI at http://127.0.0.1:5000
- [ ] Can fill form and get predictions

---

**Ready to use!** 🎉

For questions or issues, refer to the README.md file or check application logs.
