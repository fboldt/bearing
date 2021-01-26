from sklearn.model_selection import cross_validate, KFold, GroupKFold
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
import numpy as np
from database import Database_Experimenter

"""
Class definition of dataset segmentation and experiments.
"""
debug = 0

class Experimenter(Database_Experimenter):
  """
  Datasets class wrapper for experiment framework.

  ...
  Attributes
  ----------
  acquisitions : dict
    Dictionary with the sample_rate, sample_size, conditions, dirdest and acquisitions
  
  Methods
  -------
  segmentate()
    Semgmentate the raw files.
  perform()
    Perform experiments.

  """
  def __init__(self, acquisitions, sample_size):
    self.sample_size = sample_size
    self.acquisitions = acquisitions['acquisitions']

  def segmentate(self):
    """
    Segmentate files by the conditions and returns signals data, signals
    condition and signals acquisition.
    """
    
    n = len(self.acquisitions)

    self.signal_dt = np.empty((0,self.sample_size))
    self.signal_or = []
    self.signal_gr = []

    for i,key in enumerate(self.acquisitions):
      acquisition_size = len(self.acquisitions[key])
      if debug:
        n_samples = 15
      else:
        n_samples = acquisition_size//self.sample_size
      print('{}/{} --- {}: {}'.format(i+1, n, key, n_samples))
      self.signal_dt = np.concatenate((self.signal_dt, self.acquisitions[key][:(n_samples*self.sample_size)].reshape(
          (n_samples,self.sample_size))))
      for j in range(n_samples):
        self.signal_gr.append(key)
        self.signal_or.append(key[0])

  def perform(self, clfs, scoring, verbose=0):
    
    self.segmentate()
    
    #print(self.signal_dt)
    #print(self.signal_or.shape)


    # Estimators
    for clf_name, estimator in clfs:
      print("*"*(len(clf_name)+8),'\n***',clf_name,'***\n'+"*"*(len(clf_name)+8))
      

      if clf_name == 'CNN':
        
        #print(self.signal_dt)
        x_train = self.signal_dt.reshape(self.signal_dt.shape[0], 1, self.signal_dt.shape[1])
        #print(x_train)

        y_train = np.array(self.signal_or)
        #print(y_train)
        y_train = y_train.reshape(y_train.shape[0], 1)
        #print(y_train)

        score = cross_validate(estimator, x_train, y_train,
                              scoring=scoring, cv=KFold(n_splits=2), verbose=verbose, error_score='raise')
        print("Kfold")
        for metric,s in score.items():
          print(metric, ' \t', s, ' Mean: ', format(s.mean(), '.2f'), ' Std: ', format(s.std(), '.2f'))

        score = cross_validate(estimator, x_train, y_train,
                              self.signal_gr, scoring, cv=GroupKFold(n_splits=2), verbose=verbose)
        print("GroupKfold")
        for metric,s in score.items():
          print(metric, ' \t', s, ' Mean: ', format(s.mean(), '.2f'), ' Std: ', format(s.std(), '.2f'))

      else:    
        score = cross_validate(estimator, self.signal_dt, np.array(self.signal_or),
                              scoring=scoring, cv=KFold(n_splits=2), verbose=verbose, error_score='raise')
        print("Kfold")
        for metric,s in score.items():
          print(metric, ' \t', s, ' Mean: ', format(s.mean(), '.2f'), ' Std: ', format(s.std(), '.2f'))

        score = cross_validate(estimator, self.signal_dt, np.array(self.signal_or),
                              self.signal_gr, scoring, cv=GroupKFold(n_splits=2), verbose=verbose)
        print("GroupKfold")
        for metric,s in score.items():
          print(metric, ' \t', s, ' Mean: ', format(s.mean(), '.2f'), ' Std: ', format(s.std(), '.2f'))
        
        print("Custom - First 10 samples of each health condition for training")
        aux = self.signal_or[0]
        ind = [0]
        for i in range(len(self.signal_or)):
          if aux != self.signal_or[i]:
            ind.append(i)
            aux = self.signal_or[i]

        signal_dt_train = []
        signal_dt_test = []
        signal_or_train = []
        signal_or_test = []
        signal_dt_aux = []
        signal_or_aux = []

        for i in range(len(ind)):
          if i < len(ind)-1:
            signal_dt_aux = self.signal_dt[ind[i]:ind[i+1]]
            signal_or_aux = self.signal_or[ind[i]:ind[i+1]]
          else:
            signal_dt_aux = self.signal_dt[ind[i]:]
            signal_or_aux = self.signal_or[ind[i]:]
          signal_dt_train.extend(signal_dt_aux[0:10])
          signal_or_train.extend(signal_or_aux[0:10])
          signal_dt_test.extend(signal_dt_aux[10:])
          signal_or_test.extend(signal_or_aux[10:])

        estimator.fit(signal_dt_train, signal_or_train)
        pred = estimator.predict(signal_dt_test)

        print("test_accuracy: ", format(accuracy_score(signal_or_test, pred), '.2f'))
        print("test_f1_macro: ", format(f1_score(signal_or_test, pred, average='macro'), '.2f'))
