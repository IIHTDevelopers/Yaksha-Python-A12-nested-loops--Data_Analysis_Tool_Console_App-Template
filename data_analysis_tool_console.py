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
    if sales_data is None:
        raise TypeError("sales_data cannot be None")
        
    regional_analysis = {}
    highest_region = {"name": "", "total": 0}
    lowest_region = {"name": "", "total": float('inf')}
    
    for region, products in sales_data.items():
        regional_total = 0
        
        for product, amount in products.items():
            # Validate data types
            if not isinstance(amount, (int, float)):
                raise TypeError(f"Sales amount for {region}, {product} must be a number")
            
            # Validate values
            if amount < 0:
                raise ValueError(f"Sales amount for {region}, {product} cannot be negative")
            
            regional_total += amount
        
        regional_analysis[region] = regional_total
        
        # Track highest and lowest regions
        if regional_total > highest_region["total"]:
            highest_region["name"] = region
            highest_region["total"] = regional_total
            
        if regional_total < lowest_region["total"]:
            lowest_region["name"] = region
            lowest_region["total"] = regional_total
    
    # Add highest/lowest indicators
    for region in regional_analysis:
        if region == highest_region["name"]:
            regional_analysis[region] = (regional_analysis[region], "Highest performing region")
        elif region == lowest_region["name"]:
            regional_analysis[region] = (regional_analysis[region], "Lowest performing region")
        else:
            regional_analysis[region] = (regional_analysis[region], "")
            
    return regional_analysis

def analyze_product_performance(sales_data):
    """
    Analyze product performance across all regions
    Return: Dictionary with product performance data
    """
    if sales_data is None:
        raise TypeError("sales_data cannot be None")
        
    product_analysis = {}
    
    # First, collect all unique products
    all_products = set()
    for region, products in sales_data.items():
        for product in products:
            all_products.add(product)
    
    # Calculate total sales for each product across all regions
    for product in all_products:
        product_total = 0
        
        for region, products in sales_data.items():
            if product in products:
                product_total += products[product]
        
        product_analysis[product] = product_total
    
    # Identify top and bottom products
    sorted_products = sorted(product_analysis.items(), key=lambda x: x[1], reverse=True)
    
    # Add rankings to the results
    result = {}
    for i, (product, total) in enumerate(sorted_products):
        if i == 0:
            result[product] = (total, "Top product")
        elif i == len(sorted_products) - 1:
            result[product] = (total, "Bottom product")
        else:
            result[product] = (total, "")
    
    return result

def display_results(results, analysis_type):
    """Display formatted analysis results"""
    print("\nSales Data Analysis Tool")
    print(f"Analysis Type: {analysis_type}")
    print("-" * 50)
    
    if analysis_type == "Regional Sales Analysis":
        print(f"{'Region':<10}{'Total Sales':^15}{'Performance':>20}")
        print("-" * 50)
        for region, (total, label) in results.items():
            print(f"{region:<10}${total:>14,.2f}{label:>20}")
    
    elif analysis_type == "Product Performance Analysis":
        print(f"{'Product':<10}{'Total Units':^15}{'Ranking':>20}")
        print("-" * 50)
        for product, (total, label) in results.items():
            print(f"{product:<10}{total:>14,.0f}{label:>20}")
    
    print("-" * 50)

def load_sales_data():
    """Load sample sales data"""
    return sales_data

def main():
    """Main program execution"""
    data = load_sales_data()
    
    while True:
        print("\nSales Data Analysis Tool")
        print("1. Regional Sales Analysis")
        print("2. Product Performance Analysis")
        print("3. Exit")
        
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            
            if choice == 1:
                results = analyze_regional_sales(data)
                display_results(results, "Regional Sales Analysis")
            elif choice == 2:
                results = analyze_product_performance(data)
                display_results(results, "Product Performance Analysis")
            elif choice == 3:
                print("Thank you for using the Sales Data Analysis Tool!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()