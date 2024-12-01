import openai

from ultralytics import YOLO

PICTURE = {
  "0": "메두사 호의 뗏목",
  "1": "단테의 배",
  "2": "키오스 섬의 학살",
  "3": "사느다나팔의 죽음",
  "4": "민중을 이끄는 자유의 여신",
  "5": "알제리의 여인들",
  "6": "자파의 페스트 격리소를 방문한 나폴레옹",
  "7": "호라티우스 형제의 맹세",
  "8": "나폴레옹 황제의 대관식",
  "9": "카롤린 리비에르",
  "10": "오달리스크",
  "11": "아탈라의 매장",
  "12": "전원의 합주곡",
  "13": "거울을 보는 여인",
  "14": "모나리자",
  "15": "가나의 혼인잔치",
  "16": "천국",
  "17": "하얀 장갑을 낀 남자",
  "18": "사계 연작",
  "19": "점쟁이",
  "20": "성모의 죽음",
  "21": "다윗과 골리앗의 싸움",
  "22": "헬레네의 납치",
  "23": "두 경배자에 의해 추앙받는 십자가에 못박힌 예수",
  "24": "내반족 소년",
  "25": "거지 소년",
  "26": "공원에서의 대화",
  "27": "멀리 만이 보이는 강가 풍경",
  "28": "성 세바스티아노",
  "29": "어린 소년과 함께 있는 노인",
  "30": "암굴의 성모",
  "31": "페로니에르를 한 아름다운 여인",
  "32": "성 안나와 성 모자",
  "33": "세례자 성 요한",
  "34": "세례요한의 머리를 받는 살로메",
  "35": "젊은 공주의 초상화 · 시지스몬도 판돌포 말라테스타",
  "36": "성흔을 받는 프란체스코",
  "37": "성모 대관식",
  "38": "정원사 성모 마리아",
  "39": "리슐리외 추기경의 초상",
  "40": "사모트라케의 니케",
  "41": "아메노피스 4세 상",
  "42": "아크나톤 왕과 네페르티티 왕비",
  "43": "앉아 있는 서기",
  "44": "네소스와 데이아니라",
  "45": "쉬제르의 독수리",
  "46": "황제의 개선",
  "47": "샤를7세의 초상",
  "48": "롤랭 재상의 성모",
  "49": "엉겅퀴를 든 자화상",
  "50": "고리대금업자와 그의 아내",
  "51": "글쓰는 에라스무스",
  "52": "가브리엘 데스트레와 그녀의 여동생",
  "53": "천문학자",
  "54": "에이스를 든 사기꾼",
  "55": "최후의 만찬",
  "56": "루이14세의 초상",
  "57": "피에로 질",
  "58": "마리 마들렌 기마르의 초상",
  "59": "발생퐁의 목욕하는 여인",
  "60": "터키탕",
  "61": "쇼팽의 초상",
  "62": "보르게제의 검투사",
  "63": "테르베테리 부부의 관(사르코파구스)",
  "64": "아그리파 흉상",
  "65": "밀로의 비너스",
  "66": "웅크린 아프로디테",
  "67": "벨레트리의 팔라스(아테나 여신)",
  "68": "거대 스핑크스",
  "69": "람세스2세 좌상",
  "70": "람세스3세 석관(사르코파구스)",
  "71": "덴데라 신전의 황도12궁",
  "72": "잠자는 헤르마프로디토스",
  "73": "버려진 프시케",
  "74": "필립 포의 무덤",
  "75": "반항하는 노예",
  "76": "죽어가는 노예",
  "77": "큐피트의 키스로 환생하는 프시케",
  "78": "네 국가의 포로",
  }

