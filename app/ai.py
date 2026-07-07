import json
import os
import ollama


class LocalAI:

    def __init__(self):

        self.model = "qwen2.5:7b-instruct"
        self.test_mode = os.getenv("TEST_MODE", "false").lower() == "true"

        self.system_prompt = """
You are an Offline MongoDB Command Translator.

Your ONLY task is to convert English commands into valid JSON.

Rules:

1. Return ONLY JSON.
2. Never explain anything.
3. Never use markdown.
4. Never add extra text.
5. Output must be valid JSON.
6. Use only these operations:
   - find
   - insert
   - update
   - delete

Database schema:

Database:
military

Collections:
- soldiers
- weapons
- vehicles

Examples:

User:
Show all soldiers

Output:
{
    "operation": "find",
    "collection": "soldiers",
    "filter": {}
}

User:
Delete soldier Rahul

Output:
{
    "operation": "delete",
    "collection": "soldiers",
    "filter": {
        "name": "Rahul"
    }
}

User:
Update Rahul rank to Major

Output:
{
    "operation": "update",
    "collection": "soldiers",
    "filter": {
        "name": "Rahul"
    },
    "update": {
        "rank": "Major"
    }
}

User:
Insert a soldier named Arjun with rank Captain

Output:
{
    "operation": "insert",
    "collection": "soldiers",
    "document": {
        "name": "Arjun",
        "rank": "Captain"
    }
}
"""

    def _parse_command(self, prompt):
        """Parse English command to MongoDB JSON"""
        prompt_lower = prompt.lower()
        
        # FIND operations
        if any(word in prompt_lower for word in ["show", "list", "get", "find", "display"]):
            # Determine collection
            collection = "soldiers"
            if "weapon" in prompt_lower:
                collection = "weapons"
            elif "vehicle" in prompt_lower:
                collection = "vehicles"
            
            return {
                "operation": "find",
                "collection": collection,
                "filter": {}
            }
        
        # DELETE operations
        elif "delete" in prompt_lower or "remove" in prompt_lower:
            collection = "soldiers"
            if "weapon" in prompt_lower:
                collection = "weapons"
            elif "vehicle" in prompt_lower:
                collection = "vehicles"
            
            # Extract name
            name = self._extract_name(prompt)
            return {
                "operation": "delete",
                "collection": collection,
                "filter": {"name": name} if name else {}
            }
        
        # UPDATE operations
        elif "update" in prompt_lower or "change" in prompt_lower or "modify" in prompt_lower:
            collection = "soldiers"
            name = self._extract_name(prompt)
            
            # Extract field to update
            update_data = {}
            if "rank" in prompt_lower:
                # Extract rank value
                words = prompt.split()
                for i, word in enumerate(words):
                    if word.lower() in ["major", "captain", "lieutenant", "colonel"]:
                        update_data["rank"] = word
                        break
            
            return {
                "operation": "update",
                "collection": collection,
                "filter": {"name": name} if name else {},
                "update": update_data
            }
        
        # INSERT operations
        elif "insert" in prompt_lower or "add" in prompt_lower or "create" in prompt_lower:
            collection = "soldiers"
            if "weapon" in prompt_lower:
                collection = "weapons"
            elif "vehicle" in prompt_lower:
                collection = "vehicles"
            
            name = self._extract_name(prompt)
            doc = {"name": name} if name else {}
            
            # Extract rank if mentioned
            if "rank" in prompt_lower:
                words = prompt.split()
                for i, word in enumerate(words):
                    if word.lower() in ["major", "captain", "lieutenant", "colonel"]:
                        doc["rank"] = word
                        break
            
            return {
                "operation": "insert",
                "collection": collection,
                "document": doc
            }
        
        # Default: find all
        return {
            "operation": "find",
            "collection": "soldiers",
            "filter": {}
        }

    def _extract_name(self, prompt):
        """Extract person/item name from prompt"""
        # Simple extraction - look for capitalized words
        words = prompt.split()
        for word in words:
            if word and word[0].isupper() and word.lower() not in ["show", "update", "delete", "insert", "soldier", "weapon", "vehicle", "to", "with", "named", "a", "an"]:
                return word
        return None

    def generate(self, prompt):
        """Generate MongoDB command from English prompt"""
        
        if self.test_mode:
            print("  [TEST MODE - Using mock AI]")
            return self._parse_command(prompt)

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = response["message"]["content"].strip()

            try:
                return json.loads(result)

            except json.JSONDecodeError:

                raise Exception(
                    "\nLLM returned invalid JSON.\n\n"
                    f"Response:\n{result}"
                )
        
        except Exception as e:
            print(f"  [Falling back to mock mode: {str(e)}]")
            return self._parse_command(prompt)