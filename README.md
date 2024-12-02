<div align="center">
<h2>[2024 CUK DeepLearning Term Project]</h2>
사람의 얼굴 이미지를 가지고 성별과 나이를 예측하는 딥러닝 모델 구축을 위한 프로젝트<br> Deep Learning Project for Estimating gender, age of face image datasets
</div>

## <br>*To run our project*
You should change the image folder path before running eval.py
```bash
Final model name(=checkpoint): checkpoint_final
Python file to check results with test datasets: eval.py

```

## *Data Preprocessing: Entropy Calculate for Noise Label Data Correction*
요약: age 및 gender 분류 작업에 사용되는 face image dataset의 Label Data를 식별하고 수정하기 위해 Active Learning의 접근법의 구현을 포함하고 있다. 해당 method는 모델의 불확실성을 활용해 Nosie Label Data를 분류함으로써 데이터의 전체적인 품질을 향상시킵니다.
- Introduction <br> 과제를 위해 제공받은 데이터에는 잘못 라벨링된 데이터가 포함되어 있다. 이는 face image에서 age 및 gender을 인식하는 작업에 문제가 될 수 있다. 이를 해결하기 위해 Active Learning 기반의 접근법을 구현하여 잘못 라벨링된 데이터를 처리한다.
- Method <br>
  1. Active Learning: Active Learning은 모델이 현재 불확실성 상태에 기반하여 모델 자체가 가장 유익한 데이터 포인트를 훈련시키는 것이다. 이는 초기 모델 학습 이후 Query Strategy, Labeling, Retraining, Iteration의 순서로 진행된다.
  2. Calculate Entropy: Entropy는 불확실성을 측정하며 각 이미지에 대해 예측된 class 확률의 엔트로피를 계산한다. 높은 엔트로피는 모델의 예측에 대한 높은 불확실성을 나타내며, 이는 데이터 포인트가 잘못 라벨링되었을 가능성이 있음을 말한다.
  3. Apply to our model: 훈련된 모델을 사용하여 데이터셋의 각 이미지에 대한 엔트로피를 계산한다. 기존 Active Learning은 Relabeling의 과정이 포함되지만 본 프로젝트에서는 Active learning의 Query Strategy에 집중했다. 또한 직접 Relabeling을 진행하면 육안으로 클래스의 분류가 어렵다는 문제가 있기에 본 프로젝트에서는 Entropy 계산을 통해 얻은 데이터셋을 원본 데이터에서 삭제한 다음, Re-training을 진행했다.

## *Modeling: Multi-task Learning(Gender-> CNN, Age-> RAN)*
요약: gender의 경우 다양한 논문과 프로젝트에서 정확도 100%에 가까운 성능을 내고 있지만 그에 반해 age의 경우 좋은 성능을 내는 것이 쉽지가 않다. 이는 본 프로젝트에서 사용한 데이터셋을 가지고도 동일했다. 따라서 본 프로젝트를 통해서는 gender뿐만 아닌 age estimation을 위한 성능을 높이며 보다 안정적인 모델 구축을 진행했다.
- Gender Estimation <br> 복잡하지 않은 간단한 CNN모델을 통해서도 성능이 잘 나오며 동시에 모델을 경량화할 수 있기에, 간단한 CNN모델을 통해 gender estimation을 진행했다.
- Age Estimation <br> 이미지의 중요한 부분에 더 attention을 할 수 있는 "attention mechanism"을 갖고 있으며 효과적으로 이미지의 중요한 부분을 추출하는 "feature extraction"은 Residual attention Network이 갖는 장점이다. 따라서 age를 파악하는데 중요한 feature를 다룰 수 있는 RAN 모델을 사용해서 개선된 성능을 갖는 age estimation을 진행했다.
<p align="center">
  <img src="https://github.com/DL-teamproject-AGEANDGENDERPREDICT/DL_AgeGenderPrediction/assets/104899385/1296e8d2-762a-4d69-a944-badff55a80e2", height=30% width=30%>
  <p align="center">Multi-tasking model architecture for gender & age estimation</p>
</p>


## *Reference*
1. Active Learning With Imbalanced Multiple Noisy Labeling(Zhang et al, 2014)
2. Exploiting Context for Robustness to Label Noise in Active Learning(Paul et al, 2020)
3. QActor: Active Learning on Noisy Labels(Younesian et al, 2021)
4. Active Deep Learning to Tune Down the Noise in Labels(Samel et al, 2018)
5. Residual Attention Network for Image Classification(Wang et al, 2017)
6. GRA_Net: A Deep Learning Model for Classification of Age and Gender From Facial Images(Garain et al, 2021)
7. Age and Gender Classification using Convolutional Neural Networks(Levi et al, 2015)

