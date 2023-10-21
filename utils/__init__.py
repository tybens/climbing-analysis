import pickle 

def pickle_dump(obj, filename):
    with open('data/' + filename + '.pickle', 'wb') as f:
        pickle.dump(obj, f)


def pickle_load(filename):
    with open('data/' + filename + '.pickle', 'rb') as f:
        return pickle.load(f)