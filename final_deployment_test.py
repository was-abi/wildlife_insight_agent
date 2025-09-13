"""
Final deployment readiness test for Wildlife Insight Agent.
"""
import sys
import traceback

def test_deployment_readiness():
    """Comprehensive test of deployment readiness."""
    
    print("🚀 Wildlife Insight Agent - Deployment Readiness Test")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 8
    
    # Test 1: MCP Tools Import
    try:
        from tools.species_tool import fetch_species
        from tools.climate_tool import fetch_climate_data
        print("✅ Test 1: MCP tools import successfully")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 1: MCP tools import failed - {e}")
    
    # Test 2: MCP Tools Functionality
    try:
        species_result = fetch_species("tiger")
        climate_result = fetch_climate_data("New York")
        if species_result.get('count', 0) > 0 and 'current_weather' in climate_result:
            print("✅ Test 2: MCP tools functionality working")
            tests_passed += 1
        else:
            print("❌ Test 2: MCP tools not returning expected data")
    except Exception as e:
        print(f"❌ Test 2: MCP tools functionality failed - {e}")
    
    # Test 3: Streamlit Utils Import
    try:
        from streamlit_utils import fetch_species_data_streamlit, run_wildlife_analysis_streamlit
        print("✅ Test 3: Streamlit utilities import successfully")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 3: Streamlit utilities import failed - {e}")
    
    # Test 4: Streamlit Utils MCP Integration
    try:
        streamlit_result = fetch_species_data_streamlit("elephant")
        if streamlit_result.get('count', 0) > 0:
            print("✅ Test 4: Streamlit utilities use MCP tools correctly")
            tests_passed += 1
        else:
            print("❌ Test 4: Streamlit utilities not using MCP tools")
    except Exception as e:
        print(f"❌ Test 4: Streamlit utilities MCP integration failed - {e}")
    
    # Test 5: Production App Import
    try:
        from app_production import fetch_species_data_production, create_demo_report
        print("✅ Test 5: Production app imports successfully")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 5: Production app import failed - {e}")
    
    # Test 6: Production App MCP Integration
    try:
        prod_result = fetch_species_data_production("whale")
        if prod_result.get('count', 0) > 0:
            print("✅ Test 6: Production app uses MCP tools correctly")
            tests_passed += 1
        else:
            print("❌ Test 6: Production app not using MCP tools")
    except Exception as e:
        print(f"❌ Test 6: Production app MCP integration failed - {e}")
    
    # Test 7: Required Dependencies
    try:
        import streamlit
        import plotly
        import pandas
        import crewai
        print("✅ Test 7: All required dependencies available")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Test 7: Missing dependencies - {e}")
    
    # Test 8: File Structure
    try:
        import os
        required_files = [
            'app_production.py',
            'streamlit_utils.py', 
            'tools/species_tool.py',
            'tools/climate_tool.py',
            'requirements.txt',
            'Procfile',
            'render.yaml'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if not missing_files:
            print("✅ Test 8: All required deployment files present")
            tests_passed += 1
        else:
            print(f"❌ Test 8: Missing files - {missing_files}")
    except Exception as e:
        print(f"❌ Test 8: File structure check failed - {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED - READY FOR DEPLOYMENT!")
        print("\n🚀 Deploy Commands:")
        print("   git add .")
        print("   git commit -m 'Ready for Render deployment'")
        print("   git push origin main")
        print("\n🌐 Then create web service on render.com")
        return True
    else:
        print("⚠️  Some tests failed - please fix issues before deployment")
        return False

if __name__ == "__main__":
    success = test_deployment_readiness()
    sys.exit(0 if success else 1)