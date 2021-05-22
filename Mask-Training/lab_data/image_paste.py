#마스크 이미지를 원본 이미지에 합성하는 코드
import face_recognition
from PIL import Image, ImageDraw

#이미지 열어주기
image_path = 'actor.jpg'
mask_image_path = '../data/mask.png'

face_image_np = face_recognition.load_image_file(image_path) # 이미지를 일단 불러오기만,,
face_locations = face_recognition.face_locations(face_image_np, model='hog')
face_image = Image.fromarray(face_image_np)
draw = ImageDraw.Draw(face_image)

for face_location in face_locations: # 각 얼굴 위치([(46, 114, 108, 52)])들이 face location 안에 들어감
    top = face_location[0]  #46
    right = face_location[1]    #114
    bottom = face_location[2]   #108
    left = face_location[3]     #52
print(top, bottom, right, left)
# 마스크 이미지 불러오기
mask_image = Image.open(mask_image_path) # 경로에서 불러오기

# print(type(face_image_np)) #<class 'numpy.ndarray'> -> 넘파이에 있는 단순 배열로 저장
# print(type(face_image)) # <class 'PIL.Image.Image'> -> 넘파이 어레이에 값을 넘겨줘서 불러온 image -> image 자료형
# print(type(mask_image)) # <class 'PIL.PngImagePlugin.PngImageFile'> -> pngimagefile로 불러와짐

a=int(((right+left)//2)-(right-left)//2)
b=int(bottom*(2.5/4))
print(a, b)
#마스크 이미지 resize
num1=right-left
num2=bottom-b
# num2=(bottom-top)//2
mask_image = mask_image.resize((num1, num2)) # 사이즈 변경
# (0,0)이 위치
draw.rectangle(((left, top), (right, bottom)), outline=(255,9,220), width=10)
face_image.paste(mask_image,(a,b), mask_image)  # 배경이 검정이 안나오도록 세번째 인자: 이미지가 있는 부분만 보여주고 나머지는 투명처리를 해줘서 배경이 제대로 나옴
face_image.show()
