# -*- coding: utf-8 -*-
"""
@CREATETIME: 29/05/2018 14:25 
@AUTHOR: Chans
@VERSION:  1.0
"""

import tensorflow as tf
import reader
import os
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

DATA_PATH = "/Users/Apple/datadata/ptb/data"
HIDDEN_SIZE = 200 # 隐藏层长度
NUM_LAYERS = 2  # 几个LSTM结构
VOCAB_SIZE = 10000

LEARNING_RATE = 0.5
TRAIN_BATCH_SIZE = 20
TRAIN_NUM_STEP = 35

EVAL_BATCH_SIZE = 1
EVAL_NUM_STEP = 1
NUM_EPOCH = 2
KEEP_PROB = 0.5
MAX_GRAD_NORM = 5


class PTBModel(object):
    def __init__(self, is_training, batch_size, num_steps):

        self.batch_size = batch_size
        self.num_steps = num_steps

        ## 定义输入层。
        self.input_data = tf.placeholder(tf.int32, [batch_size, num_steps])
        self.targets = tf.placeholder(tf.int32, [batch_size, num_steps])

        ## 定义使用LSTM结构及训练时使用dropout。
        lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(HIDDEN_SIZE)
        if is_training:
            # 训练集需要进行dropout
            lstm_cell = tf.nn.rnn_cell.DropoutWrapper(lstm_cell, output_keep_prob=KEEP_PROB)
        cell = tf.nn.rnn_cell.MultiRNNCell([lstm_cell] * NUM_LAYERS)
        '''Create a RNN cell composed sequentially of a number of RNNCells'''

        # 初始化最初的状态。
        self.initial_state = cell.zero_state(batch_size, tf.float32)
        embedding = tf.get_variable(name = "embedding", shape = [VOCAB_SIZE, HIDDEN_SIZE])
        '''
        get_variable():由于tf.Variable() 每次都在创建新对象，所有reuse=True 和它并没有什么关系。对于get_variable()，来说，
        如果已经创建的变量对象，就把那个对象返回，如果没有创建变量对象的话，就创建一个新的。
        '''

        # 将原本单词ID转为单词向量。
        inputs = tf.nn.embedding_lookup(embedding, self.input_data)

        if is_training:
            inputs = tf.nn.dropout(inputs, KEEP_PROB)

        # 定义输出列表。
        outputs = []
        state = self.initial_state
        with tf.variable_scope("RNN"):
            '''所以要共享变量，需要使用tf.variable_scope()'''
            for time_step in range(num_steps):
                if time_step > 0: tf.get_variable_scope().reuse_variables()
                cell_output, state = cell(inputs[:, time_step, :], state)
                outputs.append(cell_output)
        output = tf.reshape(tf.concat(outputs, 1), [-1, HIDDEN_SIZE])

        weight = tf.get_variable("weight", [HIDDEN_SIZE, VOCAB_SIZE])
        bias = tf.get_variable("bias", [VOCAB_SIZE])
        logits = tf.matmul(output, weight) + bias

        # 定义交叉熵损失函数和平均损失。
        loss = tf.contrib.legacy_seq2seq.sequence_loss_by_example(
            [logits],
            [tf.reshape(self.targets, [-1])],
            [tf.ones([batch_size * num_steps], dtype=tf.float32)])
        self.cost = tf.reduce_sum(loss) / batch_size
        self.final_state = state

        # 只在训练模型时定义反向传播操作。
        if not is_training: return
        trainable_variables = tf.trainable_variables()

        # 控制梯度大小，定义优化方法和训练步骤。
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, trainable_variables), MAX_GRAD_NORM)
        optimizer = tf.train.GradientDescentOptimizer(LEARNING_RATE)
        self.train_op = optimizer.apply_gradients(zip(grads, trainable_variables))


def run_epoch(session, model, data, train_op, output_log, epoch_size):
    total_costs = 0.0
    iters = 0
    state = session.run(model.initial_state)

    # 训练一个epoch。
    for step in range(epoch_size):
        x, y = session.run(data)
        cost, state, _ = session.run([model.cost, model.final_state, train_op],
                                        {model.input_data: x, model.targets: y, model.initial_state: state})
        total_costs += cost
        iters += model.num_steps

        if output_log and step % 100 == 0:
            print("After %d steps, perplexity is %.3f" % (step, np.exp(total_costs / iters)))
    return np.exp(total_costs / iters)


def main():
    train_data, valid_data, test_data, _ = reader.ptb_raw_data(DATA_PATH)

    # 计算一个epoch需要训练的次数
    train_data_len = len(train_data)
    train_batch_len = train_data_len // TRAIN_BATCH_SIZE
    train_epoch_size = (train_batch_len - 1) // TRAIN_NUM_STEP

    valid_data_len = len(valid_data)
    valid_batch_len = valid_data_len // EVAL_BATCH_SIZE
    valid_epoch_size = (valid_batch_len - 1) // EVAL_NUM_STEP

    test_data_len = len(test_data)
    test_batch_len = test_data_len // EVAL_BATCH_SIZE
    test_epoch_size = (test_batch_len - 1) // EVAL_NUM_STEP

    initializer = tf.random_uniform_initializer(-0.05, 0.05)
    with tf.variable_scope("language_model", reuse=None, initializer=initializer):
        train_model = PTBModel(True, TRAIN_BATCH_SIZE, TRAIN_NUM_STEP)

    with tf.variable_scope("language_model", reuse=True, initializer=initializer):
        eval_model = PTBModel(False, EVAL_BATCH_SIZE, EVAL_NUM_STEP)

    # 训练模型。
    with tf.Session() as session:
        tf.global_variables_initializer().run()

        train_queue = reader.ptb_producer(train_data, train_model.batch_size, train_model.num_steps)
        eval_queue  = reader.ptb_producer(valid_data, eval_model.batch_size, eval_model.num_steps)
        test_queue  = reader.ptb_producer(test_data , eval_model.batch_size, eval_model.num_steps)

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=session, coord=coord)
        #多线程

        for i in range(NUM_EPOCH):
            print("In iteration: %d" % (i + 1))
            run_epoch(session, train_model, train_queue, train_model.train_op, True, train_epoch_size)

            valid_perplexity = run_epoch(session, eval_model, eval_queue, tf.no_op(), False, valid_epoch_size)
            print("Epoch: %d Validation Perplexity: %.3f" % (i + 1, valid_perplexity))

        test_perplexity = run_epoch(session, eval_model, test_queue, tf.no_op(), False, test_epoch_size)
        print("Test Perplexity: %.3f" % test_perplexity)

        coord.request_stop()
        coord.join(threads)

if __name__ == "__main__":
    main()