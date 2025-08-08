import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

# Load CSV file using file dialog
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Select a CSV File",
    filetypes=[("CSV Files", "*.csv")]
)

if not file_path:
    raise Exception("No file selected. Please run the script again and select a CSV file.")

#  Read the dataset
df = pd.read_csv(file_path)

#  Output directory
output_dir = "report_output"
os.makedirs(output_dir, exist_ok=True)

#  Summary statistics
summary_stats = df.describe(include="all").transpose()
summary_stats.fillna("-", inplace=True)

#  Helper to save plots
def save_plot(plot_func, filename):
    plt.figure()
    plot_func()
    plt.tight_layout()
    path = os.path.join(output_dir, filename)
    plt.savefig(path)
    plt.close()
    return path

#  Generate visualizations
hist_path = save_plot(lambda: df.hist(figsize=(10, 8)), "histograms.png")
boxplot_path = save_plot(lambda: sns.boxplot(data=df.select_dtypes(include="number")), "boxplot.png")

# Correlation heatmap
if not df.select_dtypes(include="number").empty:
    corr = df.select_dtypes(include="number").corr()
    heatmap_path = save_plot(lambda: sns.heatmap(corr, annot=True, cmap="coolwarm"), "correlation_heatmap.png")
else:
    heatmap_path = None

# Barplot for first categorical column (if exists)
categorical_cols = df.select_dtypes(include="object").columns
if not categorical_cols.empty:
    barplot_path = save_plot(lambda: sns.countplot(x=categorical_cols[0], data=df), "barplot.png")
else:
    barplot_path = None

#  Create PDF report
pdf_path = os.path.join(output_dir, "data_analysis_report.pdf")
doc = SimpleDocTemplate(pdf_path, pagesize=A4)
styles = getSampleStyleSheet()
elements = []

# Title and metadata
elements.append(Paragraph("📄 Automated Data Analysis Report", styles['Title']))
elements.append(Spacer(1, 12))
elements.append(Paragraph(f"Dataset: {os.path.basename(file_path)}", styles['Normal']))
elements.append(Paragraph(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}", styles['Normal']))
elements.append(Spacer(1, 12))

# Summary statistics table
summary_data = [['Column', 'Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']]
for col in summary_stats.index:
    row = [col] + [str(summary_stats.loc[col].get(k, "-")) for k in summary_data[0][1:]]
    summary_data.append(row)

summary_table = Table(summary_data[:20], repeatRows=1)  # show top 20 rows
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
]))
elements.append(summary_table)
elements.append(Spacer(1, 12))

# Add charts
plot_sections = [
    ("Histograms", hist_path),
    ("Boxplot", boxplot_path),
    ("Correlation Heatmap", heatmap_path),
    ("Barplot (Categorical Distribution)", barplot_path)
]

for title, img_path in plot_sections:
    if img_path:
        elements.append(Paragraph(title, styles['Heading2']))
        elements.append(Image(img_path, width=400, height=250))
        elements.append(Spacer(1, 12))

# Build the PDF
doc.build(elements)

print(f"✅ Report generated: {pdf_path}")
