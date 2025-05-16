import cv2
from pyzbar import pyzbar
import pygame
import time  # Para el cooldown

# Inicializar pygame mixer
pygame.mixer.init()
beep_sound = pygame.mixer.Sound("sonidos/beep.mp3")  # Asegúrate de que esta ruta sea correcta

# Diccionario simulado de productos
productos = {
    '123456789012': {'nombre': 'Leche Entera', 'precio': 1100},
    '987654321098': {'nombre': 'Pan Integral', 'precio': 1300},
    '000111222333': {'nombre': 'Jugo de Naranja', 'precio': 1400},
    '010203040506': {'nombre': 'Torta de Lucuma', 'precio': 2000},
}

# Diccionario para manejar el cooldown de cada código
codigos_detectados = {}
COOLDOWN = 2  # segundos

def decodificar(frame):
    codigos = pyzbar.decode(frame)
    tiempo_actual = time.time()

    for codigo in codigos:
        x, y, w, h = codigo.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        datos = codigo.data.decode('utf-8')
        tipo = codigo.type

        # Verificar cooldown
        if datos in codigos_detectados:
            tiempo_ultimo = codigos_detectados[datos]
            if tiempo_actual - tiempo_ultimo < COOLDOWN:
                continue  # Aún en cooldown, ignorar

        # Actualizar último tiempo de escaneo
        codigos_detectados[datos] = tiempo_actual

        if datos in productos:
            producto = productos[datos]
            texto = f"{producto['nombre']} - ${producto['precio']:.2f}"

            cv2.putText(frame, texto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 255, 50), 2)

            print("🧾 Producto detectado:")
            print(f"  - Nombre: {producto['nombre']}")
            print(f"  - Precio: ${producto['precio']:.2f}")
            print(f"  - Código: {datos}")
            print("-" * 30)

            beep_sound.play()  # 🔊 Reproducir sonido

        else:
            texto = f"Código: {datos} - No registrado"
            cv2.putText(frame, texto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            print(f"⚠️ Código no registrado: {datos}")
    return frame

def main():
    cap = cv2.VideoCapture(0)
    print("📷 Escaneando... Presiona 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = decodificar(frame)
        cv2.imshow("Lector de Códigos de Barra", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
