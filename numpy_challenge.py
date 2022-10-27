# 3 ways to create an array
if __name__ == "__main__":
    print(np.arange(7))
    print(np.ones(7))
    print(np.eye(7))
    
# 1. This function takes 2 matrices and multiplies them (NOT by elements) and returns the result
def matrix_multiplication(m, n):
    return np.dot(m, n)

  
# 2. This function checks takes some matrices, checks if matrices can be multiplied in the order they are presented and returns True if they can or False if they can't
def multiplication_check(*matrices):
    mult = 0 # var for further storage of multiply result
    rows, cols = matrices[0].shape
    mult = matrices[0]
    for matr in matrices[1:]:
        rows, cols = matr.shape
        if rows == mult.shape[1] or cols == mult.shape[0]:
            mult = np.dot(mult, matr)
        else:
            return False
    return True
  
# 3. This function takes some matrices, checks if matrices can be  in the order they are presented and returns the result of multiplication if they can or False if they can't

def multiply_matrices(*matrices):
    mult = 0 # var for further storage of multiply result
    rows, cols = matrices[0].shape
    mult = matrices[0]
    for matr in matrices[1:]:
        rows, cols = matr.shape
        if (rows == mult.shape[1] or cols == mult.shape[0]):
            mult = np.dot(mult, matr)
        else:
            return None
    return mult

# 4. This function takes two 1d arrays, each with a couple of coordinates and returns a distance between them
def compute_2d_distance(arr1, arr2):
    return np.linalg.norm(arr1 - arr2)
  
# 5. This function takes two 1d arrays with any equal quantity of coordinates and returns a distance between them
def compute_multidimensional_distance(arr1, arr2):
    return compute_2d_distance(arr1, arr2)

# 6. This function takes one 2d array with any number of arrays in it and returns distance between each and every one
def compute_pair_distances(arr_2d):
    x2 = np.sum(arr_2d ** 2, axis=1) # summing squares of all vector elements
    y2 = np.sum(arr_2d ** 2, axis=1)
    xy = np.matmul(arr_2d, arr_2d.T)
    x2 = x2.reshape(-1, 1)
    return np.sqrt(x2 - 2*xy + y2)
