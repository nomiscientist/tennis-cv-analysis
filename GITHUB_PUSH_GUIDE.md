# 🚀 Complete Step-by-Step Guide: Pushing Project Updates to GitHub

This guide covers both **Daily Code Updates** and **Setting Up on a New Machine**.

---

## ⚡ Daily Workflow (Pushing Future Updates to GitHub)

Whenever you make changes to your code, dashboard, or documentation, run these 3 simple commands in your terminal:

### Command 1: Stage All Your Changes
```powershell
git add .
```

### Command 2: Commit Your Changes
```powershell
git commit -m "Updated interactive dashboard metrics and documentation"
```

### Command 3: Push to GitHub
```powershell
git push origin main
```

---

## 🛠️ Complete Setup Workflow (If Setting Up on a New Computer)

If you clone or set up this repository on a new machine, follow these steps:

### Step 1: Open PowerShell in Project Directory
```powershell
cd c:\Users\PULKIT\OneDrive\Desktop\tennis\tennis_analysis
```

### Step 2: Initialize Git & Set Remote URL
```powershell
git init
git branch -M main
git remote add origin https://github.com/pulkit-patel/tennis-cv-analysis.git
```

### Step 3: Stage, Commit & Push
```powershell
git add .
git commit -m "Initial commit: Tennis CV Computer Vision pipeline, interactive web dashboard, analytics engine, and placement guides"
git push -u origin main --force
```

---

## 📌 Important Notes & Troubleshooting

1. **Large Files Limit (>100MB)**:
   GitHub rejects individual files larger than 100MB. Our `.gitignore` automatically excludes large binary models (`yolov8x.pt`, `models/*.pt`, `models/*.pth`) and raw long video files (`input_videos/australia_open.mp4`).

2. **Model Download Links**:
   Anyone cloning your repository can easily download pretrained weights using the download links provided in `README.md` or by running:
   ```powershell
   python download_models.py
   ```

3. **Check What Will Be Pushed**:
   To see modified or untracked files before committing:
   ```powershell
   git status
   ```
