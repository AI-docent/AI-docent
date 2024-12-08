<div align="center">
<h2>< 2024 NLP Term Project ></h2>
개인화된 AI 도슨트 챗봇 제작
</div>
  
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



## 주의할 점

#### 초기 셋팅
GPT API KEY는 빠져있습니다. API KEY 부분에 API를 입력해주세요.

#### 자유형
1. 자유형 선택시 처음에는 미술작품 이미지를 찍어주세요.
2. 아예 다른 미술작품을 물어볼시 다음 작품 질문하기 버튼을 눌러주세요.



