

# -*- coding: utf-8 -*-\
"""
Created on Thu Sep 01 22:10:03 2016

@author: Hrishikesh aka Jack

feature=[1 gremarks,2toefl score,3 percentage,4 work_exp,5paperpublished,6 university level]
label: admit=>1 , reject=>0
paper published : 0- none ,1-national,2-international,3-multiple national,4-multiple international
work_exp: in months
university level: 0-C grade, 1-Known B grade,2-Known good tier,3-super Top universities in india


THIS FILE IS ABOUT : The refined student admit-reject data is obtained from admissions.py in the form of list of student profile and their corresponding
admits or reject.
Here in this file , classifiers are generated for the university and stored in a pkl file.
The generated classifiers are then used in classifyfile for inference purposes.

This file also comes into picture when a new profile with real admit-reject is to be added to the list of existing students and retrain the classifier
with the new updated data .
"""



from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn import linear_model

import pickle
from sklearn.metrics import accuracy_score
from sklearn import cross_validation
import matplotlib.pyplot as plt
from IPython.display import Image
import pydot
from sklearn.externals.six import StringIO 
import random
import numpy as np
import admissions
from sklearn.model_selection import learning_curve
from sklearn.neighbors import KNeighborsClassifier
#from plot_learning_curve import plot_learning_curve

universityName = ''


'''
feat
ures=[[305,89,70,47,0,1],
  ?'int clf.predict([313,106,74,0,1,2])#predicted correct ,was tough

print clf.predict([300,100,77,18,0,1])#predicted correct

print clf.predict([314,100,73,30,0,2])#predicted correct

print clf.predict([307,97,86,30,0,0])#incorrect prediction (her quant was below 160) 
                                    #,not selected but predicting selected
print clf.predict([320,110,58,12,2,1])


featurenames=['GRE','TOEFL','Percentage','Work Experience','Paper Published','University Level']
targetnames=['admit','reject']

dot_data = StringIO()  
tree.export_graphviz(clf, out_file=dot_data,  
                         feature_names=featurenames,  
                         class_names=targetnames,  
                         filled=True, rounded=True,  
                         special_characters=True)  
graph = pydot.graph_from_dot_data(dot_data.getvalue())
  
graph[0].write_pdf("utdallas_decisiontree.pdf")

'''




def universityClassifier(university):
    # procuring features and labels from university
    features = university.profile1
    labels = university.profile1target
    samplee = [160, 160, 310, 110, 75, 10, 3, 1]

    #sampleobservation = [158, 165, 323, 110, 58, 12, 2, 1]

    #ddecisiontree classifier
    #dt_classifier=decisiontree_Classification(features,labels,2)
    #gradient descent classifier
    #sgd_classifier=sgd_classification(features,labels)

    #print 'Predictions'

    #print 'DT : '+str(dt_classifier.predict(samplee))
    #print 'SGD : '+str(sgd_classifier.predict(samplee))

    svm_classifier ,svmscore,svmplt= svm_Classification(features, labels)
    print 'SVM Classifier generated.'

    knnclassifier , knnscore = knnClassification(features,labels)
    print 'KNN Classifier generated.'
    dtclassifier , dtscore = decisiontree_Classification(features,labels,2)
    print 'Decision Tree Classifier.'

    context ={
        'svc':svm_classifier,
        'svcscore':svmscore,
        'svmplt':svmplt,
        'knn':knnclassifier,
        'knnscore':knnscore,
        'dt' :dtclassifier,
        'dtscore':dtscore,
    }

    '''
    with open('my_svc_classifier.pkl', 'rb') as fid:
       svm_classifier = pickle.load(fid)

    print 'SVM : ' + str(svm_classifier.predict(samplee))
    '''
    return context


def super_classifier(classification_function,university,sample_observation):
    balance=0
    features = university.profile1
    labels = university.profile1target
    for i in range(20):
        clf = classification_function(features,labels,i)
        prediction= clf.predict(sample_observation)
        if prediction=='admit':
            balance=balance+1
        else:
            balance=balance-1

    print
    if balance>=-1:
        print 'Final Verdict ADMIT'
    else :
        print 'Final Verdict REJECT'


def decisiontree_Classification(features,labels,random):

    dtclassifier = tree.DecisionTreeClassifier(max_depth=4,random_state=0)
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(features, labels, test_size=0.3,
                                                                   random_state=random)
    '''
    print 'Decision TRee Classifier'

    print 'X train '+str(X_train)
    print 'y train '+str(y_train)
    print
    print 'X test '+str(X_test)
    print 'Y Test '+str(y_test)
    '''

    dtclassifier.fit(X_train,y_train)
    predictions=dtclassifier.predict(X_test)
    dtscore =dtclassifier.score(X_test, y_test)
    #print 'dt score '+str()
    return dtclassifier,dtscore


def sgd_classification(features,labels):
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(features, labels, test_size=0.3,
                                                                         random_state=0)
    sgdclassifier = linear_model.SGDClassifier()
    sgdclassifier.fit(X_train,y_train)
    wannacheck=True
    if wannacheck==True:
        predictions = sgdclassifier.predict(X_test)
        print 'Accuracy Score SGD' +str(accuracy_score(y_test,predictions))

    return sgdclassifier

def knnClassification(features,labels):
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(features, labels, test_size=0.3,
                                                                         random_state=0)
    knnclassifier = KNeighborsClassifier(n_neighbors=5)
    knnclassifier.fit(X_train,y_train)
    knnscore = knnclassifier.score(X_test,y_test)

    return knnclassifier,knnscore


