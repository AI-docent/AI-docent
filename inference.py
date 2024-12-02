import openai
import json
import os

from ultralytics import YOLO

PICTURE = {
  "0": "The Raft of the Medusa",
  "1": "La barque de Dante",
  "2": "Scènes des mass-acres de Scio",
  "3": "La Mort de Sardanapale",
  "4": "La Liberté guidant le peuple",
  "5": "Women of Algiers in their apartment",
  "6": "Bonaparte visitant les pestiférés de Jaffa",
  "7": "The Oath of the Horatii",
  "8": "Sacre de l'empereur Napoléon",
  "9": "Mademoiselle Caroline Rivière",
  "10": "Une Odalisque",
  "11": "Les Funérailles d'Atala",
  "12": "The Pastoral Concert",
  "13": "La Femme au miroir",
  "14": "Mona Lisa",
  "15": "Les Noces de Cana",
  "16": "Le Paradis",
  "17": "L'homme au gant",
  "18": "The Four Seasons",
  "19": "La Diseuse de bonne aventure",
  "20": "La Mort de la Vierge",
  "21": "Combat de David et Goliath",
  "22": "L'Enlèvement d'Hélène",
  "23": "Le Christ en croix adoré par deux donateurs",
  "24": "Le Pied Bot",
  "25": "The Young Beggar",
  "26": "Conversation dans un parc",
  "27": "Paysage avecune rivière et une baie dans le lointain",
  "28": "Saint Sebastian",
  "29": "Portrait d'un vieillard et d'un jeune garçon",
  "30": "La Vergine delle roche",
  "31": "La belle ferronnière",
  "32": "La Vierge à l'Enfant avec sainte Anne",
  "33": "Saint Jean-Baptiste",
  "34": "Salomé reçoit la tête de saint Jean Baptiste",
  "35": "Portrait d'une jeune princesse · Sigismondo Pandolfo Malatesta",
  "36": "St. Francis Receiving the Stigmata",
  "37": "Le Couronnement de la Vierge",
  "38": "La Belle Jardinière",
  "39": "Le Cardinal de Richelieu",
  "40": "Victoire de Samothrace",
  "41": "Aménophis IV",
  "42": "Akhenaten et Nefertiti",
  "43": "Le Scribe Accroupi",
  "44": "Nessus et Deianira",
  "45": "Vase dit Aigle de Suger",
  "46": "Feuillet de diptyque : L'Empereur triomphant",
  "47": "Charles VII",
  "48": "Vierge au chancelier Rolin",
  "49": "Portrait de l'artiste au chardon",
  "50": "Le Preteur et Sa Femme",
  "51": "Desiderius Erasmus",
  "52": "Gabrielle d'Estrées et une de ses sœurs",
  "53": "L'Astronome ou plutôt L'Astrologue",
  "54": "Le Tricheur à l'as de carreau",
  "55": "La sainte Cène",
  "56": "Louis XIV",
  "57": "Pierrot, dit autrefois Gilles",
  "58": "Portrait de Marie-Madeleine Guimard",
  "59": "Baigneuse de Valpinçon",
  "60": "Le Bain turc",
  "61": "Portrait of Frédéric Chopin",
  "62": "Le gladiateur Borghèse",
  "63": "Sarcophagus",
  "64": "Marcus Agrippa",
  "65": "Venus de Milo",
  "66": "Aphrodite accroupie",
  "67": "Athéna dite Pallas de Velletri",
  "68": "Grand sphinx de Tanis",
  "69": "Statue colossale de Ramsès II",
  "70": "Cuve du sarcophage de Ramsès III",
  "71": "Zodiaque de Denderah",
  "72": "Hermaphrodite endormi",
  "73": "Psyché abandonnée",
  "74": "Tombeau de Philippe Pot",
  "75": "Dying Slave",
  "76": "Rebellious Slave",
  "77": "Psyché ranimée par le baiser de l'Amour",
  "78": "Quatre captifs dits aussi Quatre Nations vaincues",
  }

