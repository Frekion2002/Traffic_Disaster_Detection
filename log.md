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
  
