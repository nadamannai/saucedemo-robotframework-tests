# Robot Framework Test Automation

A Robot Framework test automation project for web application testing with custom libraries and keyword-driven test cases.

## Project Structure

```
.
├── Libraries/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── base.py
│   ├── BrowserKeywords.py
│   ├── BurgerMenuKeywords.py
│   └── LoginKeywords.py
├── Variables/
│   ├── config.json
│   └── selectors.json
├── tests/
│   ├── __init__.py
│   └── burger_menu_navigation.robot
├── results/
│   ├── log.html
│   ├── output.xml
│   └── report.html
├── README.md
└── requirements.txt
```

## Features

- Custom Python libraries for browser automation
- Keyword-driven test architecture
- JSON-based configuration and selectors
- Modular and reusable keywords
- Comprehensive test reporting

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

### config.json

Contains environment-specific configurations such as URLs, credentials, and timeout values.

### selectors.json

Stores UI element selectors (CSS, XPath) for easy maintenance and updates.

## Custom Libraries

### BrowserKeywords.py

Contains keywords for browser operations like opening browsers, navigation, and page interactions.

### LoginKeywords.py

Provides keywords for authentication and login-related operations.

### BurgerMenuKeywords.py

Handles burger menu navigation and related interactions.

### base.py

Base utility functions and common methods used across other libraries.

## Running Tests

### Run all tests:

```bash
robot tests/
```

### Run a specific test file:

```bash
robot tests/burger_menu_navigation.robot
```

### Run with custom output directory:

```bash
robot --outputdir results tests/
```

## Test Reports

After execution, test reports are generated in the `results/` directory:

- **log.html**: Detailed test execution log
- **report.html**: High-level test summary report
- **output.xml**: Machine-readable test results

## Known Issues

- `BUG_saucelabs_link_incorrect.png`: Screenshot of issue with Sauce Labs link
- `debug_add_button_missing.png`: Debug screenshot for missing add button issue
