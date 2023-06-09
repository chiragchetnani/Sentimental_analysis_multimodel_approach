# -*- coding: utf-8 -*-
"""n-3notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nEG3MQbqBGpdbScRXXdbQET0mHB6pYA7

Importing all the required libraries.
"""

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds
import re
import shutil
import string
import matplotlib.pyplot as plt

"""#TASK 0
Run the original tutorial code using the built-in IMDB dataset.

"""

#loading the inbulid IMDB data.
train_data, test_data = tfds.load(name="imdb_reviews", split=["train", "test"], 
                                  batch_size=-1, as_supervised=True)

train_examples, train_labels = tfds.as_numpy(train_data)
test_examples, test_labels = tfds.as_numpy(test_data)

print("Training entries: {}, test entries: {}".format(len(train_examples), len(test_examples)))

train_examples[:10]

train_labels[:10]

# Original tutorial model (OrigNN)
model_orig = tf.keras.Sequential(name = 'OrigNN')
model_orig.add(hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim50/2", input_shape=[], dtype=tf.string, trainable=True))
model_orig.add(tf.keras.layers.Dense(16, activation='relu'))
model_orig.add(tf.keras.layers.Dense(1))

model_orig.summary()

model_orig.compile(optimizer='adam', loss=tf.losses.BinaryCrossentropy(from_logits=True), metrics=[tf.metrics.BinaryAccuracy(threshold=0.0, name='accuracy')])

x_val = train_examples[:10000]
partial_x_train = train_examples[10000:]

y_val = train_labels[:10000]
partial_y_train = train_labels[10000:]

history_orig = model_orig.fit(partial_x_train, partial_y_train, epochs=10, batch_size=512,validation_data=(x_val, y_val),verbose=1)
results_orig = model_orig.evaluate(test_examples, test_labels)

"""# Task 1
Compare the pretrained model (OrigNN) with a model that does not use pretrained embeddings (ScratchNN).
"""

# Extract values from the dictionary and convert to list of strings
train_examples_converted = [example.decode('utf-8') for example in train_examples]

# Preprocessing
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=10000, oov_token='<OOV>')
tokenizer.fit_on_texts(train_examples_converted)

train_generated = tokenizer.texts_to_sequences(train_examples_converted)
test_examples_converted = [example.decode('utf-8') for example in test_examples]
# Convert test examples from byte strings to regular strings

test_gen_sequences = tokenizer.texts_to_sequences(test_examples_converted)
# Convert test examples to sequences of integers using tokenizer

train_padded = tf.keras.preprocessing.sequence.pad_sequences(train_generated, maxlen=256, truncating='post')
test_padded = tf.keras.preprocessing.sequence.pad_sequences(test_gen_sequences, maxlen=256, truncating='post')
# Pad the sequences with zeros to have a fixed length of 256
# Truncate longer sequences from the end and pad shorter sequences with zeros

"""Model 2. = ScratchNN"""

model_2 = tf.keras.Sequential(name = 'ScratchNN')
model_2.add(tf.keras.layers.Embedding(10000, 16))
model_2.add(tf.keras.layers.GlobalAveragePooling1D())
model_2.add(tf.keras.layers.Dense(16, activation='relu'))
model_2.add(tf.keras.layers.Dense(1, activation='sigmoid'))
model_2.compile(optimizer='adam',loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),metrics=['accuracy'])
history_2 = model_2.fit(train_padded,train_labels,epochs=10,batch_size=512,validation_split=0.2)
results_2 = model_2.evaluate(test_padded, test_labels)

# Plot the accuracy and loss curves for OrigNN
acc_orig = history_orig.history['accuracy']
val_acc_orig = history_orig.history['val_accuracy']
loss_orig = history_orig.history['loss']
val_loss_orig = history_orig.history['val_loss']
epochs_orig = range(1, len(acc_orig) + 1)

