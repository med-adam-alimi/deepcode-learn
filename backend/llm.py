from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import difflib

MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"

print("⏳ Loading model...")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device set to: {device}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    trust_remote_code=True
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

print("✅ Model loaded successfully!")

def call_deepseek(prompt: str, max_tokens: int = 512) -> str:
    outputs = pipe(prompt, max_new_tokens=max_tokens, do_sample=False)
    return outputs[0]["generated_text"].strip()



def evaluate_code_with_tests(code: str, test_cases: list[dict], 
                             weight_tests=0.7, weight_similarity=0.3,
                             feedback=True) -> dict:
    output_log = ""
    passed = 0

    for i, test in enumerate(test_cases):
        prompt = f"""You are a code executor.
Execute the following code and return only the output, assuming the input is:

Input:
{test['input']}

Code:
{code}

Only return the raw output with no explanation.
"""
        try:
            llm_output = call_deepseek(prompt, max_tokens=256).strip()
        except Exception as e:
            llm_output = f"Error: {str(e)}"

        expected = test['output'].strip()
        actual = llm_output.strip()
        if expected == actual:
            passed += 1

        output_log += f"Test {i+1}:\nInput: {test['input']}\nExpected: {expected}\nLLM Output: {actual}\n\n"

    # 🧠 Ideal code generation
    generate_prompt = f"""Given the following test cases, write a correct function that satisfies them:

Test Cases:
{test_cases}

Only return the raw code."""

    ideal_code = call_deepseek(generate_prompt, max_tokens=512)
    similarity = calculate_similarity(code, ideal_code)
    total = len(test_cases)
    test_score = (passed / total) if total else 0
    final_score = round((weight_tests * test_score + weight_similarity * similarity) * 100, 2)

    result = {
        "output_log": output_log.strip(),
        "passed": passed,
        "total": total,
        "score": final_score,
        "similarity": similarity,
        "ideal_code": ideal_code,
    }

    if feedback:
        if passed == total:
            result["feedback"] = "✅ All tests passed! Great job."
        else:
            failed = [f"❌ Test {i+1}: Input={t['input']}, Expected={t['output']}, Got={call_deepseek(prompt)}" 
                      for i, t in enumerate(test_cases) if t['output'].strip() != call_deepseek(prompt).strip()]
            result["feedback"] = "\n".join(failed)

    return result




def calculate_similarity(code1: str, code2: str) -> float:
    """
    Returns a float in range [0, 1] indicating how similar code1 and code2 are.
    """
    return difflib.SequenceMatcher(None, code1.strip(), code2.strip()).ratio()

