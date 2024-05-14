import numpy as np
import tensorflow
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import sequential
from tensorflow.keras.layers import Embedding, LSTM , Dense

with open ('Corpus.txt', "r", encoding='utf-8') as myfile:
    mytext = myfile.read()
mytokenizer = Tokenizer()

mytokenizer.file_on_texts([mytext])
total_words = len(mytokenizer.word_index)


my_input_sequences = []
for line in mytext.split('\n'):
    print(line)
    token_list = mytokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        my_n_gram_sequence = token_list[:i+1]
        print(my_n_gram_sequence)
        my_input_sequences.append(my_n_gram_sequence)
max_sequence_len = max([len(seq) for seq in my_input_sequences])
input_sequences = np.array(pad_sequences(my_input_sequences, maxlen= max_sequence_len , padding='pre'))
input_sequences = [0]
x=input_sequences[:,:-1]
y=input_sequences[:, -1]
y=np.array(tf.keras.utils.to_categorical(y,num_classes=total_words))
model = sequential()
model.add(Embedding(total_words,100, input_length = max_sequence_len-1))
model.add(LSTM(150))
model.add(Dense(total_words, activation = 'softmax'))
print(model.summary())
model.compile(loss='categorical_crossentropy', omtimizer='Information', metrics=['accuracy'])
model.fit(x,y, epochs=100, verbs=1)
input_text = "information"
predict_next_words = 2
for _ in range(predict_next_words):
    token_list = mytokenizer.texts_to_sequences([input_text])[0]
    print(token_list)
    token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
    predicted = np.argmax(model.predict(token_list), axis = -1)
    output_word = ""
    for word, index in mytokenizer.word_index.items():
        if index == predicted:
            output_word = word
            break
    input_text += "  " + output_word
print(input_text)
