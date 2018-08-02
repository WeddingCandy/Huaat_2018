# -*- coding: utf-8 -*-
"""
@CREATETIME: 31/05/2018 16:43 
@AUTHOR: Chans
@VERSION: 1.0
"""

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import os
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

tf.set_random_seed(1)   # set random seed


# hyperparameters
lr = 0.001                  # learning rate
training_iters = 100000     # train step 上限
batch_size = 128
n_inputs = 28               # MNIST data input (img shape: 28*28)
n_steps = 28                # time steps
n_hidden_units = 128        # neurons in hidden layer ?????? embedding length
target_classes = 10         # MNIST classes (0-9 digits)

'''
batch_size = num_steps * seq_length
'''


x = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
y = tf.placeholder(tf.float32, [None, target_classes])
x1 = tf.Variable(tf.random_normal(shape=[2,3,10],mean=0,stddev=1,seed=1))
a = tf.constant([[[ 1,  2,  3],
                    [ 4,  5,  6]],
                   [[ 7,  8,  9],
                    [10, 11, 12]]]) #shape: 2,2,3
weights1 = tf.Variable(tf.random_normal([3,128]))
X1 = tf.reshape(x1,[-1,3])

with tf.Session() as sess1:
    sess1.run(tf.global_variables_initializer())
    print(x1.shape)
    print(x1.shape,X1.shape)
    # print(sess1.run(X1))
    # print(weights1)
    print(sess1.run(tf.matmul(X1,weights1)))


weights = {
    'in':  tf.Variable(tf.random_normal([n_inputs, n_hidden_units])),# shape (28, 128)
    'out': tf.Variable(tf.random_normal([n_hidden_units, target_classes]))# shape (128, 10)
}

biases = {
    'in':  tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ])),# shape (128, )
    'out': tf.Variable(tf.constant(0.1, shape=[target_classes, ]))# shape (10, )
}

def RNN(X, weights, biases):
    # 原始的 X 是 3 维数据, 我们需要把它变成 2 维数据才能使用 weights 的矩阵乘法
    # X ==> (128 batches * 28 steps, 28 inputs)
    X = tf.reshape(X, [-1, n_inputs])

    # X_in = W*X + b
    X_in = tf.matmul(X, weights['in']) + biases['in']
    # print('before', X_in)
    # X_in ==> (128 batches, 28 steps, 128 hidden) 换回3维
    X_in = tf.reshape(X_in, [-1, n_steps, n_hidden_units])
    # print('after',X_in)

    # 使用 basic LSTM Cell.
    lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(n_hidden_units, forget_bias=1.0, state_is_tuple=True)
    init_state = lstm_cell.zero_state(batch_size, dtype=tf.float32) # 初始化全零 state
    outputs, final_state = tf.nn.dynamic_rnn(lstm_cell, X_in, initial_state=init_state, time_major=False)
    #outputs.shape (128, 28, 128)
    print(outputs.shape)

    # 把 outputs 变成 列表 [(batch, outputs)..] * steps
    outputs = tf.unstack(tf.transpose(outputs, [1, 0, 2]))
    print(np.array(outputs).shape)
    results = tf.matmul(outputs[-1], weights['out']) + biases['out']  # 选取最后一个 output
    return results

pred = RNN(x, weights, biases)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits= pred))
train_op = tf.train.AdamOptimizer(lr).minimize(cost)


correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
with tf.Session() as sess:
    sess.run(init)
    step = 0
    while step * batch_size < training_iters:
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)
        # print('before')
        batch_xs = batch_xs.reshape([batch_size, n_steps, n_inputs])
        # print('after', batch_xs.shape())
        sess.run([train_op], feed_dict={
            x: batch_xs,
            y: batch_ys,
        })
        # if step % 20 == 0:
        #     print('The current accuracy is :',sess.run(accuracy, feed_dict={
        #     x: batch_xs,
        #     y: batch_ys,
        # }))
        step += 1
