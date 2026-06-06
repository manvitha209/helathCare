# 🎯 Quick Reference Card

**MedPredict AI** - Essential Commands & Links

---

## ⚡ Quick Start Commands

### Windows
```bash
cd path\to\health\ care
venv\Scripts\activate
python -r requirements.txt
python train_models.py
python app.py
```

### macOS/Linux
```bash
cd path/to/health\ care
source venv/bin/activate
pip install -r requirements.txt
python train_models.py
python app.py
```

---

## 🌐 Important URLs

| Purpose | URL |
|---------|-----|
| Application | http://127.0.0.1:5000 |
| Health Check | http://127.0.0.1:5000/health |
| Diabetes API | POST http://127.0.0.1:5000/predict/diabetes |
| Heart API | POST http://127.0.0.1:5000/predict/heart |

---

## 📋 API Quick Reference

### Test API Health
```bash
curl http://127.0.0.1:5000/health
```

### Test Diabetes Prediction
```bash
curl -X POST http://127.0.0.1:5000/predict/diabetes \
  -H "Content-Type: application/json" \
  -d '{"pregnancies":1,"glucose":120,"bloodPressure":70,"skinThickness":23,"insulin":79,"bmi":28.0,"diabetesPedigreeFunction":0.47,"age":33}'
```

### Test Heart Prediction
```bash
curl -X POST http://127.0.0.1:5000/predict/heart \
  -H "Content-Type: application/json" \
  -d '{"age":50,"sex":1,"cp":1,"trestbps":130,"chol":246,"fbs":0,"restecg":1,"thalach":150,"exang":0,"oldpeak":1.0,"slope":1,"ca":0,"thal":2}'
```

---

## 🔧 Common Troubleshooting

| Problem | Solution |
|---------|----------|
| Python not found | Use `python3` instead of `python` |
| Module not found | Activate venv: `source venv/bin/activate` |
| Port in use | `lsof -i :5000` then `kill -9 <PID>` |
| Models not found | Run: `python train_models.py` |
| No module flask | `pip install -r requirements.txt` |

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Full documentation |
| SETUP.md | Installation guide |
| USER_GUIDE.md | How to use the app |
| .env.example | Configuration template |

---

## 🚀 Deployment Quick Links

- **Docker**: `docker build -t medpredict . && docker run -p 5000:5000 medpredict`
- **Heroku**: `heroku create && git push heroku main`
- **Network**: `python app.py --host 0.0.0.0`
- **Debug Mode**: `python app.py --debug`

---

## 🎯 Risk Level Quick Guide

| Score | Level | Action |
|-------|-------|--------|
| 0-20% | Very Low ✅ | Continue good habits |
| 20-40% | Low 🟢 | Minor adjustments |
| 40-60% | Moderate ⚠️ | More attention needed |
| 60-80% | High 🔶 | See doctor soon |
| 80-100% | Very High 🚨 | Urgent medical attention |

---

## 📱 Mobile Access

```
From any device on local network:
http://<your-computer-ip>:5000
```

**Find your IP:**
- Windows: `ipconfig` 
- Mac/Linux: `ifconfig`

---

## 💾 File Backups

```bash
# Backup models
cp -r models/ models_backup/

# Backup logs
cp app.log app.log.backup
```

---

## 🔐 Production Checklist

- [ ] Set FLASK_ENV=production
- [ ] Set FLASK_DEBUG=False
- [ ] Configure HTTPS
- [ ] Set SECRET_KEY
- [ ] Review CORS settings
- [ ] Enable logging
- [ ] Test error handlers
- [ ] Backup models regularly
- [ ] Update dependencies

---

## 📞 Emergency Commands

**Kill stuck process:**
```bash
# Windows
taskkill /PID <PID> /F

# Mac/Linux
kill -9 <PID>
```

**Reset everything:**
```bash
deactivate
rm -rf venv/
python -m venv venv
pip install -r requirements.txt
```

**Clear logs:**
```bash
rm app.log
```

---

## 🎓 Learning Paths

### New User Path
1. Read README.md (overview)
2. Follow SETUP.md (installation)
3. Read USER_GUIDE.md (usage)
4. Try the app

### Developer Path
1. Review app.py structure
2. Check API endpoints
3. Run with --debug mode
4. Test APIs with curl
5. Review requirements.txt

### DevOps Path
1. Read Deployment section in README
2. Review production checklist
3. Set up Docker
4. Choose cloud platform
5. Configure monitoring

---

## 🔗 External Resources

- Python: https://python.org
- Flask: https://flask.palletsprojects.com
- scikit-learn: https://scikit-learn.org
- Docker: https://docker.com

---

**Print this card for quick reference!**

Version: 1.0.0 | Status: Production Ready | Updated: June 2026
