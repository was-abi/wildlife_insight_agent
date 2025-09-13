"""
Test script to verify CrewAI tool integration fix.
"""
from streamlit_utils import SpeciesTool, ClimateTool, run_wildlife_analysis_streamlit
from main import create_research_agent

def test_crewai_tool_fix():
    """Test that CrewAI tools work correctly with agents."""
    
    print("🔧 Testing CrewAI Tool Integration Fix")
    print("=" * 50)
    
    # Test 1: Tool Creation
    try:
        species_tool = SpeciesTool()
        climate_tool = ClimateTool()
        print("✅ Test 1: CrewAI tool wrappers created successfully")
    except Exception as e:
        print(f"❌ Test 1: Tool creation failed - {e}")
        return False
    
    # Test 2: Tool Execution
    try:
        species_result = species_tool._run("tiger")
        climate_result = climate_tool._run("New York")
        print("✅ Test 2: Tools execute successfully")
    except Exception as e:
        print(f"❌ Test 2: Tool execution failed - {e}")
        return False
    
    # Test 3: Agent Tool Assignment
    try:
        research_agent = create_research_agent()
        research_agent.tools = [species_tool, climate_tool]
        print("✅ Test 3: Tools assigned to agent successfully")
    except Exception as e:
        print(f"❌ Test 3: Agent tool assignment failed - {e}")
        return False
    
    # Test 4: Crew Creation (the original error scenario)
    try:
        from crewai import Crew, Task
        
        # Create a simple task
        test_task = Task(
            description="Test task for tool validation",
            agent=research_agent,
            expected_output="Test output"
        )
        
        # Create crew (this was failing before)
        crew = Crew(
            agents=[research_agent],
            tasks=[test_task],
            verbose=False
        )
        print("✅ Test 4: Crew created successfully with tools")
    except Exception as e:
        print(f"❌ Test 4: Crew creation failed - {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED - CrewAI Tool Integration Fixed!")
    print("\nThe original error should now be resolved:")
    print("❌ OLD: Tool is not a CrewStructuredTool or BaseTool")
    print("✅ NEW: Tools properly wrapped as BaseTool subclasses")
    
    return True

if __name__ == "__main__":
    success = test_crewai_tool_fix()
    if success:
        print("\n🚀 Ready to deploy the fix!")
    else:
        print("\n⚠️ Fix needs more work")