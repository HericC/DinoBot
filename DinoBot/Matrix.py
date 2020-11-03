import numpy as np


class Matrix:
    def __init__(self, rows, cols):
        self.__rows = rows
        self.__cols = cols
        self.__data = np.zeros((self.__rows, self.__cols))

    def randomize(self):
        self.__data = np.random.rand(self.__rows, self.__cols)

    @staticmethod
    def array_to_matrix(array):
        matrix = Matrix(len(array), 1)
        matrix.__set_data(np.array([array]))
        return matrix

    @staticmethod
    def transpose(a):
        matrix = Matrix(a.get_rows(), a.get_cols())
        matrix.__set_data(np.transpose(a.get_data()))
        return matrix

    @staticmethod
    def add(a, b):
        matrix = Matrix(a.get_rows(), a.get_cols())
        matrix.__set_data(np.add(a.get_data(), b.get_data()))
        return matrix

    @staticmethod
    def subtract(a, b):
        matrix = Matrix(a.get_rows(), a.get_cols())
        matrix.__set_data(np.subtract(a.get_data(), b.get_data()))
        return matrix

    @staticmethod
    def multiply(a, b):
        matrix = Matrix(a.get_rows(), a.get_cols())
        matrix.__set_data(np.multiply(a.get_data(), b.get_data()))
        return matrix

    @staticmethod
    def dot(a, b):
        matrix = Matrix(a.get_rows(), a.get_cols())
        matrix.__set_data(np.dot(a.get_data(), b.get_data()))
        return matrix

    @staticmethod
    def climb(a, climb):
        matrix = Matrix(a.get_rows(), a.get_cols())
        for i in range(len(matrix.get_data())):
            for j in range(len(matrix.get_data()[i])):
                matrix.__set_data(a.get_data()[i][j] * climb, (i, j))
        return matrix

    @staticmethod
    def sigmoid(a):
        array = []
        for i in a.get_data():
            for j in i:
                array.append(1 / (1 + np.exp(-j)))
        return Matrix.array_to_matrix(array)

    def get_rows(self):
        return self.__rows

    def get_cols(self):
        return self.__cols

    def get_data(self):
        return self.__data

    def __set_data(self, data, pos=None):
        if type(data) == np.ndarray:
            self.__data = data
        elif pos:
            self.__data[pos[0]][pos[1]] = data
        else:
            raise Exception('Informe um objeto do tipo numpy.ndarray,'
                            'ou, um valor e um interavel com a sua posição na matrix')
