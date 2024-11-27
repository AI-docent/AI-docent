import openai

from ultralytics import YOLO

def prediction(model_path, image_path):
    model = YOLO(model_path)
    result = model(image_path)

    class_values = result[0].boxes.cls

    class_names = [model.names[int(cls)] for cls in class_values]

    return class_names[0]

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

if __name__ == "__main__":
    result = prediction("checkpoint/best.pt", "static/test.JPG")
    print("Detected Classes:", result)