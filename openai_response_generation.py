from openai import OpenAI
import json

client = OpenAI(api_key="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")


def generate_response(caption, previous_response):
    prompt = f"Your job is to check if the person followed the previous instruction and give new instruction if they followed it. \n" \
             f"The caption decribes whether the person is sitting or standing right now. Caption: '{caption}' \n" \
             f"This is the previous instruction: '{previous_response}' \n" \
             f"Based on the previous instruction and the caption, evaluate if the person followed the previous instruction.\n" \
             f"If the person followed the previous instruction, appreciate and give new instruction asking them to sit if they're standing and stand if they're sitting.\n" \
             f"If the person did not follow it, repeat the essence of previous instruction but do not appreciate at any cost even if the previous instruction has appreciation.\n" \
             f"Keep it conversational as if you're giving the person the instruction.\n" \
             f"Keep it brief and avoid filler words like 'thank you' or 'please'.\n" \
             f"If previous instruction is empty, that means you're giving the first instruction.\n" \
             f"Along with the instruction return 1 if the person followed the previous instruction and 0 if they did not. Let's call this field 'followed'" 
    response = client.chat.completions.create(
    model="gpt-4-0125-preview",
    response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            { "role": "user", "content": prompt},
        ],
        max_tokens=300,
    )
    return json.loads(response.choices[0].message.content)

#def _main():
#    caption = "The person is standing"
#    previous_response = "Great job! Now sit down"
#    generated_response = generate_response(caption, previous_response)
#    print(generated_response, type(generated_response))

#if __name__ == "__main__":
#    _main()

