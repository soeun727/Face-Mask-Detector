import tensorflow as tf_new
# a = tf.constant(3)
# b = tf.constant(4)
# c = a + b
# print(c)
# a = 3
# b = 4
# c = a+b
# print(c)

#선언형 프로그램을 대표하는 예시 코드 구조
tf = tf_new.compat.v1

g = tf.Graph()
with g.as_default() as graph:
    hello = tf.constant("Hello TensorFlow!")
    sess = tf.Session()
    print(sess.run(hello))