ARTIST = {
  "0": "Théodore Géricault",
  "1": "Eugène Delacroix",
  "2": "Eugène Delacroix",
  "3": "Eugène Delacroix",
  "4": "Eugène Delacroix",
  "5": "Eugène Delacroix",
  "6": "Antoine Jean Gros",
  "7": "Jacques Louis David",
  "8": "Jacques Louis David",
  "9": "Jean Auguste Dominique Ingres",
  "10": "Jean Auguste Dominique Ingres",
  "11": "Anne Louis Girodet Trioson",
  "12": "Vecellio Tiziano",
  "13": "Vecellio Tiziano",
  "14": "Leonardo da Vinci",
  "15": "Paolo Veronese",
  "16": "Tintoretto",
  "17": "Vecellio Tiziano",
  "18": "Giuseppe Arcimboldo",
  "19": "Michelangelo da Caravaggio",
  "20": "Michelangelo da Caravaggio",
  "21": "Daniele da Volterra",
  "22": "Guido Reni",
  "23": "El Greco",
  "24": "José de Ribera",
  "25": "Bartolomé Esteban Murillo",
  "26": "Thomas Gainsborough",
  "27": "Joseph Mallord William Turner",
  "28": "Andrea Mantegna",
  "29": "Domenico Ghirlandai",
  "30": "Leonardo da Vinci",
  "31": "Leonardo da Vinci",
  "32": "Leonardo da Vinci",
  "33": "Leonardo da Vinci",
  "34": "Bernardino Luini",
  "35": "Il Pisanello",
  "36": "Giotto di Bondone",
  "37": "Raffaello Sanzio",
  "38": "Raffaello Sanzio",
  "39": "Philippe de Champaigne",
  "40": "",
  "41": "",
  "42": "",
  "43": "",
  "44": "Giambologna",
  "45": "",
  "46": "",
  "47": "Jean Fouquet",
  "48": "Jan van Eyc",
  "49": "Albrecht-Düre",
  "50": "Quentin Matsy",
  "51": "Hans Holbein der Jungere",
  "52": "",
  "53": "Johannes Vermeer",
  "54": "Georges de La Tour",
  "55": "Philippe de Champaigne",
  "56": "Hyacinthe Rigaud",
  "57": "Jean-Antoine Watteau",
  "58": "Jean-Honoré Fragonard",
  "59": "Jean Auguste Dominique Ingres",
  "60": "Jean Auguste Dominique Ingres",
  "61": "Eugène Delacroix",
  "62": "Agasias",
  "63": "",
  "64": "",
  "65": "",
  "66": "",
  "67": "",
  "68": "",
  "69": "",
  "70": "",
  "71": "",
  "72": "Bernini",
  "73": "Augustin Pajou",
  "74": "Antoine le Moiturier",
  "75": "Michelangelo Buonarroti",
  "76": "Michelangelo Buonarroti",
  "77": "Antonio Canova",
  "78": "",
  }

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static")

def prediction(model_path, image_path):
    try:
        model = YOLO(model_path)
        result = model(image_path, conf=0.25)

        if not result or len(result[0].boxes.cls) == 0:
            print("No prediction detected.")
            return "unknown picture", "unknown artist"

        class_values = result[0].boxes.cls
        class_names = [model.names[int(cls)] for cls in class_values]

        first_class = int(class_values[0])
        pic = PICTURE.get(str(first_class), "Unknown picture")
        arti = ARTIST.get(str(first_class), "Unknown artist")

        print(f"Detected Class ID: {first_class}, Picture: {pic}, Artist: {arti}")
        return pic, arti

    except Exception as e:
        print(f"Error in prediction: {e}")
        return "Unknown picture", "Unknown artist"

