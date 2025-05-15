## Traffic Disaster Detection LOG

0514수요일
- 재난 및 사고 상황(교통사고, 화재, 홍수, 싱크홀)에 대한 classification으로 도로 교통 상황 정보를 획득하는 프로그램을 만들고자 정함
- 정확도가 높고, 실시간 처리에 최적화되어있다는 점을 고려해 YOLOv10모델을 사용하려고 하였음. 
- 그러나 개발 생태계 면에서 v10보다 v8이 우수함을 느낌(dataset을 찾는 과정에서 v8에 보다 적합한 데이터들이 더 많음을 알게 됨)
- YOLOv8 모델을 사용하기로 방향 재조정
- Roboflow, Kaggle 등 웹에서 화재, 홍수, 교통사고, 싵크홀(포트홀) 데이터를 수집함.
- YOLOv8에게 단일 클래스(홍수) 데이터를 학습시킴(Epoch 50)

0515목요일
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
