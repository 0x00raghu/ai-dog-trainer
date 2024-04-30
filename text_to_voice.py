from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="9304539842f0fecc3a4e02ba36897f7f", 
)


def text_to_speech(text):
    audio = client.generate(text=text, voice="MmpYX2YKGFU5c1jMMF1q")
    play(audio)