plt.plot(epochs_orig, acc_orig, 'bo', label='Train acc')
plt.plot(epochs_orig, val_acc_orig, 'b', label='Validation acc')
plt.title('Training and validation accuracy (OrigNN)')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

plt.plot(epochs_orig, loss_orig, 'bo', label='Train loss')
plt.plot(epochs_orig, val_loss_orig, 'b', label='Validation loss')
plt.title('Training and validation loss (OrigNN)')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

acc_2 = history_2.history['accuracy']
val_acc_2 = history_2.history['val_accuracy']
loss_2 = history_2.history['loss']
val_loss_2 = history_2.history['val_loss']
epochs_2 = range(1, len(acc_2) + 1)

plt.plot(epochs_2, acc_2, 'bo', label='Training acc')
plt.plot(epochs_2, val_acc_2, 'b', label='Validation acc')
plt.title('Training and validation accuracy (ScratchNN)')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

plt.plot(epochs_2, loss_2, 'bo', label='Training loss')
plt.plot(epochs_2, val_loss_2, 'b', label='Validation loss')
plt.title('Training and validation loss (ScratchNN)')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

"""#TASK 2
Train and evaluate the modified model (DenseNNi), and plot the graphs for accuracy and loss at each epoch.
Compare DenseNNi with OrigNN at each epoch.
DenseNNi = OrigNN + the Dense hidden layer in the neural network from 16 neurons to (50 + 10 * N) neurons.

***VALUE OF N = 3***
"""

N = 3

"""Model 3. = DenseNNi"""

