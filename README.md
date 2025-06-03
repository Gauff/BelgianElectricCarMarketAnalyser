# Electric Car Market Analyzer

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python application for analyzing the Belgian second-hand electric car market by scraping, processing, and visualizing data from multiple car listing websites.

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Development Setup](#development-setup)
- [Contributing](#contributing)
- [License](#license)
- [Contact/Support](#contactsupport)

## Project Description

The Electric Car Market Analyzer is designed to provide comprehensive insights into the Belgian electric vehicle market by collecting and analyzing data from major car listing platforms. This tool helps potential buyers, market researchers, and automotive enthusiasts make informed decisions by providing:

- **Real-time market data** from multiple sources
- **Price trend analysis** and drop detection
- **Interactive visualizations** for market exploration
- **Data-driven insights** into electric vehicle pricing and availability

### Target Audience

- **Car buyers** looking for the best deals on electric vehicles
- **Market researchers** studying automotive trends
- **Automotive dealers** monitoring competitor pricing
- **Data analysts** interested in market dynamics

### Key Benefits

- Save time by aggregating data from multiple platforms
- Identify price drops and market opportunities
- Understand market trends through comprehensive analytics
- Make data-driven purchasing decisions

## Features

### Core Functionality
- **Multi-source web scraping** from major Belgian car platforms:
  - **Gocar** - Premium car listings platform
  - **AutoScout24** - European automotive marketplace
  - **2ememain** - Belgian classified ads platform

- **Advanced data processing**:
  - Data cleaning and normalization
  - Electric vehicle identification and filtering
  - Price range filtering (€500 - €300,000)
  - Duplicate detection and removal

- **Price drop detection**:
  - Automatic comparison between scraping sessions
  - Identification of vehicles with reduced prices
  - Historical price tracking

- **Interactive web dashboard**:
  - Real-time data visualization using Plotly and Dash
  - Price range filtering with interactive sliders
  - Detailed vehicle information on hover
  - Visit advertisement on click
  - Refresh functionality for live updates

- **Comprehensive logging**:
  - Detailed operation logs for debugging
  - Separate log files for each module
  - Console and file output

- **Data export and visualization**:
  - Multiple chart types (box plots, scatter plots)
  - SweetViz integration for automated data profiling
  - Export capabilities for further analysis

![Screenshot](https://github.com/Gauff/BelgianElectricCarMarketAnalyser/blob/main/screenshots/03.png)

## Prerequisites

### System Requirements
- **Python 3.9 or higher** (as specified in pyproject.toml)
- **UV package manager** (recommended) or pip as fallback
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 4GB RAM (8GB recommended for large datasets)
- **Storage**: At least 1GB free space for data and logs

### Required Accounts/API Access
- **Gocar Bearer Token**: Required for accessing Gocar API
  - Contact Gocar support or check their developer documentation
  - Token should be added to your `.env` file

### Network Requirements
- Stable internet connection for web scraping
- Access to target websites (some may have regional restrictions)

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Gauff/BelgianElectricCarMarketAnalyser.git
cd electricCarMarketAnalyser
```

### Step 2: Install UV Package Manager (Recommended)

UV is a fast Python package manager that's 10-100x faster than pip:

```bash
# Install UV
pip install uv
```

Or follow the official installation guide: https://github.com/astral-sh/uv

### Step 3: Install Dependencies

**Using UV (recommended):**
```bash
uv pip install -r src/requirements.txt
```

**Using pip (fallback):**
```bash
# Create virtual environment first
python -m venv venv
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
# Install dependencies
pip install -r src/requirements.txt
```

**Required packages include:**
- `beautifulsoup4>=4.12.0` - HTML parsing for web scraping
- `botasaurus` - Web automation framework
- `dash>=2.14.0` - Web application framework
- `matplotlib>=3.8.0` - Plotting library
- `numpy>=1.24.0` - Numerical computing
- `pandas>=2.1.0` - Data manipulation and analysis
- `plotly>=5.18.0` - Interactive plotting
- `requests>=2.31.0` - HTTP library
- `seaborn>=0.13.0` - Statistical data visualization
- `sweetviz>=2.2.1` - Automated EDA
- `python-dotenv>=1.0.0` - Environment variable management

### Step 4: Environment Configuration

1. **Copy the environment template:**
   ```bash
   cp src/.env.example src/.env
   ```

2. **Edit the `.env` file** and add your API credentials:
   ```env
   GOCAR_BEARER_TOKEN=your_actual_token_here
   ```

3. **Obtain Gocar Bearer Token:**
   - Visit the Gocar developer portal or contact their support
   - Follow their authentication process
   - Add the token to your `.env` file

### Step 5: Verify Installation

Run the example script to test your setup:
```bash
python run_gocar_example.py
```

If successful, you should see output similar to:
```
Current working directory: /path/to/electricCarMarketAnalyser
Running gocar script...
Successfully retrieved X cars from Gocar
Successfully loaded X cars from last file
```

## Usage

### Basic Usage

**Run the complete analysis pipeline:**
```bash
python src/main.py
```

This command will:
1. Scrape data from all configured sources (Gocar, AutoScout24, 2ememain)
2. Clean and process the data
3. Detect price drops from previous runs
4. Launch the interactive web dashboard
5. Automatically open your browser to `http://127.0.0.1:8050/`

### Web Dashboard Features

Once the application is running, you can:

- **View interactive scatter plots** of car prices vs. registration years
- **Filter by price range** using the interactive slider
- **Hover over data points** to see detailed car information
- **Click the "Refresh Data" button** to update with latest scraped data
- **Explore different car models** and their price distributions

### Command Line Options

The application supports different execution modes:

**Scrape data only (without launching dashboard):**
```python
from src.main import scrap_ads
scrap_ads()
```

**Launch dashboard with existing data:**
```python
from src.main import run_server
run_server()
```

### Data Access

**Scraped data is stored in:**
- `results/` - Processed datasets (pickle format)
- `results/gocar/` - Raw Gocar data (JSON)
- `results/autoscout24/` - Raw AutoScout24 data (JSON)
- `results/2ememain/` - Raw 2ememain data (JSON)

**Logs are available in:**
- `logs/` - Application logs for debugging and monitoring

## Project Structure

```
electricCarMarketAnalyser/
│
├── src/                          # Source code directory
│   ├── sites/                    # Website-specific scrapers
│   │   ├── autoscout24/         # AutoScout24 scraping module
│   │   ├── deuxieme_main/       # 2ememain scraping module
│   │   └── gocar/               # Gocar API integration
│   │       ├── gocar.py         # Main Gocar scraper
│   │       ├── gocar_data.py    # Data models
│   │       └── gocar_electric_car_search.json
│   ├── data/                    # Data models and utilities
│   │   ├── electric_car_data.py # ElectricCar class definition
│   │   ├── electric_car_models.py # Car model identification
│   │   └── dataframes.py        # DataFrame utilities
│   ├── config.py                # Configuration and paths
│   ├── data_cleaning.py         # Data cleaning utilities
│   ├── data_preparation.py      # Data processing pipeline
│   ├── file_management.py       # File I/O operations
│   ├── graph_utils.py           # Graph generation utilities
│   ├── logging_config.py        # Logging configuration
│   ├── main.py                  # Main application entry point
│   ├── requirements.txt         # Python dependencies
│   ├── utilities.py             # General utility functions
│   ├── visualization.py         # Data visualization
│   ├── .env.example            # Environment variables template
│   └── .env                    # Environment variables (create this)
│
├── results/                     # Generated data files
│   ├── autoscout24/            # AutoScout24 raw data
│   ├── gocar/                  # Gocar raw data
│   ├── 2ememain/               # 2ememain raw data
│   └── YYYYMMDDHHMMSS_df.pkl   # Processed datasets
│
├── logs/                       # Application logs
│   ├── __main__.log           # Main application logs
│   ├── data_preparation.log   # Data processing logs
│   ├── autoscout24.log        # AutoScout24 scraper logs
│   └── deuxieme_main.log      # 2ememain scraper logs
│
├── visualizations/            # Generated plots and charts
├── screenshots/               # Application screenshots
├── build/                     # Build artifacts
├── run_gocar_example.py      # Example script for testing
├── README.md                 # This file
├── .gitignore               # Git ignore rules
└── .gitattributes           # Git attributes
```

### Key Components

**Core Modules:**
- `main.py` - Application entry point and Dash web server
- `data_preparation.py` - Data scraping and processing pipeline
- `config.py` - Centralized configuration management

**Scraping Modules:**
- `sites/gocar/` - Gocar API integration with bearer token authentication
- `sites/autoscout24/` - AutoScout24 web scraping
- `sites/deuxieme_main/` - 2ememain classified ads scraping

**Data Processing:**
- `data_cleaning.py` - Filters out non-electric vehicles
- `electric_car_models.py` - Electric vehicle identification
- `dataframes.py` - Price drop detection and analysis

**Utilities:**
- `file_management.py` - File operations with timestamp management
- `logging_config.py` - Centralized logging setup
- `visualization.py` - Chart generation and data visualization

## Configuration

### Environment Variables

The application uses environment variables for sensitive configuration. Create a `.env` file in the `src/` directory:

```env
# Gocar API Configuration
GOCAR_BEARER_TOKEN=your_gocar_bearer_token_here
```

### Application Settings

The `src/config.py` file manages paths and directories:

```python
# Automatically created directories
RESULTS_DIR = 'results/'           # Scraped data storage
VISUALIZATIONS_DIR = 'visualizations/'  # Generated charts
LOGS_DIR = 'logs/'                # Application logs

# Site-specific data directories
AUTOSCOUT24_RESULTS = 'results/autoscout24/'
DEUXIEMEMAIN_RESULTS = 'results/2ememain/'
GOCAR_RESULTS = 'results/gocar/'
```

### Scraping Configuration

**Price Filtering:**
- Default range: €500 - €300,000
- Configurable in `data_preparation.py`

**Data Sources:**
- All three sources are scraped in parallel for efficiency
- Individual sources can be disabled by modifying `data_preparation.py`

**Update Frequency:**
- Manual execution by default
- Can be automated using cron jobs or task schedulers

### Web Dashboard Configuration

**Server Settings:**
- Default port: 8050
- Debug mode: Enabled (disable for production)
- Auto-reload: Disabled to prevent conflicts

**Display Options:**
- Default price range: €2,000 - €20,000
- Interactive filtering available
- Real-time updates via refresh button

## Troubleshooting

### Common Issues

#### 1. Missing Gocar Bearer Token
**Error:** `ValueError: GOCAR_BEARER_TOKEN not found in environment variables`

**Solution:**
1. Ensure you have created the `.env` file in the `src/` directory
2. Verify the token is correctly added: `GOCAR_BEARER_TOKEN=your_token_here`
3. Check that there are no extra spaces or quotes around the token

#### 2. Import Errors
**Error:** `ModuleNotFoundError: No module named 'dash'`

**Solution:**
1. Install dependencies using UV: `uv pip install -r src/requirements.txt`
2. Or use pip with virtual environment: `pip install -r src/requirements.txt`
3. Verify Python version compatibility (3.9+)

#### 3. Web Dashboard Not Loading
**Error:** Dashboard doesn't open or shows connection errors

**Solution:**
1. Check if port 8050 is already in use
2. Verify firewall settings allow local connections
3. Try accessing manually: `http://127.0.0.1:8050/`
4. Check console logs for error messages

#### 4. No Data Displayed
**Error:** Empty charts or "No data available" messages

**Solution:**
1. Verify internet connection for web scraping
2. Check if scraping sources are accessible
3. Review logs in `logs/` directory for scraping errors
4. Ensure Gocar token is valid and not expired

#### 5. Permission Errors
**Error:** `PermissionError: [Errno 13] Permission denied`

**Solution:**
1. Ensure write permissions for `results/`, `logs/`, and `visualizations/` directories
2. Run with appropriate user permissions
3. Check disk space availability

### Debug Mode

Enable detailed logging by modifying `src/logging_config.py`:

```python
logger.setLevel(logging.DEBUG)  # Change from INFO to DEBUG
```

### Performance Issues

**Slow scraping:**
- Reduce the number of pages scraped per source
- Implement delays between requests to avoid rate limiting
- Check network connectivity and speed

**High memory usage:**
- Process data in smaller chunks
- Clear unused DataFrames after processing
- Monitor system resources during execution

### FAQ

**Q: How often should I run the scraper?**
A: Daily runs are recommended for price drop detection. More frequent runs may trigger rate limiting.

**Q: Can I add more car listing websites?**
A: Yes, create a new module in `src/sites/` following the existing patterns.

**Q: How do I export data for external analysis?**
A: Processed data is stored as pickle files in `results/`. Use pandas to load and export to CSV/Excel.

**Q: Is the application suitable for production use?**
A: The current version is designed for research and personal use. For production, implement proper error handling, rate limiting, and monitoring.

## Development Setup

This section covers the development environment setup for contributors and developers working on the Electric Car Market Analyzer project.

### 🛠️ Development Tools

The project uses modern Python development tools for code quality, formatting, and type checking:

- **[Black](https://black.readthedocs.io/)** - Code formatter for consistent styling
- **[Ruff](https://docs.astral.sh/ruff/)** - Fast Python linter and formatter (replaces flake8, isort, etc.)
- **[MyPy](https://mypy.readthedocs.io/)** - Static type checker
- **[Pydantic v2](https://docs.pydantic.dev/)** - Data validation library
- **[UV](https://github.com/astral-sh/uv)** - Fast Python package manager

### 🚀 Quick Development Setup

#### 1. Install Development Dependencies

Using UV (recommended - 10-100x faster than pip):
```bash
uv pip install -r requirements-dev.txt
```

Or using pip:
```bash
pip install -r requirements-dev.txt
```

#### 2. Automated Setup

Run the unified development script to install everything automatically:
```bash
python development.py setup
```

This will:
- Install all development dependencies using UV (or pip as fallback)
- Validate that all tools are properly installed
- Create VS Code settings for optimal development experience

### 🔧 Development Commands

Use the consolidated `development.py` script for all development operations:

```bash
# Set up development environment
python development.py setup

# Format code with Black
python development.py format

# Lint code with Ruff
python development.py lint

# Type check with MyPy
python development.py type-check

# Auto-fix formatting and linting issues
python development.py fix

# Run all tools
python development.py all
```

### ⚙️ Tool Configuration

All development tools are configured in `pyproject.toml`:

**Black Configuration:**
- Line length: 88 characters
- Target Python versions: 3.9+
- Excludes: logs, results, screenshots, visualizations

**Ruff Configuration:**
- Replaces: flake8, isort, pyupgrade, and more
- Enabled rules: pycodestyle, Pyflakes, isort, bugbear, comprehensions, pyupgrade, naming, security, simplify
- Import sorting with known first-party modules

**MyPy Configuration:**
- Target Python version: 3.9
- Lenient settings for gradual adoption
- Ignores missing imports for external libraries

### 🎯 VS Code Integration

The setup script automatically creates `.vscode/settings.json` with optimal settings:

- Black as the default formatter
- Format on save enabled
- Ruff linting enabled
- MyPy type checking enabled
- Automatic import organization

### 📈 Development Workflow

**Before Committing:**
```bash
# Run all tools to ensure code quality
python development.py all
```

**During Development:**
```bash
# Auto-fix issues as you work
python development.py fix
```

**For CI/CD Pipelines:**
```yaml
# Example GitHub Actions step
- name: Check code quality
  run: |
    uv pip install -r requirements-dev.txt
    python development.py all
```

### 🐛 Development Troubleshooting

**UV Not Found:**
```bash
# Install UV
pip install uv
# Or follow instructions at: https://github.com/astral-sh/uv
```

**Tools Not Found:**
- Use the `development.py` script which uses UV to run tools
- Or install tools globally: `pip install black ruff mypy`

**MyPy Module Errors:**
- Run MyPy from the project root directory
- Ensure `src/` is in your Python path
- Use the provided scripts which handle paths correctly

### 📊 Code Quality Standards

The development tools help maintain high code quality:

**Black:** Automatically formats code for consistency
**Ruff:** Provides import sorting, code style enforcement, bug detection, security checks, and performance suggestions
**MyPy:** Catches type-related errors and provides better IDE integration

### 📁 Development Files

Key development-related files in the project:

```
electric-car-market-analyser/
├── src/                          # Main source code
│   ├── data/                     # Data models and processing
│   ├── sites/                    # Web scraping modules
│   └── requirements.txt          # Production dependencies
├── development.py               # Unified development tools script
├── requirements-dev.txt         # Development dependencies
├── pyproject.toml              # Tool configuration (Python 3.9+)
├── uv.lock                     # UV dependency lock file
└── .vscode/settings.json       # VS Code integration (auto-generated)
```

## Contributing

We welcome contributions to improve the Electric Car Market Analyzer! Here's how you can help:

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/BelgianElectricCarMarketAnalyser.git
   cd electricCarMarketAnalyser
   ```
3. **Create a development branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Set up development environment:**
   ```bash
   # Install UV package manager (if not already installed)
   pip install uv

   # Install production dependencies
   uv pip install -r src/requirements.txt

   # Set up development tools
   python development.py setup
   ```

See the [Development Setup](#development-setup) section above for detailed information about development tools and workflow.

### Contribution Guidelines

**Code Quality:**
- Run `python development.py all` before committing to ensure code quality
- Use `python development.py fix` to auto-fix formatting and linting issues
- Follow the automated code style enforced by Black and Ruff
- Add type hints where appropriate (checked by MyPy)

**Development Workflow:**
- Use the development tools provided: `python development.py setup`
- Format code automatically: `python development.py format`
- Check for issues: `python development.py lint`
- Ensure type safety: `python development.py type-check`

**Testing:**
- Test your changes thoroughly
- Ensure existing functionality isn't broken
- Add unit tests for new features
- Run the full development tool suite before submitting

**Documentation:**
- Update README.md for new features
- Add inline comments for complex logic
- Update docstrings as needed

### Types of Contributions

**Bug Reports:**
- Use GitHub Issues to report bugs
- Include error messages, logs, and steps to reproduce
- Specify your operating system and Python version

**Feature Requests:**
- Describe the proposed feature and its benefits
- Explain the use case and expected behavior
- Consider implementation complexity

**Code Contributions:**
- New scraping sources
- Data analysis features
- Visualization improvements
- Performance optimizations
- Bug fixes

### Pull Request Process

1. **Ensure your code follows the style guidelines**
2. **Update documentation** as needed
3. **Test your changes** thoroughly
4. **Create a pull request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots for UI changes

## License

This project is licensed under the MIT License - see the details below:

```
MIT License

Copyright (c) 2024 Electric Car Market Analyzer Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Third-Party Licenses

This project uses several open-source libraries, each with their own licenses:
- **Dash** - MIT License
- **Plotly** - MIT License
- **Pandas** - BSD 3-Clause License
- **BeautifulSoup** - MIT License
- **Requests** - Apache 2.0 License

## Contact/Support

### Getting Help

**GitHub Issues:** [Report bugs or request features](https://github.com/Gauff/BelgianElectricCarMarketAnalyser/issues)

**Documentation:** This README contains comprehensive setup and usage instructions

**Community:** Check existing issues and discussions for similar problems

### Support Guidelines

When seeking support:

1. **Search existing issues** first
2. **Provide detailed information:**
   - Operating system and Python version
   - Complete error messages
   - Steps to reproduce the issue
   - Relevant log files from `logs/` directory

3. **Include context:**
   - What you were trying to accomplish
   - What you expected to happen
   - What actually happened

### Maintainers

This project is maintained by the community. Active contributors help review issues and pull requests.

### Disclaimer

This tool is for educational and research purposes. Users are responsible for:
- Complying with website terms of service
- Respecting rate limits and robots.txt files
- Using scraped data ethically and legally
- Obtaining necessary permissions for commercial use

---

**Happy analyzing! 🚗⚡📊**
