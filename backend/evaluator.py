import json
import builtins

def safe_exec(code: str, globals=None):
    exec(code, globals)

def evaluate_code(problem_id: int, student_code: str):
    with open("problems.json", "r", encoding="utf-8") as f:
        problems = json.load(f)

    prob = problems[problem_id]
    tests = prob["tests"]
    passed = 0
    results = []

    for t in tests:
        input_data = t["input"]
        expected = t["output"]

        # Safe globals to prevent leaking state
        globals_dict = {}
        try:
            safe_exec(student_code + "\nresult = main" + input_data, globals_dict)
            actual = str(globals_dict["result"])
            test_pass = (actual == expected)
        except Exception as e:
            actual = f"Error: {str(e)}"
            test_pass = False

        results.append({
            "input": input_data,
            "expected": expected,
            "actual": actual,
            "passed": test_pass
        })

        if test_pass:
            passed += 1

    score = int(passed / len(tests) * 100)
    feedback = (
        "Excellent work!" if score == 100
        else "Your code fails on some test cases. Try to debug it."
    )

    return {
        "score": score,
        "feedback": feedback,
        "results": results,
        "description": prob["description"]
    }
