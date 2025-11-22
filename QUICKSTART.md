# 🚀 Quick Start Guide - Booking.com Automation Framework

## Prerequisites Check
- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] Chrome/Firefox/Edge browser installed

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Installation
```bash
python --version
pytest --version
```

## Running Tests

### Quick Test Run (Smoke Tests Only)
```bash
pytest tests/ -m smoke -v
```

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
# Search tests
pytest tests/test_search.py -v

# Filter tests
pytest tests/test_filters.py -v

# Hotel details tests
pytest tests/test_hotel_details.py -v
```

### Run with Different Browsers
```bash
# Chrome (default)
pytest tests/ --browser=chrome -v

# Firefox
pytest tests/ --browser=firefox -v

# Edge
pytest tests/ --browser=edge -v
```

### Run in Headless Mode (No Browser Window)
```bash
pytest tests/ --headless=true -v
```

### Run Tests in Parallel (Faster)
```bash
pytest tests/ -n 3 -v
```

## Generate Allure Report

### Step 1: Run Tests with Allure
```bash
pytest tests/ --alluredir=reports/allure-results
```

### Step 2: View Report
```bash
allure serve reports/allure-results
```

> **Note**: Requires Allure CLI to be installed. See README.md for installation instructions.

## Git Setup

### Initialize Git Repository
```bash
# Run the initialization script
.\init_git.ps1

# Or manually:
git init
git add .
git commit -m "Initial commit"
```

### Push to Remote Repository
```bash
git remote add origin <your-repo-url>
git push -u origin main
```

## Azure DevOps CI/CD Setup

1. Create new pipeline in Azure DevOps
2. Select your repository
3. Use existing YAML: `azure-pipelines.yml`
4. Run pipeline
5. View results in "Tests" tab
6. Download Allure report from "Artifacts"

## Common Commands Reference

| Command | Description |
|---------|-------------|
| `pytest tests/ -v` | Run all tests with verbose output |
| `pytest tests/ -m smoke` | Run only smoke tests |
| `pytest tests/ -k search` | Run tests matching "search" |
| `pytest tests/ --browser=firefox` | Run with Firefox |
| `pytest tests/ --headless=true` | Run in headless mode |
| `pytest tests/ -n 3` | Run with 3 parallel workers |
| `pytest tests/ --lf` | Run last failed tests |
| `pytest tests/ --tb=short` | Short traceback format |

## Project Structure Quick Reference

```
booking-automation-framework/
├── config/          # Configuration and test data
├── pages/           # Page Object Models
├── tests/           # Test cases
├── utils/           # Utilities (logger, helpers, etc.)
├── reports/         # Generated reports
├── logs/            # Execution logs
└── screenshots/     # Failure screenshots
```

## Test Markers

| Marker | Description | Count |
|--------|-------------|-------|
| `smoke` | Critical smoke tests | 5 |
| `regression` | Full regression suite | 8 |
| `sanity` | Sanity tests | 3 |
| `search` | Search functionality | 5 |
| `filters` | Filters and sorting | 5 |
| `hotel` | Hotel details | 5 |

## Troubleshooting

### Issue: WebDriver not found
**Solution**: The framework uses webdriver-manager which auto-downloads drivers. Ensure internet connection.

### Issue: Tests timeout
**Solution**: Increase timeout in `config/config.py`:
```python
EXPLICIT_WAIT = 30
```

### Issue: Element not found
**Solution**: Website may have changed. Update locators in page objects.

## Need Help?

- 📖 Full documentation: [README.md](README.md)
- 🔍 Implementation details: See walkthrough.md in artifacts
- 💡 Code examples: Check existing test files in `tests/`

## Next Steps

1. ✅ Run smoke tests to verify setup
2. ✅ Explore test files to understand structure
3. ✅ Generate Allure report to see reporting
4. ✅ Set up Git repository
5. ✅ Configure Azure DevOps pipeline
6. ✅ Start adding your own tests!

---

**Happy Testing! 🎉**
