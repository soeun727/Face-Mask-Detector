#02. keras_load_data.py
import tensorflow as tf
import matplotlib.pyplot as plt

#keras는 tensorflow에 포함된 개념
# 폴더에서 이미지 데이터넷을
# 배치 사이즈 - 680개 다 학습시키면 시간이 너무 오래걸림, 여러개의 덩어리로 분리시켜서 학습(ex 32개짜리 덩어리로 랜덤으로 분류하여 학습)
train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    '../data/',
    validation_split=0.2,   # 검증 데이터 비율
    subset='training',
    seed=123,        # seed값을 고정시키니까 계속실행해도 같은 이미지가 나옴 999로 하면 랜덤으로 나옴, 현재시간을 넣으면 매번 바뀜
    image_size=(224,224),
    batch_size=16

)

valid_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    '../data/',
    validation_split=0.2,
    subset='validation',
    seed=123,
    image_size=(224,224),
    batch_size=16

)

#print(train_dataset.class_names)

#print(train_dataset)
plt.figure(0)
plt.title('train_dataset')
for images, labels in train_dataset.take(1): # 이 속에는 16개 이미지
    for i in range(9):
        plt.subplot(3, 3, i+1)
        plt.imshow(images[i].numpy().astype('uint8'))   # 정수 픽셀값으로 변환해서 출력
        plt.title(train_dataset.class_names[labels[i]])
        plt.axis('off')     # 축을 꺼버림(좌표값 없앰)

plt.show()

plt.figure(1)#0번과 구별
plt.title('valid_dataset')
for images, labels in valid_dataset.take(1):
    for i in range(16):
        plt.subplot(4,4,i+1)
        plt.imshow(images[i].numpy().astype('uint8'))   # 8바이트짜리 unsigned int
        plt.title(valid_dataset.class_names[labels[i]])
        plt.axis('off')

plt.show()