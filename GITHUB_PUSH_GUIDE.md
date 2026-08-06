# 🚀 Step-by-Step Guide: Pushing Project to GitHub

Follow these simple steps to create a new GitHub repository and push your project:

---

### Step 1: Create a New Repository on GitHub
1. Open your browser and go to: **[github.com/new](https://github.com/new)**
2. Enter Repository Name: **`tennis-cv-analysis`** (or `tennis_analysis`).
3. Set Visibility: **Public**.
4. Leave **"Add a README file"**, **"Add .gitignore"**, and **"Choose a license"** UNCHECKED (since we already created them).
5. Click **Create repository**.

---

### Step 2: Set Your New GitHub Remote URL
Open your terminal (PowerShell / Command Prompt) in `c:\Users\PULKIT\OneDrive\Desktop\tennis\tennis_analysis` and run:

```bash
# Change remote URL to your new repository (replace YOUR_USERNAME with your GitHub username)
git remote set-url origin https://github.com/YOUR_USERNAME/tennis-cv-analysis.git
```

---

### Step 3: Stage All Project Files & Commit
Run the following commands in your terminal:

```bash
# Stage all new and modified files
git add .

# Commit changes with a professional message
git commit -m "Add Tennis CV Pipeline, Interactive Web Dashboard, Placement Viva Guide, and Documentation"
```

---

### Step 4: Push to GitHub
```bash
# Push your code to your GitHub repository
git push -u origin main
```

---

### 🛠️ Troubleshooting & Notes:
- **Large Files (>100MB)**: Our `.gitignore` automatically excludes `yolov8x.pt` and `australia_open.mp4` so `git push` will succeed instantly without hitting single-file size limits.
- **Model Weights Link**: The `README.md` already includes model download links for `yolov8x.pt` and `keypoints_model.pth`.