model_3 = tf.keras.Sequential(name = 'DenseNNi')
model_3.add(hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim50/2", input_shape=[], dtype=tf.string, trainable=True))
model_3.add(tf.keras.layers.Dense((50 + 10 * N), activation='relu'))
model_3.add(tf.keras.layers.Dense(1))
model_3.compile(optimizer='adam',
              loss=tf.losses.BinaryCrossentropy(from_logits=True),
              metrics=[tf.metrics.BinaryAccuracy(threshold=0.0, name='accuracy')])
history_3 = model_3.fit(partial_x_train,
                    partial_y_train,
                    epochs=10,
                    batch_size=512,
                    validation_data=(x_val, y_val),
                    verbose=1)
results = model_3.evaluate(test_examples, test_labels)

orig_history = history_orig.history
# Get the history dictionary of the training process for OrigNN

dense_history = history_3.history
# Get the history dictionary of the training process for DenseNNi

orig_acc = orig_history['accuracy']
# Get the list of training accuracy values for OrigNN at each epoch

orig_val_acc = orig_history['val_accuracy']
# Get the list of validation accuracy values for OrigNN at each epoch

dense_acc = dense_history['accuracy']
# Get the list of training accuracy values for DenseNNi at each epoch

dense_val_acc = dense_history['val_accuracy']
# Get the list of validation accuracy values for DenseNNi at each epoch

epochs = range(1, len(orig_acc) + 1)

plt.plot(epochs, orig_acc, 'r', label='OrigNN Training accuracy')
plt.plot(epochs, orig_val_acc, 'b', label='OrigNN Validation accuracy')
plt.plot(epochs, dense_acc, 'g', label='DenseNNi Training accuracy')
plt.plot(epochs, dense_val_acc, 'm', label='DenseNNi Validation accuracy')
plt.title('Training and Validation Accuracy Comparison')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Plotting loss
orig_loss = orig_history['loss']
orig_val_loss = orig_history['val_loss']

dense_loss = dense_history['loss']
dense_val_loss = dense_history['val_loss']

plt.plot(epochs, orig_loss, 'r', label='OrigNN Training loss')
plt.plot(epochs, orig_val_loss, 'b', label='OrigNN Validation loss')
plt.plot(epochs, dense_loss, 'g', label='DenseNNi Training loss')
plt.plot(epochs, dense_val_loss, 'm', label='DenseNNi Validation loss')
plt.title('Training and Validation Loss Comparison')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

"""# Task 3
Take DenseNNi
Add L2 regularizer to the hidden Dense layer.
Compare the performance of DenseNNii with DenseNNi at each epoch.

Model 4. = DenseNNii
"""

model_4 = tf.keras.Sequential(name = 'DenseNNii')
model_4.add(hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim50/2", input_shape=[], dtype=tf.string, trainable=True))
model_4.add(tf.keras.layers.Dense((50 + 10 * N), activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)))
model_4.add(tf.keras.layers.Dense(1))
model_4.compile(optimizer='adam',
              loss=tf.losses.BinaryCrossentropy(from_logits=True),
              metrics=[tf.metrics.BinaryAccuracy(threshold=0.0, name='accuracy')])
history_4 = model_4.fit(partial_x_train,
                    partial_y_train,
                    epochs=10,
                    batch_size=512,
                    validation_data=(x_val, y_val),
                    verbose=1)
results_4 = model_4.evaluate(test_examples, test_labels)

dense_history_4 = history_4.history
# Get the history dictionary of the training process for DenseNNil

dense_acc_i = dense_history['accuracy']
# Get the list of training accuracy values for DenseNNi at each epoch

dense_val_acc_i = dense_history['val_accuracy']
# Get the list of validation accuracy values for DenseNNi at each epoch

dense_acc_il = dense_history_4['accuracy']
# Get the list of training accuracy values for DenseNNil at each epoch

dense_val_acc_il = dense_history_4['val_accuracy']
# Get the list of validation accuracy values for DenseNNil at each epoch
epochs = range(1, len(dense_acc_i) + 1)

plt.plot(epochs, dense_acc_i, 'r', label='DenseNNi Training accuracy')
plt.plot(epochs, dense_val_acc_i, 'b', label='DenseNNi Validation accuracy')
plt.plot(epochs, dense_acc_il, 'g', label='DenseNNil Training accuracy')
plt.plot(epochs, dense_val_acc_il, 'm', label='DenseNNil Validation accuracy')
plt.title('Training and Validation Accuracy Comparison')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Plotting loss
dense_loss_i = dense_history['loss']
dense_val_loss_i = dense_history['val_loss']

dense_loss_il = dense_history_4['loss']
dense_val_loss_il = dense_history_4['val_loss']

plt.plot(epochs, dense_loss_i, 'r', label='DenseNNi Training loss')
plt.plot(epochs, dense_val_loss_i, 'b', label='DenseNNi Validation loss')
plt.plot(epochs, dense_loss_il, 'g', label='DenseNNil Training loss')
plt.plot(epochs, dense_val_loss_il, 'm', label='DenseNNil Validation loss')
plt.title('Training and Validation Loss Comparison')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

"""# Task 4
Take DenseNNi
Add second regularized hidden layer, of the same size immediately following it.
modified model = (DenseNNiii), 
Compare the performance of DenseNNiii with DenseNNii at each epoch.

Model 5. = DenseNNiii
"""

model_5 = tf.keras.Sequential(name = 'DenseNNiii')
model_5.add(hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim50/2", input_shape=[], dtype=tf.string, trainable=True))
model_5.add(tf.keras.layers.Dense((50 + 10 * N), activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)))  # Regularized Dense layer
model_5.add(tf.keras.layers.Dense((50 + 10 * N), activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001))) # Regularized Dense layer
model_5.add(tf.keras.layers.Dense(1))
model_5.compile(optimizer='adam',
                       loss=tf.losses.BinaryCrossentropy(from_logits=True),
                       metrics=[tf.metrics.BinaryAccuracy(threshold=0.0, name='accuracy')])
history_5 = model_5.fit(partial_x_train,
                                      partial_y_train,
                                      epochs=10,
                                      batch_size=512,
                                      validation_data=(x_val, y_val),
                                      verbose=1)

results_5 = model_5.evaluate(test_examples, test_labels)

dense_history_5 = history_5.history
# Get the history dictionary of the training process for DenseNNii

