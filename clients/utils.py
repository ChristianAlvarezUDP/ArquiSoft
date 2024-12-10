class Colores:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def input_int(prompt: int) -> int:
    while True:
        try:
            return int(input(prompt))
        except KeyboardInterrupt:
            quit()
        except:
            print(Colores.FAIL + "Ingrese un numero" + Colores.ENDC)