# CI/CD Setup Guide

This document explains the CI/CD pipelines configured for the Booking.com Automation Framework.

## 🚀 Overview

The project uses **GitHub Actions** for continuous integration and deployment, providing automated testing, reporting, and deployment to GitHub Pages.

---

## 📋 GitHub Actions Workflows

### 1. **Main CI/CD Pipeline** (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual trigger via GitHub UI

**What it does:**
- ✅ Runs all tests with Pytest
- 📊 Generates Allure reports
- 🌐 Publishes reports to GitHub Pages
- 📦 Uploads test results, screenshots, and logs as artifacts

**Allure Report URL:**
```
https://<your-username>.github.io/booking.com/
```

### 2. **Scheduled Tests** (`scheduled.yml`)

**Triggers:**
- Daily at 9:00 AM UTC (2:30 PM IST)
- Manual trigger via GitHub UI

**What it does:**
- 🔄 Runs full test suite automatically
- 📈 Keeps test reports up-to-date
- 🔔 Helps catch issues early

---

## 🔧 Setup Instructions

### GitHub Actions (Recommended)

#### Step 1: Enable GitHub Pages

1. Go to your repository: `https://github.com/nawazitlearn/booking.com`
2. Click **Settings** → **Pages**
3. Under **Source**, select:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
4. Click **Save**

#### Step 2: Push the Workflows

The workflows are already created in `.github/workflows/`. Just push them:

```bash
cd f:/itdunia/antigravity/testing_projects/booking-automation-framework
git add .github/
git commit -m "Add GitHub Actions CI/CD workflows"
git push origin main
```

#### Step 3: Monitor Workflow Runs

1. Go to **Actions** tab in your GitHub repository
2. You'll see workflow runs automatically triggered
3. Click on any run to see detailed logs

#### Step 4: View Allure Reports

After the first successful run:
- Reports will be available at: `https://nawazitlearn.github.io/booking.com/`

---

## 📊 Viewing Results

### GitHub Actions

**Test Results:**
- Go to **Actions** tab → Select workflow run
- View test summary in the run details
- Download artifacts (screenshots, logs) from the run page

**Allure Reports:**
- Visit: `https://nawazitlearn.github.io/booking.com/`
- Interactive HTML report with:
  - Test execution timeline
  - Test case details
  - Screenshots on failures
  - Trend graphs


---

## 🔄 Workflow Features

### Automatic Triggers

| Event | Workflow | Description |
|-------|----------|-------------|
| Push to main/develop | CI/CD Pipeline | Runs all tests |
| Pull Request | CI/CD Pipeline | Validates changes |
| Daily at 9 AM UTC | Scheduled Tests | Proactive monitoring |
| Manual | Both | On-demand execution |

### Artifacts Generated

| Artifact | Contents | Retention |
|----------|----------|-----------|
| test-results | JUnit XML reports | 30 days |
| screenshots | Failure screenshots | 30 days |
| logs | Test execution logs | 30 days |
| allure-report | HTML report | Permanent (GitHub Pages) |

---

## 🛠️ Configuration

### Environment Variables

Both pipelines use these variables:

```yaml
PYTHON_VERSION: '3.11'
BROWSER: chrome
HEADLESS: true
```

### Customization

**Change test schedule:**
Edit `.github/workflows/scheduled.yml`:
```yaml
schedule:
  - cron: '0 9 * * *'  # Change time here
```

**Add email notifications:**
Add to workflow steps:
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: Test Results
    body: Check the results!
```

---

## 🐛 Troubleshooting

### Workflow Fails

1. Check **Actions** tab for error logs
2. Common issues:
   - Missing dependencies → Check `requirements.txt`
   - Browser issues → Verify ChromeDriver compatibility
   - Test failures → Review test logs and screenshots

### Allure Report Not Showing

1. Verify GitHub Pages is enabled
2. Check if `gh-pages` branch exists
3. Wait 2-3 minutes after first deployment
4. Clear browser cache

### Scheduled Tests Not Running

1. Verify workflow file is in `main` branch
2. Check **Actions** tab → **Workflows** → Enable if disabled
3. GitHub may disable scheduled workflows after 60 days of inactivity

---

## 📈 Best Practices

1. **Review test results regularly** - Check the Allure reports
2. **Keep dependencies updated** - Update `requirements.txt` periodically
3. **Monitor scheduled runs** - Ensure daily tests are passing
4. **Use pull requests** - Validate changes before merging to main
5. **Archive old reports** - GitHub Pages keeps last 20 reports

---

## 🔗 Useful Links

- **Repository:** https://github.com/nawazitlearn/booking.com
- **Actions:** https://github.com/nawazitlearn/booking.com/actions
- **Allure Reports:** https://nawazitlearn.github.io/booking.com/
- **GitHub Pages Docs:** https://docs.github.com/en/pages
- **GitHub Actions Docs:** https://docs.github.com/en/actions

---

## 📞 Support

For issues or questions:
1. Check workflow logs in Actions tab
2. Review this documentation
3. Consult `TROUBLESHOOTING.md` in the repository
