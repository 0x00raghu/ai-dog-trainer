from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="9304539842f0fecc3a4e02ba36897f7f", 
)


def text_to_speech(text):
    audio = client.generate(text=text, voice=Voice(voice_id="MmpYX2YKGFU5c1jMMF1q", settings=VoiceSettings(stability=1, similarity_boost=0.75, style=0.5, use_speaker_boost=True)), model="eleven_multilingual_v2", )
    play(audio)
