import face_recognition
from PIL import Image, ImageDraw
#face_recognition에서 특정 경로의 이미지를 불러와야됨
image_path = 'data/without_mask/105.jpg'
# image_path = 'actor.jpg'
#face_image = face_recognition.load_image_file(image_path)

#face_image로 얼굴위치 검출, hog는 얼굴인식을 담당하는 학습된 인공지능 모델 중 하나(Object Tracking에 많이 사용되는 Feature 중 하나)
#얼굴영역의 좌표를 반환
#face_locations = face_recognition.face_locations(face_image, model='hog')
#print(face_locations) # -> [(46, 114, 108, 52)] : 기준 좌표, 기준 좌표, 가로길이, 세로 길이
# -----------------------------------
#얼굴영역을 이미지에 표시해보기
face_image_np = face_recognition.load_image_file(image_path)
face_locations = face_recognition.face_locations(face_image_np, model='hog') #top, right, bottom, left 순서임(Ctrl + 함수 클릭해보기)

#이미지의 배열정보를 이용해서 이미지 생성
face_image = Image.fromarray(face_image_np)     #넘파이로 불러와서
#원본 이미지에 표시, face image를 그리기 위한 기능을 연결시켜줌
draw = ImageDraw.Draw(face_image) #이미지로 변환

#얼굴 위치
for face_location in face_locations: # 각 얼굴 위치([(46, 114, 108, 52)])들이 face location 안에 들어감
    top = face_location[0]  #46
    right = face_location[1]    #114
    bottom = face_location[2]   #108
    left = face_location[3]     #52

    # 사각형 그리기: 좌표를 이미지에 그려주기 - rectangle(((x1, y1), (x2, y2)), outline=(0,0,255), width=4) 의 형식임
    draw.rectangle(((left, top), (right, bottom)), outline=(255,9,220), width=10)
    # 원 그리기
    # draw.ellipse(((left, top), (right, bottom)), outline=(255,9,220), width=8)
face_image.show()


