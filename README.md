# Booking.com Test Automation Framework

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.26+-green.svg)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-8.3+-orange.svg)](https://pytest.org/)
[![Allure](https://img.shields.io/badge/Allure-2.13+-yellow.svg)](https://docs.qameta.io/allure/)

An industry-level test automation framework for [Booking.com](https://www.booking.com) built with Python, Selenium, Pytest, and Allure reporting. The framework follows the Page Object Model (POM) design pattern and includes comprehensive logging, error handling, and CI/CD integration with GitHub Actions.

## 🚀 Features

- ✅ **Page Object Model (POM)** - Clean separation of test logic and page interactions
- ✅ **Multi-Browser Support** - Chrome, Firefox, and Edge
- ✅ **Headless Execution** - Run tests in headless mode for CI/CD
- ✅ **Allure Reporting** - Beautiful and detailed test reports
- ✅ **Comprehensive Logging** - Rotating file logs with multiple log levels
- ✅ **Screenshot on Failure** - Automatic screenshot capture for failed tests
- ✅ **Custom Decorators** - Retry logic, logging, and error handling
- ✅ **Test Data Management** - JSON-based test data configuration
- ✅ **GitHub Actions CI/CD** - Automated testing with GitHub Actions
- ✅ **Parallel Execution** - Run tests in parallel with pytest-xdist
- ✅ **Industry-Standard Code** - Follows PEP 8 and best practices

## 📁 Project Structure

```
booking-automation-framework/
├── config/                     # Configuration files
│   ├── config.py              # Central configuration
│   └── test_data.json         # Test data
├── pages/                      # Page Object Models
│   ├── base_page.py           # Base page with common methods
│   ├── home_page.py           # Homepage page object
│   ├── search_results_page.py # Search results page object
│   └── hotel_details_page.py  # Hotel details page object
├── tests/                      # Test cases
│   ├── conftest.py            # Pytest fixtures and configuration
│   ├── test_search.py         # Search functionality tests
│   ├── test_filters.py        # Filter and sorting tests
│   └── test_hotel_details.py # Hotel details tests
├── utils/                      # Utility modules
│   ├── driver_factory.py      # WebDriver factory
│   ├── logger.py              # Logging configuration
│   ├── helpers.py             # Helper utilities
│   └── decorators.py          # Custom decorators
├── reports/                    # Test reports (generated)
├── logs/                       # Log files (generated)
├── screenshots/                # Screenshots (generated)
├── .github/workflows/ci.yml    # GitHub Actions CI/CD pipeline
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

## 🛠️ Prerequisites

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Chrome/Firefox/Edge** - At least one browser installed
- **pip** - Python package manager (comes with Python)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd booking-automation-framework
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🏃 Running Tests Locally

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_search.py -v
```

### Run Tests with Specific Browser

```bash
# Chrome (default)
pytest tests/ --browser=chrome

# Firefox
pytest tests/ --browser=firefox

# Edge
pytest tests/ --browser=edge
```

### Run Tests in Headless Mode

```bash
pytest tests/ --headless=true
```

### Run Tests with Markers

```bash
# Run only smoke tests
pytest tests/ -m smoke

# Run only search tests
pytest tests/ -m search

# Run regression tests
pytest tests/ -m regression
```

### Run Tests in Parallel

```bash
# Run with 3 workers
pytest tests/ -n 3
```

### Generate Allure Report

```bash
# Run tests and generate Allure results
pytest tests/ --alluredir=reports/allure-results

# Serve Allure report (requires Allure CLI)
allure serve reports/allure-results
```

## 📊 Viewing Reports

### Allure Report

1. **Install Allure CLI** (if not already installed):

   **Windows (using Scoop):**
   ```bash
   scoop install allure
   ```

   **Mac (using Homebrew):**
   ```bash
   brew install allure
   ```

   **Linux:**
   ```bash
   wget https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz
   tar -zxvf allure-2.24.1.tgz
   sudo mv allure-2.24.1 /opt/allure
   sudo ln -s /opt/allure/bin/allure /usr/bin/allure
   ```

2. **Generate and View Report:**
   ```bash
   allure serve reports/allure-results
   ```

### Logs

Logs are stored in the `logs/` directory with timestamps. View them with any text editor:

```bash
# View latest log
cat logs/automation_<date>.log
```

### Screenshots

Screenshots for failed tests are saved in the `screenshots/` directory with test names and timestamps.

## 🔧 Configuration

### Browser Configuration

Edit `config/config.py` to change default settings:

```python
BROWSER = "chrome"  # chrome, firefox, edge
HEADLESS = False    # True for headless mode
```

### Timeout Configuration

```python
IMPLICIT_WAIT = 10      # Implicit wait in seconds
EXPLICIT_WAIT = 20      # Explicit wait in seconds
PAGE_LOAD_TIMEOUT = 30  # Page load timeout in seconds
```

### Test Data

Edit `config/test_data.json` to add or modify test data:

```json
{
  "destinations": ["London", "Paris", "Dubai"],
  "search_scenarios": [
    {
      "destination": "London",
      "adults": 2,
      "children": 0,
      "rooms": 1
    }
  ]
}
```

## 🚀 CI/CD with GitHub Actions

### Automatic Testing

The framework includes a GitHub Actions workflow that automatically:
- Runs on push to `main` and `develop` branches
- Executes all tests in headless Chrome
- Generates and publishes Allure reports to GitHub Pages
- Uploads test results, screenshots, and logs as artifacts

### Manual Trigger

1. Go to **Actions** tab in your GitHub repository
2. Select **CI/CD Pipeline** workflow
3. Click **Run workflow** button
4. Select branch and click **Run workflow**

### View Results

1. **Test Results**: Navigate to **Actions** → Select workflow run → View summary
2. **Allure Report**: Visit `https://<username>.github.io/<repository-name>/`
3. **Artifacts**: Download from workflow run page (test-results, screenshots, logs)

**Note**: Enable GitHub Pages in repository settings (Settings → Pages → Source: gh-pages branch) to view Allure reports online.

## 📝 Writing New Tests

### 1. Create Test File

Create a new file in `tests/` directory (e.g., `test_new_feature.py`):

```python
import pytest
import allure
from pages.home_page import HomePage

@allure.feature("New Feature")
class TestNewFeature:
    
    @pytest.mark.smoke
    def test_new_functionality(self, home_page):
        # Your test code here
        pass
```

### 2. Create Page Object (if needed)

Create a new page object in `pages/` directory:

```python
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class NewPage(BasePage):
    
    # Locators
    ELEMENT = (By.ID, "element-id")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def perform_action(self):
        self.click(self.ELEMENT)
```

## 🧪 Test Markers

Available pytest markers:

- `@pytest.mark.smoke` - Critical smoke tests
- `@pytest.mark.regression` - Full regression suite
- `@pytest.mark.sanity` - Sanity tests
- `@pytest.mark.search` - Search functionality tests
- `@pytest.mark.filters` - Filter and sorting tests
- `@pytest.mark.hotel` - Hotel details tests

## 🐛 Troubleshooting

### Issue: WebDriver not found

**Solution:** The framework uses Selenium Manager (built-in to Selenium 4.6+) which automatically downloads and manages browser drivers. Ensure you have an internet connection on the first run.

### Issue: Browser driver issues

**Solution:** Selenium Manager handles all driver management automatically. If you encounter issues:
1. Ensure your browser (Chrome/Firefox/Edge) is up to date
2. Check your internet connection
3. Clear Selenium cache if needed: `Remove-Item -Path "$env:USERPROFILE\.cache\selenium" -Recurse -Force`

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more details.

### Issue: Tests fail with timeout

**Solution:** Increase timeout values in `config/config.py`:
```python
EXPLICIT_WAIT = 30  # Increase to 30 seconds
```

### Issue: Element not found

**Solution:** Check if locators in page objects are up-to-date with the current Booking.com website.

### Issue: Allure command not found

**Solution:** Install Allure CLI following the instructions in the "Viewing Reports" section.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is for educational and testing purposes only.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Selenium WebDriver community
- Pytest framework
- Allure reporting framework
- Booking.com (test target)

---

**Note:** This framework is designed for testing purposes only. Always respect the website's terms of service and robots.txt when running automated tests.
#   C I / C D   A c t i v e 
 
 