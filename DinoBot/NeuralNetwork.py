from .Matrix import Matrix


class Network:
    def __init__(self, i_nodes, h_nodes, o_nodes):
        self.__i_nodes = i_nodes
        self.__h_nodes = h_nodes
        self.__o_nodes = o_nodes

        self.__bias_ih = Matrix(1, self.__h_nodes)
        self.__bias_ho = Matrix(1, self.__o_nodes)
        self.__weights_ih = Matrix(self.__i_nodes, self.__h_nodes)
        self.__weights_ho = Matrix(self.__h_nodes, self.__o_nodes)

        self.__bias_ih.randomize()
        self.__bias_ho.randomize()
        self.__weights_ih.randomize()
        self.__weights_ho.randomize()

        self.__learning_rate = 0.1

    def feed_forward(self, data):
        data['width'] /= 80
        data['height'] /= 160
        data['dino_distance'] /= 400
        data['floor_distance'] /= 80
        data['velocity'] /= 7

        if type(data) == list:
            inputs = Matrix.array_to_matrix(data)
        elif type(data) == dict:
            inputs = []
            for i in list(data.items()):
                inputs.append(i[1])
            inputs = Matrix.array_to_matrix(inputs)
        else:
            raise Exception('error:', type(data))

        #   input -> hidden
        hidden = Matrix.dot(inputs, self.__weights_ih)
        hidden = Matrix.add(hidden, self.__bias_ih)
        hidden = Matrix.sigmoid(hidden)

        #   hidden -> output
        output = Matrix.dot(hidden, self.__weights_ho)
        output = Matrix.add(output, self.__bias_ho)
        output = Matrix.sigmoid(output)

        return {
            'hidden': hidden,
            'output': output
        }

    def training(self, score):
        pass

    def setAll(self, dic):
        if dic:
            self.__bias_ih = dic['bias_ih']
            self.__bias_ho = dic['bias_ho']
            self.__weights_ih = dic['weights_ih']
            self.__weights_ho = dic['weights_ho']
            self.__learning_rate = dic['learning_rate']

    def getAll(self):
        return {
            'bias_ih': self.__bias_ih,
            'bias_ho': self.__bias_ho,
            'weights_ih': self.__weights_ih,
            'weights_ho': self.__weights_ho,
            'learning_rate': self.__learning_rate
        }
