# 🧹 Data Cleaning & Preparation using Python

## 📌 Project Overview

This project demonstrates a complete data cleaning and preparation workflow using Python, Pandas, NumPy, and Matplotlib.

The project identifies and fixes common data-quality issues including missing values, duplicate records, inconsistent formats, invalid values, and incorrect data types.

The cleaned dataset is then prepared for further analysis.

---

## 🎯 Objectives

- 🔍 Inspect the raw dataset
- ❌ Identify missing values
- 🔁 Detect duplicate records
- 🧹 Clean inconsistent text formats
- 📧 Validate email addresses
- 📅 Standardize date formats
- 🔢 Validate numeric values
- 🛠️ Handle missing data
- 📊 Generate a cleaned dataset
- 📈 Perform basic analysis on the cleaned data

---

## 📂 Dataset

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

## ⚠️ Data Quality Issues

The raw dataset contained:

- Missing email values
- Missing order dates
- Missing quantity values
- Missing unit price values
- Invalid email addresses
- Inconsistent city names
- Inconsistent product names
- Extra spaces in text fields
- Multiple date formats
- Invalid numeric values
- Duplicate business records

---

# 🧹 Cleaning Transformations

## 1. Column Name Standardization

Column names were converted to lowercase and spaces were replaced with underscores.

**Example:**

```text
Customer Name → customer_name
