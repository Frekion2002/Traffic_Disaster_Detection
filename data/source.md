## 통합 데이터셋     
[https://drive.google.com/file/d/1ox-Nw7aIDamPs0sXOAxvdKh_jMglClrc/view?usp=drive_link    ](https://drive.google.com/drive/folders/1LH9FdjDlkFQWgh_oQGdhmS43oU_TkjoJ?usp=drive_link)

통합 데이터셋은 아래 네 개의 데이터셋을 가공하여 만들어졌습니다.   

### flood dataset    
- https://universe.roboflow.com/public-workspace-a/flood-detect-xlhvz/dataset/1
- https://universe.roboflow.com/floodestimations/floodestimation/dataset/2

### fire dataset    
- https://universe.roboflow.com/aneligna/fire-detection-yolov8-ylrh2
- https://universe.roboflow.com/t5-capstone/fire-detection-9aome/dataset/1

### car accident dataset    
- https://universe.roboflow.com/donghee/test-d95ea/dataset/17
- https://universe.roboflow.com/accident-and-nonaccident/accident-and-non-accident-label-image-dataset/dataset/14

### sink hole dataset
- https://universe.roboflow.com/search?q=sink%2520hole](https://universe.roboflow.com/school-9zcc8/sinkhole-dataset/dataset/1)


0516
- 싱크홀 데이터 보충
- flood data 세그멘테이션을 box로 바꿈

0522
- 하드 샘플 마이닝을 위해 prediction data 중 FN/FP 데이터를 나눔

0523
- 하드 샘플 마이닝을 위해 FN/FP를 증강하여 training 데이터에 추가
- 줄어든 test data를 보강하기 위해 모든 클래스 데이터 보강
