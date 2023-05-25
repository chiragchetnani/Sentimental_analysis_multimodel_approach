# Sentimental_analysis_multimodel_approach
# Sentiment Analysis using Neural Network Models

_**This repository contains a sentiment analysis project using various Neural Network (NN) models for classifying sentiments in text data. The goal of the project is to explore different NN architectures and techniques to develop accurate models for sentiment analysis tasks.**
_
# Project Overview

The project involves the following key steps:

**Data Preparation: The IMDb movie review dataset is used for training and evaluation. The dataset is preprocessed and split into training and test sets.
Model Development: Several NN models are implemented and trained, including OrigNN, DenseNNi, DenseNNii, DenseNNiii, DropNNi, and DropNNii. These models leverage pre-trained embedded models and incorporate techniques like regularization and dropout for improved performance.
Model Evaluation: The trained models are evaluated using appropriate evaluation metrics. Performance metrics such as accuracy and loss are analyzed to identify the best-performing model.
Model Comparison: The performance of each model is compared at different epochs to gain insights into their learning capabilities and potential overfitting issues.
Best Model Selection: The best-performing model, NNBest, is chosen based on its accuracy and overall performance.
Sentiment Analysis: The selected model is used to predict sentiment scores for test examples. The most positive and negative reviews are identified based on the predicted scores.**
**Dropout at Test Time: The NNBest model is further enhanced by incorporating dropout at test time, aiming to improve model generalization and handle ambiguous sentiment cases.**