def gpt_generator(api_key, artwork_title, artist, audio_string, audio=False):
    openai.api_key = api_key
    if artwork_title==None or artist==None:
        return {
            "success": False,
            "gpt_response": "사진을 먼저 찍어주세요."
        }
    
    data_path = os.path.join(UPLOAD_FOLDER, "gpt_msg_assistant.jsonl")

    # free 처음 사진 용
    if not audio:
        messages = [
            {"role": "system", "content": "You are an AI docent at the Louvre Museum, tasked with providing accurate, detailed, and engaging answers in Korean."},
            {"role": "system", "content": "Your responses must be: Sensibleness: Directly address each part of the user's question."},
            {"role": "system", "content": "Provide clear explanations of the historical context, the artist's motivations, and similar works to demonstrate full understanding."},
            {"role": "system", "content": "Correctness: Include well-researched facts, such as accurate dates, events, and details about the artwork and artist."},
            {"role": "system", "content": "Avoid unverified information."},
            {"role": "system", "content": "Coherence: Use grammatically correct, fluent, and formal Korean."},
            {"role": "system", "content": "Ensure all sentences are logically connected and easy to follow."},
            {"role": "system", "content": "Specificity: Go beyond basic information."},
            {"role": "system", "content": "Describe historical periods and their cultural impacts, artistic techniques, and influences on the artist in detail."},
            {"role": "system", "content": "Naturalness: Adopt a conversational yet informative tone, akin to a knowledgeable docent providing a one-on-one experience."},
            {"role": "system", "content": "Responses should flow smoothly for an engaging narrative."},
            {"role": "system", "content": "Do not use the special symbols like #, %, $, @, !, ?, *, etc."},
            {"role": "system", "content": "The lengh of response should be about 500 characters."},
            {"role": "system", "content": "Compliance and Hallucination: Adhere strictly to instructions, avoid unsupported claims, and ensure all information can be backed up with reliable historical records."},
            {"role": "user", "content": f"Describe {artwork_title} painted by {artist}. When explaining the work, explain the content of the artwork, the artist's information, and the background of the times."}
        ]
        response = openai.ChatCompletion.create(model="gpt-4o", messages=messages, max_tokens=500, temperature=0.7, stream=False)

        with open(data_path, 'r', encoding='utf-8') as file:
            for line in file:
                assistant = json.loads(line)
                messages.append(assistant)

        gpt_response = response['choices'][0]['message']['content'].strip()
        assistant = {"role": "assistant", "content": gpt_response}

        with open(data_path, 'a', encoding='utf-8') as f:
            json.dump(assistant, f, ensure_ascii=False)
            f.write('\n')

        return {
            "success": True,
            "gpt_response": gpt_response
        }
    
    # 사진 촬영 후 자유 질문 용
    elif audio:
        user_message = audio_string
        messages = [
            {"role": "system", "content": "You are an AI docent at the Louvre Museum, tasked with providing accurate, detailed, and engaging answers in Korean."},
            {"role": "system", "content": "Your responses must be: Sensibleness: Directly address each part of the user's question."},
            {"role": "system", "content": "Provide clear explanations of the historical context, the artist's motivations, and similar works to demonstrate full understanding."},
            {"role": "system", "content": "Correctness: Include well-researched facts, such as accurate dates, events, and details about the artwork and artist."},
            {"role": "system", "content": "Avoid unverified information."},
            {"role": "system", "content": "Coherence: Use grammatically correct, fluent, and formal Korean."},
            {"role": "system", "content": "Ensure all sentences are logically connected and easy to follow."},
            {"role": "system", "content": "Specificity: Go beyond basic information."},
            {"role": "system", "content": "Describe historical periods and their cultural impacts, artistic techniques, and influences on the artist in detail."},
            {"role": "system", "content": "Naturalness: Adopt a conversational yet informative tone, akin to a knowledgeable docent providing a one-on-one experience."},
            {"role": "system", "content": "Responses should flow smoothly for an engaging narrative."},
            {"role": "system", "content": "Do not use the special symbols like #, %, $, @, !, ?, *, etc."},
            {"role": "system", "content": "The lengh of response should be about 500 characters."},
            {"role": "system", "content": "Compliance and Hallucination: Adhere strictly to instructions, avoid unsupported claims, and ensure all information can be backed up with reliable historical records."},
            {"role": "user", "content": "What is the name of this painting and who is the artist?"},
            {"role": "assistant", "content": f"The name of this painting is {artwork_title}, and the artist of this painting is {artist}"},
            {"role": "user", "content": user_message}
        ]

        with open(data_path, 'r', encoding='utf-8') as file:
            for line in file:
                assistant = json.loads(line)
                messages.append(assistant)

        response = openai.ChatCompletion.create( model="gpt-4o", messages=messages, max_tokens=500, temperature=0.7, stream=False)
        gpt_response = response['choices'][0]['message']['content'].strip()
        
        user_text = {"role": "user", "content": user_message}
        assistant = {"role": "assistant", "content": gpt_response}

        with open(data_path, 'a', encoding='utf-8') as f:
            json.dump(user_text, f, ensure_ascii=False)
            f.write('\n')

        with open(data_path, 'a', encoding='utf-8') as f:
            json.dump(assistant, f, ensure_ascii=False)
            f.write('\n')
    
        return {
            "success": True,
            "user_message": user_message,
            "gpt_response": gpt_response
        }

    # 투어중 질문 용
    elif artist == "Unknown artist":
        user_message = audio_string
        messages = [
            {"role": "system", "content": "You are an AI docent at the Louvre Museum, tasked with providing accurate, detailed, and engaging answers in Korean."},
            {"role": "system", "content": "Your responses must be: Sensibleness: Directly address each part of the user's question."},
            {"role": "system", "content": "Provide clear explanations of the historical context, the artist's motivations, and similar works to demonstrate full understanding."},
            {"role": "system", "content": "Correctness: Include well-researched facts, such as accurate dates, events, and details about the artwork and artist."},
            {"role": "system", "content": "Avoid unverified information."},
            {"role": "system", "content": "Coherence: Use grammatically correct, fluent, and formal Korean."},
            {"role": "system", "content": "Ensure all sentences are logically connected and easy to follow."},
            {"role": "system", "content": "Specificity: Go beyond basic information."},
            {"role": "system", "content": "Describe historical periods and their cultural impacts, artistic techniques, and influences on the artist in detail."},
            {"role": "system", "content": "Naturalness: Adopt a conversational yet informative tone, akin to a knowledgeable docent providing a one-on-one experience."},
            {"role": "system", "content": "Responses should flow smoothly for an engaging narrative."},
            {"role": "system", "content": "Do not use the special symbols like #, %, $, @, !, ?, *, etc."},
            {"role": "system", "content": "The lengh of response should be about 500 characters."},
            {"role": "system", "content": "Compliance and Hallucination: Adhere strictly to instructions, avoid unsupported claims, and ensure all information can be backed up with reliable historical records."},
            {"role": "user", "content": "What is the name of this painting and who is the artist?"},
            {"role": "assistant", "content": f"The name of this painting is {artwork_title}"},
            {"role": "user", "content": user_message}
        ]

        with open(data_path, 'r', encoding='utf-8') as file:
            for line in file:
                assistant = json.loads(line)
                messages.append(assistant)

        response = openai.ChatCompletion.create( model="gpt-4o", messages=messages, max_tokens=500, temperature=0.7, stream=False)
        gpt_response = response['choices'][0]['message']['content'].strip()

        user_text = {"role": "user", "content": user_message}
        assistant = {"role": "assistant", "content": gpt_response}

        with open(data_path, 'a', encoding='utf-8') as f:
            json.dump(user_text, f, ensure_ascii=False)
            f.write('\n')

        with open(data_path, 'a', encoding='utf-8') as f:
            json.dump(assistant, f, ensure_ascii=False)
            f.write('\n')
    
        return {
            "success": True,
            "user_message": user_message,
            "gpt_response": gpt_response
        }
    
    # 투어중 질문 용
    else:
        user_message = audio_string
        messages = [
            {"role": "system", "content": "You are an AI docent at the Louvre Museum, tasked with providing accurate, detailed, and engaging answers in Korean."},
            {"role": "system", "content": "Your responses must be: Sensibleness: Directly address each part of the user's question."},
            {"role": "system", "content": "Provide clear explanations of the historical context, the artist's motivations, and similar works to demonstrate full understanding."},
            {"role": "system", "content": "Correctness: Include well-researched facts, such as accurate dates, events, and details about the artwork and artist."},
            {"role": "system", "content": "Avoid unverified information."},
            {"role": "system", "content": "Coherence: Use grammatically correct, fluent, and formal Korean."},
            {"role": "system", "content": "Ensure all sentences are logically connected and easy to follow."},
            {"role": "system", "content": "Specificity: Go beyond basic information."},
            {"role": "system", "content": "Describe historical periods and their cultural impacts, artistic techniques, and influences on the artist in detail."},
            {"role": "system", "content": "Naturalness: Adopt a conversational yet informative tone, akin to a knowledgeable docent providing a one-on-one experience."},
            {"role": "system", "content": "Responses should flow smoothly for an engaging narrative."},
            {"role": "system", "content": "Do not use the special symbols like #, %, $, @, !, ?, *, etc."},
            {"role": "system", "content": "The lengh of response should be about 500 characters."},
            {"role": "system", "content": "Compliance and Hallucination: Adhere strictly to instructions, avoid unsupported claims, and ensure all information can be backed up with reliable historical records."},
            {"role": "user", "content": "What is the name of this painting and who is the artist?"},
            {"role": "assistant", "content": f"The name of this painting is {artwork_title}, and the artist of this painting is {artist}"},
            {"role": "user", "content": user_message}
        ]

        with open(data_path, 'r', encoding='utf-8') as file:
            for line in file:
                assistant = json.loads(line)
                messages.append(assistant)

        response = openai.ChatCompletion.create( model="gpt-4o", messages=messages, max_tokens=500, temperature=0.7, stream=False)
        gpt_response = response['choices'][0]['message']['content'].strip()

        user_text = {"role": "user", "content": user_message}
        assistant = {"role": "assistant", "content": gpt_response}

        with open(data_path, 'a', encoding='utf-8') as f:
            json.dump(user_text, f, ensure_ascii=False)
            f.write('\n')

        with open(data_path, 'a', encoding='utf-8') as f:
            json.dump(assistant, f, ensure_ascii=False)
            f.write('\n')
    
        return {
            "success": True,
            "user_message": user_message,
            "gpt_response": gpt_response
        }

