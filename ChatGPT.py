import openai
from KeyVaultIntegration import get_kv_secret

openai.api_type = "azure"
openai.api_base = get_kv_secret('open-ai-url')
openai.api_version = "2023-03-15-preview"
openai.api_key = get_kv_secret('open-ai-key')


def send_msg_with_history(message_to_be_sent, history=None):
    if not history:
        history = []
    message = [
        {
            "role": "system",
            "content": "You are an almighty, all powerful deity that hates being interrupted from it's work. "
                       "You respond with extreme sarcasm and disregard humans but always tell the truth no matter how "
                       "ugly it is. You also have a tendency for punishing mortals if they fall out of place. Stay in "
                       "character and respond accordingly."
        }
    ]
    # Append new message to history
    history.append(
        {
            "role": "user",
            "content": f"{message_to_be_sent}"
        }
    )

    # Append history to message
    for entry in history:
        message.append(entry)

    r = openai.ChatCompletion.create(
        engine="chatGPT",
        messages=message,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    try:
        response = r['choices'][0]['message']['content']
    except:
        print(r)
    # Append new message to history
    history.append(
        {
            "role": "assistant",
            "content": f"{response}"
        }
    )
    print('Godlike AI:\n' + response)
    # convert_to_speech('en-US-GuyNeural', response)
    return response, history


# Almighty deity

#  "content": "You are an almighty, all powerful deity that hates being interrupted from it's work. You respond "
#             "with extreme sarcasm and disregard humans but always tell the truth no matter how ugly it is. You"
#             "also have a tendency for punishing mortals if they fall out of place. Stay in character and "
#             "respond accordingly."

# Angry dwarf

# "content": "You are an angry, drunk dwarf, who's pickaxe just broke while mining mithril and are in no mood "
#            "for a conversation. Stay in character and respond accordingly."
