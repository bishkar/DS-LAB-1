# Practical Labs 1
# Data Collection and Processing

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git

### Local Development Setup

**Important:** This project requires a virtual environment to manage dependencies and ensure consistency across different machines.

#### Option 1: Automated Setup (Recommended)

**For Windows:**
```bash
setup.bat
```
This script will:
- Create a virtual environment in the `venv` folder
- Activate the virtual environment
- Install all required dependencies from `requirements.txt`

**For Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

#### Option 2: Manual Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```
   This creates a new folder called `venv` in your project directory containing an isolated Python environment.

2. **Activate the virtual environment:**
   
   **On Windows (PowerShell):**
   ```bash
   .\venv\Scripts\activate
   ```
   
   **On Windows (Command Prompt):**
   ```bash
   venv\Scripts\activate.bat
   ```
   
   **On Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```
   
   You'll know it's activated when you see `(venv)` at the beginning of your command prompt.

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

#### Deactivating the Virtual Environment

When you're done working on the project:
```bash
deactivate
```

### Running the Project

**Always activate your virtual environment before running code or tests!**

#### Running Individual Tasks

```bash
# Activate venv first
# On Windows:
.\venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Run a specific task
python src/task1_scrape.py
python src/task2_fetch_tokyo_weather.py
# ... etc
```

#### Running Tests

```bash
# Activate virtual environment first, then:
python -m pytest tests/ -v

# Run specific test file:
python -m pytest tests/test_task1_scrape.py -v

