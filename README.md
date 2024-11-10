# Electric Car Market Analyzer

A Python application for analyzing the electric car market by scraping and visualizing data from various car listing websites.

## Features
- Scrapes electric car listings from multiple sources (Autoscout24, 2ememain, Gocar)
- Cleans and normalizes data
- Provides interactive visualizations
- Detects price changes
- Real-time data updates

## Setup
1. Clone the repository
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a .env file with your API tokens (use .env.example as a template):
   ```
   GOCAR_BEARER_TOKEN=your_token_here
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Configuration
The application uses a central config.py file for managing paths and settings. The following directories will be created automatically:
- results/ (for storing scraped data)
- visualizations/ (for storing generated plots)
- logs/ (for application logs)

## Directory Structure
```
electric-car-market-analyzer/
│
├── src/
│   ├── sites/
│   │   ├── autoscout24/
│   │   ├── deuxieme_main/
│   │   └── gocar/
│   ├── data/
│   └── visualization/
│
├── results/
├── logs/
├── config.py
├── logging_config.py
├── main.py
└── requirements.txt
```

## Logging
The application uses Python's logging module for all output. Logs are stored in the logs/ directory and are also output to the console.

## License
MIT License

## Contributing
Pull requests are welcome. Please make sure to update tests as appropriate.