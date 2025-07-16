from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

# Local loading of DeepSeek Coder 1.3B
MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"

print("⏳ Loading model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",  # or "cpu" if you have no GPU
    torch_dtype=torch.float16,  # fallback to float32 if needed
    trust_remote_code=True
)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

def call_deepseek(prompt: str, max_tokens: int = 512) -> str:
    formatted_prompt = f"<|user|>\n{prompt}\n<|assistant|>\n"
    output = pipe(
        formatted_prompt,
        max_new_tokens=max_tokens,
        temperature=0.2,
        do_sample=True,
        top_p=0.9,
    )
    return output[0]["generated_text"].split("<|assistant|>")[-1].strip()

