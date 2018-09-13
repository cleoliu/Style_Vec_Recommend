'''
tsne & tensorboard
'''
# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings(action='ignore',category=UserWarning,module='gensim')

import os
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from tensorflow.contrib.tensorboard.plugins import projector
from gensim.models.keyedvectors import KeyedVectors



def TSNE_visualize():
    fig, ax = plt.subplots(figsize=(14, 14))
    for idx in range(viz_words):
        plt.scatter(*embed_tsne[idx, :], color='steelblue')
        plt.annotate(vocab[idx], (embed_tsne[idx, 0], embed_tsne[idx, 1]), alpha=0.7)
    plt.savefig('log/tsne_digits.png', dpi=120)
    #plt.show() 

def TENSORFLOW_visualize():
    # setup a TensorFlow session
    tf.reset_default_graph()
    sess = tf.InteractiveSession()
    X = tf.Variable([0.0], name='embedding')
    place = tf.placeholder(tf.float32, shape=embed_tsne.shape)
    set_x = tf.assign(X, place, validate_shape=False)
    sess.run(tf.global_variables_initializer())
    sess.run(set_x, feed_dict={place: embed_tsne})

    # creat metadata.tsv
    with open(os.path.join('log', "metadata.tsv"), 'w') as f:
            for idx in range(viz_words):
                f.write(vocab[idx] + '\n')

    # create a TensorFlow summary writer
    summary_writer = tf.summary.FileWriter('log', sess.graph)
    config = projector.ProjectorConfig()
    embedding_conf = config.embeddings.add()
    embedding_conf.tensor_name = 'embedding:0'
    embedding_conf.metadata_path = 'metadata.tsv'
    projector.visualize_embeddings(summary_writer, config)

    # save the model
    saver = tf.train.Saver()
    saver.save(sess, os.path.join('log', "model.ckpt"))



if __name__ == "__main__":
    # ---load model---
    text_name ="CNNvec_adam_300.txt"
    model = KeyedVectors.load_word2vec_format(text_name)

    # ---vector---
    viz_words = 1000                   #romdom choose
    vocab = list(model.wv.vocab)       #vocab = word
    X = model[vocab]
    tsne = TSNE(n_components=2)        #降為2維
    embed_tsne = tsne.fit_transform(X) #embed_tsne = tsne vec[1*2]

    # ---RUN---
    TSNE_visualize()
    #TENSORFLOW_visualize()             #tensorboard --logdir=log