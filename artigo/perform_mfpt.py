from mfpt import MFPT
from experimenter import Experimenter

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV


def main():
    debug = 0
    sample_size = 8192
    
    database = MFPT()
    database_acq = database.load()
    print(database_acq)
      
    #Classifiers
    
    # KNN
    from sklearn.neighbors import KNeighborsClassifier
    
    knn = Pipeline([
                    ('scaler', StandardScaler()),
                    ('knn', KNeighborsClassifier()),
                    ])
    
    parameters_knn = {'knn__n_neighbors': list(range(1,16,2))}
    
    knn = GridSearchCV(knn, parameters_knn)
    
    # SVM
    from sklearn.svm import SVC
    
    svm = Pipeline([
                    ('scaler', StandardScaler()),
                    ('svc', SVC()),
                    ])
    
    parameters_svm = {
        'svc__C': [10**x for x in range(-3,2)],
        'svc__gamma': [10**x for x in range(-3,1)],
        }
    
    svm = GridSearchCV(svm, parameters_svm)
    
    
    clfs = [('K-Nearest Neighbors', knn), ('SVM', svm)]
    scoring = ['accuracy', 'f1_macro']#, 'precision_macro', 'recall_macro']  
      
    database_exp = Experimenter(database_acq, sample_size)
    database_exp.perform(clfs, scoring)


if __name__ == "__main__":
  main()
