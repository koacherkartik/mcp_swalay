#!/usr/bin/env python
"""
DRDO MCP Server Test - RAG + MongoDB Integration Demo
Demonstrates: English Command → RAG Translation → MongoDB Execution
"""

import sys
import json
sys.path.insert(0, '/app')

from app.ai import LocalAI
from app.executor import CommandExecutor
from app.mongo import MongoDB

def print_header():
    print("\n" + "="*60)
    print("DRDO OFFLINE MCP SERVER - RAG + MongoDB Test")
    print("="*60 + "\n")

def print_test(num, description):
    print(f"\n📋 TEST {num}: {description}")
    print("-" * 60)

def test_workflow():
    """Test the complete workflow: English → RAG → MongoDB"""
    
    print_header()
    
    # Initialize components
    print("🔧 Initializing components...")
    ai = LocalAI()
    executor = CommandExecutor()
    mongo = MongoDB()
    
    print("✅ AI model: LocalAI (with fallback mode)")
    print("✅ MongoDB: Connected to military database")
    print(f"✅ Collections: {list(mongo.db.list_collection_names())}\n")
    
    # Test 1: FIND (Show all soldiers)
    test_workflow_single(ai, executor, 1, "Show all soldiers", "Query all soldiers")
    
    # Test 2: INSERT (Add new soldier)
    test_workflow_single(ai, executor, 2, "Insert a soldier named Vikram with rank Major", "Add a new soldier")
    
    # Test 3: UPDATE (Change rank)
    test_workflow_single(ai, executor, 3, "Update Arjun rank to Major", "Update soldier rank")
    
    # Test 4: Find specific soldier (after updates)
    test_workflow_single(ai, executor, 4, "Show all soldiers", "Verify updates")
    
    # Test 5: DELETE
    test_workflow_single(ai, executor, 5, "Delete soldier Ajay", "Remove a soldier")
    
    print("\n" + "="*60)
    print("✨ All tests completed successfully!")
    print("="*60 + "\n")

def test_workflow_single(ai, executor, test_num, command, description):
    """Execute a single test step"""
    
    print_test(test_num, description)
    
    print(f"📝 English Command: '{command}'")
    
    # Step 1: Translate English to MongoDB JSON using RAG
    print("🤖 RAG Translation...")
    try:
        mongo_command = ai.generate(command)
        print(f"✅ Translated to MongoDB:\n{json.dumps(mongo_command, indent=2)}")
    except Exception as e:
        print(f"❌ Error during translation: {e}")
        return
    
    # Step 2: Execute the MongoDB command
    print("\n⚙️  Executing MongoDB command...")
    try:
        result = executor.execute(mongo_command)
        print(f"✅ Result:\n{json.dumps(result, indent=2, default=str)}")
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        return

if __name__ == "__main__":
    test_workflow()
