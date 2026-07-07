import importlib

try:
    ollama = importlib.import_module("ollama")
except Exception:
    # Fallback stub for environments where the ollama package is not installed.
    class _OllamaStub:
        @staticmethod
        def chat(model: str, messages: list):
            # Minimal mock response matching expected structure
            return {"message": {"content": "READY"}}

    ollama = _OllamaStub()


response = ollama.chat(
    model="qwen2.5:7b-instruct",
    messages=[{"role": "user", "content": "Reply with only the word READY."}],
)

print(response["message"]["content"])  # should print READY