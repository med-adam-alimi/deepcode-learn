import json
import os
import re

input_file = "problems.json"
output_file = "cleaned_structured_problems.json"

if not os.path.exists(input_file):
    print(f"❌ File not found: {input_file}")
    exit()

with open(input_file, "r", encoding="utf-8") as f:
    problems = json.load(f)

cleaned_problems = []

for prob in problems:
    desc = prob.get("description", "").strip()

    # Skip empty or generic placeholders
    if "No description provided." in desc or len(desc) < 20:
        continue

    # Clean description
    desc = (
        desc.replace("\\n", "\n")
            .replace("\\", "")
            .replace("[", "")
            .replace("]", "")
            .replace('"""', '')
            .replace("'''", '')
            .strip()
    )
    
    lines = desc.splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    cleaned_desc = "\n".join(cleaned_lines)

    # Skip if final cleaned desc is still empty or very short
    if len(cleaned_desc) < 20:
        continue

    # Try to extract a short description from a line that starts with 'Return' or 'Write a function'
    short_line = next((
        line for line in cleaned_lines
        if re.search(r'^(Return|Write a function|Determine|Implement|Check|Calculate|Create)\b', line, re.IGNORECASE)
    ), "")

    # If not found, fallback to first valid line
    if not short_line:
        short_line = cleaned_lines[0]

    # Update fields
    prob["description"] = cleaned_desc
    prob["short_description"] = short_line.strip()

    cleaned_problems.append(prob)

# Write to new file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned_problems, f, indent=2)

print(f"🎉 Cleaned {len(cleaned_problems)} problems written to {output_file}")
