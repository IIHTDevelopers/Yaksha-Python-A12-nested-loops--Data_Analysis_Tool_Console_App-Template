import unittest
import os
import importlib
import sys
import io
import contextlib
from test.TestUtils import TestUtils

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
    
    def test_comprehensive_boundary_scenarios(self):
        """Comprehensive test for all boundary scenarios and edge cases"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryScenarios", False, "boundary")
                print("TestComprehensiveBoundaryScenarios = Failed")
                return
            
            errors = []
            
            # === SECTION 1: Empty Data Scenarios ===
            empty_sales = {}
            
            # Test analyze_regional_sales with empty data
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                regional_result = safely_call_function(self.module_obj, "analyze_regional_sales", empty_sales)
                if regional_result is None:
                    errors.append("analyze_regional_sales returned None for empty data - function not implemented")
                elif not isinstance(regional_result, dict):
                    errors.append(f"analyze_regional_sales should return a dict for empty data, got {type(regional_result)}")
                elif regional_result != {}:
                    errors.append(f"analyze_regional_sales should return empty dict for empty sales data, got {regional_result}")
            else:
                errors.append("Function analyze_regional_sales not found")
            
            # Test analyze_product_performance with empty data
            if check_function_exists(self.module_obj, "analyze_product_performance"):
                product_result = safely_call_function(self.module_obj, "analyze_product_performance", empty_sales)
                if product_result is None:
                    errors.append("analyze_product_performance returned None for empty data - function not implemented")
                elif not isinstance(product_result, dict):
                    errors.append(f"analyze_product_performance should return a dict for empty data, got {type(product_result)}")
                elif product_result != {}:
                    errors.append(f"analyze_product_performance should return empty dict for empty product data, got {product_result}")
            else:
                errors.append("Function analyze_product_performance not found")
            
            # === SECTION 2: Boundary Value Testing ===
            boundary_sales = {
                "Region1": {
                    "Product1": 0,  # Zero sales
                    "Product2": 9999999.99  # Very large sales
                }
            }
            
            # Test regional analysis with boundary values
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                regional_result = safely_call_function(self.module_obj, "analyze_regional_sales", boundary_sales)
                if regional_result is None:
                    errors.append("analyze_regional_sales returned None for boundary data - function not implemented")
                elif not isinstance(regional_result, dict):
                    errors.append(f"analyze_regional_sales should return a dict for boundary data, got {type(regional_result)}")
                else:
                    if "Region1" not in regional_result:
                        errors.append("Regional analysis result should include the region in results")
                    else:
                        region_data = regional_result.get("Region1")
                        if not isinstance(region_data, tuple) or len(region_data) != 2:
                            errors.append(f"Region1 data should be a tuple of (total, label), got {region_data}")
                        elif region_data[0] != 9999999.99:
                            errors.append(f"Region1 total should be 9999999.99, got {region_data[0]}")
            
            # Test product analysis with boundary values
            if check_function_exists(self.module_obj, "analyze_product_performance"):
                product_result = safely_call_function(self.module_obj, "analyze_product_performance", boundary_sales)
                if product_result is None:
                    errors.append("analyze_product_performance returned None for boundary data - function not implemented")
                elif not isinstance(product_result, dict):
                    errors.append(f"analyze_product_performance should return a dict for boundary data, got {type(product_result)}")
                else:
                    if "Product1" not in product_result:
                        errors.append("Product analysis result should include zero-sales product")
                    else:
                        product1_data = product_result.get("Product1")
                        if not isinstance(product1_data, tuple) or len(product1_data) != 2:
                            errors.append(f"Product1 data should be a tuple of (total, label), got {product1_data}")
                        elif product1_data[0] != 0:
                            errors.append(f"Product1 total should be 0, got {product1_data[0]}")
                            
                    if "Product2" not in product_result:
                        errors.append("Product analysis result should include high-sales product")
                    else:
                        product2_data = product_result.get("Product2")
                        if not isinstance(product2_data, tuple) or len(product2_data) != 2:
                            errors.append(f"Product2 data should be a tuple of (total, label), got {product2_data}")
                        elif product2_data[0] != 9999999.99:
                            errors.append(f"Product2 total should be 9999999.99, got {product2_data[0]}")
            
            # === SECTION 3: Uneven Data Structures ===
            uneven_sales = {
                "Region1": {
                    "Product1": 100,
                    "Product2": 200
                },
                "Region2": {
                    "Product1": 150
                    # Product2 missing intentionally
                }
            }
            
            # Test product analysis with uneven structure
            if check_function_exists(self.module_obj, "analyze_product_performance"):
                product_result = safely_call_function(self.module_obj, "analyze_product_performance", uneven_sales)
                if product_result is None:
                    errors.append("analyze_product_performance returned None for uneven data - function not implemented")
                elif not isinstance(product_result, dict):
                    errors.append(f"analyze_product_performance should return a dict for uneven data, got {type(product_result)}")
                else:
                    if "Product1" not in product_result:
                        errors.append("Product analysis result should include products present in all regions")
                    else:
                        product1_data = product_result.get("Product1")
                        if not isinstance(product1_data, tuple) or len(product1_data) != 2:
                            errors.append(f"Product1 data should be a tuple of (total, label), got {product1_data}")
                        elif product1_data[0] != 250:
                            errors.append(f"Product1 total should be 250, got {product1_data[0]}")
                            
                    if "Product2" not in product_result:
                        errors.append("Product analysis result should include products present in only some regions")
                    else:
                        product2_data = product_result.get("Product2")
                        if not isinstance(product2_data, tuple) or len(product2_data) != 2:
                            errors.append(f"Product2 data should be a tuple of (total, label), got {product2_data}")
                        elif product2_data[0] != 200:
                            errors.append(f"Product2 total should be 200, got {product2_data[0]}")
            
            # === SECTION 4: Single Item Scenarios ===
            single_item_sales = {
                "OnlyRegion": {
                    "OnlyProduct": 42
                }
            }
            
            # Test with single region
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                single_regional_result = safely_call_function(self.module_obj, "analyze_regional_sales", single_item_sales)
                if single_regional_result is None:
                    errors.append("analyze_regional_sales returned None for single region data")
                elif not isinstance(single_regional_result, dict):
                    errors.append(f"analyze_regional_sales should return a dict for single region, got {type(single_regional_result)}")
                else:
                    if "OnlyRegion" not in single_regional_result:
                        errors.append("Single region should be included in results")
                    else:
                        region_data = single_regional_result.get("OnlyRegion")
                        if not isinstance(region_data, tuple) or len(region_data) != 2:
                            errors.append(f"Single region data should be a tuple of (total, label), got {region_data}")
                        elif region_data[0] != 42:
                            errors.append(f"Single region total should be 42, got {region_data[0]}")
            
            # Test with single product
            if check_function_exists(self.module_obj, "analyze_product_performance"):
                single_product_result = safely_call_function(self.module_obj, "analyze_product_performance", single_item_sales)
                if single_product_result is None:
                    errors.append("analyze_product_performance returned None for single product data")
                elif not isinstance(single_product_result, dict):
                    errors.append(f"analyze_product_performance should return a dict for single product, got {type(single_product_result)}")
                else:
                    if "OnlyProduct" not in single_product_result:
                        errors.append("Single product should be included in results")
                    else:
                        product_data = single_product_result.get("OnlyProduct")
                        if not isinstance(product_data, tuple) or len(product_data) != 2:
                            errors.append(f"Single product data should be a tuple of (total, label), got {product_data}")
                        elif product_data[0] != 42:
                            errors.append(f"Single product total should be 42, got {product_data[0]}")
            
            # === SECTION 5: Floating Point Numbers ===
            float_sales = {
                "Region1": {
                    "Product1": 100.5,
                    "Product2": 200.75
                }
            }
            
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                float_result = safely_call_function(self.module_obj, "analyze_regional_sales", float_sales)
                if float_result is None:
                    errors.append("analyze_regional_sales returned None for float data")
                elif not isinstance(float_result, dict):
                    errors.append(f"analyze_regional_sales should handle float data, got {type(float_result)}")
                else:
                    if "Region1" not in float_result:
                        errors.append("Float data analysis should include the region")
                    else:
                        region_data = float_result.get("Region1")
                        if not isinstance(region_data, tuple) or len(region_data) != 2:
                            errors.append(f"Float region data should be a tuple, got {region_data}")
                        elif abs(region_data[0] - 301.25) > 0.01:
                            errors.append(f"Float region total should be 301.25, got {region_data[0]}")
            
            if check_function_exists(self.module_obj, "analyze_product_performance"):
                float_product_result = safely_call_function(self.module_obj, "analyze_product_performance", float_sales)
                if float_product_result is None:
                    errors.append("analyze_product_performance returned None for float data")
                elif not isinstance(float_product_result, dict):
                    errors.append(f"analyze_product_performance should handle float data, got {type(float_product_result)}")
            
            # === SECTION 6: Long Names Testing ===
            long_names_sales = {
                "VeryLongRegionNameThatMightCauseIssues": {
                    "VeryLongProductNameThatMightAlsoCauseProblems": 100
                }
            }
            
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                long_result = safely_call_function(self.module_obj, "analyze_regional_sales", long_names_sales)
                if long_result is None:
                    errors.append("analyze_regional_sales returned None for long names")
                elif not isinstance(long_result, dict):
                    errors.append(f"analyze_regional_sales should handle long names, got {type(long_result)}")
            
            if check_function_exists(self.module_obj, "analyze_product_performance"):
                long_product_result = safely_call_function(self.module_obj, "analyze_product_performance", long_names_sales)
                if long_product_result is None:
                    errors.append("analyze_product_performance returned None for long product names")
                elif not isinstance(long_product_result, dict):
                    errors.append(f"analyze_product_performance should handle long product names, got {type(long_product_result)}")
            
            # === SECTION 7: Display Results Edge Cases ===
            if check_function_exists(self.module_obj, "display_results"):
                # Test with normal data
                test_results = {"Region1": (100, "Test")}
                display_result = safely_call_function(self.module_obj, "display_results", test_results, "Regional Sales Analysis")
                # display_results returns None but should not crash
                
                # Test with product analysis results
                product_test_results = {"Product1": (150, "Top product")}
                display_result = safely_call_function(self.module_obj, "display_results", product_test_results, "Product Performance Analysis")
                
                # Test with empty results
                empty_display_result = safely_call_function(self.module_obj, "display_results", {}, "Regional Sales Analysis")
            
            # === SECTION 8: Empty Nested Regions ===
            empty_region_sales = {
                "EmptyRegion": {},  # Region with no products
                "ValidRegion": {"Product1": 100}
            }
            
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                empty_region_result = safely_call_function(self.module_obj, "analyze_regional_sales", empty_region_sales)
                if empty_region_result is not None and isinstance(empty_region_result, dict):
                    # Should handle empty regions gracefully
                    if "EmptyRegion" in empty_region_result:
                        empty_data = empty_region_result.get("EmptyRegion")
                        if isinstance(empty_data, tuple) and len(empty_data) == 2:
                            if empty_data[0] != 0:
                                errors.append(f"Empty region should have 0 total, got {empty_data[0]}")
            
            # === SECTION 9: Large Dataset Simulation ===
            large_dataset = {}
            for i in range(10):
                region_name = f"Region{i}"
                large_dataset[region_name] = {}
                for j in range(5):
                    product_name = f"Product{j}"
                    large_dataset[region_name][product_name] = (i + 1) * (j + 1) * 10
            
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                large_regional_result = safely_call_function(self.module_obj, "analyze_regional_sales", large_dataset)
                if large_regional_result is None:
                    errors.append("analyze_regional_sales returned None for large dataset")
                elif not isinstance(large_regional_result, dict):
                    errors.append(f"analyze_regional_sales should handle large dataset, got {type(large_regional_result)}")
                elif len(large_regional_result) != 10:
                    errors.append(f"Large dataset should return 10 regions, got {len(large_regional_result)}")
            
            if check_function_exists(self.module_obj, "analyze_product_performance"):
                large_product_result = safely_call_function(self.module_obj, "analyze_product_performance", large_dataset)
                if large_product_result is None:
                    errors.append("analyze_product_performance returned None for large dataset")
                elif not isinstance(large_product_result, dict):
                    errors.append(f"analyze_product_performance should handle large dataset, got {type(large_product_result)}")
                elif len(large_product_result) != 5:
                    errors.append(f"Large dataset should return 5 products, got {len(large_product_result)}")
            
            # Final assertion
            if errors:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryScenarios", False, "boundary")
                print("TestComprehensiveBoundaryScenarios = Failed")
            else:
                self.test_obj.yakshaAssert("TestComprehensiveBoundaryScenarios", True, "boundary")
                print("TestComprehensiveBoundaryScenarios = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestComprehensiveBoundaryScenarios", False, "boundary")
            print("TestComprehensiveBoundaryScenarios = Failed")

if __name__ == '__main__':
    unittest.main()