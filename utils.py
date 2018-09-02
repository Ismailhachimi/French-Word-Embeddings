import numpy as np
import keras.backend as K
import os, shutil

########################### Sentences loading ##############################

class MySentences(object):
    def __init__(self, dirname):    
        """
        Sentences loading class
        A memory-friendly iterator for word2vec model.
        # Arguments
            dirname : directory path of sentencens/data files.
        # Returns
            Sentences.
        """
        self.dirname = dirname
 
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

def read_sentences(path):
    """
    Sentences loading function.
    A simple reader/loader for the attention model.
    # Arguments
        path : directory path of sentencens/data files.
    # Returns
        Sentences.
    """
    tmp = []
    with open(path) as file:
        for sentence in file.readlines():
            tmp.append(sentence.strip())
    return np.array(tmp)
                
    
########################## For Keras layers #################################

def softmax(x, axis=1):
    """
    Softmax activation function.
    # Arguments
        x : Tensor.
        axis: Integer, axis along which the softmax normalization is applied.
    # Returns
        Tensor, output of softmax transformation.
    # Raises
        ValueError: In case `dim(x) == 1`.
    """
    ndim = K.ndim(x)
    if ndim == 2:
        return K.softmax(x)
    elif ndim > 2:
        e = K.exp(x - K.max(x, axis=axis, keepdims=True))
        s = K.sum(e, axis=axis, keepdims=True)
        return e / s
    else:
        raise ValueError('Cannot apply softmax to a tensor that is 1D')
     
    
########################## For Keras layers #################################
    
def save_model_json(model, word_dim):
    """
    serialize model to json.
    # Arguments
        model : keras model.
        word_dim : w2v word length
    # Returns
        file_name : the model file name
    """
    model_json = model.to_json()

    with open("model_{}.json".format(word_dim), "w") as json_file:
        json_file.write(model_json)
    
    # serialize weights to HDF5
    model.save_weights("model_{}.h5".format(word_dim))
    print("Saved model to disk")
    
    file_name = 'model_{}'.format(word_dim)
    return file_name
    
def load_model_json(file_name):
    """
    load model from json.
    # Arguments
        model : keras model.
        word_dim : w2v word length
    # Returns
        model : keras model
    """
    json_file = open(file_name+".json", "r")
    loaded_model_json = json_file.read()
    json_file.close()

    model = model_from_json(loaded_model_json)

    # load weights into new model
    model.load_weights(file_name+".h5")

    print("Loaded model from disk")
    
    return model

############################## Glove model  ################################

def similar_posneg(model, positive, negative, topn=10):
    """
    Doc is not available
    """
    mean_vecs = []
    
    for word in positive: 
        mean_vecs.append(model.word_vectors[model.dictionary[word]])
    for word in negative: 
        mean_vecs.append(-1*model.word_vectors[model.dictionary[word]])

    mean = np.array(mean_vecs).mean(axis=0)
    mean /= np.linalg.norm(mean)        
        
    dists = np.dot(model.word_vectors, mean)
    
    best = np.argsort(dists)[::-1]
    
    results = [(model.inverse_dictionary[i], dists[i]) for i in best if (model.inverse_dictionary[i] not in positive and 
                                                                         model.inverse_dictionary[i] not in negative)][:topn]
    
    return results
    
############################### More utils #################################

def get_by_address(address):
    """
    get a variable by its address function.
    # Arguments
        address : Variable Adress.
    # Returns
        Variable.
    # Raises
        Error removing a file.
    """
    return [x for x in globals().values() if id(x)==address]

def delete_weights(folder='./models'):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)