import unittest
import os
import importlib
import sys
import io
import contextlib
import re
import inspect
from test.TestUtils import TestUtils

def check_file_exists(filename):
    """Check if a file exists in the current directory."""
    return os.path.exists(filename)

def safely_import_module(module_name):
    """Safely import a module, returning None if import fails."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None

def check_function_exists(module, function_name):
    """Check if a function exists in a module."""
    return hasattr(module, function_name) and callable(getattr(module, function_name))

def safely_call_function(module, function_name, *args, **kwargs):
    """Safely call a function, returning the result or None if it fails."""
    if not check_function_exists(module, function_name):
        return None
    try:
        # Suppress stdout to prevent unwanted output
        with contextlib.redirect_stdout(io.StringIO()):
            return getattr(module, function_name)(*args, **kwargs)
    except Exception:
        return None

def load_module_dynamically():
    """Load the student's module for testing"""
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    return module_obj

class TestAssignment(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()
    
    def test_nested_loop_implementation(self):
        """Test if nested loops are correctly implemented in the functions"""
        try:
            # Check if file exists
            if not check_file_exists("skeleton.py"):
                self.test_obj.yakshaAssert("TestNestedLoopImplementation", False, "functional")
                print("TestNestedLoopImplementation = Failed")
                return
            
            errors = []
            
            with open('skeleton.py', 'r') as file:
                content = file.read()
            
            # Extract analyze_regional_sales function
            regional_func = re.search(r'def\s+analyze_regional_sales\s*\(.*?\).*?(?=def\s|\Z)', content, re.DOTALL)
            if not regional_func:
                errors.append("Could not find complete analyze_regional_sales function")
            else:
                regional_code = regional_func.group(0)
                
                # Check if function contains only 'pass'
                code_lines = [line.strip() for line in regional_code.split('\n') 
                             if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('def')]
                
                # Filter out docstrings
                filtered_lines = []
                in_docstring = False
                for line in code_lines:
                    if '"""' in line or "'''" in line:
                        in_docstring = not in_docstring
                        continue
                    if not in_docstring:
                        filtered_lines.append(line)
                
                if len(filtered_lines) == 1 and filtered_lines[0] == 'pass':
                    errors.append("analyze_regional_sales function is not implemented (contains only 'pass')")
                else:
                    # Check for outer loop iterating through regions
                    outer_loop = re.search(r'for\s+(\w+)\s*,\s*(\w+)\s+in\s+sales_data\.items\(\)', regional_code)
                    if not outer_loop:
                        errors.append("analyze_regional_sales must use for loop with .items() to iterate through regions")
                    else:
                        # Get variable names from outer loop for checking inner loop
                        region_var = outer_loop.group(1)
                        products_var = outer_loop.group(2)
                        
                        # Check for inner loop within the outer loop context
                        outer_loop_pos = regional_code.find(outer_loop.group(0))
                        if outer_loop_pos == -1:
                            errors.append("Could not locate outer loop position")
                        else:
                            # Get code after the outer loop declaration
                            outer_loop_code = regional_code[outer_loop_pos:]
                            
                            # Check for inner loop using the products variable from outer loop
                            inner_loop_pattern = r'for\s+\w+\s*,\s*\w+\s+in\s+' + re.escape(products_var) + r'\.items\(\)'
                            if not re.search(inner_loop_pattern, outer_loop_code):
                                errors.append(f"Missing inner loop that iterates through {products_var}.items()")
            
            # Extract analyze_product_performance function and check for its loop structure
            product_func = re.search(r'def\s+analyze_product_performance\s*\(.*?\).*?(?=def\s|\Z)', content, re.DOTALL)
            if not product_func:
                errors.append("Could not find complete analyze_product_performance function")
            else:
                product_code = product_func.group(0)
                
                # Check if function contains only 'pass'
                code_lines = [line.strip() for line in product_code.split('\n') 
                             if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('def')]
                
                # Filter out docstrings
                filtered_lines = []
                in_docstring = False
                for line in code_lines:
                    if '"""' in line or "'''" in line:
                        in_docstring = not in_docstring
                        continue
                    if not in_docstring:
                        filtered_lines.append(line)
                
                if len(filtered_lines) == 1 and filtered_lines[0] == 'pass':
                    errors.append("analyze_product_performance function is not implemented (contains only 'pass')")
                else:
                    # Look for both a loop through products and a loop through regions
                    has_product_loop = re.search(r'for\s+\w+\s+in\s+\w+(?:_products)?', product_code) is not None
                    has_region_loop = re.search(r'for\s+\w+\s*,\s*\w+\s+in\s+sales_data\.items\(\)', product_code) is not None
                    
                    if not has_product_loop or not has_region_loop:
                        errors.append("analyze_product_performance should iterate through products and regions")
            
            # Final assertion
            if errors:
                self.test_obj.yakshaAssert("TestNestedLoopImplementation", False, "functional")
                print("TestNestedLoopImplementation = Failed")
            else:
                self.test_obj.yakshaAssert("TestNestedLoopImplementation", True, "functional")
                print("TestNestedLoopImplementation = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestNestedLoopImplementation", False, "functional")
            print("TestNestedLoopImplementation = Failed")

    def test_regional_analysis_functionality(self):
        """Test if analyze_regional_sales produces correct results"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestRegionalAnalysisFunctionality", False, "functional")
                print("TestRegionalAnalysisFunctionality = Failed")
                return
            
            errors = []
            
            # Check if required functions exist
            if not check_function_exists(self.module_obj, "analyze_regional_sales"):
                errors.append("Function analyze_regional_sales not found")
                self.test_obj.yakshaAssert("TestRegionalAnalysisFunctionality", False, "functional")
                print("TestRegionalAnalysisFunctionality = Failed")
                return
            
            # Try to get data from load_sales_data if it exists, otherwise use fallback
            data = None
            if check_function_exists(self.module_obj, "load_sales_data"):
                data = safely_call_function(self.module_obj, "load_sales_data")
            
            # Fallback data if load_sales_data doesn't exist or returns None
            if data is None:
                data = {
                    "North": {"Product A": 120, "Product B": 85, "Product C": 45},
                    "South": {"Product A": 95, "Product B": 110, "Product C": 30},
                    "East": {"Product A": 105, "Product B": 90, "Product C": 40},
                    "West": {"Product A": 130, "Product B": 120, "Product C": 50}
                }
            
            result = safely_call_function(self.module_obj, "analyze_regional_sales", data)
            if result is None:
                errors.append("analyze_regional_sales returned None - function not implemented")
                self.test_obj.yakshaAssert("TestRegionalAnalysisFunctionality", False, "functional")
                print("TestRegionalAnalysisFunctionality = Failed")
                return
            
            # Verify results format
            if not isinstance(result, dict):
                errors.append(f"analyze_regional_sales should return a dictionary, got {type(result)}")
            else:
                # Check if all regions are included
                if set(result.keys()) != set(data.keys()):
                    errors.append(f"Result should include all regions. Expected: {set(data.keys())}, Got: {set(result.keys())}")
                
                # Calculate expected totals manually and verify
                for region, products in data.items():
                    try:
                        expected_total = sum(products.values())
                        region_result = result.get(region)
                        
                        if region_result is None:
                            errors.append(f"Missing result for region {region}")
                        elif not isinstance(region_result, tuple) or len(region_result) != 2:
                            errors.append(f"Result for region {region} should be a tuple of (total, label), got {region_result}")
                        elif region_result[0] != expected_total:
                            errors.append(f"{region} total should be {expected_total}, got {region_result[0]}")
                    except (TypeError, AttributeError) as e:
                        errors.append(f"Error calculating total for region {region}: {str(e)}")
                
                # Verify highest and lowest regions are correctly marked
                try:
                    region_totals = {region: sum(products.values()) for region, products in data.items()}
                    highest_region = max(region_totals.items(), key=lambda x: x[1])[0]
                    lowest_region = min(region_totals.items(), key=lambda x: x[1])[0]
                    
                    for region, (total, label) in result.items():
                        if region == highest_region and label != "Highest performing region":
                            errors.append(f"{region} should be marked as highest performing region")
                        elif region == lowest_region and label != "Lowest performing region":
                            errors.append(f"{region} should be marked as lowest performing region")
                        elif region != highest_region and region != lowest_region and label != "":
                            errors.append(f"{region} should have an empty label, got '{label}'")
                except (TypeError, AttributeError, ValueError) as e:
                    errors.append(f"Error verifying region labels: {str(e)}")
            
            # Final assertion
            if errors:
                self.test_obj.yakshaAssert("TestRegionalAnalysisFunctionality", False, "functional")
                print("TestRegionalAnalysisFunctionality = Failed")
            else:
                self.test_obj.yakshaAssert("TestRegionalAnalysisFunctionality", True, "functional")
                print("TestRegionalAnalysisFunctionality = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestRegionalAnalysisFunctionality", False, "functional")
            print("TestRegionalAnalysisFunctionality = Failed")

    def test_product_analysis_functionality(self):
        """Test if analyze_product_performance produces correct results"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestProductAnalysisFunctionality", False, "functional")
                print("TestProductAnalysisFunctionality = Failed")
                return
            
            errors = []
            
            # Check if required functions exist
            if not check_function_exists(self.module_obj, "analyze_product_performance"):
                errors.append("Function analyze_product_performance not found")
                self.test_obj.yakshaAssert("TestProductAnalysisFunctionality", False, "functional")
                print("TestProductAnalysisFunctionality = Failed")
                return
            
            # Try to get data from load_sales_data if it exists, otherwise use fallback
            data = None
            if check_function_exists(self.module_obj, "load_sales_data"):
                data = safely_call_function(self.module_obj, "load_sales_data")
            
            # Fallback data if load_sales_data doesn't exist or returns None
            if data is None:
                data = {
                    "North": {"Product A": 120, "Product B": 85, "Product C": 45},
                    "South": {"Product A": 95, "Product B": 110, "Product C": 30},
                    "East": {"Product A": 105, "Product B": 90, "Product C": 40},
                    "West": {"Product A": 130, "Product B": 120, "Product C": 50}
                }
            
            result = safely_call_function(self.module_obj, "analyze_product_performance", data)
            if result is None:
                errors.append("analyze_product_performance returned None - function not implemented")
                self.test_obj.yakshaAssert("TestProductAnalysisFunctionality", False, "functional")
                print("TestProductAnalysisFunctionality = Failed")
                return
            
            # Verify results format
            if not isinstance(result, dict):
                errors.append(f"analyze_product_performance should return a dictionary, got {type(result)}")
            else:
                # Find all unique products in the data
                all_products = set()
                for products in data.values():
                    all_products.update(products.keys())
                
                # Check if all products are included
                if set(result.keys()) != all_products:
                    errors.append(f"Result should include all products. Expected: {all_products}, Got: {set(result.keys())}")
                
                # Calculate expected totals manually and verify
                for product in all_products:
                    try:
                        expected_total = 0
                        for region, products in data.items():
                            if product in products:
                                expected_total += products[product]
                        
                        product_result = result.get(product)
                        if product_result is None:
                            errors.append(f"Missing result for product {product}")
                        elif not isinstance(product_result, tuple) or len(product_result) != 2:
                            errors.append(f"Result for product {product} should be a tuple of (total, label), got {product_result}")
                        elif product_result[0] != expected_total:
                            errors.append(f"{product} total should be {expected_total}, got {product_result[0]}")
                    except (TypeError, AttributeError) as e:
                        errors.append(f"Error calculating total for product {product}: {str(e)}")
                
                # Get product totals and find top and bottom products
                try:
                    product_totals = {product: 0 for product in all_products}
                    for region, products in data.items():
                        for product, amount in products.items():
                            product_totals[product] += amount
                    
                    top_product = max(product_totals.items(), key=lambda x: x[1])[0]
                    bottom_product = min(product_totals.items(), key=lambda x: x[1])[0]
                    
                    for product, (total, label) in result.items():
                        if product == top_product and label != "Top product":
                            errors.append(f"{product} should be marked as top product")
                        elif product == bottom_product and label != "Bottom product":
                            errors.append(f"{product} should be marked as bottom product")
                        elif product != top_product and product != bottom_product and label != "":
                            errors.append(f"{product} should have an empty label, got '{label}'")
                except (TypeError, AttributeError, ValueError) as e:
                    errors.append(f"Error verifying product labels: {str(e)}")
            
            # Final assertion
            if errors:
                self.test_obj.yakshaAssert("TestProductAnalysisFunctionality", False, "functional")
                print("TestProductAnalysisFunctionality = Failed")
            else:
                self.test_obj.yakshaAssert("TestProductAnalysisFunctionality", True, "functional")
                print("TestProductAnalysisFunctionality = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestProductAnalysisFunctionality", False, "functional")
            print("TestProductAnalysisFunctionality = Failed")

    def test_required_functions_exist(self):
        """Test if all required functions exist with correct signatures and are implemented"""
        try:
            # Check if file exists
            if not check_file_exists("skeleton.py"):
                self.test_obj.yakshaAssert("TestRequiredFunctionsExist", False, "functional")
                print("TestRequiredFunctionsExist = Failed")
                return
            
            errors = []
            
            with open('skeleton.py', 'r') as file:
                content = file.read()
            
            required_functions = {
                'analyze_regional_sales': r'def\s+analyze_regional_sales\s*\(\s*sales_data\s*\)\s*:',
                'analyze_product_performance': r'def\s+analyze_product_performance\s*\(\s*sales_data\s*\)\s*:',
                'display_results': r'def\s+display_results\s*\(\s*results\s*,\s*analysis_type\s*\)\s*:',
                'load_sales_data': r'def\s+load_sales_data\s*\(\s*\)\s*:',
                'main': r'def\s+main\s*\(\s*\)\s*:'
            }
            
            missing_funcs = []
            
            # Check for function existence
            for func_name, pattern in required_functions.items():
                if not re.search(pattern, content):
                    missing_funcs.append(func_name)
            
            # Check if critical functions contain only 'pass' (skeleton implementation)
            critical_functions = ['analyze_regional_sales', 'analyze_product_performance']
            skeleton_funcs = []
            
            for func_name in critical_functions:
                func_match = re.search(rf'def\s+{func_name}.*?(?=def\s|\Z)', content, re.DOTALL)
                if func_match:
                    func_code = func_match.group(0)
                    # Remove comments, docstrings, and whitespace
                    lines = [line.strip() for line in func_code.split('\n')]
                    code_lines = []
                    in_docstring = False
                    
                    for line in lines:
                        if line.startswith('def ') or line.startswith('#') or not line:
                            continue
                        if '"""' in line or "'''" in line:
                            in_docstring = not in_docstring
                            continue
                        if not in_docstring:
                            code_lines.append(line)
                    
                    # If only 'pass' remains, it's a skeleton
                    if len(code_lines) == 1 and code_lines[0] == 'pass':
                        skeleton_funcs.append(func_name)
            
            if missing_funcs:
                errors.append(f"Missing functions or incorrect signatures: {', '.join(missing_funcs)}")
            
            if skeleton_funcs:
                errors.append(f"Functions are not implemented (contain only 'pass'): {', '.join(skeleton_funcs)}")
            
            if errors:
                self.test_obj.yakshaAssert("TestRequiredFunctionsExist", False, "functional")
                print("TestRequiredFunctionsExist = Failed")
            else:
                self.test_obj.yakshaAssert("TestRequiredFunctionsExist", True, "functional")
                print("TestRequiredFunctionsExist = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestRequiredFunctionsExist", False, "functional")
            print("TestRequiredFunctionsExist = Failed")

    def test_function_implementation_quality(self):
        """Test the quality of function implementations"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestFunctionImplementationQuality", False, "functional")
                print("TestFunctionImplementationQuality = Failed")
                return
            
            errors = []
            
            # Test with sample data to verify function behavior
            test_data = {
                "Region1": {"ProductA": 100, "ProductB": 200},
                "Region2": {"ProductA": 150, "ProductB": 50}
            }
            
            # Test regional analysis
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                regional_result = safely_call_function(self.module_obj, "analyze_regional_sales", test_data)
                if regional_result is not None:
                    # Check if results are properly formatted
                    for region, result_data in regional_result.items():
                        if not isinstance(result_data, tuple) or len(result_data) != 2:
                            errors.append(f"Regional analysis result for {region} should be a tuple of (total, label)")
                        else:
                            total, label = result_data
                            if not isinstance(total, (int, float)):
                                errors.append(f"Regional total for {region} should be a number, got {type(total)}")
                            if not isinstance(label, str):
                                errors.append(f"Regional label for {region} should be a string, got {type(label)}")
                else:
                    errors.append("analyze_regional_sales returned None - function may not be properly implemented")
            
            # Test product analysis
            if check_function_exists(self.module_obj, "analyze_product_performance"):
                product_result = safely_call_function(self.module_obj, "analyze_product_performance", test_data)
                if product_result is not None:
                    # Check if results are properly formatted
                    for product, result_data in product_result.items():
                        if not isinstance(result_data, tuple) or len(result_data) != 2:
                            errors.append(f"Product analysis result for {product} should be a tuple of (total, label)")
                        else:
                            total, label = result_data
                            if not isinstance(total, (int, float)):
                                errors.append(f"Product total for {product} should be a number, got {type(total)}")
                            if not isinstance(label, str):
                                errors.append(f"Product label for {product} should be a string, got {type(label)}")
                else:
                    errors.append("analyze_product_performance returned None - function may not be properly implemented")
            
            # Test load_sales_data
            if check_function_exists(self.module_obj, "load_sales_data"):
                data = safely_call_function(self.module_obj, "load_sales_data")
                if data is not None:
                    if not isinstance(data, dict):
                        errors.append(f"load_sales_data should return a dictionary, got {type(data)}")
                    else:
                        # Check data structure
                        for region, products in data.items():
                            if not isinstance(products, dict):
                                errors.append(f"Products for {region} should be a dictionary, got {type(products)}")
                            else:
                                for product, amount in products.items():
                                    if not isinstance(amount, (int, float)):
                                        errors.append(f"Sales amount for {region}/{product} should be a number, got {type(amount)}")
                else:
                    errors.append("load_sales_data returned None - function may not be properly implemented")
            
            # Final assertion
            if errors:
                self.test_obj.yakshaAssert("TestFunctionImplementationQuality", False, "functional")
                print("TestFunctionImplementationQuality = Failed")
            else:
                self.test_obj.yakshaAssert("TestFunctionImplementationQuality", True, "functional")
                print("TestFunctionImplementationQuality = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestFunctionImplementationQuality", False, "functional")
            print("TestFunctionImplementationQuality = Failed")

    def test_code_structure_analysis(self):
        """Test the overall code structure and best practices"""
        try:
            # Check if file exists
            if not check_file_exists("skeleton.py"):
                self.test_obj.yakshaAssert("TestCodeStructureAnalysis", False, "functional")
                print("TestCodeStructureAnalysis = Failed")
                return
            
            errors = []
            
            with open('skeleton.py', 'r') as file:
                content = file.read()
            
            # Check for proper error handling in functions
            if 'analyze_regional_sales' in content:
                regional_func = re.search(r'def\s+analyze_regional_sales.*?(?=def|\Z)', content, re.DOTALL)
                if regional_func:
                    func_code = regional_func.group(0)
                    
                    # Check if function is just skeleton
                    code_lines = [line.strip() for line in func_code.split('\n') 
                                 if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('def')]
                    
                    filtered_lines = []
                    in_docstring = False
                    for line in code_lines:
                        if '"""' in line or "'''" in line:
                            in_docstring = not in_docstring
                            continue
                        if not in_docstring:
                            filtered_lines.append(line)
                    
                    if len(filtered_lines) == 1 and filtered_lines[0] == 'pass':
                        errors.append("analyze_regional_sales function is not implemented (contains only 'pass')")
                    elif 'TypeError' not in func_code and 'ValueError' not in func_code:
                        errors.append("analyze_regional_sales should include proper error handling (TypeError/ValueError)")
            
            if 'analyze_product_performance' in content:
                product_func = re.search(r'def\s+analyze_product_performance.*?(?=def|\Z)', content, re.DOTALL)
                if product_func:
                    func_code = product_func.group(0)
                    
                    # Check if function is just skeleton
                    code_lines = [line.strip() for line in func_code.split('\n') 
                                 if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('def')]
                    
                    filtered_lines = []
                    in_docstring = False
                    for line in code_lines:
                        if '"""' in line or "'''" in line:
                            in_docstring = not in_docstring
                            continue
                        if not in_docstring:
                            filtered_lines.append(line)
                    
                    if len(filtered_lines) == 1 and filtered_lines[0] == 'pass':
                        errors.append("analyze_product_performance function is not implemented (contains only 'pass')")
                    elif 'TypeError' not in func_code:
                        errors.append("analyze_product_performance should include proper error handling")
            
            # Check for main function with proper structure
            if 'def main' in content:
                main_func = re.search(r'def\s+main.*?(?=def|\Z)', content, re.DOTALL)
                if main_func:
                    main_code = main_func.group(0)
                    
                    # Check if main function is just skeleton
                    code_lines = [line.strip() for line in main_code.split('\n') 
                                 if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('def')]
                    
                    filtered_lines = []
                    in_docstring = False
                    for line in code_lines:
                        if '"""' in line or "'''" in line:
                            in_docstring = not in_docstring
                            continue
                        if not in_docstring:
                            filtered_lines.append(line)
                    
                    if len(filtered_lines) == 1 and filtered_lines[0] == 'pass':
                        errors.append("main function is not implemented (contains only 'pass')")
                    else:
                        if 'while' not in main_code and 'for' not in main_code:
                            errors.append("main function should include a loop for menu interaction")
                        if 'try' not in main_code or 'except' not in main_code:
                            errors.append("main function should include try/except for error handling")
            
            # Check for proper variable naming conventions
            functions_to_check = ['analyze_regional_sales', 'analyze_product_performance']
            for func_name in functions_to_check:
                if func_name in content:
                    func_match = re.search(rf'def\s+{func_name}.*?(?=def|\Z)', content, re.DOTALL)
                    if func_match:
                        func_code = func_match.group(0)
                        
                        # Skip if function is just skeleton
                        code_lines = [line.strip() for line in func_code.split('\n') 
                                     if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('def')]
                        
                        filtered_lines = []
                        in_docstring = False
                        for line in code_lines:
                            if '"""' in line or "'''" in line:
                                in_docstring = not in_docstring
                                continue
                            if not in_docstring:
                                filtered_lines.append(line)
                        
                        if not (len(filtered_lines) == 1 and filtered_lines[0] == 'pass'):
                            # Check for meaningful variable names
                            if func_name == 'analyze_regional_sales':
                                if 'regional' not in func_code.lower():
                                    errors.append(f"{func_name} should use meaningful variable names related to regions")
                            elif func_name == 'analyze_product_performance':
                                if 'product' not in func_code.lower():
                                    errors.append(f"{func_name} should use meaningful variable names related to products")
            
            # Final assertion
            if errors:
                self.test_obj.yakshaAssert("TestCodeStructureAnalysis", False, "functional")
                print("TestCodeStructureAnalysis = Failed")
            else:
                self.test_obj.yakshaAssert("TestCodeStructureAnalysis", True, "functional")
                print("TestCodeStructureAnalysis = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestCodeStructureAnalysis", False, "functional")
            print("TestCodeStructureAnalysis = Failed")

if __name__ == '__main__':
    unittest.main()