def svm_Classification(features, labels):
        print '\nSupport Vector Machine - Crossvalidated Prediction\n'
        # 1. Split into training and test data

        X_train, X_test, y_train, y_test = cross_validation.train_test_split(features, labels, test_size=0.2,
                                                                             random_state=0)

        # 2 . Declare estimator

        estimator = SVC(kernel='poly', degree=1)

        # 3. Choose cross_validation iterator

        from sklearn.cross_validation import ShuffleSplit
        cv = ShuffleSplit(np.array(X_train).shape[0], n_iter=10, test_size=0.2, random_state=1)

        # 4. Tune the hyperparameters : Applying the cross-validation hyperparameter on the training set

        from sklearn.grid_search import GridSearchCV
        gammas = np.logspace(-6, -1, 10)
        classifier = GridSearchCV(estimator=estimator, cv=cv, param_grid=dict(gamma=gammas))

        classifier.fit(X_train, y_train)
        print 'jjjfjnjd'
        yes = True

        # 5. Debug algorithm with the learning curve
        # from sklearn.learning_curve import learning_curve
        plt = None
        if yes == False:
            print '1'
            # title = 'Learning Curves (SVM, Polynomial kernel,' % classifier.best_estimator_.gamma
            title = 'Learning Curves Polynomial SVM \n' + universityName
            estimator = SVC(kernel='linear', gamma=classifier.best_estimator_.gamma)
            print '2'
            plt = plot_learning_curve(estimator, title, X_train, y_train, cv=cv)
            print '3'
            # plt.show()
            print '4'

        # Final evaluation on test set
        score = classifier.score(X_test, y_test)
        print 'Score = ' + str(score)

        '''
        svm_ispickled=False
        import pickle
        #pickle the classifier
        if svm_ispickled ==False:

            with open('my_svc_classifier.pkl','wb') as fid:
                pickle.dump(classifier,fid)

            with open('my_svc_classifier.pkl','rb') as fid:
                classifier=pickle.load(fid)


        '''

        return classifier, score, plt




def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and training learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross-validation,
          - integer, to specify the number of folds.
          - An object to be used as a cross-validation generator.
          - An iterable yielding train/test splits.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt


#sampleobservation = [158, 165, 323, 110, 58, 12, 2, 1]



def pickle_classifier(classifier):
    return None



def createClassifier(auniversity):
    #print auniversity.name
    universityName = auniversity.name

    print '\n First: Extracting data from csv and transforming it into python lists'
    auniversity.list = admissions.AdmissionProfile(auniversity.admitfilename,auniversity.rejectfilename)
    print 'Successfully extracted and preprocessed data from .csv files'
    print '\n Creating Classifiers'
    context= universityClassifier(auniversity.list)

    auniversity.svm_classifier_comp = context['svc']  # some classifier -now SVC
    auniversity.svm_classifier_comp_score = context['svcscore']  # it's score when it was created
    #auniversity.svm_classifier_plt = context['svmplt']
    auniversity.dt_classifier_comp = context['dt']
    auniversity.dt_comp_score = context['dtscore']
    auniversity.knn_classifier_comp = context['knn']
    auniversity.knn_comp_score = context['knnscore']




    print 'Successfully created classifiers for university : '+str(auniversity.name)
    print













universityFiles={

    '1':'University Of Texas Dallas',
    '2':'Arizona State University',
    '3':'San Jose State University',
    '4':'Texas Arlington',
    '5':'Illinois Institute Of Technology',
    '6':'Rochester Institute Of Technology',
    '7':'New York University',
    '8':'Northeastern University',
    '9':'Virginia TEch'
}

'''
for i in universityFiles:
    print '\n'
    print universityFiles[i]
    print
    admitfile=i+'A.csv'
    rejectfile = i+'R.csv'
    collegelistdata=admissions.AdmissionProfile(admitfile,rejectfile)
    sampleobservation = [158, 165, 323, 110, 58, 12, 2, 1]
    universityClassifier(collegelistdata,sampleobservation)




print '\n\n            UtDallas'
utdallas=admissions.AdmissionProfile('1A.csv','1R.csv')
universityClassifier(utdallas,[158, 165, 323, 110, 58, 12, 2, 1])



print '\n\n         SanJose State'
sanjose=admissions.AdmissionProfile('3A.csv','3R.csv')
universityClassifier(sanjose,[158, 165, 323, 110, 58, 12, 2, 1])


print '\n\nTexas Arlington'
utarlington=admissions.AdmissionProfile('texasarlingtonadmits.csv','texasarlingtonrejects.csv')
universityClassifier(utarlington)

print '\n\nArizona State University'
arizonastate=admissions.AdmissionProfile('arizonastateadmits.csv','arizonastaterejects.csv')
universityClassifier(arizonastate)

print '\n\nNew York University'
newyorkuni=admissions.AdmissionProfile('newyorkuniversity_admits.csv','newyorkuniversity_rejects.csv')uni)

print '\n\nIllinois Institute Of Technology Chicago'
iitc = admissions.AdmissionProfile('iitc_admits.csv','iitc_rejects.csv')
universityClassifier(iitc)

print '\n\nNortheastern University'
northeastern = admissions.AdmissionProfile('northeastern_admits.csv','northeastern_rejects.csv')
universityClassifier(northeastern)

print '\n\nRochester Institute Of Technology'
rochester = admissions.AdmissionProfile('rochester_admits.csv','rochester_rejects.csv')
universityClassifier(rochester)

'''
'''



print '\n\nColumbia'
collist = admissions.AdmissionProfile('10A.csv','10R.csv')
universityClassifier(collist)
samplee=[165, 158, 323, 110, 64, 10, 0, 1]


print 'New Way'



super_classifier(decisiontree_Classification,collist,samplee)
print 'SVM Prediction'
print svmc.predict(samplee)

'''






