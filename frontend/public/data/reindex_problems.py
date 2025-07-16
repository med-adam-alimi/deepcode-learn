import json

# Load cleaned file
with open("cleaned_structured_problems.json", "r", encoding="utf-8") as f:
    problems = json.load(f)

# Re-index
for index, problem in enumerate(problems, start=1):
    problem["id"] = f"problem-{index}"
    problem["title"] = f"Problem {index}"

# Save updated version
with open("reindexed_problems.json", "w", encoding="utf-8") as f:
    json.dump(problems, f, indent=2)

print(f"✅ Re-indexed {len(problems)} problems and saved to reindexed_problems.json")
