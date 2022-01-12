# -*- coding: utf-8 -*-
"""comparing-regression-models.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ErJNnnYvDxjvxkYNBz7On9nZzrb9TxX7

**Hello everyone.This is a notebook comparing various regression models such as Ridge,Knn,Bayesian Regression,Decision Tree and SVM.**
*It is extremely beneficial for beginners to take a close look at the notebook so as to get an insight as to how different algorithms work and also which algorithms can perform better in some cases depending upon cases*
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

# from subprocess import check_output
# print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.

# Commented out IPython magic to ensure Python compatibility.
# Importing packages

import os
import pandas as pd
from keras import Sequential
from keras.layers import Dense
from pandas import DataFrame,Series
from sklearn import tree
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import statsmodels.formula.api as smf
import statsmodels.api as sm
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from sklearn import neighbors
from sklearn import linear_model
# %matplotlib inline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.model_selection import cross_val_score
from statistics import mean
from numpy import savetxt
from sklearn.pipeline import Pipeline

import warnings
warnings.filterwarnings('ignore')

f = pd.read_excel("TahminSon_Grafik_Raw.xlsx","tum")

data=DataFrame(f)
data.head()[:2]

"""*Getting non-object elements*

"""

X_data=data.dtypes[data.dtypes!='object'].index
X_train=data[X_data]
X_train.head()[:2]

X_train.describe()

# Finding all the columns with NULL values

np.sum(X_train.isnull())

# Filling all Null values
X_train=X_train.fillna(0)
columns=X_train.columns.tolist()

#X1     X2    X3  X4(%)  Ø(°)   Fs(kay)   Fs(dev)  Fs(topgoc)


y1=(X_train['Fs(kay)'],'Fs(kay)')
y2=(X_train['Fs(dev)'],'Fs(dev)')
y3=(X_train['Fs(topgoc)'],'Fs(topgoc)')
y_list = [y1,y2,y3]

X_train.drop(["Fs(kay)", "Fs(dev)", "Fs(topgoc)"],axis=1,inplace=True)

for y_ in y_list:
    y = y_[0]
    y = list(y)
    y_name = y_[1]

    X_train.head()[:2]

    # GETTING Correllation matrix
    corr_mat=X_train.corr(method='pearson')
    plt.figure(figsize=(20,10))
    sns.heatmap(corr_mat,vmax=1,square=True,annot=True,cmap='cubehelix')

    X_Train=X_train.values
    X_Train=np.asarray(X_Train)

    # Finding normalised array of X_Train
    X_std=StandardScaler().fit_transform(X_Train)

    # from sklearn.decomposition import PCA
    # pca = PCA().fit(X_std)
    # plt.plot(np.cumsum(pca.explained_variance_ratio_))
    # plt.xlim(0,7,1)
    # plt.xlabel('Number of components')
    # plt.ylabel('Cumulative explained variance')
    #
    # """**Since 5 components can explain more than 70% of the variance, we choose the number of the components to be 5**"""
    #
    # from sklearn.decomposition import PCA
    # sklearn_pca=PCA(n_components=5)
    # X_Train=sklearn_pca.fit_transform(X_std)

    sns.set(style='darkgrid')
    f, ax = plt.subplots(figsize=(8, 8))
    # ax.set_aspect('equal')
    ax = sns.kdeplot(X_Train[:,0], X_Train[:,1], cmap="Greens",
              shade=True, shade_lowest=False)
    ax = sns.kdeplot(X_Train[:,1], X_Train[:,2], cmap="Reds",
              shade=True, shade_lowest=False)
    ax = sns.kdeplot(X_Train[:,2], X_Train[:,3], cmap="Blues",
              shade=True, shade_lowest=False)
    red = sns.color_palette("Reds")[-2]
    blue = sns.color_palette("Blues")[-2]
    green = sns.color_palette("Greens")[-2]
    ax.text(0.5, 0.5, "2nd and 3rd Projection", size=12, color=blue)
    ax.text(-4, 0.0, "1st and 3rd Projection", size=12, color=red)
    ax.text(2, 0, "1st and 2nd Projection", size=12, color=green)
    plt.xlim(-6,5)
    plt.ylim(-2,2)

    number_of_samples = len(y)
    x_train = X_Train[:1024]
    y_train=y[:1024]
    x_test=X_Train[1024:]
    y_test=y[1024:]
    y_Train=list(y_train)

    keras = Sequential()
    keras.add(Dense(4, input_dim=2, activation='relu'))
    keras.add(Dense(4, activation='relu'))
    keras.add(Dense(1, activation='sigmoid'))
    keras.compile(loss='binary_crossentropy', optimizer='adam')

    models = ['Ridge Regression', 'Knn', 'Bayesian Regression', 'Decision Tree', 'SVM', "Lin. Reg.", "Pol. Reg", "Keras"]
    modelObjects = [linear_model.Ridge(),neighbors.KNeighborsRegressor(5,weights='uniform'),linear_model.BayesianRidge(),
                    tree.DecisionTreeRegressor(max_depth=1),svm.SVR(),linear_model.LinearRegression(),
                    Pipeline([('polfeat',  PolynomialFeatures(degree = 4)), ('linreg', linear_model.LinearRegression())]),keras]
    y_all = y_test.copy()
    train_errors = []
    test_errors = []
    for modelname, model in zip(models, modelObjects):
        model.fit(x_train, y_train)
        y_predict = model.predict(x_train)

        error = 0
        for i in range(len(y_Train)):
            error += (abs(y_Train[i] - y_predict[i]) / y_Train[i])
        train_error = error / len(y_Train) * 100
        print("Train error = "'{}'.format(train_error) + " percent in Ridge Regression")
        train_errors.append(train_error)
        Y_predict = model.predict(x_test)
        y_Predict = list(Y_predict)
        y_Test = list(y_test)
        y_all = np.column_stack((y_all, y_Predict))
        error = 0
        for i in range(len(y_Test)):
            error += (abs(y_Predict[i] - y_Test[i]) / y_Predict[i])
        test_error = error / len(y_Test) * 100
        print("Test error = "'{}'.format(test_error) + " percent in {}".format(modelname))
        test_errors.append(test_error)

        matplotlib.rcParams['figure.figsize'] = (6.0, 6.0)

        preds = pd.DataFrame({"preds": model.predict(x_train), "true": y_train})
        preds["residuals"] = preds["true"] - preds["preds"]
        preds.plot(x="preds", y="residuals", kind="scatter")
        plt.title("Residual plot in {}".format(modelname))
        plt.savefig("graph/train_test_residual_{}_{}.png".format(y_name,modelname))

    df = DataFrame(y_all)
    df.to_excel("Train-Test-"+str(y_name).replace("(","").replace(")","")+"-"+"_preds.xlsx","sheet")

    col={'Train Error':train_errors,'Test Error':test_errors}

    df=DataFrame(data=col,index=models)

    df.plot(kind='bar')

    plt.savefig("graph/train_test_{}_barplot.png".format(y_name))

    cv = LeaveOneOut()

    y_all = y_test.copy()
    for modelname, model in zip(models, modelObjects):
        error = 0

        scores = cross_val_score(model, x_train, y, scoring='neg_mean_absolute_error',
                                 cv=cv, n_jobs=-1)
        y_predict = cross_val_predict(model, x_train, y, cv=cv)

        y_all = np.column_stack((y_all, y_predict))
        print("Test error = " + '{}'.format(mean(scores)) + " percent" + " in {}".format(modelname))

        matplotlib.rcParams['figure.figsize'] = (6.0, 6.0)
        preds = pd.DataFrame({"preds": model.predict(x_train), "true": y_train})
        preds["residuals"] = preds["true"] - preds["preds"]
        preds.plot(x="preds", y="residuals", kind="scatter")
        plt.title("Residual plot in {}".format(modelname))
        plt.savefig("graph/loo_residual_{}_{}.png".format(y_name,modelname))

    df = DataFrame(y_all)
    df.to_excel("Train-Test-"+str(y_name).replace("(","").replace(")","")+"-"+"_preds.xlsx","sheet")

    col={'Train Error':train_errors,'Test Error':test_errors}

    df=DataFrame(data=col,index=models)

    df.plot(kind='bar')

    plt.savefig("graph/loo_{}_barplot.png".format(y_name))


"""**Seems that KNN turned out to be the winner.Its because of the fact that there are very large number of data points and and also  features are highly continuous**
*Moreover the dimentionality of the processed data is not too high*
"""