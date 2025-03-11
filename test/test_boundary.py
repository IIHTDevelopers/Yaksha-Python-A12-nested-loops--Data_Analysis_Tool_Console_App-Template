import pytest
from test.TestUtils import TestUtils
from data_analysis_tool_console import *  # Import all functions directly

@pytest.fixture
def test_obj():
    return TestUtils()

def test_boundary_scenarios(test_obj):
    """Consolidated test for all boundary scenarios"""
    try:
        # Test with empty data
        empty_sales = {}
        
        # Test analyze_regional_sales with empty data
        result = analyze_regional_sales(empty_sales)
        assert result == {}, "Should return empty dict for empty sales data"
        
        # Test analyze_product_performance with empty data
        result = analyze_product_performance(empty_sales)
        assert result == {}, "Should return empty dict for empty product data"
        
        # Test with boundary values
        boundary_sales = {
            "Region1": {
                "Product1": 0,  # Zero sales
                "Product2": 9999999.99  # Very large sales
            }
        }
        
        # Test regional analysis with boundary values
        result = analyze_regional_sales(boundary_sales)
        assert "Region1" in result, "Should include the region in results"
        assert result["Region1"][0] == 9999999.99, "Should handle large sales values"
        
        # Test product analysis with boundary values
        result = analyze_product_performance(boundary_sales)
        assert "Product1" in result, "Should include zero-sales product"
        assert result["Product1"][0] == 0, "Should handle zero sales"
        assert "Product2" in result, "Should include high-sales product"
        assert result["Product2"][0] == 9999999.99, "Should handle large sales values"
        
        # Test with uneven data structures
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
        result = analyze_product_performance(uneven_sales)
        assert "Product1" in result, "Should include products present in all regions"
        assert "Product2" in result, "Should include products present in only some regions"
        assert result["Product1"][0] == 250, "Should correctly calculate total for product in all regions"
        assert result["Product2"][0] == 200, "Should correctly calculate total for product in some regions"
        
        test_obj.yakshaAssert("TestBoundaryScenarios", True, "boundary")
    except Exception as e:
        test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
        pytest.fail(f"Boundary scenarios test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])