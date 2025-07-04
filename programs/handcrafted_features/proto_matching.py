# =============================================================================
# constructs a prototype digit by computing the average image out of a given
# set (train/test) then one can compute the similarity between a given image
# and said prototype by computing their dot product
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt

# resconstruct 16 x 15 image from 240 x 1 graysacle vector
def reconstruct_image(grayscale_vector):

    image_data = grayscale_vector.reshape((16, 15))

    plt.imshow(image_data, cmap='gray')
    plt.axis('off')
    plt.show()

# construct prototype digit using mean
def prototype(digit, train_data):
    
    proto_digit = np.array([])
    for i in range(240):
        average_pixel_value = 0
        for j in range(100):
            average_pixel_value += train_data[100 * digit + j][i]
        average_pixel_value /= 100
        proto_digit = np.append(proto_digit, average_pixel_value)
        
    return proto_digit

# compare prototype of digit to a given training sample row via the dot product
def dot_prod_compare(proto_digit, training_digit):
    return np.dot(proto_digit, training_digit) / (np.linalg.norm(proto_digit) * np.linalg.norm(training_digit))

# this is similar to dot_prod_compare, just used for features_to_csv.py instead
def dot_prod_compare_remake(digit, image, train_data):
    proto_digit = prototype(digit, train_data)
    return round(dot_prod_compare(proto_digit, image), 2)

# outputs the similarity of prototype digit with testing data digits
# training data used to construct prototype
# testing data used for comparison
def similarity_ranking(digit, data):
    
    proto_digit = prototype(digit, data)
    reconstruct_image(proto_digit)
    cosine_similarities = []
    for i in range(10):
        avg = 0
        for j in range(100):
            avg += dot_prod_compare(proto_digit, test_data[100 * i + j])
        cosine_similarities.append([i, np.round(avg / 100, 3)])
    
    print(f'Ranked cosine similarities of prototype digit {digit} with testing data:')
    for element in sorted(cosine_similarities, key = lambda x : x[1], reverse = True):
        print(element)
    print("\n")


if __name__ == "__main__":

    # load data
    with open('../data.txt', 'r') as file:
        dataset = np.array([list(map(int, line.split())) for line in file])

    # parition data into training and testing datasets
    train_data = np.empty((0, 240))
    test_data  = np.empty((0, 240))
    for i in range(10):
        train_data = np.vstack((train_data, dataset[200 * i : 200 * i + 100]))
        test_data  = np.vstack((test_data , dataset[200 * i + 100 : 200 * i + 200]))
        
    # data = test_data
    # for digit in range(10):
    #     similarity_ranking(digit, data)

    proto = prototype(8, train_data)
    temp = train_data[550]
    # reconstruct_image(temp)
    print(dot_prod_compare(proto, temp))
