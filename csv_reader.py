import csv
import numpy as np
from PIL import Image
import pickle
mat = []
train_data = []
with open ('mnist_train.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for rows in reader:
        mat.append(rows)
mat = np.asarray(mat)
magic = mat[:,0]
mat = np.delete(mat,0,1)
for i in range(0,len(mat)):
    train_data.append(mat[i].reshape(28,28))
train_data = np.asarray(train_data)
train_data = train_data.astype(np.uint8)
with open('mnist_train_magic','wb') as fp:
    pickle.dump(magic, fp)