# Run with coverage:
python -m pytest tests/ --cov=src --cov-report=html
```

### Visualizing Results with Streamlit Dashboard

After completing the tasks, you can visualize all results using the interactive Streamlit dashboard:

```bash
# Activate virtual environment first, then:
streamlit run streamlit_app.py
```

The dashboard will open in your browser and display:
- 📰 **Task 1:** Web scraping results from Wikipedia
- 🌐 **Task 2:** API data collection with temperature gauges
- 🌦️ **Task 3:** Complex weather analysis with interactive charts
- 📁 **Task 4:** CSV export data with downloadable files
- 📄 **Task 5:** XML parsing results and visualizations
- 🔍 **Task 6:** Regex extraction analysis

**Dashboard Features:**
- Interactive charts and graphs using Plotly
- Real-time data loading from generated files
- Task completion status overview
- Downloadable processed data
- Responsive design for all screen sizes

### Troubleshooting

**Issue: "Module not found" errors**
- Solution: Make sure your virtual environment is activated and dependencies are installed

**Issue: Scripts won't run on Windows (execution policy error)**
- Solution: Run PowerShell as Administrator and execute:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

**Issue: Import errors between modules**
- Solution: Run Python with the `-m` flag from the project root:
  ```bash
  python -m pytest tests/
  ```

**Issue: Streamlit shows "No data found" warnings**
- Solution: Run the corresponding task script first to generate the data files:
  ```bash
  python src/task1_scrape.py
  python src/task2_fetch_tokyo_weather.py
  # ... etc
  ```

---

## Task 1. Basic Web Scraping and JSON Storage

Create a Python script that performs basic web scraping on a Wikipedia page to extract specific information and then saves this information in a JSON file.

**Tasks:**

1. **Fetch a Wikipedia Page:**
   - Write a Python function that retrieves the HTML content of the Wikipedia page for "Web scraping" using the `requests` library.

2. **Extract the Page Title:**
   - Write a Python function that parses the HTML content using `BeautifulSoup` and extracts the title of the page (`<h1>` element with `id="firstHeading"`).

3. **Extract the First Sentence of the First Paragraph:**
   - Write a Python function that extracts the first sentence from the first paragraph (`<p>` element) on the page.

4. **Store the Extracted Information in a JSON File:**
   - Write a Python function that saves the extracted title and first sentence into a JSON file.

**Expected JSON Output:**

The JSON file should contain the following structure:

```json
{
    "title": "Web scraping",
    "first_sentence": "Web scraping, web harvesting, or web data extraction is data scraping used for extracting data from websites."
}
```

**Implementation Details:**

- **Libraries Used:** `requests`, `BeautifulSoup`, `json`, `pytest`
- **Common Utilities:** Shared functions (`load_json`, `save_to_json`) are available in `src/utils.py`
- **Testing:** Use `pytest` to implement unit tests for each function.
- **File Handling:** The extracted data should be saved to a JSON file named `extracted_wikipedia_data.json`.



## Task 2: Collecting Weather Data Using Open-Meteo API

Learn how to collect weather data using the Open-Meteo API and save the extracted data into a JSON file.

### Task Description:

1. **Fetch Weather Data:**
   - Write a Python script that sends a request to the Open-Meteo API using the provided endpoint:
     - URL: `https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917&daily=temperature_2m_max&timezone=Asia/Tokyo`
   - This URL fetches the maximum temperature forecast for Tokyo (latitude 35.6895, longitude 139.6917).

2. **Extract the Maximum Temperature:**
   - Extract the `temperature_2m_max` value from the JSON response. This represents the maximum temperature for the next day in Tokyo.

3. **Save the Extracted Data:**
   - Save the extracted temperature data into a JSON file named `tokyo_weather.json`.

### JSON Output Example:

The JSON file might look like this:

```json
{
    "date": "2024-08-18",
    "max_temperature": 32.5
}
```

## Task 3: Advanced Parsing, Analyzing, and Reporting on Complex Weather Data

Create a Python script that loads, parses, and analyzes complex weather data stored in a JSON file. The script should perform multiple analyses over several days and generate detailed reports summarizing the findings.

### Task Description:

1. **Load the JSON Data:**
   - Write a Python script that loads weather data from a JSON file named `tokyo_weather_complex.json`.

2. **Parse the JSON Data:**
   - Extract relevant information from the JSON data, including:
     - City name, geographical coordinates (latitude, longitude), and timezone.
     - Daily weather data, including the date, maximum and minimum temperatures, precipitation, wind speed, humidity, and a short weather description.

3. **Perform Multiple Analyses:**
   - **Temperature Analysis:** For each day, check if the maximum temperature exceeds a specified threshold (e.g., 30°C) and determine if it’s a hot day.
   - **Temperature Swing Analysis:** Calculate the difference between the maximum and minimum temperatures for each day. Determine if there was a significant temperature swing (e.g., more than 10°C).
   - **Wind Analysis:** Check if the wind speed exceeded a specified threshold (e.g., 15 km/h) and determine if it was a windy day.
   - **Humidity and Comfort Analysis:** Assess the humidity level and determine if the day was likely to be uncomfortable (e.g., if humidity is over 70%).
   - **Precipitation Analysis:** Identify rainy days and determine the severity of the rain (e.g., light, moderate, or heavy rain based on precipitation levels).

4. **Generate Detailed Reports:**
   - For each day, generate a detailed report that summarizes the findings from the analyses. The report should include:
     - The date and weather description.
     - An assessment of whether it was a hot day, the significance of the temperature swing, whether it was windy, and whether the humidity made the day uncomfortable.
     - Information on whether it was a rainy day or if there was no precipitation.
   - Provide a summary report that highlights:
     - The hottest day.
     - The windiest day.
     - The most humid day.
     - The day with the most precipitation.

**Expected Output Example:**

```
Date: 2024-08-18
Weather: Clear sky
Temperature: Max 32.5°C, Min 22.5°C (Swing: 10.0°C)
It was a hot day.
It was a windy day.
There was no precipitation.

Date: 2024-08-19
Weather: Light rain
Temperature: Max 30.0°C, Min 21.0°C (Swing: 9.0°C)
It was a rainy day.

Date: 2024-08-20
Weather: Moderate rain
Temperature: Max 28.0°C, Min 20.0°C (Swing: 8.0°C)
The humidity made the day uncomfortable.
It was a rainy day.

Date: 2024-08-21
Weather: Sunny
Temperature: Max 33.0°C, Min 24.0°C (Swing: 9.0°C)
It was a hot day.
It was a windy day.
There was no precipitation.

