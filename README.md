# System Requirements Specification
# Data Analysis Tool Version 1.0
To run all tests 
python -m pytest test/

## TABLE OF CONTENTS
1. Project Abstract
2. Business Requirements
3. Constraints
4. Template Code Structure
5. Execution Steps to Follow

# Data Analysis Tool Requirements Specification

## 1. PROJECT ABSTRACT

## 2. BUSINESS REQUIREMENTS
1. Application must process sales data by region and product
2. System must calculate basic statistics (totals, averages)
3. Program must identify top-performing products and regions

## 3. CONSTRAINTS

### 3.1 INPUT REQUIREMENTS
1. Data Structure:
   - Sales data organized by regions and products
   - Data provided as a nested dictionary
   - Example: sales_data[region][product] = quantity_sold

### 3.2 CALCULATION CONSTRAINTS

1. Regional Analysis:
   - Calculate total sales per region
   - Identify highest and lowest performing regions

2. Product Analysis:
   - Calculate total sales per product across all regions
   - Identify top and bottom products

### 3.3 OUTPUT CONSTRAINTS

1. Display Format:
   - Show "Sales Data Analysis Tool"
   - Show analysis type and results
   - Format numbers appropriately

## 4. TEMPLATE CODE STRUCTURE
1. Analysis Functions:
   - analyze_regional_sales(sales_data)
   - analyze_product_performance(sales_data)
   - display_results(results, analysis_type)

2. Main Program:
   - load_sales_data()
   - display_menu()
   - perform_selected_analysis(analysis_type)

## 5. EXECUTION STEPS TO FOLLOW
1. Run the program
2. Select analysis type from menu
3. View calculated statistics
4. Repeat with different analysis or exit