# 📄 Automated Data Analysis Report Generator

This project is a Python-based tool to generate a visual and statistical PDF report from any CSV file. It loads the dataset, analyzes key statistics, creates various visualizations, and outputs a clean, styled report in PDF format.

## ✨ Features

- CSV file selection via GUI
- Automatically generates:
  - Summary statistics table
  - Histograms of numerical columns
  - Boxplots
  - Correlation heatmap (if numerical data exists)
  - Categorical barplot (if categorical data exists)
- Clean PDF report layout with embedded images and styled tables
- Output saved to `report_output/` folder

## 📂 Output

- PDF report: `report_output/data_analysis_report.pdf`
- Plot images: Saved in the same folder for PDF inclusion

## 🛠 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

Ensure `tkinter` is available. On Linux systems:

```bash
sudo apt-get install python3-tk
```

## 🚀 Usage

Run the script:

```bash
python data_report_generator.py
```

- A file dialog will open to let you select a CSV file.
- A PDF report will be generated in the `report_output` folder.

## 📷 Preview

> Example of the PDF output includes:
- Summary statistics table
- Histograms
- Boxplots
- Heatmaps
- Bar charts (if categorical columns exist)




