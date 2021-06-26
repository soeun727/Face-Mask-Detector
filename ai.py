# ai.py
import tensorflow as tf
import numpy as np
import os

# 모델 가공
resize_and_crop = tf.keras.Sequential([
    tf.keras.layers.experimental.preprocessing.RandomCrop(height=224, width=224),
    tf.keras.layers.experimental.preprocessing.Rescaling(1. / 255)  # #얘가 핵심 -> Rescaling 내에 들어오는 값을 모두 곱해줌, 실수로 인식
])


# 학습 데이터 로드
def load_data():
    train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        'data/',
        validation_split=0.2,   # 검증 데이터 비율
        subset='training',
        seed=123,               # seed값을 고정시키니까 계속실행해도 같은 이미지가 나옴 999로 하면 랜덤으로 나옴, 현재시간을 넣으면 매번 바뀜
        image_size=(224, 224),
        batch_size=16
    )

    valid_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        'data/',
        validation_split=0.2,
        subset='validation',
        seed=123,
        image_size=(224, 224),
        batch_size=16
    )

    rc_train_dataset = train_dataset.map(lambda x, y: (resize_and_crop(x), y))  # # 문제와 정답이 x, y// 그리고 문제에만 resize and crop 적용)
    rc_valid_dataset = valid_dataset.map(lambda x, y: (resize_and_crop(x), y))

    return rc_train_dataset, rc_valid_dataset


# 모델 생성
def create_model():
    if os.path.exists('models/mymodel'):
        model = tf.keras.models.load_model('models/mymodel')    # 모델 불러오기

        model.layers[0].trainable = False       # 얘는 최적의 상태로 훈련이 되어있기 때문에 훈련 안시키겠다
        model.layers[2].trainable = True
    else:           #mymodel이 없으면,
        model = tf.keras.applications.MobileNet(         # MobileNet: 모바일 기기에서도 동작할수있을만큼 가벼운 모델, cpu로만 학습해도 할만한 ..
            input_shape=(224, 224, 3),
            include_top=False,
            weights='imagenet'
        )

        model.trainable = False

        model = tf.keras.Sequential([
            model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(1)
        ])

        learning_rate = 0.001
        model.compile(
            loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
            optimizer=tf.keras.optimizers.RMSprop(lr=learning_rate),
            metrics=['accuracy']
        )

        train_dataset, valid_dataset = load_data()
        train_model(model, 2, train_dataset, valid_dataset, True)
    return model


# 모델 학습
def train_model(model, epochs, train_dataset, valid_dataset, save_model):
    history = model.fit(train_dataset, epochs=epochs, validation_data=valid_dataset)
    if save_model:  # save_mode이 true라면,,
        model.save('models/mymodel')
    return history


# 학습된 모델로 예측(얘가 핵심)
def predict(model, image):
    rc_image = resize_and_crop(np.array([image]))
    result = model.predict(rc_image)
    if result[0] > 0.5:
        return 1        # 마스크를 안썼다고 예측
    else:
        return 0        # 마스크를 썼다고 예측

# 이파일을 직접 실행했을때만 실행되는 코드(다른곳에서 불러오면 실행안되는 코드)
if __name__ == '__main__':
    train_dataset, valid_dataset = load_data()
    model = create_model()
    train_model(model, 2, train_dataset, valid_dataset, True)