import pickle

def error_analysis():
    pass

if __name__ == '__main__':
    f = open("dump.data", "r")
    X_test, y_test, y_pred = pickle.load(f)
    print 0
