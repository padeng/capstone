#requires 'filename.csv', integer value of clean label, columns to be use in list form,
# alpha (percentage of dirty data to be used), beta (percentage of clean data to be used)

#example of how to call train_test fuction:
# filename = 'http_9columns_all_-1_clean.csv'
# cleanLabel = float(-1)
# columns = list(range(0,10))
# alpha = 0
# beta = 50
# train_test(filename,cleanLabel,columns,alpha,beta)

import csv
import random
from sklearn.preprocessing import normalize
import numpy as np


def train_test(filename, cleanLabel, columns, alpha, beta):
    row_list = csv.reader(open(filename, newline=''))
    # row_list = np.loadtxt(filename,delimiter=',')
    # print(row_list[0])
    # labels = row_list[:, [-1]]
    # row_list = normalize(row_list[:,range(0,len(row_list[0]-1))])
    # row_list = np.concatenate((row_list, labels), axis=1)
    # row_list = row_list.tolist()
    # print(row_list[0])

    train_features = []
    train_clean = []
    train_dirty = []
    train_class = []
    X_test = []
    y_test = []

    cleanTrain = 0
    dirtyTrain = 0
    cleanTest = 0
    dirtyTest = 0
    total = 0


    if len(columns) == len(next(row_list))-1:
        for row in row_list:
            row = list(map(float, row))
            total += 1
            rand = random.randint(0, 100)
            if row[-1] == cleanLabel:
                if rand < beta:
                    # train_features.append(row[:-1])
                    # train_class.append(row[-1])
                    train_clean.append(row)
                    cleanTrain += 1
                else:
                    X_test.append(row[:-1])
                    y_test.append(row[-1])
                    cleanTest += 1
            else:
                if rand < alpha:
                    # train_features.append(row[:-1])
                    # train_class.append(row[-1])
                    train_dirty.append(row)
                    dirtyTrain += 1
                else:
                    X_test.append(row[:-1])
                    y_test.append(row[-1])
                    dirtyTest += 1
    else:
        for row in row_list:
            #print(row)
            #print(columns[0])
            y = [row[index] for index in columns]
            y.append(row[-1])
            row = list(map(float, y))
            #print(row)
            #print(cleanLabel)
            total += 1
            rand = random.randint(0, 100)
            if row[-1] == cleanLabel:
                if rand < beta:
                    # train_features.append(row[:-1])
                    # train_class.append(row[-1])
                    train_clean.append(row)
                    cleanTrain += 1
                else:
                    X_test.append(row[:-1])
                    y_test.append(row[-1])
                    cleanTest += 1
            else:
                if rand < alpha:
                    # train_features.append(row[:-1])
                    # train_class.append(row[-1])
                    train_dirty.append(row)
                    dirtyTrain += 1
                else:
                    X_test.append(row[:-1])
                    y_test.append(row[-1])
                    dirtyTest += 1


    print(len(train_clean))

    train = dirtyTrain + cleanTrain
    trainPercent = (train / total) * 100
    dirtyTrainPercent = (dirtyTrain / train) * 100
    test = dirtyTest + cleanTest
    dirtyTestPercent = (dirtyTest / test) * 100

    detailString = 'file used: "{}" \n' \
                   'columns used: {}, apha: {}, beta: {} \n' \
                   'training set: {} dirty + {} clean = {} total -- {}%. of all data in the file. \n' \
                   'percentage of dirty in training set: {}% \n' \
                   'testing set: {} dirty + {} clean = {} total \n' \
                   'percentage of dirty in test set: {}%'.format(filename, columns, alpha, beta, dirtyTrain,
                                                                 cleanTrain, train, round(trainPercent, 3),
                                                                 round(dirtyTrainPercent, 3), dirtyTest, cleanTest,
                                                                 test, round(dirtyTestPercent, 3))
    # print(filename)
    # print('columns used:',columns,', apha:', alpha, ', beta:', beta)
    # print('training set:', dirtyTrain, 'dirty +', cleanTrain, 'clean = ', train, 'total --', round(trainPercent, 3),
    #       '%. of all data in the file.')
    # print('percentage of dirty in training set:', round(dirtyTrainPercent, 3), '%')
    # print('testing set:', dirtyTest, 'dirty +', cleanTest, 'clean = ', test, 'total')
    # print('percentage of dirty in test set:', round(dirtyTestPercent, 3), '%')
    print(detailString)
    print()

    return detailString, train_clean, train_dirty, X_test, y_test, cleanTrain, dirtyTrain, cleanTest, dirtyTest
