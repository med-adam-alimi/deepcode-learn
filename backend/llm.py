from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch # type: ignore

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
    formatted_prompt = f"<|user|>\n{prompt.strip()}\n<|assistant|>\n"
    output = pipe(
        formatted_prompt,
        max_new_tokens=max_tokens,
        temperature=0.2,
        do_sample=True,
        top_p=0.9,
    )
    return output[0]["generated_text"].split("<|assistant|>")[-1].strip()
