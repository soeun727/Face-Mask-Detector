# 얼굴 랜드마크 추출

import face_recognition
from PIL import Image, ImageDraw
import math
import numpy as np

face_image_path = 'data/without_mask/augmented_image_200.jpg'
#face_image_path = 'data/without_mask/255.jpg'
#face_image_path = 'data/without_mask/augmented_image_100.jpg'
#face_image_path = 'BTS.jpg'
mask_image_path = 'data/mask.png'

face_image_np = face_recognition.load_image_file(face_image_path)
face_locations = face_recognition.face_locations(face_image_np) # face_recognition에서 자동으로 이미지의 배열정보를 뽑아주는거임
face_landmarks = face_recognition.face_landmarks(face_image_np, face_locations) # np는 배열정보, 재료를 랜드매크 함수로 넘겨주는 원리
# (랜드마크 함수도 학습의 결과물임 - 다른 사람들의 랜드마크 정보를 학습해서 아무사람의 이미지가 들어왔을 때 영역을 출력을 하게끔한 함수)

face_landmark_image = Image.fromarray(face_image_np)    # 배열에서 이미지를 생성해옴
draw = ImageDraw.Draw(face_landmark_image)

mask_image = Image.open(mask_image_path) # 경로에서 불러오기

for face_location in face_locations: # 각 얼굴 위치([(46, 114, 108, 52)])들이 face location 안에 들어감
    top = face_location[0]  #46
    right = face_location[1]    #114
    bottom = face_location[2]   #108
    left = face_location[3]     #52
print(top, bottom, right, left)
center = bottom-right//2
draw.line((left, top), fill=128)

for face_landmark in face_landmarks:
    mask_image = mask_image.resize((face_landmark['chin'][16][0] - face_landmark['chin'][0][0],
                                    face_landmark['chin'][7][1] - face_landmark['nose_bridge'][0][1]))  # 사이즈 변경

    a = abs(face_landmark['nose_bridge'][3][1] - face_landmark['nose_bridge'][0][1])
    b = abs(face_landmark['nose_bridge'][0][0] - face_landmark['nose_bridge'][3][0])
    myradians = np.arctan2(b,a) #arctan2는 라디안으로 반환해줌
    #print(np.rad2deg(myradians) 와 같이 라디안을 각도로 변환해주기
    #angle = math.degrees(myradians)
    angle = np.rad2deg(myradians)
    print(a,b,angle)
    mask_image = mask_image.rotate(360 - angle, expand=False)
    face_landmark_image.paste(mask_image, (face_landmark['chin'][0][0], face_landmark['nose_bridge'][0][1]),
                              mask_image)

face_landmark_image.show()

