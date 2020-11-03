from .Scan import Scan
import pyautogui
import time
import timeit
import numpy as np


class Game:
    def __init__(self):
        self.__dinoPosition = {
            'left': -1,
            'top': -1,
            'width': -1,
            'height': -1,
        }
        self.__dinoFront = (-1, -1)

        self.__score = 0
        self.__velocity = 0
        self.__time = timeit.default_timer()

        self.__highestScore = 0
        self.__training = 0

        self.__obstacle = {
            'width': -1,
            'height': -1,
            'dino_distance': -1,
            'floor_distance': -1
        }
        self.__lastObstacle = {
            'bool': False,
            'time': timeit.default_timer()
        }

    def update(self):
        """
        atualiza os dados do game
        :return:
        """

        assert self.__dinoFront[0] != -1, 'Posição do Dino não encontrada, Utilize o Metodo "getDinoPosition()"'

        self.__upVelocity()

        if self.__searchObstacle():
            self.__lastObstacle['bool'] = True
        else:
            if self.__lastObstacle['bool']:
                self.__addScore()
                self.__lastObstacle['bool'] = False
                self.__lastObstacle['time'] = timeit.default_timer()

        """
        se estiver detectando obstaculos por 6 segundos, verifica se deu 'GameOver'
        """
        if timeit.default_timer() - self.__lastObstacle['time'] > 6:
            if self.checkGameOver():
                self.__training += 1
                print('\033[1;31mGameOver\033[0;0m')
                return True
        return False

    def restart(self):
        """
        reinicia o game
        redefine os principais atributos
        :return:
        """

        print('\033[1;33mBot Reiniciando...\033[0;0m')
        self.__score = 0
        self.__velocity = 0
        self.__time = timeit.default_timer()
        self.__lastObstacle = {
            'bool': False,
            'time': timeit.default_timer()
        }
        time.sleep(2)
        print('\033[1;34mBot Reiniciado!\033[0;0m')

    @staticmethod
    def checkGameOver():
        """
        checa se apareceu a mensagem de 'GameOver'
        :return:
        """

        mode = ('light', 'dark')
        for i in range(2):
            # for j in range(4):
            if pyautogui.locateOnScreen(f'./img/gameover/gameover{4}_{mode[i]}.png'):
                return True
        return False

    def __upVelocity(self):
        """
        aumenta a velocidade do game com o passar do tempo, numa taxa de '0.1' a cada '1.666666666666667' segundos

        velocidade inicial 6
        velocidade maxima alcançavel 13

        :return:
        """

        if self.__velocity < 7:
            if timeit.default_timer() - self.__time >= 1.666666666666667:
                self.__time = timeit.default_timer()
                self.__velocity += 0.1

            if self.__velocity > 7:
                print('Velocidade Maxima!')

    def getDinoPosition(self):
        """
        busca a posição do Dino na tela 10 vezes a cada 4 segungdos
        :return:
        """

        while True:
            print('\033[1;33mProcurando Dino...\033[0;0m')
            for i in range(10):
                position = pyautogui.locateOnScreen('./img/dino.png')
                if position:
                    print('\033[1;34mDino Encontrado!\033[0;0m')
                    self.__dinoPosition = {
                        'left': position[0],
                        'top': position[1],
                        'width': position[2],
                        'height': position[3],
                    }
                    self.__dinoFront = position[0] + position[2], position[1] + position[3] / 2
                    return True

            print('\033[1;31mDino não Encontrado!\n'
                  'Verificando Novamente em 4 Segundos.\033[0;0m')
            time.sleep(4)

    def __searchObstacle(self):
        """
        realiza uma busca por obstaculos na tela
        :return:
        """

        """tira uma foto da tela e o converte numa matrix"""
        img = pyautogui.screenshot(region=(self.__dinoFront[0], self.__dinoPosition['top'] - 40, 400, 200))
        img = np.array(img)

        scan = Scan(len(img[0]), len(img))

        end = 140   # limite da tela
        con = 200   # limite de confirmação

        """
        Busca a distancia do Obstaculo
        
        'x' percorre a tela da esquerda para a direita
        'y' percorre a tela de cima para baixo
        
        'x' e 'y' são as coord do Obstaculo do seu lado esquerdo
        'x' é a distancia do Dino até o Obstaculo
        
        se não encontrar redefine os atributos do Obstaculo
        """
        for x in range(len(img[0])):
            y = scan.scanArray((0, end, 2), img, x, 0)
            if y:
                self.__obstacle['dino_distance'] = x

                """
                Busca a largura do Obstaculo
                
                'x_reverse' percorre a tela da direita para a esquerda
                y_reverse percorre a tela de cima para baixo
                
                'x_reverse' e 'y_reverse' são as coord do Obstaculo do seu lado direito
                a largura do Obstaculo é 'x - x_reverse'
                """
                for x_reverse in range(len(img[0])-1, -1, -1):
                    y_reverse = scan.scanArray((0, end, 2), img, x_reverse, 0)
                    if y_reverse:
                        self.__obstacle['width'] = x_reverse - x

                        """
                        Busca a altura do Obstaculo

                        'y_height' percorre a tela de cima para baixo
                        'x_height' percorre a tela da esquerda para a direita

                        'x_height' e 'y_height' são as coord da parte de cima do Obstaculo
                        
                        'height' percorre o obstaculo de cima para baixo até não detectar o Obstaculo
                        'height' é a altura do Obstaculo
                        """
                        for y_height in range(end):
                            x_height = scan.scanArray((0, x_reverse, 2), img, x, y_height, False)
                            if x_height:
                                height = scan.notScanArray((0, con, 1), img, x + x_height, y_height)
                                if height and height > 20:
                                    self.__obstacle['height'] = height

                                    """
                                    Busca a altura do Obstaculo em relação ao chão
                                    
                                    'floor' percorre da parte de baixo do obstaculo até o chão
                                    
                                    se 'floor' for diferente de None, 'height' é multiplicado por 3 e percorre 'floor' novamente
                                    'floor' é a distancia do Obstaculo em relação ao chão
                                    
                                    se 'floor' for None, a distancia do Obstaculo em relação ao chão é 0
                                    """
                                    floor = scan.scanArray((0, con, 1), img, x + x_height, y_height + height)
                                    if floor:
                                        self.__obstacle['height'] *= 3
                                        floor = scan.scanArray((0, con, 1), img, x + x_height, y_height + self.__obstacle['height'])
                                        if floor:
                                            self.__obstacle['floor_distance'] = floor
                                            return True
                                    self.__obstacle['floor_distance'] = 0
                                    return True
        self.__obstacle = {
            'width': -1,
            'height': -1,
            'dino_distance': -1,
            'floor_distance': -1,
            'velocity': self.__velocity
        }
        return False

    def __addScore(self):
        self.__score += 1
        if self.__score > self.__highestScore:
            self.__highestScore = self.__score

    def getScore(self):
        return {
            'score': self.__score,
            'highestScore': self.__highestScore
        }

    def getObstacle(self):
        return self.__obstacle

    def getVelocity(self):
        return self.__velocity

    def getTraining(self):
        return self.__training

    def setData(self, dic):
        try:
            self.__highestScore = int(dic['highestScore'])
            self.__training = int(dic['training'])
            return True
        except ValueError:
            print('\033[1;31mError: não foi possivel atribuir a dic.\033[0;0m')
            return False
