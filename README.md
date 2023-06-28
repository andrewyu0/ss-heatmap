# SS-Heatmap

This is a simple Flask application to visualize the distribution of screenshots over time as a heatmap.

## Setup and Usage

1. Clone this repository and navigate to its directory.
2. Install the required Python packages: `pip install -r requirements.txt`
3. Run the application: `python heatmap.py`
4. Access the application in your browser at `http://localhost:5001`

The application reads screenshot filenames from the `ss` directory and generates a heatmap where each bar represents the count of screenshots taken in that hour. By hovering over the bars, you can see the exact time and screenshot links.

You can filter the heatmap by date range by providing `start_date` and `end_date` in the URL (YYYY-MM-DD format). Example: `http://localhost:5001?start_date=2023-06-20&end_date=2023-06-27`

## Structure

- `ss`: Directory containing the screenshots.
- `templates`: Directory containing the HTML template for the heatmap.
- `heatmap.py`: Python script that generates the heatmap using Bokeh and serves it using Flask.
- `.gitignore`: File specifying what files and directories Git should ignore.
- `README.md`: This file.
