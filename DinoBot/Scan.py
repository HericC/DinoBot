class Scan:
    def __init__(self, x, y):
        self.colorLight = (83, 83, 83)
        self.colorDark = (172, 172, 172)

        self.len_x = x
        self.len_y = y

    def __compareArrayRGB(self, array):
        for i in range(len(array)):
            if array[i] != self.colorLight[i] and array[i] != self.colorDark[i]:
                return False
        return True

    def __insideScreen(self, x, y, default):
        """
        verifica se as coord estão dentro do limite

        :param x:
        :param y:
        :param default: define qual dimensão será verificado
        :return:
        """
        if not default:
            if x >= self.len_x:
                return False
        else:
            if y >= self.len_y:
                return False
        return True

    def scanArray(self, loop, array, x, y, default=True):
        """
        percorre um array, cada indice é um array contendo os valores do RGB
        compara os indices com as cores predefinidas, se for True, retorna o indice

        :param loop: config do 'for in range'
        :param array:
        :param x:
        :param y:
        :param default: define em qual dimensão será pecorrido
        :return:
        """
        for i in range(loop[0], loop[1], loop[2]):
            if self.__insideScreen(x+i, y+i, default):
                if default:
                    if self.__compareArrayRGB(array[y+i][x]):
                        return i
                elif self.__compareArrayRGB(array[y][x+i]):
                    return i
        return None

    def notScanArray(self, loop, array, x, y, default=True):
        """
        percorre um array, cada indice é um array contendo os valores do RGB
        compara os indices com as cores predefinidas, se for False, retorna o indice

        :param loop: config do 'for in range'
        :param array:
        :param x:
        :param y:
        :param default: define em qual dimensão será pecorrido
        :return:
        """
        for i in range(loop[0], loop[1], loop[2]):
            if self.__insideScreen(x+i, y+i, default):
                if default:
                    if not self.__compareArrayRGB(array[y+i][x]):
                        return i
                elif not self.__compareArrayRGB(array[y][x+i]):
                    return i
        return None
