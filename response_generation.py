from openai import OpenAI
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs
import time

openai_client = OpenAI(api_key="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")
elevenlabs_client = ElevenLabs(
  api_key="9304539842f0fecc3a4e02ba36897f7f", 
)

def next_instruction(previous_instruction):
    prompt = f"If the previous instruction is to sit down, ask the person to stand up. \n" \
             f"If the previous instruction is to stand up, then ask the person to sit down. \n" \
             f"This is the previous instruction: '{previous_instruction}' \n" \
             f"Keep it conversational as if you're giving the person the instruction.\n" \
             f"Keep it brief and avoid filler words like 'thank you' or 'please'."
    current_time = time.time() # track current time for processing time comparison
    response = openai_client.chat.completions.create(
    model="gpt-4-turbo",
        messages=[
            { "role": "user", "content": prompt}
        ],
        max_tokens=50,
    )
    next_ins = response.choices[0].message.content
    print(next_ins)
    print("instruction gen time", time.time()-current_time)   
    text_to_speech(next_ins)
    return next_ins

def text_to_speech(text):
    try:
        current_time = time.time() # track current time for processing time comparison
        audio = elevenlabs_client.generate(text=text, voice=Voice(voice_id="MmpYX2YKGFU5c1jMMF1q", settings=VoiceSettings(stability=1, similarity_boost=0.75, style=0.5, use_speaker_boost=True)), model="eleven_multilingual_v2", )     
#        audio = elevenlabs_client.generate(text=text, voice=Voice(voice_id="MmpYX2YKGFU5c1jMMF1q", settings=VoiceSettings(stability=1, similarity_boost=0.75, style=0.5, use_speaker_boost=True)), model="eleven_turbo_v2", )     
        play(audio)
        print("speech time", time.time()-current_time)   
    except Exception as e:
        print("An error occurred:", e)

def appreciate(previous_instruction):
    prompt = f"Appreciate the person for following the action in the instruction: '{previous_instruction}, ask them to 'have the treat and get ready for the next instruction' \n" \
             f"Respond as if you're talking to the person. Get to the point. Don't be thankful."
    current_time = time.time() # track current time for processing time comparison
    response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
        messages=[
            { "role": "user", "content": prompt}
        ],
        max_tokens=50,
    )
    print("aprreciation gen time", time.time()-current_time)   
    text_to_speech(response.choices[0].message.content)