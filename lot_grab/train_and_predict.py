import keras
import keras.backend as K
from keras.utils.np_utils import to_categorical
import pandas as pd

sequence_length = 7
feature_num = 33+16

adam = keras.optimizers.Adam()

def l1_loss(y_true, y_pred):
    return K.sum(K.abs(y_pred - y_true), axis=-1)

input_sequence = keras.layers.Input(shape=(sequence_length, feature_num))
lstm_feature = keras.layers.LSTM(64)(input_sequence)
time_layer = keras.layers.Dense(64, activation='relu')(lstm_feature)
time_layer = keras.layers.Dense(64, activation='relu')(time_layer)
time_layer = keras.layers.Dense(64, activation='relu')(time_layer)
time_out = keras.layers.Dense(feature_num, activation='sigmoid')(time_layer)
lstm_model = keras.models.Model(inputs=[input_sequence], outputs=[time_out])
lstm_model.compile(loss=l1_loss, optimizer='sgd')

test_size = 100
train_set = pd.read_csv("train_set.csv")
train_x = train_set.iloc[:-test_size, 0:sequence_length*feature_num].values
train_x = train_x.reshape(train_x.shape[0], sequence_length, feature_num)

train_y = train_set.iloc[:-test_size, sequence_length*feature_num:(sequence_length+1)*feature_num].values

test_x = train_set.iloc[-test_size:, 0:sequence_length*feature_num].values
test_x = test_x.reshape(test_x.shape[0], sequence_length, feature_num)

test_y = train_set.iloc[-test_size:, sequence_length*feature_num:(sequence_length+1)*feature_num].values

lstm_model.fit(train_x, train_y,
                epochs=10,
                batch_size=32,
                verbose=1,
                validation_data=(test_x, test_y))

pred_y = lstm_model.predict(test_x)
print(len(pred_y))
for idx in range(len(pred_y)):
    for red_idx in range(0, 33):
        if pred_y[idx][red_idx] > 0:
            print(str(red_idx+1)+" ")
    for blue_idx in range(33, 49):
        if pred_y[idx][blue_idx] > 0:
            print("blue:"+str(blue_idx-32)+"\n")

