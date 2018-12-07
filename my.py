from sklearn import svm
import pandas as pd
import numpy as np

data = pd.read_csv('ee.csv')
data = np.array(data)
X = data[..., :137]
Y = data[..., 137:141]
clf = svm.SVC(kernel='linear', C=1.0)
clf.fit(X, range(len(X)))
x = [X[0]]
t = clf.predict(x)
print(Y)