dense_acc_i = dense_history_4['accuracy']
# Get the list of training accuracy values for DenseNNi at each epoch

dense_val_acc_i = dense_history_4['val_accuracy']
# Get the list of validation accuracy values for DenseNNi at each epoch

dense_acc_ii = dense_history_5['accuracy']
# Get the list of training accuracy values for DenseNNii at each epoch

dense_val_acc_ii = dense_history_5['val_accuracy']
# Get the list of validation accuracy values for DenseNNii at each epoch

epochs = range(1, len(dense_acc_i) + 1)

plt.plot(epochs, dense_acc_i, 'r', label='DenseNNi Training accuracy')
plt.plot(epochs, dense_val_acc_i, 'b', label='DenseNNi Validation accuracy')
plt.plot(epochs, dense_acc_ii, 'g', label='DenseNNii Training accuracy')
plt.plot(epochs, dense_val_acc_ii, 'm', label='DenseNNii Validation accuracy')
plt.title('Training and Validation Accuracy Comparison')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Plotting loss
dense_loss_i = dense_history_4['loss']
dense_val_loss_i = dense_history_4['val_loss']

dense_loss_ii = dense_history_5['loss']
dense_val_loss_ii = dense_history_5['val_loss']

plt.plot(epochs, dense_loss_i, 'r', label='DenseNNi Training loss')
plt.plot(epochs, dense_val_loss_i, 'b', label='DenseNNi Validation loss')
plt.plot(epochs, dense_loss_ii, 'g', label='DenseNNii Training loss')
plt.plot(epochs, dense_val_loss_ii, 'm', label='DenseNNii Validation loss')
plt.title('Training and Validation Loss Comparison')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

"""# Task 5
Take DenseNNii
Add a Dropout layer, with a dropout parameter of 0.2, after the single hidden Dense layer.
modified model = (DropNNi),
Compare the performance of DropNNi with DenseNNii at each epoch.

Model 6. = DropNNi
"""

model_6 = tf.keras.Sequential(name = 'DropNNi')
model_6.add(hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim50/2", input_shape=[], dtype=tf.string, trainable=True))
model_6.add(tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)))  # Regularized Dense layer
model_6.add(tf.keras.layers.Dropout(0.2))  # Dropout layer
model_6.add(tf.keras.layers.Dense(1))
model_6.compile(optimizer='adam',
                     loss=tf.losses.BinaryCrossentropy(from_logits=True),
                     metrics=[tf.metrics.BinaryAccuracy(threshold=0.0, name='accuracy')])
history_6 = model_6.fit(partial_x_train,
                                  partial_y_train,
                                  epochs=10,
                                  batch_size=512,
                                  validation_data=(x_val, y_val),
                                  verbose=1)

results_6 = model_6.evaluate(test_examples, test_labels)

drop_history_dict_i = history_6.history
# Get the history dictionary of the training process for DropNNi

dense_acc_ii = dense_history_4['accuracy']
# Get the list of training accuracy values for DenseNNi at each epoch

dense_val_acc_ii = dense_history_4['val_accuracy']
# Get the list of validation accuracy values for DenseNNi at each epoch

drop_acc_i = drop_history_dict_i['accuracy']
# Get the list of training accuracy values for DropNNi at each epoch

drop_val_acc_i = drop_history_dict_i['val_accuracy']
# Get the list of validation accuracy values for DropNNi at each epoch

epochs = range(1, len(dense_acc_ii) + 1)

plt.plot(epochs, dense_acc_ii, 'r', label='DenseNNii Training accuracy')
plt.plot(epochs, dense_val_acc_ii, 'b', label='DenseNNii Validation accuracy')
plt.plot(epochs, drop_acc_i, 'g', label='DropNNi Training accuracy')
plt.plot(epochs, drop_val_acc_i, 'm', label='DropNNi Validation accuracy')
plt.title('Training and Validation Accuracy Comparison')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Plotting loss
dense_loss_ii = dense_history_4['loss']
dense_val_loss_ii = dense_history_4['val_loss']

