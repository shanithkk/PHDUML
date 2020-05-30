import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.metrics import accuracy_score



balance_data=pd.read_csv('C:\\Users\\SHANi\\Desktop\\heart.csv',sep=',', header=None)
print(balance_data)

X = balance_data.values[:, 0:13]
Y = balance_data.values[:, 13]

print("================")
print(X)
print("================")
print(Y)

test_data=[[25,1,0,160,289,0,0,145,1,0.8,1,1,3]]


rfc = RandomForestClassifier()
rfc.fit(X,Y)
rfc_predict = rfc.predict(test_data)

print("prediction")
print(rfc_predict)




sv = svm.SVC(kernel='linear')

sv.fit(X, Y)

Y_pred_svm = sv.predict(test_data)
print("svm")
print(Y_pred_svm)

Y_pred_svm.shape
#
# score_svm = round(accuracy_score(Y_pred_svm,Y_test)*100,2)
# print("The accuracy score achieved using Linear SVM is: "+str(score_svm)+" %")