import os, csv
import numpy as np

path = '/Users/dan/PycharmProjects/KDD/CSVs/service_type' # you'll need to change the path on your comp.
csvFiles = os.listdir(path)
os.chdir(path)
print(csvFiles)

path2 = '/Users/dan/PycharmProjects/KDD/CSVs/service_type/logTransformed' # you'll need to change the path on your comp.
for file in csvFiles:
    if file == '.DS_Store' or file == 'logTransformed':
        a=0
    else:
        X = np.genfromtxt(file,delimiter=',',dtype=np.int)
        Y = X[:,-1]
        X = np.log2(X[:, 0:-1] + 1) # Choose columns of X to log transform
        X = np.c_[X, Y]
        print(X[:5])
        print(X.shape)
        wr = csv.writer(open(path2+'/'+file[:file.index('.')]+'_log2', 'w'))
        for row in X:
            wr.writerow(row)
        print('completed file:',file)
        print()