drop_loss_i = drop_history_dict_i['loss']
drop_val_loss_i = drop_history_dict_i['val_loss']

plt.plot(epochs, dense_loss_ii, 'r', label='DenseNNii Training loss')
plt.plot(epochs, dense_val_loss_ii, 'b', label='DenseNNii Validation loss')
plt.plot(epochs, drop_loss_i, 'g', label='DropNNi Training loss')
plt.plot(epochs, drop_val_loss_i, 'm', label='DropNNi Validation loss')
plt.title('Training and Validation Loss Comparison')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

"""# Task 6
Take DropNNi
Change the dropout parameter to (0.3 + 0.05 * N).
modified model = (DropNNii),
Compare the performance of DropNNii with DropNNi at each epoch.

Model 7. = DropNNii
"""

model_7 = tf.keras.Sequential(name = 'DropNNii')
model_7.add(hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim50/2", input_shape=[], dtype=tf.string, trainable=True))
model_7.add(tf.keras.layers.Dense(50, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)))  # Regularized Dense layer
model_7.add(tf.keras.layers.Dropout((0.3 + 0.05 * N)))  # Dropout layer
model_7.add(tf.keras.layers.Dense(1))
model_7.compile(optimizer='adam',
                     loss=tf.losses.BinaryCrossentropy(from_logits=True),
                     metrics=[tf.metrics.BinaryAccuracy(threshold=0.0, name='accuracy')])
history_7 = model_7.fit(partial_x_train,
                                  partial_y_train,
                                  epochs=10,
                                  batch_size=512,
                                  validation_data=(x_val, y_val),
                                  verbose=1)

"""THe saturartion point of the model appeared at the 7th epoch and after that it started to overfit and as we can see the degrading results of the model in validation accuracies """

results_7 = model_7.evaluate(test_examples, test_labels)

drop_history_dict_ii = history_7.history
# Get the history dictionary of the training process for DropNNii

drop_acc_ii = drop_history_dict_ii['accuracy']
# Get the list of training accuracy values for DropNNii at each epoch

drop_val_acc_ii = drop_history_dict_ii['val_accuracy']
# Get the list of validation accuracy values for DropNNii at each epoch

drop_acc_i = drop_history_dict_i['accuracy']
# Get the list of training accuracy values for DropNNi at each epoch

drop_val_acc_i = drop_history_dict_i['val_accuracy']
# Get the list of validation accuracy values for DropNNi at each epoch

epochs = range(1, len(drop_acc_ii) + 1)

plt.plot(epochs, drop_acc_ii, 'r', label='dropNNii Training accuracy')
plt.plot(epochs, drop_val_acc_ii, 'b', label='DropNNii Validation accuracy')
plt.plot(epochs, drop_acc_i, 'g', label='DropNNi Training accuracy')
plt.plot(epochs, drop_val_acc_i, 'm', label='DropNNi Validation accuracy')
plt.title('Training and Validation Accuracy Comparison')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Plotting loss
drop_loss_ii = drop_history_dict_ii['loss']
drop_val_loss_ii = drop_history_dict_ii['val_loss']

drop_loss_i = drop_history_dict_i['loss']
drop_val_loss_i = drop_history_dict_i['val_loss']

plt.plot(epochs, drop_loss_ii, 'r', label='DropNNii Training loss')
plt.plot(epochs, drop_val_loss_ii, 'b', label='DropNNii Validation loss')
plt.plot(epochs, drop_loss_i, 'g', label='DropNNi Training loss')
plt.plot(epochs, drop_val_loss_i, 'm', label='DropNNi Validation loss')
plt.title('Training and Validation Loss Comparison')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

