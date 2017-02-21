from sklearn.metrics import confusion_matrix
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import normalize
from train_test_split import train_test
import warnings; warnings.filterwarnings('ignore') #used to suppressed warning for data conversion of float to int
import csv
import random
import numpy as np
import time

filename = 'http_9columns_all_-1_clean.csv'
cleanLabel = -1
columns = [0,4,5]
alpha = 0
beta = 50
gamma_list = [2]*1
detailString, train_clean, train_dirty, X_test, y_test, cleanTrain, dirtyTrain, cleanTest, dirtyTest = \
    train_test(filename,cleanLabel,columns,alpha,beta)

startTime = time.time()

outliers_fraction = dirtyTest/(dirtyTest+cleanTest)

serviceType = filename[:filename.index('_')]
file_name = '{}_oneClassSVM{}'.format(serviceType,'_alpha{}'.format(alpha))

csvFile = '{}.csv'.format(file_name)
file = open(csvFile,'w')
wr = csv.writer(file, lineterminator="\n")
wr.writerow(['TP','TN','FP','FN','TP Accuray [%]','FP Error [%]'])
rowList = []

for gamma in gamma_list:
    if gamma == 100:
        train_clean.extend(train_dirty)
        random.shuffle(train_clean)
        X_train = train_clean[:-1]
        y_train = train_clean[-1]
    else:
        # cleanTrainSize = int(cleanTrain * (gamma/100))
        # dirtyTrainSize = int(dirtyTrain * (gamma/100))
        # indexList = random.sample(range(0, len(train_class)), cleanTrainSize + dirtyTrainSize)
        X_train = []
        y_train = []
        cln = 0
        dirt = 0

        # for i in indexList:
        #     if train_class[i] == cleanLabel and cln != cleanTrainSize:
        #         X_train.append(train_features[i])
        #         y_train.append(train_class[i])
        #         cln += 1
        #     elif train_class[i] != cleanLabel and dirt != dirtyTrainSize:
        #         X_train.append(train_features[i])
        #         y_train.append(train_class[i])
        #         dirt += 1
        for row in train_clean:
            if random.randint(0,100) < gamma:
                X_train.append(row)
                cln += 1
        for row in train_dirty:
            if random.randint(0,100) < gamma:
                X_train.append(row)
                dirt += 1
        random.shuffle(X_train)
        X_train = np.array(X_train)
        y_train = X_train[:,-1]
        X_train = X_train[:,:-1]

    print('gamma applied')


    normalize(X_train)
    normalize(X_test)
    # y_train = np.array(y_train)
    y_test = np.array(y_test)

    ocSVM = OneClassSVM(nu=0.95 * outliers_fraction + 0.05, kernel="rbf", gamma=0.1)
    ocSVM = ocSVM.fit(X_train)
    ypred = ocSVM.predict(X_test)
    distance = ocSVM.decision_function(X_test)
    print('max distance:', max(distance))
    print('min distance:', min(distance))
    #conf = confusion_matrix(y_test, ypred)
    #print(conf/len(ypred))
    #print(conf)
    trueNegative = 0    #predicted correctly as no attack
    falseNegative = 0   #predicted incorrectly as no attack
    truePositive = 0    #predicted correctly as intrusion
    falsePositive = 0   #predicted incorrectly as intrusion
    for i in range(0,len(y_test)):
        if y_test[i] == cleanLabel:

            if ypred[i] == y_test[i]:
                trueNegative += 1
            else:
                falseNegative += 1
        else:
            if ypred[i] == y_test[i]:
                truePositive += 1
            else:
                falsePositive += 1


    row = [truePositive, trueNegative, falsePositive, falseNegative, round((truePositive/dirtyTest)*100,3), round((falsePositive/cleanTest)*100,3)]
    rowList.append(row)

    # print('True Positives:', truePositive)
    # print('True Negatives:', trueNegative)
    # print('False Positives:', falsePositive)
    # print('False Negatives:', falseNegative)
    # print()

column1 = 0
column2 = 1
column3 = 2
column4 = 3
column5 = 4
column6 = 5

n = len(gamma_list)

tpAve = int((sum(row[column1] for row in rowList))/n)
tnAve = int((sum(row[column2] for row in rowList))/n)
fpAve = int((sum(row[column3] for row in rowList))/n)
fnAve = int((sum(row[column4] for row in rowList))/n)
tpPerAve = round((sum(row[column5] for row in rowList))/n,3)
fpPerAve = round((sum(row[column6] for row in rowList))/n,3)

aves = [tpAve, tnAve, fpAve, fnAve, tpPerAve, fpPerAve]

for row in rowList:
    wr.writerow(row)
wr.writerow([])
wr.writerow(aves)

txtFile = '{}_readme.txt'.format(file_name)
file = open(txtFile,'w')
file.write(detailString)
file.write('\n \n')
file.write('averages based on {} runs: \n'.format(len(gamma_list)))
file.write('TP: {}, TN: {}, FP: {}, FN: {}, TP percent: {}%, FP percent: {}% \n \n'.format
           (tpAve, tnAve, fpAve, fnAve, tpPerAve, fpPerAve))
file.write('run time: {} seconds'.format(round(time.time()-startTime,3)))
file.close()
