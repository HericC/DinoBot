import pickle
import timeit
import time


class Data:
    def __init__(self, game, network):
        self.__game = game
        self.__network = network

    def load(self):
        print('\033[1;33mCarregando Dados...\033[0;0m')
        initTime = timeit.default_timer()

        file1 = open('fileTXT/data_game.txt', 'rb')
        dic1 = pickle.load(file1)
        file1.close()
        self.__game.setData(dic1)

        file2 = open('fileTXT/weights_network.txt', 'rb')
        dic2 = pickle.load(file2)
        file2.close()
        self.__network.setAll(dic2)

        if timeit.default_timer() - initTime < 2:
            time.sleep(2)
        print('\033[1;34mDados Carregados!\033[0;0m')

    def save(self):
        print('\033[1;33mSalvando Dados...\033[0;0m')
        initTime = timeit.default_timer()

        dic1 = {
            'highestScore': self.__game.getScore()['highestScore'],
            'training': self.__game.getTraining()
        }
        file1 = open('fileTXT/data_game.txt', 'wb')
        pickle.dump(dic1, file1)
        file1.close()

        dic2 = self.__network.getAll()
        file2 = open('fileTXT/weights_network.txt', 'wb')
        pickle.dump(dic2, file2)
        file2.close()

        if timeit.default_timer() - initTime < 2:
            time.sleep(2)
        print('\033[1;34mDados Salvos!\033[0;0m')

    @staticmethod
    def reset():
        print('\033[1;33mResetando Dados...\033[0;0m')
        initTime = timeit.default_timer()

        dic1 = {
            'highestScore': 0,
            'training': 0
        }
        file1 = open('fileTXT/data_game.txt', 'wb')
        pickle.dump(dic1, file1)
        file1.close()

        file2 = open('fileTXT/weights_network.txt', 'wb')
        pickle.dump(None, file2)
        file2.close()

        if timeit.default_timer() - initTime < 2:
            time.sleep(2)
        print('\033[1;34mDados Resetado!\033[0;0m')

    @staticmethod
    def view():
        print('\033[1;33mBuscando Dados...\033[0;0m')
        initTime = timeit.default_timer()

        file1 = open('fileTXT/data_game.txt', 'rb')
        dic1 = pickle.load(file1)
        file1.close()

        file2 = open('fileTXT/weights_network.txt', 'rb')
        dic2 = pickle.load(file2)
        file2.close()

        if timeit.default_timer() - initTime < 2:
            time.sleep(2)

        print('\033[1;35mGame:\033[0;0m', dic1)
        print('\033[1;35mNetwork:\033[0;0m', dic2)
