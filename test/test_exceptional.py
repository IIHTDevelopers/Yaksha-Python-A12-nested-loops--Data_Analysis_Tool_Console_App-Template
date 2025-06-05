import unittest
import os
import importlib
import sys
import io
import contextlib
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

def check_raises(func, args, expected_exception=Exception):
    """Check if a function raises an expected exception."""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            func(*args)
        return False
    except expected_exception:
        return True
    except Exception:
        return False

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
    
    def test_comprehensive_error_handling(self):
        """Comprehensive test for all error handling scenarios"""
        try:
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestComprehensiveErrorHandling", False, "exception")
                print("TestComprehensiveErrorHandling = Failed")
                return
            
            errors = []
            
            # === SECTION 1: None Input Validation ===
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                func = getattr(self.module_obj, "analyze_regional_sales")
                result = check_raises(func, [None], TypeError)
                if not result:
                    errors.append("analyze_regional_sales does not raise TypeError with None input")
            else:
                errors.append("Function analyze_regional_sales not found")
            
            if check_function_exists(self.module_obj, "analyze_product_performance"):
                func = getattr(self.module_obj, "analyze_product_performance")
                result = check_raises(func, [None], TypeError)
                if not result:
                    errors.append("analyze_product_performance does not raise TypeError with None input")
            else:
                errors.append("Function analyze_product_performance not found")
            
            # === SECTION 2: Invalid Data Type Validation ===
            invalid_sales = {
                "Region1": {
                    "Product1": "100"  # String instead of number
                }
            }
            
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                func = getattr(self.module_obj, "analyze_regional_sales")
                result = check_raises(func, [invalid_sales], TypeError)
                if not result:
                    errors.append("analyze_regional_sales does not raise TypeError for string sales amounts")
            
            if check_function_exists(self.module_obj, "analyze_product_performance"):
                func = getattr(self.module_obj, "analyze_product_performance")
                result = check_raises(func, [invalid_sales], TypeError)
                if not result:
                    errors.append("analyze_product_performance does not raise TypeError for string sales amounts")
            
            # === SECTION 3: Negative Sales Validation (Only for analyze_regional_sales) ===
            negative_sales = {
                "Region1": {
                    "Product1": -100  # Negative sales
                }
            }
            
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                func = getattr(self.module_obj, "analyze_regional_sales")
                result = check_raises(func, [negative_sales], ValueError)
                if not result:
                    errors.append("analyze_regional_sales does not raise ValueError for negative sales amounts")
            
            # Note: analyze_product_performance may not validate negative values, so we test it gracefully
            if check_function_exists(self.module_obj, "analyze_product_performance"):
                # Just test that it doesn't crash - it may or may not validate negatives
                product_result = safely_call_function(self.module_obj, "analyze_product_performance", negative_sales)
                # If it returns None, that means it raised an exception (which is acceptable)
                # If it returns a result, that means it handled negatives gracefully (also acceptable)
            
            # === SECTION 4: Flat Dictionary Structure ===
            flat_structure = {
                "Region1": 100,
                "Region2": 200
            }
            
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                exception_raised = False
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.module_obj.analyze_regional_sales(flat_structure)
                except (TypeError, AttributeError, KeyError):
                    exception_raised = True
                except Exception:
                    exception_raised = True  # Any exception is acceptable for invalid structure
                    
                if not exception_raised:
                    errors.append("analyze_regional_sales should raise an exception for flat dictionary structure")
            
            # === SECTION 5: List Input Instead of Dict ===
            list_input = [("Region1", {"Product1": 100})]
            
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                exception_raised = False
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.module_obj.analyze_regional_sales(list_input)
                except (TypeError, AttributeError):
                    exception_raised = True
                except Exception:
                    exception_raised = True  # Any exception is acceptable
                    
                if not exception_raised:
                    errors.append("analyze_regional_sales should raise an exception for list input")
            
            # === SECTION 6: Mixed Data Types ===
            mixed_sales = {
                "Region1": {
                    "Product1": 100,
                    "Product2": None,  # None value
                    "Product3": "invalid"  # String value
                }
            }
            
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                exception_raised = False
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.module_obj.analyze_regional_sales(mixed_sales)
                except (TypeError, ValueError):
                    exception_raised = True
                except Exception:
                    exception_raised = True
                    
                if not exception_raised:
                    errors.append("analyze_regional_sales should raise an exception for mixed data types")
            
            # === SECTION 7: Complex Numbers ===
            complex_sales = {
                "Region1": {
                    "Product1": 100 + 2j  # Complex number
                }
            }
            
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                exception_raised = False
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.module_obj.analyze_regional_sales(complex_sales)
                except (TypeError, ValueError):
                    exception_raised = True
                except Exception:
                    exception_raised = True
                    
                if not exception_raised:
                    errors.append("analyze_regional_sales should raise an exception for complex numbers")
            
            # === SECTION 8: Display Results Error Handling ===
            if check_function_exists(self.module_obj, "display_results"):
                # Test with empty results
                safely_call_function(self.module_obj, "display_results", {}, "Regional Sales Analysis")
                
                # Test with invalid analysis type
                safely_call_function(self.module_obj, "display_results", {"Region1": (100, "")}, "Invalid Analysis Type")
                
                # Test with invalid results structure
                safely_call_function(self.module_obj, "display_results", {"Region1": 100}, "Regional Sales Analysis")
                
                # Test with None inputs
                safely_call_function(self.module_obj, "display_results", None, "Regional Sales Analysis")
                safely_call_function(self.module_obj, "display_results", {"Region1": (100, "")}, None)
            else:
                errors.append("Function display_results not found")
            
            # === SECTION 9: Empty Nested Dictionaries ===
            empty_nested = {
                "Region1": {},  # Empty products dict
                "Region2": {"Product1": 100}
            }
            
            if check_function_exists(self.module_obj, "analyze_regional_sales"):
                # This should either handle gracefully or raise an appropriate exception
                regional_result = safely_call_function(self.module_obj, "analyze_regional_sales", empty_nested)
                # If it returns None, that means it raised an exception (acceptable)
                # If it returns a result, it handled empty regions gracefully (also acceptable)
            
            if check_function_exists(self.module_obj, "analyze_product_performance"):
                # This should either handle gracefully or raise an appropriate exception
                product_result = safely_call_function(self.module_obj, "analyze_product_performance", empty_nested)
                # Same logic as above
            
            # Final assertion
            if errors:
                self.test_obj.yakshaAssert("TestComprehensiveErrorHandling", False, "exception")
                print("TestComprehensiveErrorHandling = Failed")
            else:
                self.test_obj.yakshaAssert("TestComprehensiveErrorHandling", True, "exception")
                print("TestComprehensiveErrorHandling = Passed")
                
        except Exception as e:
            self.test_obj.yakshaAssert("TestComprehensiveErrorHandling", False, "exception")
            print("TestComprehensiveErrorHandling = Failed")

if __name__ == '__main__':
    unittest.main()