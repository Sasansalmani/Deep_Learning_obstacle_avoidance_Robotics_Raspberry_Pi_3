import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core   import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import time

def network(X, Y, test_x, test_y, N_epoch):
    X = X.reshape([-1,224,224,3])
    test_x = test_x.reshape([-1,224,224,3])

    convnet = input_data(shape=[None, 224,224,3], name='input')

    convnet = conv_2d(convnet, 64, 5, 2, activation='relu')
    convnet = max_pool_2d(convnet, 2)

    convnet = conv_2d(convnet, 64, 5, 2, activation='relu')
    convnet = max_pool_2d(convnet, 2)

    convnet = conv_2d(convnet, 128, 5, 2, activation='relu')
    convnet = max_pool_2d(convnet, 2)

    convnet = fully_connected(convnet, 4*1024, activation='relu')
    convnet = fully_connected(convnet, 2*1024, activation='relu')
    convnet = fully_connected(convnet, 1024, activation='relu')
    convnet = dropout(convnet, 0.8)

    convnet = fully_connected(convnet, 5, activation='softmax')
    convnet = regression(convnet, optimizer='sgd', learning_rate=0.01, loss='categorical_crossentropy', name='target')

    model = tflearn.DNN(convnet)

    time_last = time.time()

    model.fit({'input': X}, {'target': Y}, n_epoch=N_epoch, validation_set=({'input': test_x}, {'target': test_y}),
              snapshot_step=500, show_metric=True)

    print("time is :    ")
    print(time.time()-time_last)

    model.save('Model.model')

