## Traffic Disaster Detection LOG

### 0514 수요일
- 재난 및 사고 상황(교통사고, 화재, 홍수, 싱크홀)에 대한 classification으로 도로 교통 상황 정보를 획득하는 프로그램을 만들고자 정함
- 정확도가 높고, 실시간 처리에 최적화되어있다는 점을 고려해 YOLOv10모델을 사용하려고 하였음. 
- 그러나 개발 생태계 면에서 v10보다 v8이 우수함을 느낌(dataset을 찾는 과정에서 v8에 보다 적합한 데이터들이 더 많음을 알게 됨)
- YOLOv8 모델을 사용하기로 방향 재조정
- Roboflow, Kaggle 등 웹에서 화재, 홍수, 교통사고, 싵크홀(포트홀) 데이터를 수집함.
- YOLOv8에게 단일 클래스(홍수) 데이터를 학습시킴(Epoch 50)

### 0515 목요일
- 데이터 전처리 : singleclass classification dataset 여러개를 muliclass detection용 데이터셋으로 합치기 위한 과정
  1. 데이터 다시 라벨링 : 단일 클래스용 data들의 label을 multiclass에 맞게 바꿈
  2. yaml 파일 재작성
- 딥러닝을 위한 환경설정 개시
  1. NVDIA 설정을 통해 학습에 GPU를 사용할 수 있도록 환경 설정
  2. CUDA를 사용하기 위한 환경 구축
  3. 딥러닝에 필요한 라이브러리 다운로드
- 다중 클래스 detect 할 수 있는 YOLOv8 코드 작성
  1. 데이터 속 세그멘테이션 라벨 삭제 -> 박스 라벨만 남기기
  2. mAP50, cls loss, box loss, dfl loss 분석 및 하이퍼파마리터 튜닝
  3. 결과 시각화를 위한 코드 작성 (실패)

### 0516 금요일
- 코드 실행 결과 비어있는 파일로 인한 오류를 확인
- 원인: 이전 다운받은 데이터에서 segmentation label을 삭제하였는데, 그로 인해 비어있는 파일이 있음을 확인
- 해결: train/val/test 데이터 셋에 있는 비어있는 파일을 모두 삭제
- 같은 실수를 하지 않기 위한 데이터 셋 속 비어있는 파일의 여부를 알 수 있는 코드 작성
- YOLO를 학습하다보면 새롭게 생기는 캐시로 인해 오류를 야기할 수 있으므로 캐시를 삭제하는 코드 작성
- 데이터 셋을 삭제했으므로, 현재 남아 있는 데이터의 각 클래스 별 데이터의 균형을 유지하기 위해서 각 클래스 별 데이터 개수 확인 코드 작성
- 확인 결과 train data에 class가 3개만 등장하는 것을 확인하였고 이는 0번 class인 flood 데이터가 전부 사라졌음을 의미(flood data가 전부 segmentation data였음)
- 전체 클래스의 segmentation용 label 데이터들을 bounding box label로 변경하는 작업 수행
- 싱크홀에 대한 사진 데이터 추가.
- 테스트 결과 accident에 대한 detection 성능이 낮아서 해당 class에 대한 threshold값을 0.5 -> 0.2로 낮춤 (아래는 결과)
  ![image](https://github.com/user-attachments/assets/50828a15-af8a-49ae-84f1-8e871fcca0a7)
- fire는 매우 잘 검출되고, 나머지 클래스는 Precision은 양호하지만 Recall이 낮아 놓치는 경우가 많음
- 전체적으로 fire를 제외한 클래스의 Recall과 IoU 개선이 필요

### 0520 화요일
- Recall을 늘리기 위한 Threshold 값을 낮추려 했지만 이미 accident의 경우 0.2로 낮은 상태라서 더 낮추면 Precision이 낮아질 가능성이 높음
- 결국 optuna에서 threshold도 최적화 해야할 하이퍼파라미터로 설정하고, 자동적으로 찾도록 함
- image 해상도를 640으로 했었지만, 더 높은 성능을 위해 800으로 변경
- epoch을 20에서 50으로 바꾼 후 정확도를 높임과 동시에 의미없는 학습을 진행할 경우 조기에 멈출 수 있도록 Patience 를 20으로 설정

### 0522 목요일
- 학습 결과(predictions)를 바탕으로 False Negative와 False Positive 데이터들을 추출해냄

### 0523 금요일
- FN, FP 데이터를 이용해 하드 샘플 마이닝을 하기 위해 데이터 증강
- 증강 데이터 training set에 추가
- 위의 추가에 따른 test 데이터 손실을 보상하기 위해 데이터 추가 수집
- 전체 클래스 데이터 총 400장 수집, test data 보강, 데이터셋 구축 완료
- 구축 완료한 데이터셋을 바탕으로 학습 (epoch 100)

### 0527 화요일
- Class     Images   Instances      Box(P          R      mAP50  mAP50-95)
    all        752         936      0.928      0.857      0.914      0.679
- 100epoch 학습 결과 가장 좋은 성능을 낸 hyperparameter가 train54 폴더에 best.pt로 저장
- 해당 모델을 기반으로 Test를 진행 결과 Precision은 0.9이상, Recall 또한 0.8이상의 좋은 성능을 보임
- 해당 프로젝트는 도로 속 재난 탐지 후 사람에게 알릴 수 있는 인공지능 모델 구축이 목표
- 따라서 Precision보다는 재난 상황을 놓치지 않는 Recall을 높이는게 더 중요하다고 판단
- 직접 Threshold를 바꿔가며 진행한 결과 0.01일 때가 Precision이 너무 해치지 않음과 동시에 높은 Recall을 확보할 수 있음
- Class     Images  Instances      Box(P          R      mAP50  mAP50-95)
  all          561        687      0.883      0.827      0.884      0.668
  flood        135        207       0.86      0.816       0.85      0.712
  fire         106        142      0.924      0.965      0.976      0.697
  accident     236        249      0.902      0.775      0.885      0.626
  sinkhole      84         89      0.844      0.753      0.824      0.635
- 해당 모델을 기반으로 실제 재난 상황을 담은 cctv 영상을 가져와서 Test
- 고속도로, 시내도로 교통관제용 cctv는 15~30fps로 촬영되는 경우가 많기 때문에 15프레임 단위로 detection을 수행
- 만약 15프레임씩 연속 5번 이상 detection을 하면 해당 class에 속하는 재난이 발생했다고 알리는 코드 작성
- Youtube에서 클래스별 CCTV/뉴스 영상 수집
- 수집된 영상으로 코드 테스트 진행하며 코드 내의 클래스 별 threshold 조정
