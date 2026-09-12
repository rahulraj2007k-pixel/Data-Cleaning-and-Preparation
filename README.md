# Data Cleaning & Preparation using Python

## Project Overview

This project demonstrates a complete data cleaning and preparation workflow using Python, Pandas, NumPy, and Matplotlib.

The project identifies and fixes common data-quality issues including missing values, duplicate records, inconsistent formats, invalid values, and incorrect data types.

The cleaned dataset is then prepared for further analysis.

---

## Objectives

- Inspect the raw dataset
- Identify missing values
- Detect duplicate records
- Clean inconsistent text formats
- Validate email addresses
- Standardize date formats
- Validate numeric values
- Handle missing data
- Generate a cleaned dataset
- Perform basic data analysis
- Generate visualizations
- Document all data transformations

---

## Dataset

The project uses a synthetic customer sales dataset created specifically for this project.

The dataset contains the following fields:

- Order ID
- Customer Name
- Email
- City
- Order Date
- Product
- Quantity
- Unit Price

The raw dataset contains intentionally introduced data-quality issues to demonstrate the cleaning process.

---

## Data Quality Issues

The raw dataset contained:

- Missing email values
- Missing order date
- Missing quantity
- Missing unit price
- Invalid email format
- Extra spaces in text fields
- Inconsistent city capitalization
- Inconsistent product capitalization
- Multiple date formats
- Negative quantity
- Negative price
- One business-key duplicate record

---

## Cleaning Transformations

### 1. Column Name Standardization

Column names were converted to lowercase and spaces were replaced with underscores.

Example:

`Customer Name` → `customer_name`

### 2. Text Cleaning

Leading and trailing spaces were removed from text fields.

### 3. City Standardization

City names were converted to a consistent title-case format.

Example:

`delhi` → `Delhi`

### 4. Product Standardization

Product names were converted to a consistent title-case format.

Example:

`mobile phone` → `Mobile Phone`

### 5. Email Cleaning

Email addresses were converted to lowercase and unnecessary spaces were removed.

### 6. Email Validation

Invalid email addresses were detected using a regular expression and converted to missing values.

### 7. Date Standardization

Multiple date formats were converted to a standard:

`YYYY-MM-DD`

### 8. Numeric Validation

Quantity and unit price were converted to numeric data types.

### 9. Invalid Values

Negative quantities and negative prices were considered invalid and converted to missing values.

### 10. Duplicate Handling

Business-key duplicates were identified using:

- Customer Name
- Email
- Order Date
- Product
- Quantity
- Unit Price

One duplicate record was removed.

### 11. Missing Values

Missing numeric values were filled using median values.

Missing email values were replaced with:

`unknown@example.com`

Missing order dates were filled using the median order date.

### 12. Derived Column

A new column was created:

`total_amount = quantity × unit_price`

---

## Results

| Metric | Before Cleaning | After Cleaning |
|---|---:|---:|
| Rows | 30 | 29 |
| Columns | 8 | 9 |
| Missing Values | 5 | 0 |
| Duplicate Rows | 0 | 0 |

One business-key duplicate was removed during the cleaning process.

---

## Analysis Results

### Product-wise Sales

| Product | Total Sales |
|---|---:|
| Laptop | 439000 |
| Tablet | 256500 |
| Mobile Phone | 211500 |
| Headphones | 20800 |

Laptop generated the highest total sales.

### City-wise Sales

| City | Total Sales |
|---|---:|
| Delhi | 397800 |
| Bangalore | 229000 |
| Mumbai | 195100 |
| Kolkata | 105900 |

Delhi generated the highest total sales.

---

## Project Structure

```text
Data-Cleaning-and-Preparation/
│
├── data/
│   ├── raw_dataset.csv
│   └── cleaned_dataset.csv
│
├── screenshots/
│   ├── cleaning_output.png
│   ├── product_sales.png
│   ├── city_sales.png
│   └── missing_values_comparison.png
│
├── report/
│
├── src/
│   ├── data_cleaning.py
│   └── data_analysis.py
│
├── analysis_summary.txt
├── cleaning_log.txt
├── requirements.txt
├── README.md
└── .gitignore