"""# Task 7
Choose the best performing model out of OrigNN plus all of those in Tasks 1 to 6 and call it NNBest.
Find the 5 most positive and 5 most negative reviews from the test set under the best model
NNBest.
(Note: From the lecture notes on dropout, you'll see there's a softmax in the output layer, although it will be a sigmoid activation function for a binary output. The reason it's not in there for the tutorial code (so you just have the raw output Dense (1) with no activation) is that the sigmoid is imposed in the loss function (loss=losses.BinaryCrossentropy(from_logits=
That means that the Dense (1) output layer is producing logits and the loss function is incorporating the sigmoid when calculating binary cross-entropy. So to identify the most positive and and negative reviews, just consider the most extreme positive and scores produced by the predict) function.)
"""

model_list = [model_orig, model_2, model_3, model_4, model_5, model_6, model_7]
model_names = ['OrigNN', 'DenseNNi', 'DenseNNii', 'DenseNNiii', 'DropNNi', 'DropNNii']
model_accuracies = []

for model in model_list:
    if model == model_2:
        accuracy = model.evaluate(test_padded, test_labels)[1]
    else:
        accuracy = model.evaluate(test_examples, test_labels)[1]
    model_accuracies.append(accuracy)

# Find the index of the best performing model
max_accuracy = max(model_accuracies)
best_model_index = model_accuracies.index(max_accuracy)-1
print(best_model_index)
best_model = model_list[best_model_index]
best_model_name = model_names[best_model_index]

# Get the predicted sentiment scores for the test set using the best model
if best_model == model_2:
    scores = best_model.predict(test_padded)
else:
    scores = best_model.predict(test_examples)

# Sort the scores in ascending order
sorted_indices = np.argsort(scores.flatten())

# Get the 5 most positive and 5 most negative reviews
most_positive_reviews = [test_examples[i] for i in sorted_indices[-5:]]
most_negative_reviews = [test_examples[i] for i in sorted_indices[:5]]

print("Best Model: ", best_model_name)
print("Most Positive Reviews:")
for review in most_positive_reviews:
    print(review)
print("\nMost Negative Reviews:")
for review in most_negative_reviews:
    print(review)

best_model_name

"""# Task 8
Change your NNBest model to apply dropout at test time, as described in the lecture notes on Training Deep Neural Networks. Call this NNBestDrop. Does this change the overall accuracy of the model?
(Hint: See the note above about the sigmoid.
You may want to use an architecture more similar to the ones from the lecture / textbook used to discuss dropout at test time.)
Consider the 20 reviews to be found in test_examples [100+20N:120+20N]. Discuss whether the probabilities assigned by NNBest or those assigned by NNBestDrop better reflect whether the review sentiment is clear (either positive or negative) or ambiguous.
"""

model_8 = tf.keras.Sequential(name='NNBestDrop')
model_8.add(hub.KerasLayer("https://tfhub.dev/google/nnlm-en-dim50/2", input_shape=[], dtype=tf.string, trainable=True))
model_8.add(tf.keras.layers.Dense(16, activation='relu'))
model_8.add(tf.keras.layers.Dropout((0.3 + 0.05 * N)))
model_8.add(tf.keras.layers.Dropout(0.2))
model_8.add(tf.keras.layers.Dense(1, activation='sigmoid'))  # Apply sigmoid activation for binary output
model_8.compile(optimizer='adam',
                        loss=tf.losses.BinaryCrossentropy(),
                        metrics=[tf.metrics.BinaryAccuracy(threshold=0.5, name='accuracy')])
history_NN_best_drop = model_8.fit(partial_x_train, partial_y_train, epochs=10, batch_size=512,validation_data=(x_val, y_val),verbose=1)
results_NN_best_drop = model_8.evaluate(test_examples, test_labels)

accuracy_best_drop = model_8.evaluate(test_examples, test_labels)[1]

# Get the probabilities assigned by NNBest model
probabilities_best = best_model.predict(test_examples[100:120])

# Get the probabilities assigned by NNBestDrop model
probabilities_best_drop = model_8.predict(test_examples[100:120])