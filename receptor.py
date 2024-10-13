import os
import cv2
import numpy as np
import time

# Função para detectar a cor (preto ou branco)


def detectar_cor(frame):
    # Definir área central
    altura, largura, _ = frame.shape
    centro_x, centro_y = largura // 2, altura // 2
    tamanho_area = 25

    # Recorte da área central
    area_central = frame[centro_y - tamanho_area:centro_y +
                         tamanho_area, centro_x - tamanho_area:centro_x + tamanho_area]

    # Converter para o espaço de cores HSV
    hsv = cv2.cvtColor(area_central, cv2.COLOR_BGR2HSV)

    # Definir intervalos de cores para preto e branco
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])

    # Verde
    lower_green = np.array([35, 52, 72])
    upper_green = np.array([85, 255, 255])

    # Roxo
    lower_purple = np.array([130, 50, 50])
    upper_purple = np.array([160, 255, 255])

    # Criar máscaras para preto e branco
    mask_black = cv2.inRange(hsv, lower_black, upper_black)
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)

    # Contar pixels nas máscaras
    black_pixels = np.sum(mask_black == 255)
    white_pixels = np.sum(mask_white == 255)
    green_pixels = np.sum(mask_green == 255)
    purple_pixels = np.sum(mask_purple == 255)

    # Número total de pixels da área (dividido por 3 para RGB)
    total_pixels = area_central.size // 3

    # Definir um limite para considerar a cor predominante
    limite = total_pixels * 0.5

    # Se a maioria dos pixels forem pretos, brancos, verdes ou vermelhos, retorna a respectiva cor
    if black_pixels > limite:
        return "Preto"
    elif white_pixels > limite:
        return "Branco"
    elif green_pixels > limite:
        return "Verde"
    elif purple_pixels > limite:
        return "Roxo"
    else:
        return "Preto"


contBit = 0
# Função para registrar a cor detectada em um arquivo .txt


def registrar_cor(cor):
    with open("registroBinario.txt", "a", encoding='utf-8') as arquivo:
        if cor == "Preto":
            global contBit
            contBit += 1
            print(contBit)
            arquivo.write("1")

        elif cor == "Branco":
            contBit += 1
            print(contBit)
            arquivo.write("0")


def binary_to_text(binary_string):
    """Converte uma string binária (em blocos de 8 bits) para texto."""
    text = ''
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]  # Pega 8 bits por vez
        text += chr(int(byte, 2))  # Converte para caractere ASCII
    return text


# Capturar vídeo da webcam
cap = cv2.VideoCapture(0)

# Ajustar a exposição da câmera (valor baixo)
cap.set(cv2.CAP_PROP_EXPOSURE, 0)

# Definir o intervalo de tempo em segundos para registrar uma nova cor
# Intervalo de 5 segundos e no cell 3800ms///3 e de 2000ms///2 e de 1000ms//
intervalo_tempo = 2
ultimo_registro = time.time()  # Marca o tempo do último registro

# Variáveis de controle para o processo
registro_ativo = False
processo_finalizado = False
delayContagem = True

while True:
    # Ler o frame da webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Inverter o frame verticalmente
    frame = cv2.flip(frame, 1)

    # Detectar a cor predominante na área central
    cor = detectar_cor(frame)

    # Se detectarmos verde e o registro ainda não estiver ativo
    if cor == "Verde" and not registro_ativo:
        print("Início dos registros!")
        registro_ativo = True

    # Se detectarmos roxo, finaliza o processo
    if cor == "Roxo" and registro_ativo and not processo_finalizado:
        print("Fim dos registros!")
        processo_finalizado = True
        registro_ativo = False

    # Se o registro estiver ativo e não finalizado, registrar preto ou branco
    if registro_ativo and not processo_finalizado:
        if cor in ["Preto", "Branco"] and delayContagem:
            print("entrou")
            time.sleep(0.12)  # 0.12 = 14dig. em=1000
            delayContagem = False

        # Calcular o tempo restante para o próximo registro
        tempo_atual = time.time()
        tempo_restante = max(
            0, int(intervalo_tempo - (tempo_atual - ultimo_registro)))

        if cor in ["Preto", "Branco"] and tempo_restante == 0:
            # Registrar a cor detectada
            registrar_cor(cor)
            ultimo_registro = tempo_atual  # Atualizar o tempo do último registro

    # Desenhar a área central (quadrado) na imagem
    altura, largura, _ = frame.shape
    centro_x, centro_y = largura // 2, altura // 2
    tamanho_area = 25
    cv2.rectangle(frame, (centro_x - tamanho_area, centro_y - tamanho_area),
                  (centro_x + tamanho_area, centro_y + tamanho_area), (0, 255, 0), 2)

    # Exibir a cor detectada e o contador regressivo na tela
    cv2.putText(frame, f"Cor detectada: {
                cor}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    if registro_ativo and cor in ["Preto", "Branco"]:
        cv2.putText(frame, f"Proximo registro em: {
                    tempo_restante}s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Mostrar o vídeo com a área e o nome da cor
    cv2.imshow('Reconhecimento de Cor', frame)

    # Sair ao pressionar a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        if os.path.exists("registroBinario.txt"):  # Verifica se o arquivo existe
            with open("registroBinario.txt", "r", encoding='utf-8') as file:
                binary_data = file.read()

            if len(binary_data) % 8 != 0:
                print("Erro: A sequência binária não tem múltiplos de 8 bits!")
            else:
                converted_text = binary_to_text(binary_data)

                with open("texto_traduzido.txt", "w", encoding='utf-8') as output_file:
                    output_file.write(converted_text)

                print("Texto convertido e salvo em 'texto_traduzido.txt'.")
        else:
            print("O arquivo 'registroBinario.txt' não foi encontrado.")
        break

# Liberar a captura e fechar as janelas
cap.release()
cv2.destroyAllWindows()
