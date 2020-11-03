import pyautogui
import time
import numpy as np

from .Matrix import Matrix
from .Game import Game
from .NeuralNetwork import Network

from Data import Data


def start(loop=1, reset_data=False):
    if loop >= 0:
        game = Game()
        network = Network(5, 20, 3)
        data = Data(game, network)

        if reset_data:
            data.reset()

        data.load()

        if game.getDinoPosition():
            game.restart()
            clickCenter()

            num = 1
            while True:
                if game.update():
                    network.training(game.getScore()['highestScore'])
                    data.save()
                    if loop != 0 and num == loop:
                        break
                    game.restart()
                    clickCenter()
                    num += 1
                move(network.feed_forward(game.getObstacle()))
        print('\033[1;36mBot Encerrado!\033[0;0m')
    else:
        raise Exception('loop --> Número Inteiro Positivo!')


def clickCenter():
    """
    move o mouse para o centro da tela, e clica depois de meio segundo
    :return:
    """

    size = pyautogui.size()
    width = size.width
    height = size.height

    pyautogui.moveTo((width/2, height/2))
    time.sleep(0.5)
    pyautogui.click()


def move(data):
    output = data['output'].get_data()
    action = np.argmax(output[0])
    if action == 0:
        pyautogui.keyUp('down')
        pyautogui.keyDown('up')

    elif action == 1:
        pyautogui.keyUp('up')
        pyautogui.keyDown('down')

    else:
        pyautogui.keyUp('up')
        pyautogui.keyUp('down')
