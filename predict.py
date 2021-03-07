import numpy as np 
import tensorflow as tf
import keras
from keras.models import load_model
import librosa
import pickle
max_pad_len = 174
num_rows = 40
num_columns = 174
num_channels = 1


# model loading code
#loaded_model = pickle.load(open('model.pkl', 'rb'))
model =load_model('models/full_model.h5')
#loaded_model.summary()

# Label map for your strings and number 
LABEL_MAP = {0:'Dog_bark', 1:'drilling ',2:'glass_breaking',3:'gun_shot',4:'jackhammer'}

# actual prediction function 
def extract_features(file_name):
   
    try:
        audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast') 
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        pad_width = max_pad_len - mfccs.shape[1]
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
        
    except Exception as e:
        print("Error encountered while parsing file: ", file_name)
        return None 
     
    return mfccs
def predict(path):

    # read wav file and do data processing as per model training
    amplitude = extract_features(path)
    print(amplitude)
    print(path)
    amplitude=amplitude.reshape(1, num_rows, num_columns, num_channels)
    # make predictions using model
    predictions = model.predict(amplitude)

    # get index of the highest probability
    idx = np.argmax(predictions, axis=1).tolist()[0]
    print(idx)
    print(type(idx))
    label = LABEL_MAP[idx]
    return label