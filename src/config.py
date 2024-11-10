import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
VISUALIZATIONS_DIR = os.path.join(BASE_DIR, 'visualizations')

# Site-specific paths
AUTOSCOUT24_RESULTS = os.path.join(RESULTS_DIR, 'autoscout24')
DEUXIEMEMAIN_RESULTS = os.path.join(RESULTS_DIR, '2ememain')
GOCAR_RESULTS = os.path.join(RESULTS_DIR, 'gocar')

# Files and directories that need to exist
REQUIRED_DIRS = [
    RESULTS_DIR,
    VISUALIZATIONS_DIR,
    AUTOSCOUT24_RESULTS,
    DEUXIEMEMAIN_RESULTS,
    GOCAR_RESULTS
]

# Create required directories if they don't exist
for directory in REQUIRED_DIRS:
    os.makedirs(directory, exist_ok=True)

# Ensure the results directory exists on import
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)