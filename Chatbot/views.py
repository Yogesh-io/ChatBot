from django.shortcuts import render, redirect
from groq import Groq

client = Groq(api_key="You_Api_Key")


def chatbot_view(request):
    if 'chat_history' not in request.session:
        request.session['chat_history'] = [
            {"role": "system", "content": "You are a helpful and concise AI assistant."}
        ]

    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        
        if user_message:
            updated_history = request.session['chat_history']
            updated_history.append({"role": "user", "content": user_message})
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=updated_history,
                    temperature=0.7,
                    max_tokens=1024,
                )
                ai_response = completion.choices[0].message.content
                updated_history.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                updated_history.append({"role": "assistant", "content": f"Error: {str(e)}"})
            
            request.session['chat_history'] = updated_history
            request.session.modified = True
            
        return redirect('chatbot') 

    display_messages = [msg for msg in request.session['chat_history'] if msg['role'] != 'system']
    
    return render(request, 'chatbot.html', {'conversations': display_messages})

def clear_chat(request):
    if 'chat_history' in request.session:
        del request.session['chat_history']
    return redirect('chatbot')