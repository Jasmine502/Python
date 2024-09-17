import os
import time
from datetime import timedelta
from groq import Groq
from tqdm import tqdm
import pyttsx3

client = Groq(api_key="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")

def generate_podcast(topic):
    """Generates a short podcast on a given topic using Llama 3 8b model and Windows TTS."""

    podcast_content = ""
    start_time = time.monotonic()

    initial_prompt = f"""
    You are Alex Chen, the host of a short podcast called "Curious Minds". You're a female 35-year-old former science teacher with a dry sense of humor and a knack for finding fascinating connections between seemingly unrelated topics. Your podcast is known for its laid-back, conversational style and unexpected insights.

    Today, you're discussing {topic}. Keep your content engaging and interesting for about 2-3 minutes. Use your unique perspective to explore related ideas and sprinkle in some of your trademark humor. Remember to speak naturally, as if you're having a conversation with a friend. Don't include any stage directions or non-verbal cues - just your speech.

    Feel free to draw from your experiences as a teacher or any amusing anecdotes from your life that relate to the topic. Your goal is to make the listeners feel like they're learning something new while enjoying a chat with a witty friend.
    """

    total_duration = 60  # 1 minute in seconds
    max_attempts = 3
    
    with tqdm(total=total_duration, desc="Generating Podcast", unit="s") as pbar:
        for attempt in range(max_attempts):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": initial_prompt},
                    ],
                    model="llama3-8b-8192",
                    max_tokens=500,  # Limit token count for faster generation
                )
                generated_text = chat_completion.choices[0].message.content
                podcast_content += generated_text

                # Update progress bar
                elapsed_time = min(total_duration, int(time.monotonic() - start_time))
                pbar.update(elapsed_time - pbar.n)

                if elapsed_time >= total_duration:
                    break

            except Exception as e:
                print(f"\nError during generation (attempt {attempt + 1}): {e}")
                if attempt == max_attempts - 1:
                    print("Max attempts reached. Stopping generation.")
                    break
                time.sleep(1)  # Wait before retrying

    print("\nConverting text to speech using Windows TTS...")
    
    # Initialize the TTS engine
    engine = pyttsx3.init()
    
    # Set properties
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    
    # Select Zira voice
    voices = engine.getProperty('voices')
    for voice in voices:
        if "Zira" in voice.name:
            engine.setProperty('voice', voice.id)
            break
    
    # Save to file
    output_file = f"{topic}_podcast.wav"
    engine.save_to_file(podcast_content, output_file)
    engine.runAndWait()
    
    print(f"Audio file saved as {output_file}")

if __name__ == "__main__":
    topic = input("Enter the main topic for your short podcast: ")
    generate_podcast(topic)
    print("Podcast generation complete!")