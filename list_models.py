import google.generativeai as genai

API_KEY = "AIzaSyBikQRfy4gPlQJQUdu7ZKZbm2o11VaO-ns"  # <--- Your Key
genai.configure(api_key=API_KEY)

print("Checking available models...")

try:
    # This asks Google: "What models can I use?"
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- Found Model: {m.name}")

except Exception as e:
    print("\n❌ CRITICAL ERROR: Your Key is invalid or blocked.")
    print(e)