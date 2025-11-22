# Git Initialization Script
# Run this script to initialize Git repository and make first commit

# Initialize Git repository
Write-Host "Initializing Git repository..." -ForegroundColor Green
git init

# Add all files
Write-Host "Adding files to Git..." -ForegroundColor Green
git add .

# Create initial commit
Write-Host "Creating initial commit..." -ForegroundColor Green
git commit -m "Initial commit: Booking.com automation framework

- Complete framework structure with POM pattern
- Configuration and utilities modules
- Page objects for Home, Search Results, and Hotel Details
- Comprehensive test suite with 13+ test cases
- Allure reporting integration
- Azure DevOps CI/CD pipeline
- Comprehensive logging and error handling
- README with detailed documentation"

Write-Host "`nGit repository initialized successfully!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create a remote repository (GitHub, Azure DevOps, etc.)"
Write-Host "2. Add remote: git remote add origin <repository-url>"
Write-Host "3. Push to remote: git push -u origin main"
