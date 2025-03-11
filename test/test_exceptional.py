import pytest
import io
import sys
from test.TestUtils import TestUtils
from data_analysis_tool_console import *  # Import all functions directly

@pytest.fixture
def test_obj():
    return TestUtils()

def test_error_handling_data_validation(test_obj):
    """Consolidated test for error handling with invalid data"""
    try:
        # Test with None input
        with pytest.raises(TypeError):
            analyze_regional_sales(None)
            
        with pytest.raises(TypeError):
            analyze_product_performance(None)
            
        # Test with invalid sales amount (string instead of number)
        invalid_sales = {
            "Region1": {
                "Product1": "100"  # String instead of number
            }
        }
        
        with pytest.raises(TypeError):
            analyze_regional_sales(invalid_sales)
        
        # Test with negative sales amount
        negative_sales = {
            "Region1": {
                "Product1": -100  # Negative sales
            }
        }
        
        with pytest.raises(ValueError):
            analyze_regional_sales(negative_sales)
        
        # Test with flat dictionary instead of nested
        flat_structure = {
            "Region1": 100,
            "Region2": 200
        }
        
        # This should raise a proper exception for invalid structure
        with pytest.raises((TypeError, AttributeError, KeyError)):
            analyze_regional_sales(flat_structure)
            
        test_obj.yakshaAssert("TestErrorHandlingDataValidation", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestErrorHandlingDataValidation", False, "exception")
        pytest.fail(f"Error handling test failed: {str(e)}")

def test_display_results_handling(test_obj):
    """Consolidated test for display_results error handling"""
    try:
        # Capture stdout to prevent unnecessary output during tests
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Test with empty results
        display_results({}, "Regional Sales Analysis")
        
        # Test with invalid analysis type
        display_results({"Region1": (100, "")}, "Invalid Analysis Type")
        
        # Test with invalid results structure
        try:
            display_results({"Region1": 100}, "Regional Sales Analysis")
            # If we get here without exception, function handles it gracefully
        except (TypeError, AttributeError, ValueError):
            # These are acceptable exceptions for invalid results
            pass
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        test_obj.yakshaAssert("TestDisplayResultsHandling", True, "exception")
    except Exception as e:
        sys.stdout = sys.__stdout__  # Reset stdout in case of exception
        test_obj.yakshaAssert("TestDisplayResultsHandling", False, "exception")
        pytest.fail(f"Display results handling test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])