ARTIST = {
  "0": "테오도르 제리코",
  "1": "외젠 들라크루아",
  "2": "외젠 들라크루아",
  "3": "외젠 들라크루아",
  "4": "외젠 들라크루아",
  "5": "외젠 들라크루아",
  "6": "앙투안 장 그로",
  "7": "자크 루이 다비드",
  "8": "자크 루이 다비드",
  "9": "장 오귀스트 도미니크 앵그르",
  "10": "장 오귀스트 도미니크 앵그르",
  "11": "앙느 루이 지로데 드 루시 트리오종",
  "12": "베첼리오 티치아노",
  "13": "베첼리오 티치아노",
  "14": "레오나르도 다 빈치",
  "15": "파올로 베로네세",
  "16": "티치아노 베첼리오",
  "17": "장 오귀스트 도미니크 앵그르",
  "18": "굴리엘모 아르침볼도",
  "19": "미켈란젤로 메리시 다 카라바조",
  "20": "미켈란젤로 메리시 다 카라바조",
  "21": "오라치오 볼테라",
  "22": "귀도 레니",
  "23": "엘 그레코",
  "24": "호세 데 리베라",
  "25": "바르톨로메 에스테반 무리요",
  "26": "토머스 게인즈버러",
  "27": "윌리엄 터너",
  "28": "안드레아 만테냐",
  "29": "도메니코 기를란다요",
  "30": "레오나르도 다 빈치",
  "31": "레오나르도 다 빈치",
  "32": "레오나르도 다 빈치",
  "33": "레오나르도 다 빈치",
  "34": "베르나르디노 루이니",
  "35": "피사넬로",
  "36": "조토 디 본도네",
  "37": "라파엘로 산치오",
  "38": "라파엘로 산치오",
  "39": "필립 드 샹파뉴",
  "40": "",
  "41": "",
  "42": "",
  "43": "",
  "44": "잠볼로냐",
  "45": "",
  "46": "",
  "47": "장 푸케",
  "48": "얀 반 에이크",
  "49": "한스 홀바인",
  "50": "캥팅 마시",
  "51": "",
  "52": "퐁텐블로 화파",
  "53": "요하네스 베르메르",
  "54": "조르주 드 라 투르",
  "55": "상페뉴",
  "56": "이아생트 리고",
  "57": "앙투안 와토",
  "58": "장 오노레 프라고나르",
  "59": "장 오귀스트 도미니크 앵그르",
  "60": "장 오귀스트 도미니크 앵그르",
  "61": "외젠 들라크루아",
  "62": "",
  "63": "",
  "64": "",
  "65": "",
  "66": "",
  "67": "",
  "68": "",
  "69": "",
  "70": "",
  "71": "",
  "72": "",
  "73": "오귀스탱 파주",
  "74": "에르베르 모와튀리에",
  "75": "미켈란젤로 부오나로티",
  "76": "미켈란젤로 부오나로티",
  "77": "안토니오 카노바",
  "78": "",
  }

def prediction(model_path, image_path):
    try:
        model = YOLO(model_path)
        result = model(image_path, conf=0.25)

        if not result or len(result[0].boxes.cls) == 0:
            print("No prediction detected.")
            return "미상", "미상"

        class_values = result[0].boxes.cls
        class_names = [model.names[int(cls)] for cls in class_values]

        # 첫 번째 예측값으로 PICTURE 및 ARTIST 가져오기
        first_class = int(class_values[0])
        pic = PICTURE.get(str(first_class), "Unknown Picture")
        arti = ARTIST.get(str(first_class), "Unknown Artist")

        print(f"Detected Class ID: {first_class}, Picture: {pic}, Artist: {arti}")
        return pic, arti

    except Exception as e:
        print(f"Error in prediction: {e}")
        return "1000", "1000"

def gpt_generator(api_key, artwork_title, artist, audio_string, audio=False):
    openai.api_key = api_key
    
    try:
        # 메시지 구성
        if not audio:
            user_message = f"Tell me about {artwork_title} and {artist}."
        else:
            user_message = audio_string

        # GPT-4 API 호출
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI docent at the Louvre Museum. Answer questions in Korean as if you are explaining artwork to visitors."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # 응답 데이터 구성
        gpt_response = response['choices'][0]['message']['content'].strip()
        return {
            "success": True,
            "user_message": user_message,
            "gpt_response": gpt_response
        }

    except Exception as e:
        # 에러 발생 시 JSON 응답 반환
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # result = prediction("checkpoint/best.pt", "static/test.jpg")
    # result = prediction("checkpoint/best.pt", "static/upload_img.jpg")
    # print("Detected Classes:", result)
    print(gpt_generator("API KEY", '단테의 배', '외젠 들라크루아', None, False))
    # print("result type: ", type(result))
