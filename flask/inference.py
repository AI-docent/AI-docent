import openai

from ultralytics import YOLO

def prediction(model_path, image_path):
    model = YOLO(model_path)
    result = model(image_path, conf=0.1)

    class_values = result[0].boxes.cls

    class_names = [model.names[int(cls)] for cls in class_values]
    if not class_names:
        return "1000"

    return class_names[0]

def chat_gpt(api_key, artwork_title):
    openai.api_key = api_key

    response = openai.Completion.create(
        model="gpt-4",
        prompt=f"You are an AI docent at the Louvre Museum. You are receiving questions about {artwork_title}. Answer the questions like a docent in Korean.",
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    result = prediction("checkpoint/best.pt", "static/test.jpg")
    # result = prediction("checkpoint/best.pt", "static/upload_img.jpg")
    print("Detected Classes:", result)
    print("result type: ", type(result))