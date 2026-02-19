from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product
import google.generativeai as genai

# --- CONFIGURATION ---
# This tells Python to look for a hidden password on the server
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def ask_ai(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_query = data.get('message', '')

            # 1. Search Database
            results = Product.objects.filter(name__icontains=user_query)
            
            # Prepare context for AI
            if results.exists():
                db_context = "INVENTORY DATA:\n"
                for p in results:
                    db_context += f"- {p.name} (Price: ₹{p.price}): {p.description}\n"
            else:
                db_context = None

            # 2. Ask AI (Google Gemini)
            # Use 'gemini-pro' as it is the most stable model
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            
            if db_context:
                # --- THIS IS WHERE THE ERROR LIKELY WAS ---
                # Ensure you have TRIPLE quotes (""") at start and end
                prompt = f"""
                You are a helpful sales assistant named 'Delta Tech AI'.
                
                We have these products in stock:
                {db_context}
                
                User Question: "{user_query}"
                
                Instructions:
                - Answer politely and naturally.
                - Mention prices in Rupees (₹).
                - Do not make up products not in the list.
                """
            else:
                prompt = f"""
                The user asked: "{user_query}"
                We do not have this in our database.
                Politely apologize and ask if they are looking for Laptops or Mice.
                """
            
            response = model.generate_content(prompt)
            return JsonResponse({'reply': response.text})

        except Exception as e:
            # This prints the REAL error to your Black Terminal Window
            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("🔥 CRITICAL ERROR:", e)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            return JsonResponse({'reply': "Sorry, my AI brain is offline."})