import os
import time
from datetime import timedelta
from groq import Groq
from tqdm import tqdm
import requests
import base64
import json

client = Groq(api_key="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")

def get_voice_list():
    """Fetches the list of available voices from FakeYou API and saves them to a file."""
    url = "https://api.fakeyou.com/tts/list"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        voices = data.get('models', [])
        
        # Save voices to a text file
        with open("available_voices.txt", "w", encoding="utf-8") as file:
            for voice in voices:
                file.write(f"{voice.get('title', 'Unknown')} ({voice.get('ietf_primary_language_tag', 'Unknown')}) - {voice.get('model_token', 'Unknown')}\n")
        
        print("Available voices saved to 'available_voices.txt'")
        return voices
    else:
        print("Failed to fetch voice list.")
        return None

def select_voice(voices):
    """Selects voice 291 from the list."""
    if len(voices) >= 291:
        return voices[290]['model_token']
    else:
        print("Voice 291 not available. Using default voice.")
        return "TM:8j10w4x4abfq"

def generate_podcast(topic):
    """Generates a short podcast on a given topic using Llama 3 8b model and FakeYou TTS."""

    podcast_content = ""
    start_time = time.monotonic()

    initial_prompt = f"""
    You are Alex Chen, the host of a short podcast called "Curious Minds". You're a 35-year-old former science teacher with a dry sense of humor and a knack for finding fascinating connections between seemingly unrelated topics. Your podcast is known for its laid-back, conversational style and unexpected insights.

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

    print("\nConverting text to speech using FakeYou API...")
    tts_url = "https://api.fakeyou.com/tts/inference"
    headers = {
        "Content-Type": "application/json",
    }
    
    # Fetch available voices and select voice 291
    voices = get_voice_list()
    if voices:
        voice_token = select_voice(voices)
    else:
        print("Using default voice token.")
        voice_token = "TM:8j10w4x4abfq"
    
    payload = {
        "tts_model_token": voice_token,
        "uuid_idempotency_token": str(time.time()),
        "inference_text": podcast_content
    }

    response = requests.post(tts_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        inference_job_token = response.json()['inference_job_token']
        
        # Poll for job completion
        while True:
            status_url = f"https://api.fakeyou.com/tts/job/{inference_job_token}"
            status_response = requests.get(status_url)
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                if status_data['state']['status'] == 'complete_success':
                    audio_url = status_data['state']['maybe_public_bucket_wav_audio_path']
                    break
                elif status_data['state']['status'] in ['attempt_failed', 'dead']:
                    print("TTS conversion failed.")
                    return
            
            time.sleep(5)  # Wait before polling again
        
        # Download the audio file
        audio_response = requests.get(f"https://storage.googleapis.com/vocodes-public{audio_url}")
        
        if audio_response.status_code == 200:
            with open(f"{topic}_podcast.wav", "wb") as audio_file:
                audio_file.write(audio_response.content)
            print("Audio file saved successfully!")
        else:
            print("Failed to download the audio file.")
    else:
        print("Failed to initiate TTS conversion.")

if __name__ == "__main__":
    topic = input("Enter the main topic for your short podcast: ")
    generate_podcast(topic)
    print("Podcast generation complete!")