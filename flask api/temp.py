from sklearn.externals import joblib

# obj=pickle.load(open('scaling','rb'))


obj = joblib.load('my_scaler.pkl')  # load from disk


