import google.generativeai as genai

# 1. SETUP KEY
API_KEY ="AIzaSyBikQRfy4gPlQJQUdu7ZKZbm2o11VaO-ns" # <-- Paste your "AIza..." key inside these quotes
genai.configure(api_key=API_KEY)

print("Testing API Key...")

try:
    # 2. TRY TO CONNECT
    model = genai.GenerativeModel('models/gemini-2.5-pro')
    response = model.generate_content("Hello, are you working?")
    
    # 3. SUCCESS?
    print("\n✅ SUCCESS! The API Key is working.")
    print("AI Replied:", response.text)

except Exception as e:
    # 4. FAILURE?
    print("\n❌ ERROR: The Key failed.")
    print("Error Details:", e)