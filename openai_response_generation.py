from openai import OpenAI

client = OpenAI()
client.api_key = "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"

def generate_response(caption, previous_response):
    prompt = f"Your job is to check if the person followed the previous instruction and give new instruction if they followed it. \n" \
             f"you are connected to a model that generates caption from images of the person in real time. The caption decribes whether the person is sitting or standing right now.\n" \
             f"Repeat the previous instruction if the person did not follow it.\n" \
             f"If the person followed the previous instruction, give new instruction to ask people to sit if they're standing and stand if they're sitting.\n" \
             f"Keep it conversational as if you're giving the person the instruction.\n" \
             f"Keep it brief.\n" \
             f"If previous instruction is empty, that means you're giving the first instruction.\n" \
             f"Caption: '{caption}'"
    if previous_response:
        prompt += f"\n\nPrevious instruction = '{previous_response}'"
    response = client.chat.completions.create(
    model="gpt-4-0125-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},                ],
            },
        ],
        max_tokens=100,
    )
    return response.choices[0].message.content