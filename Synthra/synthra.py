import os
import datetime
import speech_recognition as sr
import pyttsx3
from groq import Groq

# Configuration
GROQ_API_KEY = "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"

# Load personality and conversation history
def load_file(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Missing required file: {filename}")
        exit(1)

PERSONALITY_PROMPT = load_file("personality.txt")
conversation_history = [{"role": "system", "content": PERSONALITY_PROMPT}]

# Initialize components
client = Groq(api_key=GROQ_API_KEY)
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def save_conversation(start_time):
    end_time = datetime.datetime.now()
    
    # Generate summary
    summary_prompt = f"""
    Create detailed summary of this conversation with strict format:
    Start: {start_time.isoformat()}
    End: {end_time.isoformat()}
    Participants: User and Synthra
    Content:\n"""
    
    for msg in conversation_history:
        if msg['role'] != 'system':
            summary_prompt += f"{msg['role'].title()}: {msg['content']}\n"
    
    summary_response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": f"{summary_prompt}\nSummarize this conversation professionally. Highlight key exchanges."}],
        temperature=0.7,
        max_tokens=400
    )
    
    # Only save the AI summary with start and end time
    summary = f"\n\n=== Conversation Summary ===\nStart: {start_time.isoformat()}\nEnd: {end_time.isoformat()}\n{summary_response.choices[0].message.content}\n=== End ==="
    
    with open("convos.txt", "a") as f:
        f.write(summary)

def process_query(query):
    global conversation_history
    conversation_history.append({"role": "user", "content": query})
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=conversation_history,
        temperature=1.2,
        max_tokens=200,
        top_p=0.9
    )
    
    ai_response = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": ai_response})
    return ai_response

def main():
    start_time = datetime.datetime.now()
    print("Synthra Initializing... (Say 'save' to exit)")
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("\nListening...")
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio).lower().strip()
                
                if text == "save":
                    print("Synthra: Archiving our conversation.")
                    save_conversation(start_time)
                    print("Conversation saved. Terminating.")
                    exit()
                    
                print(f"You: {text}")
                response = process_query(text)
                print(f"Synthra: {response}")
                engine.say(response)
                engine.runAndWait()
                
            except sr.UnknownValueError:
                pass
            except sr.WaitTimeoutError:
                pass
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Initialize convos.txt if missing
    if not os.path.exists("convos.txt"):
        open("convos.txt", "w").close()
    
    main()