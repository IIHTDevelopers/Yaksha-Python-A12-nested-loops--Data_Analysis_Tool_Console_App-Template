# DO NOT MODIFY THE SECTIONS MARKED AS "DO NOT MODIFY"

# Sample data structure - DO NOT MODIFY
sales_data = {
    "North": {
        "Product A": 120,
        "Product B": 85,
        "Product C": 45
    },
    "South": {
        "Product A": 95,
        "Product B": 110,
        "Product C": 30
    },
    "East": {
        "Product A": 105,
        "Product B": 90,
        "Product C": 40
    },
    "West": {
        "Product A": 130,
        "Product B": 120,
        "Product C": 50
    }
}

def analyze_regional_sales(sales_data):
    """
    Analyze sales across regions using FOR loop
    Return: Dictionary with regional sales data
    """
    # Validation - DO NOT MODIFY
    if sales_data is None:
        raise TypeError("sales_data cannot be None")
        
    # TODO: Implement the following
    # 1. Create dictionaries to store:
    #    - regional_analysis: will hold the final results
    #    - highest_region: to track the highest performing region
    #    - lowest_region: to track the lowest performing region
    
    # 2. IMPORTANT: Loop through each region and its products using a nested for loop structure
    #    - MUST use "for region, products in sales_data.items():" for the outer loop
    #    - MUST use "for product, amount in products.items():" for the inner loop
    #    - For each region, calculate the total sales across all products
    #    - Validate that sales amounts are numbers and not negative
    #    - Store the regional total in regional_analysis
    
    # 3. Track the highest and lowest performing regions
    #    - Compare each region's total with the current highest and lowest
    #    - Update highest_region and lowest_region as needed
    
    # 4. Add performance indicators to the results
    #    - For each region in regional_analysis, add a label
    #    - "Highest performing region" for the highest
    #    - "Lowest performing region" for the lowest
    #    - Empty string for others
    #    - Format the entry as a tuple: (total_sales, label)
    
    # 5. Return the completed regional_analysis dictionary
    pass

def analyze_product_performance(sales_data):
    """
    Analyze product performance across all regions
    Return: Dictionary with product performance data
    """
    # Validation - DO NOT MODIFY
    if sales_data is None:
        raise TypeError("sales_data cannot be None")
        
    # TODO: Implement the following
    # 1. Create a dictionary to store product analysis results
    
    # 2. Collect all unique products across all regions
    #    - Use a set to store unique product names
    #    - MUST use "for region, products in sales_data.items():" to loop through regions
    #    - Loop through each product in the region and add to the set
    
    # 3. Calculate total sales for each product across all regions
    #    - MUST loop through each product in all_products
    #    - For each product, MUST use nested loops to sum sales across regions
    #    - MUST use "for region, products in sales_data.items():" for the inner loop
    #    - Store the total in the product_analysis dictionary
    
    # 4. Sort products by total sales (highest to lowest)
    #    - MUST use sorted() with a lambda function to sort by sales values
    #    - Example: sorted(product_analysis.items(), key=lambda x: x[1], reverse=True)
    
    # 5. Add rankings to the results
    #    - Create a result dictionary
    #    - Add labels: "Top product" for the highest, "Bottom product" for the lowest
    #    - Format each entry as a tuple: (total_sales, label)
    
    # 6. Return the completed result dictionary
    pass

def display_results(results, analysis_type):
    """Display formatted analysis results"""
    # TODO: Implement the following
    # 1. Print header with the analysis tool name and type
    
    # 2. Check the analysis type and format the output accordingly
    #    - For Regional Sales Analysis:
    #      * Show column headers: Region, Total Sales, Performance
    #      * For each region, display its name, formatted total sales with $ symbol, and performance label
    
    #    - For Product Performance Analysis:
    #      * Show column headers: Product, Total Units, Ranking
    #      * For each product, display its name, formatted total units, and ranking label
    
    # 3. Add formatting to make the output readable
    #    - Use string formatting to align columns
    #    - Add separators for readability
    pass

def load_sales_data():
    """Load sample sales data"""
    # DO NOT MODIFY
    return sales_data

def main():
    """Main program execution"""
    # TODO: Implement the following
    # 1. Load the sales data
    
    # 2. Create a menu loop that continues until user chooses to exit
    #    - Display menu options (Regional Analysis, Product Analysis, Exit)
    #    - Get user choice with error handling
    
    # 3. Based on choice, call appropriate analysis function
    #    - For option 1: Call analyze_regional_sales and display results
    #    - For option 2: Call analyze_product_performance and display results
    #    - For option 3: Display exit message and break the loop
    
    # 4. Handle exceptions appropriately
    #    - MUST use try/except blocks
    #    - Handle ValueError for invalid number inputs
    #    - Handle general exceptions with informative error messages
    pass

if __name__ == "__main__":
    main()