import openai

from ultralytics import YOLO

def prediction(model_path, image_path):
    model = YOLO(model_path)
    result = model(image_path)

    return result

# 필요 없을수도....?
def chat_gpt(api_key, content):
    openai.api_key = api_key

    chat = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role":"user", "content":f"{content}"},
        ],
        temperature=0,
        max_tokens=2048
    )
    return chat

