import asyncio
import websockets
import json
import base64
from openai import AsyncOpenAI
import shutil
import os
import subprocess

OPENAI_API_KEY = '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'
ELEVENLABS_API_KEY = '9304539842f0fecc3a4e02ba36897f7f'
VOICE_ID = 'MmpYX2YKGFU5c1jMMF1q'

# Set OpenAI API key
aclient = AsyncOpenAI(api_key=OPENAI_API_KEY)

def is_installed(lib_name):
    return shutil.which(lib_name) is not None

async def text_chunker(chunks):
    """Split text into chunks, ensuring to not break sentences."""
    splitters = (".", ",", "?", "!", ";", ":", "—", "-", "(", ")", "[", "]", "}", " ")
    buffer = ""

    async for text in chunks:
        if text is not None:
            if buffer.endswith(splitters):
                yield buffer + " "
                buffer = text
            elif text.startswith(splitters):
                yield buffer + text[0] + " "
                buffer = text[1:]
            else:
                buffer += text

    if buffer:
        yield buffer + " "

async def stream(audio_stream):
    """Stream audio data using mpv player."""
    if not is_installed("mpv"):
        raise ValueError(
            "mpv not found, necessary to stream audio. "
            "Install instructions: https://mpv.io/installation/"
        )

    mpv_process = subprocess.Popen(
        ["mpv", "--no-cache", "--no-terminal", "--", "fd://0"],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    print("Started streaming audio")
    async for chunk in audio_stream:
        if chunk:
            mpv_process.stdin.write(chunk)
            mpv_process.stdin.flush()

    if mpv_process.stdin:
        mpv_process.stdin.close()
    mpv_process.wait()


async def text_to_speech_input_streaming(voice_id, text_iterator):
    """Send text to ElevenLabs API and stream the returned audio."""
    uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id=eleven_turbo_v2"

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "text": " ",
            "voice_settings": {"stability": 1, "similarity_boost": 0.75, "style": 0.5, "use_speaker_boost": True},
            "xi_api_key": ELEVENLABS_API_KEY,
        }))

        async def listen():
            """Listen to the websocket for audio data and stream it."""
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if data.get("audio"):
                        yield base64.b64decode(data["audio"])
                    elif data.get('isFinal'):
                        break
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed")
                    break

        listen_task = asyncio.create_task(stream(listen()))

        async for text in text_chunker(text_iterator):
            await websocket.send(json.dumps({"text": text, "try_trigger_generation": True}))

        await websocket.send(json.dumps({"text": ""}))

        await listen_task

async def appreciate(previous_instruction):
    prompt = f"Appreciate the person for following the action in the instruction: '{previous_instruction}, ask them to 'have the treat and get ready for the next instruction' \n" \
             f"Respond as if you're talking to the person. Get to the point. Don't be thankful."
    response = await aclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        stream=True
    )

    async def text_iterator():
        async for chunk in response:
            delta = chunk.choices[0].delta
            yield delta.content

    await text_to_speech_input_streaming(VOICE_ID, text_iterator())

# async def reward(previous_instruction):
#     # print("rotating")
#     # rotate_thread = threading.Thread(target=rotate_60_degrees)
#     # rotate_thread.start()    
#     await appreciate(previous_instruction)  # Await the coroutine directly
# #    rotate_thread.join()  # Wait for rotation to complete

# def main():
#     previous_instruction = "Sit down."
#     print("starting reward")
#     asyncio.run(reward(previous_instruction)) # drop treat + appreciate (implement streaming)


# if __name__ == '__main__':
#     main()


