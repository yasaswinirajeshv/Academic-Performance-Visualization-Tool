# Academic Performance Visualization Tool

This project is a Python and Bash-based visualization tool for analyzing and visualizing student academic performance data extracted from PDF marksheets.

## Project Structure

- `extract_grades.sh`: Shell script to extract individual student grade data from a PDF and format it into JSON.
- `combine_json.sh`: Combines multiple student JSON outputs into one `combined_results.json` file.
- `analyze_visualize.py`: Python script that processes and visualizes the data using Plotly.

## Features

- Extracts student details and grades from PDFs
- Combines all student data into a single JSON file
- Converts letter grades to numeric values
- Visualizes:
  - Average final grades per subject
  - Internal (CA), End Sem (ESE), and Practical grade trends
  - GPA distribution across students
  - Final grade trend per student
  - Topper's detailed grade breakdown

## Requirements

- Python 3.x
- Bash (for running shell scripts)
- [pdftotext](https://www.xpdfreader.com/pdftotext-man.html)
- Python libraries:
  - `pandas`
  - `plotly`

Install Python dependencies using:

```bash
pip install pandas plotly
```

## How to Use

1. **Extract grades from individual PDFs:**

```bash
./extract_grades.sh path/to/student.pdf > student.json
```

2. **Combine all student JSONs into one file:**

```bash
./combine_json.sh path/to/pdf_folder
```

3. **Run visualization script:**

```bash
python analyze_visualize.py
```

Make sure `dummy_result.json` or `combined_results.json` is present in the script directory.

## Sample Visuals

- Average grade comparison per subject
- GPA bar chart for all students
- Line graph of each student's subject-wise grades
- Topper's detailed performance breakdown

## Contribution

Feel free to fork this repo and contribute with improvements or new visualizations!

## License
This project is licensed under the MIT License.
