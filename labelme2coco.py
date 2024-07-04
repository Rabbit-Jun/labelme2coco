import json
import glob
import os

def labelme2coco(json_path, idx):
    with open(json_path) as f:
        labelme_data = json.load(f)
    


    # bbox에 넣기 위해 좌측 상단 x,y 그리고 이미지의 너비와 높이 설정
    x = []
    y = []
    for shapes in labelme_data['shapes'][0]['points']:
        x.append(shapes[0])
        y.append(shapes[1])
    x_min = min(x)
    x_max = max(x)
    y_min = min(y)
    y_max = max(y)
    width = x_max - x_min
    height = y_max - y_min
    bbox = [x_min, y_max, width, height]
    id = idx

    # segementation이 폴리곤이라 각 객체의 points의 값을 가져오기 위해
    for shape in labelme_data['shapes']:
        points = shape['points']
    
    segmentation = [points]
    
    # category_id 설정
    if 'cat' in json_path:
        category_id = 0
    else:
        category_id = 1 
    
    # 코코데이터 형태 

    cocodata = {
        "info" : {
            "year": 2024,
            "version": labelme_data['version'],
            "date_created": "2024-07-03",

        },
        "images" :[
            {
                "id": id,
                "width": width,
                "height": height,
                "file_name": str(json_path.split('.json')[0])+'.jpg'
            }
        ],
        "annotations": [
            {
                "id": id,
                "image_id" : id,
                "category_id": category_id,
                "segmentation": segmentation ,
                "area": width * height,
                "bbox": bbox,
                "iscrowd" : 0

            }
        ],
        "categories": [
            {"id": 0, 
             "name": "cat", 
             "supercategory": "animal"},
            {"id": 1, 
             "name": "dog", 
             "supercategory": "animal"}
        ]
    }
    
    
    return cocodata

cocodata_list =[]
    
# 현재 경로에서 명시된 폴더에서 json을 확장자로 갖는 파일 모두 불러옴
json_paths = glob.glob('dogNcat/*.json')  
output_filename = 'dogNcat.json'

# id 번호 부여하고 경로 넣고 함수 돌림
for idx, json_path in enumerate(json_paths):
    coco_data = labelme2coco(json_path, idx)
    cocodata_list.append(coco_data)

# print(len(cocodata_list))
# print(cocodata_list[0].keys())
# print(cocodata_list[0]['images'][0])

# 코코 형식은 키: [값1, 2, 3] 이런식으로 되어있어서 밖에있는 리스트를 벗겨주고 묶기 위한 코드
images = []
annotations = []
categories = []

for i in range(len(cocodata_list)):
    img = cocodata_list[i]['images'][0]
    images.append(img)
    ann = cocodata_list[i]['annotations'][0]
    annotations.append(ann)
    catg = cocodata_list[i]['categories'][0]
    categories.append(catg)



cocodata_format ={
    "info" : {
            "year": 2024,
            "version": cocodata_list[0]['info']['version'],
            "date_created": "2024-07-03",

        },
    "images": images,
    "annotations": annotations,
    "categories": categories


}

# print(cocodata_format)

with open(output_filename, 'w') as outfile:
    json.dump(cocodata_format, outfile)