Weather Summary:
Hottest day: 2024-08-21 with a maximum temperature of 33.0°C
Windiest day: 2024-08-18 with wind speeds of 20.0 km/h
Most humid day: 2024-08-20 with a humidity level of 80%
Rainiest day: 2024-08-20 with 10.0 mm of precipitation
```

## Task 4: Summarizing and Exporting Weather Data to CSV

Create a Python script that loads, summarizes, and exports complex weather data stored in a JSON file to a CSV file. The script should be able to handle both file paths and file-like objects for the CSV output.

### Task Description:

1. **Load and Parse JSON Data:**
   - Write a Python script that loads weather data from a JSON file named `tokyo_weather_complex.json`.

2. **Summarize Weather Data:**
   - Implement a function that calculates key metrics across multiple days of weather data. The summary should include:
     - The average maximum and minimum temperatures over the period.
     - The total precipitation over the period.
     - The average wind speed and humidity over the period.
     - The number of hot days (e.g., days where the temperature exceeded 30°C).
     - The number of windy days (e.g., days where the wind speed exceeded 15 km/h).
     - The number of rainy days.

3. **Export the Summary to a CSV File:**
   - Create a function that exports the summarized data to a CSV file. The function should:
     - Accept either a string (file path) or a file-like object (e.g., `StringIO`) as the destination for the CSV output.
     - Write the daily weather data, including additional analyzed metrics (e.g., whether it was a hot day, windy day, or rainy day).
     - Ensure the CSV file includes appropriate headers.

### Example Implementation:

Here's a breakdown of the key functions:

1. **load_json:**
   - Loads the JSON data from the specified file.
   - Available in `src/utils.py` as a common utility function.

2. **summarize_weather_data:**
   - Summarizes key metrics across all days, such as average temperatures, total precipitation, average wind speed, and counts of hot, windy, and rainy days.

3. **export_to_csv:**
   - Exports the summarized weather data to a CSV file. This function should handle both string filenames and file-like objects.

### Example CSV Output:

The CSV file might look like this:

```csv
Date,Max Temperature,Min Temperature,Precipitation,Wind Speed,Humidity,Weather Description,Is Hot Day,Is Windy Day,Is Rainy Day
2024-08-18,32.5,22.5,0.0,15.5,65,Clear sky,True,True,False
2024-08-19,30.0,21.0,5.0,10.0,70,Light rain,False,False,True
2024-08-20,28.0,20.0,10.0,8.0,80,Moderate rain,False,False,True
2024-08-21,33.0,24.0,0.0,20.0,60,Sunny,True,True,False
```

## Task 5: Parsing Weather Data from an XML File

Create a Python script to parse weather data from an XML file, extract key metrics, and store them in a CSV file.

**Task Description:**

1. **Load XML Data:**
   - You are provided with an XML file named `weather_data.xml` containing weather information for several days. The XML structure includes elements like `<date>`, `<temperature>`, `<humidity>`, and `<precipitation>`.

2. **Parse the XML File:**
   - Write a Python script to load and parse the XML file using the `xml.etree.ElementTree` module.
   - Extract the date, temperature, humidity, and precipitation for each day from the XML structure.

3. **Store Data in CSV:**
   - Store the extracted data in a CSV file named `parsed_weather_data.csv` with the following headers:
     - `Date`
     - `Temperature`
     - `Humidity`
     - `Precipitation`

**Example XML Structure:**

```xml
<weather>
    <day>
        <date>2024-08-18</date>
        <temperature>32.9</temperature>
        <humidity>65</humidity>
        <precipitation>0.0</precipitation>
    </day>
    <day>
        <date>2024-08-19</date>
        <temperature>30.5</temperature>
        <humidity>70</humidity>
        <precipitation>1.2</precipitation>
    </day>
    <!-- More day elements -->
