import json
import re

input_file = "reindexed_problems.json"
output_file = "final_enhanced_problems.json"

def extract_short_description(description: str) -> str:
    lines = description.splitlines()

    # Step 1: Look for line starting with "Return", "Task:", etc.
    for line in lines:
        line = line.strip()
        if re.match(r"^(Return|return|Task:|The task is to)", line):
            return line

    # Step 2: Use the first meaningful line (not a def, import, or comment)
    for line in lines:
        line = line.strip()
        if line and not line.startswith(("def ", "import ", "#")) and len(line) > 20:
            return line

    # Step 3: Fallback if nothing found
    return "Solve the coding task described below."

# Load data
with open(input_file, "r", encoding="utf-8") as f:
    problems = json.load(f)

# Update short_description
for problem in problems:
    problem["short_description"] = extract_short_description(problem["description"])

# Save enhanced data
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(problems, f, indent=2)

print(f"✅ Enhanced short descriptions saved to {output_file}")
