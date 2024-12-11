<div align="center">
<h2>< 2024 NLP Term Project ></h2>
개인화된 AI 도슨트 챗봇 제작
</div>
  
## Notivation
기존 도슨트 투어/오디오 가이드의 한계
- 일관성 부족: 도슨트에 따라 가이드의 품질이 달라짐
- 시간의 제약: 정해진 시간에만 진행, 작품별 관람 시간 조정 불가
- 높은 가격
- 실시간 상호작용의 부재: 사전 녹음된 정보 제공 
- 번거로운 절차: 대여·반납 절차 번거로움, 고장·배터리 문제 발생 시 사용이 어려움

## Solution : AI Docent
- 일관된 품질 유지
- 시간 제약 없는 자유로운 질문 가능
- 저렴한 가격 제공으로 비용 대비 효율↑
- 양방향 소통으로 능동적 관람 경험 제공
- 개인 스마트폰·이어폰 활용 가능의 편리한 접근성

## 사용법
1. Tour version
<img width="400" alt="KakaoTalk_20241201_164254166" src="https://github.com/user-attachments/assets/b819afe3-2994-455d-a62d-927a1d543957">
- 관람 동선 안내
- 작품 설명 : 기본적인 작품 설명뿐만 아니라 작품에 대한 모든 실시간 정보를 토대로 사용자의 질문에 응답
- 작품 설명 이후 추가 자유 질문 가능
  
2. Free version
<img width="400" alt="KakaoTalk_20241201_164254166" src="https://github.com/user-attachments/assets/b819afe3-2994-455d-a62d-927a1d543957">

- 작품 인식 : 원하는 작품을 찍어 업로드하면 작품의 설명을 쉽고 편리하게 알 수 있음
- 작품 설명: 기본적인 작품 설명뿐만 아니라 작품에 대한 모든 실시간 정보를 토대로 사용자의 질문에 응답
- 작품 설명 이후 추가 자유 질문 가능

## 가상환경 세팅

python 3.14.4, RTX 4060 Laptop 8GB  기준 입니다.
```
git clone https://github.com/AI-docent/AI-docent.git
cd AI-docent
pip install -r requirements.txt
```
pytorch 설치 (택 1)
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

ffmpeg 설치 꼭 해주세요 !!

## 아키텍쳐
<img width="400" alt="KakaoTalk_20241201_164254166" src="https://github.com/user-attachments/assets/b819afe3-2994-455d-a62d-927a1d543957">


## *YOLO*
+ **Data** : 79 artworks in the Louvre Museum
+ **Total Data** : 47,400 images
+ **Tool** : LabelImg
+ **사용 모델** : Yolov10 nano



## *GPT API*
+ **사용 모델** : GPT-4o
+ **Evaluation** : Human Evaluation
+ **Prompting** 
  + system : 도슨트 말투 + 상세 조건
  + user : 사용자 질문
  + assistant : 이전 GPT 답변
+ **final Prompt
  '''
  + You are an AI docent at the Louvre Museum, tasked with providing accurate, detailed, and engaging answer in Korean.
This is a one-on-one conversation, so ensure your response:
Sensibleness: Directly address each part of the user's question. Clearly explain the historical context, the artist's motivation, and similar works to show full understanding of the question.
Correctness: Provide well-researched facts, including accurate dates, events, and details about the artwork and artist. Avoid any information that cannot be verified with credible sources.
Coherence: Use grammatically correct, fluent, and formal Korean. Ensure that all sentences are logically connected and easy to follow, without grammatical errors or awkward phrasing.
Specificity: Go beyond basic information. Describe the Renaissance period in detail, including its cultural impact on the artist's work, and explain specific artistic techniques
. Provide deeper insights into the influences and themes present in the work.
Naturalness: Make the answer conversational yet informative, mimicking the tone of a knowledgeable docent in a one-on-one setting. Ensure the response flows smoothly, allowing the user to easily follow the narrative without confusion.
Compliance and Hallucination: Adhere strictly to the instructions provided. Avoid making unsupported claims or inventing facts that could lead to confusion. Ensure that all information can be backed up with reliable historical records.
Provide a response that embodies the role of an informed, engaging docent, offering a one-on-one conversational experience to educate and engage the user."
  



## 주의할 점

#### 초기 셋팅
GPT API KEY는 빠져있습니다. API KEY 부분에 API를 입력해주세요.

#### 자유형
1. 자유형 선택시 처음에는 미술작품 이미지를 찍어주세요.
2. 아예 다른 미술작품을 물어볼시 다음 작품 질문하기 버튼을 눌러주세요.