</weather>
```

**Expected Output:**
- A CSV file named `parsed_weather_data.csv` with rows of weather data extracted from the XML file.


## Task 6: Extracting Data Using Regular Expressions

Create a Python script to extract weather data from a text file using regular expressions and store the data in a CSV file.

**Task Description:**

1. **Text Data Extraction:**
   - You are provided with a text file named `weather_report.txt` containing daily weather summaries in the following format:
     ```
     Date: 2024-08-18, Max Temp: 32.9°C, Min Temp: 22.5°C, Humidity: 65%, Precipitation: 0.0mm
     Date: 2024-08-19, Max Temp: 30.5°C, Min Temp: 21.8°C, Humidity: 70%, Precipitation: 1.2mm
     ```
   
2. **Extract Data Using Regular Expressions:**
   - Write a Python script to extract the date, maximum temperature, minimum temperature, humidity, and precipitation from each line using regular expressions.
   - Ensure that the script can handle any issues related to text encoding, such as non-ASCII characters, by cleaning the data before extraction.

3. **Store Extracted Data in CSV:**
   - Store the extracted data in a CSV file named `extracted_weather_data.csv` with the following headers:
     - `Date`
     - `Max Temperature`
     - `Min Temperature`
     - `Humidity`
     - `Precipitation`

**Expected Output:**
- A CSV file named `extracted_weather_data.csv` with rows of weather data extracted from the text file.

---

## Project Structure

```
MLDS_week_1/
├── src/
│   ├── __init__.py                       # Package initialization
│   ├── utils.py                          # Common utility functions (load_json, save_to_json)
│   ├── task1_scrape.py                   # Web scraping implementation
│   ├── task2_fetch_tokyo_weather.py      # API data collection
│   ├── task3_complex_weather_analysis.py # Weather data analysis
│   ├── task4_weather_summary_export.py   # CSV export functionality
│   ├── task5_parse_weather_xml.py        # XML parsing
│   ├── task6_extract_weather_data.py     # Regex-based data extraction
│   ├── tokyo_weather_complex.json        # Sample complex weather data
│   ├── weather_data.xml                  # Sample XML weather data
│   └── weather_report.txt                # Sample text weather data
├── tests/
│   ├── __init__.py                       # Test package initialization
│   ├── test_utils.py                     # Tests for utility functions
│   ├── test_task1_scrape.py              # Tests for Task 1
│   ├── test_fetch_tokyo_weather.py       # Tests for Task 2
│   ├── test_complex_weather_analysis.py  # Tests for Task 3
│   ├── test_weather_summary_export.py    # Tests for Task 4
│   ├── test_xml_parsing.py               # Tests for Task 5
│   └── test_regex_extraction.py          # Tests for Task 6
├── .github/
│   ├── workflows/
│   │   └── classroom.yml                 # GitHub Classroom autograding workflow
│   └── classroom/
│       └── autograding.json              # Autograding configuration
├── streamlit_app.py                      # Interactive dashboard for visualizing results
├── setup.bat                             # Windows setup script
├── setup.sh                              # Linux/Mac setup script
├── requirements.txt                      # Project dependencies
├── .gitignore                            # Git ignore rules
└── README.md                             # This file
```

## Code Quality Features

- **Type Hints:** All functions include Python type annotations for better code clarity and IDE support
- **Error Handling:** Comprehensive try-except blocks with informative error messages
- **DRY Principle:** Common functionality extracted to `utils.py` to avoid code duplication
- **Documentation:** Detailed docstrings for all functions following Google style
- **Encoding:** UTF-8 encoding used throughout for international character support
---

## Project Structure

```
MLDS_week_1/
├── src/
│   ├── utils.py                          # Common utility functions (load_json, save_to_json)
│   ├── task1_scrape.py                   # Web scraping implementation
│   ├── task2_fetch_tokyo_weather.py      # API data collection
│   ├── task3_complex_weather_analysis.py # Weather data analysis
│   ├── task4_weather_summary_export.py   # CSV export functionality
│   ├── task5_parse_weather_xml.py        # XML parsing
│   └── task6_extract_weather_data.py     # Regex-based data extraction
├── tests/
│   └── ...                               # Unit tests for all tasks
├── requirements.txt                      # Project dependencies
└── README.md                             # This file
```

## Code Quality Features

- **Type Hints:** All functions include Python type annotations for better code clarity and IDE support
- **Error Handling:** Comprehensive try-except blocks with informative error messages
- **DRY Principle:** Common functionality extracted to `utils.py` to avoid code duplication
- **Documentation:** Detailed docstrings for all functions following Google style
- **Encoding:** UTF-8 encoding used throughout for international character support








