from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="9304539842f0fecc3a4e02ba36897f7f", 
)


def text_to_speech(text):
    audio = client.generate(text=text, voice="y6Ao4Y93UrnTbmzdVlFc")
    play(audio)
