import traceback
import textwrap

# Define test cases (for now we hardcode them)
PROBLEMS = {
    "reverse_string": {
        "description": "Write a function that reverses a string.",
        "tests": [
            {"input": "'hello'", "expected": "olleh"},
            {"input": "'world'", "expected": "dlrow"}
        ],
        "reference_solution": "def reverse_string(s): return s[::-1]"
    }
}

def run_student_code(problem_id: str, student_code: str):
    problem = PROBLEMS.get(problem_id)
    if not problem:
        return {"error": "Problem not found."}

    # Build the full Python code to run
    wrapped_code = textwrap.dedent(f"""
    {student_code}

    def run_tests():
        results = []
    """)

    for idx, test in enumerate(problem["tests"], 1):
        wrapped_code += f"""
        try:
            result = reverse_string({test['input']})
            results.append(f"Test {idx}: {{'✅ Passed' if result == '{test['expected']}' else '❌ Failed: expected {test['expected']}, got {{result}}'}}")
        except Exception as e:
            results.append(f"Test {idx}: ❌ Error: {{str(e)}}")
        """

    wrapped_code += """
        return results

    output = run_tests()
    for res in output:
        print(res)
    """

    # Write and execute code in sandboxed subprocess
    with open("temp_code.py", "w") as f:
        f.write(wrapped_code)

    import subprocess

    try:
        result = subprocess.run(
            ["python", "temp_code.py"],
            capture_output=True,
            text=True,
            timeout=5
        )
        output_lines = result.stdout.strip().split("\n")

        # Count correct tests
        passed = sum(1 for line in output_lines if "✅ Passed" in line)
        total = len(problem["tests"])

        feedback = (
            "✅ Great job! All tests passed."
            if passed == total
            else "❌ Some tests failed. Try again!"
        )

        return {
            "score": f"{passed}/{total}",
            "feedback": feedback,
            "results": output_lines,
            "reference_solution": problem["reference_solution"]
        }

    except subprocess.TimeoutExpired:
        return {"error": "⏰ Execution timed out."}
    except Exception as e:
        return {"error": f"💥 Execution error: {str(e)}"}
