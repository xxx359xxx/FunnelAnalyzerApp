# GitHub Upload Instructions

Since GitHub CLI is not installed, follow these steps to upload your project to GitHub:

## Step 1: Create a New Repository on GitHub

1. Go to [GitHub.com](https://github.com) and sign in to your account
2. Click the "+" button in the top right corner
3. Select "New repository"
4. Fill in the repository details:
   - **Repository name**: `gambling-funnel-analysis`
   - **Description**: `A comprehensive tool for analyzing gambling conversion funnels with interactive Streamlit interface and PDF report generation`
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 2: Connect Your Local Repository

After creating the repository, GitHub will show you commands. Use these in your terminal:

```bash
# Add the remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/gambling-funnel-analysis.git

# Rename the default branch to main (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

## Step 3: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. The README.md will be displayed automatically

## Your Repository is Ready!

Your repository will contain:
- ✅ Streamlit web application (`app.py`)
- ✅ Core analysis functions (`utils.py`)
- ✅ Font system with DejaVu fonts
- ✅ PDF report generation
- ✅ Test files and utilities
- ✅ Comprehensive English documentation
- ✅ Requirements file for easy installation

## Repository Features

### 🎯 What's Included:
- **Interactive Dashboard**: Streamlit web interface
- **Funnel Analysis**: Registration → Deposit → First Bet → Second Deposit
- **PDF Reports**: Professional English reports
- **Segment Analysis**: Traffic source, country, device breakdowns
- **Font System**: Proper Unicode support for international text
- **Test Suite**: Comprehensive testing utilities

### 📊 Ready for Use:
- Clone and run with `pip install -r requirements.txt`
- Start with `streamlit run app.py`
- Upload CSV data and generate reports
- Professional PDF output in English

## Alternative: Using Git Commands

If you prefer command line, here are the exact commands to run in your terminal:

```bash
# Navigate to your project directory
cd "F:\Учебка\Учусь\Gambling Analyze\RealData"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/gambling-funnel-analysis.git

# Push to GitHub
git push -u origin master
```

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username in the commands above.

---

**Your gambling funnel analysis tool is now ready to be shared on GitHub! 🚀**