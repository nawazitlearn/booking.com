# Troubleshooting Guide - ChromeDriver Architecture Issue

## Issue
`OSError: [WinError 193] %1 is not a valid Win32 application`

This error occurs when webdriver-manager downloads the 32-bit (win32) ChromeDriver on a 64-bit system.

## Quick Fix Option 1: Clear Cache and Retry

```powershell
# Clear the ChromeDriver cache
Remove-Item -Path "$env:USERPROFILE\.wdm" -Recurse -Force

# Run tests again
pytest tests/ -m smoke -v
```

## Quick Fix Option 2: Manual ChromeDriver Download

1. **Download ChromeDriver manually**:
   - Go to: https://googlechromelabs.github.io/chrome-for-testing/
   - Download the **win64** version matching your Chrome version
   - Extract `chromedriver.exe`

2. **Place in PATH or specify location**:
   ```powershell
   # Option A: Add to PATH
   # Place chromedriver.exe in C:\Windows\System32 or add its folder to PATH
   
   # Option B: Update config.py to use specific path
   # Add this to config/config.py:
   CHROMEDRIVER_PATH = r"C:\path\to\chromedriver.exe"
   ```

3. **Update driver_factory.py**:
   ```python
   # In _create_chrome_driver method, replace:
   service = ChromeService(ChromeDriverManager().install())
   
   # With:
   from config.config import Config
   if hasattr(Config, 'CHROMEDRIVER_PATH'):
       service = ChromeService(Config.CHROMEDRIVER_PATH)
   else:
       service = ChromeService(ChromeDriverManager().install())
   ```

## Quick Fix Option 3: Use Firefox Instead

```powershell
# Run with Firefox (no architecture issues)
pytest tests/ -m smoke --browser=firefox -v
```

## Quick Fix Option 4: Update webdriver-manager

```powershell
# Upgrade to latest version
pip install --upgrade webdriver-manager

# Clear cache
Remove-Item -Path "$env:USERPROFILE\.wdm" -Recurse -Force

# Run tests
pytest tests/ -m smoke -v
```

## Permanent Solution

The framework code has been updated to detect and handle this issue automatically. If the problem persists:

1. Delete the `.wdm` folder in your user directory
2. Update webdriver-manager: `pip install --upgrade webdriver-manager`
3. Run tests again

## Alternative: Use Selenium Manager (Selenium 4.6+)

Selenium 4.6+ includes built-in driver management. To use it:

1. **Remove webdriver-manager** from driver_factory.py
2. **Simplify the code**:
   ```python
   # Just create the driver - Selenium will handle the rest
   driver = webdriver.Chrome(options=options)
   ```

This is the most reliable solution for Selenium 4.x.
