import pickle

weight_file = open('weights.pkl','rb')
weights = pickle.load(weight_file)
bias_file=open('biases.pkl','rb')
biases = pickle.load(bias_file)

print(weights)
print(biases)