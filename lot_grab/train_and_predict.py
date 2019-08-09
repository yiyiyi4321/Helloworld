import keras
import keras.backend as K
from keras.utils.np_utils import to_categorical
import pandas as pd
from sklearn import metrics

sequence_length = 1
feature_num = 33+16

adam = keras.optimizers.Adam()

input_sequence = keras.layers.Input(shape=(feature_num,))
time_layer = keras.layers.Dense(64, activation='relu')(input_sequence)
time_out = keras.layers.Dense(1, activation='sigmoid')(time_layer)
lstm_model = keras.models.Model(inputs=[input_sequence], outputs=[time_out])
lstm_model.compile(loss='binary_crossentropy', optimizer='adam')

test_size = 300
train_set = pd.read_csv("train_set.csv")
train_x = train_set.iloc[500:-test_size, 0:sequence_length*feature_num].values
train_x = train_x.reshape(train_x.shape[0], feature_num)

train_y = train_set.iloc[500:-test_size, sequence_length*feature_num].values

test_x = train_set.iloc[-test_size:, 0:sequence_length*feature_num].values
test_x = test_x.reshape(test_x.shape[0], feature_num)

test_y = train_set.iloc[-test_size:, sequence_length*feature_num].values

for i in range(10):
        lstm_model.fit(train_x, train_y,
                                        epochs=1,
                                        batch_size=32,
                                        verbose=1,
                                        validation_data=(test_x, test_y),
                                        class_weight='auto')

        pred_y = lstm_model.predict(test_x)
        fpr, tpr, thresholds = metrics.roc_curve(test_y, pred_y, pos_label = 1)
        print('auc = ', metrics.auc(fpr, tpr))

