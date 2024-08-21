import time
from pyfirmata import Arduino, util

# Configuração da placa Arduino
board = Arduino('/dev/ttyUSB0')  # Certifique-se de que a porta esteja correta

# Definição dos pinos
pinoAnalog = 0  # Pino A0 no Arduino
pinoRele = 8
pino5V = 7

# Configuração dos pinos como saídas
board.digital[pinoRele].mode = 1  # OUTPUT
board.digital[pino5V].mode = 1  # OUTPUT
board.digital[pino5V].write(1)  # Coloca o pino5V em estado Alto

# Leitura analógica usando pyFirmata
it = util.Iterator(board)
it.start()
board.analog[pinoAnalog].enable_reporting()

def analogRead(pin):
    # Lê o valor analógico do pino
    return board.analog[pin].read()

def map_value(value, fromLow, fromHigh, toLow, toHigh):
    # Mapeia o valor de uma escala para outra
    return (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow

while True:
    val_analog_in = analogRead(pinoAnalog)  # Lê o valor do sensor
    if val_analog_in is not None:
        val_analog_in = val_analog_in * 1023  # Converte para a escala 0-1023
        porcento = map_value(val_analog_in, 1023, 0, 0, 100)  # Mapeia para porcentagem

        print(f"{porcento}%")  # Imprime o valor da porcentagem

        if porcento <= 45:
            print("Irrigando a planta ...")
            board.digital[pinoRele].write(1)  # Liga o relé
        else:
            print("Planta Irrigada ...")
            board.digital[pinoRele].write(0)  # Desliga o relé

        time.sleep(1)  # Espera 1 segundo antes de repetir a leitura