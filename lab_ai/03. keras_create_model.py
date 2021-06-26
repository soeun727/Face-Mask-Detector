# 03. keras_create_model.py
import tensorflow as tf

# VGG16이라는 모델 생성
model = tf.keras.applications.VGG16()
print(model.summary())