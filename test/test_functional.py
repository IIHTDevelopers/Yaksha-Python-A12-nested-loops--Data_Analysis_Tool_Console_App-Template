import pytest
import re
from test.TestUtils import TestUtils
from data_analysis_tool_console import *  # Import all functions directly

@pytest.fixture
def test_obj():
    return TestUtils()

def test_nested_loop_implementation(test_obj):
    """Test if nested loops are correctly implemented in the functions"""
    try:
        with open('data_analysis_tool_console.py', 'r') as file:
            content = file.read()
        
        # Extract analyze_regional_sales function
        regional_func = re.search(r'def\s+analyze_regional_sales\s*\(.*?\).*?return\s+\w+', content, re.DOTALL)
        if not regional_func:
            test_obj.yakshaAssert("TestNestedLoopImplementation", False, "functional")
            pytest.fail("Could not find complete analyze_regional_sales function")
            
        regional_code = regional_func.group(0)
        
        # Check for outer loop iterating through regions
        outer_loop = re.search(r'for\s+(\w+)\s*,\s*(\w+)\s+in\s+sales_data\.items\(\)', regional_code)
        if not outer_loop:
            test_obj.yakshaAssert("TestNestedLoopImplementation", False, "functional")
            pytest.fail("analyze_regional_sales must use for loop with .items() to iterate through regions")
        
        # Get variable names from outer loop for checking inner loop
        region_var = outer_loop.group(1)
        products_var = outer_loop.group(2)
        
        # Check for inner loop within the outer loop context
        outer_loop_pos = regional_code.find(outer_loop.group(0))
        if outer_loop_pos == -1:
            test_obj.yakshaAssert("TestNestedLoopImplementation", False, "functional")
            pytest.fail("Could not locate outer loop position")
        
        # Get code after the outer loop declaration
        outer_loop_code = regional_code[outer_loop_pos:]
        
        # Check for inner loop using the products variable from outer loop
        inner_loop_pattern = r'for\s+\w+\s*,\s*\w+\s+in\s+' + re.escape(products_var) + r'\.items\(\)'
        if not re.search(inner_loop_pattern, outer_loop_code):
            test_obj.yakshaAssert("TestNestedLoopImplementation", False, "functional")
            pytest.fail(f"Missing inner loop that iterates through {products_var}.items()")
        
        # Extract analyze_product_performance function and check for its loop structure
        product_func = re.search(r'def\s+analyze_product_performance\s*\(.*?\).*?return\s+\w+', content, re.DOTALL)
        if not product_func:
            test_obj.yakshaAssert("TestNestedLoopImplementation", False, "functional")
            pytest.fail("Could not find complete analyze_product_performance function")
            
        product_code = product_func.group(0)
        
        # Check if the function iterates through products and regions
        # We need at least one loop for products and one for regions
        if not re.search(r'for\s+\w+\s+in\s+all_products', product_code) or \
           not re.search(r'for\s+\w+\s*,\s*\w+\s+in\s+sales_data\.items\(\)', product_code):
            test_obj.yakshaAssert("TestNestedLoopImplementation", False, "functional")
            pytest.fail("analyze_product_performance should iterate through products and regions")
        
        test_obj.yakshaAssert("TestNestedLoopImplementation", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestNestedLoopImplementation", False, "functional")
        pytest.fail(f"Nested loop implementation check failed: {str(e)}")

def test_regional_analysis_functionality(test_obj):
    """Test if analyze_regional_sales produces correct results"""
    try:
        # Use the actual sales_data from the imported module
        data = load_sales_data()
        result = analyze_regional_sales(data)
        
        # Verify results format
        assert isinstance(result, dict), "analyze_regional_sales should return a dictionary"
        
        # Check if all regions are included
        assert set(result.keys()) == set(data.keys()), "Result should include all regions"
        
        # Calculate expected totals manually and verify
        for region, products in data.items():
            expected_total = sum(products.values())
            assert result[region][0] == expected_total, f"{region} total should be {expected_total}"
        
        # Verify highest and lowest regions are correctly marked
        region_totals = {region: sum(products.values()) for region, products in data.items()}
        highest_region = max(region_totals.items(), key=lambda x: x[1])[0]
        lowest_region = min(region_totals.items(), key=lambda x: x[1])[0]
        
        assert result[highest_region][1] == "Highest performing region", f"{highest_region} should be marked as highest"
        assert result[lowest_region][1] == "Lowest performing region", f"{lowest_region} should be marked as lowest"
        
        test_obj.yakshaAssert("TestRegionalAnalysisFunctionality", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestRegionalAnalysisFunctionality", False, "functional")
        pytest.fail(f"Regional analysis functionality check failed: {str(e)}")

def test_product_analysis_functionality(test_obj):
    """Test if analyze_product_performance produces correct results"""
    try:
        # Use the actual sales_data from the imported module
        data = load_sales_data()
        result = analyze_product_performance(data)
        
        # Verify results format
        assert isinstance(result, dict), "analyze_product_performance should return a dictionary"
        
        # Find all unique products in the data
        all_products = set()
        for products in data.values():
            all_products.update(products.keys())
        
        # Check if all products are included
        assert set(result.keys()) == all_products, "Result should include all products"
        
        # Calculate expected totals manually and verify
        for product in all_products:
            expected_total = 0
            for region, products in data.items():
                if product in products:
                    expected_total += products[product]
            
            assert result[product][0] == expected_total, f"{product} total should be {expected_total}"
        
        # Get product totals and find top and bottom products
        product_totals = {product: 0 for product in all_products}
        for region, products in data.items():
            for product, amount in products.items():
                product_totals[product] += amount
        
        top_product = max(product_totals.items(), key=lambda x: x[1])[0]
        bottom_product = min(product_totals.items(), key=lambda x: x[1])[0]
        
        assert result[top_product][1] == "Top product", f"{top_product} should be marked as top product"
        assert result[bottom_product][1] == "Bottom product", f"{bottom_product} should be marked as bottom product"
        
        test_obj.yakshaAssert("TestProductAnalysisFunctionality", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestProductAnalysisFunctionality", False, "functional")
        pytest.fail(f"Product analysis functionality check failed: {str(e)}")

def test_required_functions_exist(test_obj):
    """Test if all required functions exist with correct signatures"""
    try:
        with open('data_analysis_tool_console.py', 'r') as file:
            content = file.read()
        
        required_functions = {
            'analyze_regional_sales': r'def\s+analyze_regional_sales\s*\(\s*sales_data\s*\)\s*:',
            'analyze_product_performance': r'def\s+analyze_product_performance\s*\(\s*sales_data\s*\)\s*:',
            'display_results': r'def\s+display_results\s*\(\s*results\s*,\s*analysis_type\s*\)\s*:',
            'load_sales_data': r'def\s+load_sales_data\s*\(\s*\)\s*:',
            'main': r'def\s+main\s*\(\s*\)\s*:'
        }
        
        missing_funcs = []
        for func_name, pattern in required_functions.items():
            if not re.search(pattern, content):
                missing_funcs.append(func_name)
        
        if missing_funcs:
            test_obj.yakshaAssert("TestRequiredFunctionsExist", False, "functional")
            pytest.fail(f"Missing functions or incorrect signatures: {', '.join(missing_funcs)}")
            
        test_obj.yakshaAssert("TestRequiredFunctionsExist", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestRequiredFunctionsExist", False, "functional")
        pytest.fail(f"Function existence check failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])