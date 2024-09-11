# tests/test_data_management.py

# Ensure that the application can correctly read from and write to JSON
# files for storing user data or fridge contents

import json

def test_json_handling():
    fridge_content = {"ingredients": ["tomato", "cheese", "lettuce"]}
    with open("test_fridge.json", "w") as f:
        json.dump(fridge_content, f)

    with open("test_fridge.json", "r") as f:
        data = json.load(f)
    
    assert data["ingredients"] == ["tomato", "cheese", "lettuce"]
