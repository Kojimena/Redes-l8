# --------------------------------- #
# Cifrado de una imagen con AES en modo ECB y CBC
# Integrantes:
# - Jimena Hernández
# - Mark Albrand
# --------------------------------- #

from PIL import Image
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Función para cargar la imagen y convertirla a una matriz de bytes
def load_image(image_path):
    img = Image.open(image_path).convert('RGBA')  
    img_array = np.array(img)  
    img_bytes = img_array.tobytes()  
    return img_bytes, img_array.shape

# Función para guardar la imagen a partir de bytes
def save_image(image_bytes, shape, output_path):
    truncated_bytes = image_bytes[:shape[0] * shape[1] * shape[2]]
    img_array = np.frombuffer(truncated_bytes, dtype=np.uint8).reshape(shape)
    img = Image.fromarray(img_array, 'RGBA')  
    img.save(output_path)

# Función para cifrar la imagen usando AES en modo ECB
def encrypt_image_ecb(image_bytes, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_bytes = cipher.encrypt(pad(image_bytes, AES.block_size))  
    return encrypted_bytes

# Función para cifrar la imagen usando AES en modo CBC
def encrypt_image_cbc(image_bytes, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_bytes = cipher.encrypt(pad(image_bytes, AES.block_size))  
    return encrypted_bytes

image_path = "tux.bmp"
output_ecb_path = "tux_ecb_encrypted.png"
output_cbc_path = "tux_cbc_encrypted.png"

image_bytes, image_shape = load_image(image_path)

# Clave para AES de 128 bits (16 bytes)
key = os.urandom(16)

# Cifrado en modo ECB
encrypted_bytes_ecb = encrypt_image_ecb(image_bytes, key)

# Guardar la imagen cifrada en ECB (truncamos para coincidir con el tamaño original)
save_image(encrypted_bytes_ecb, image_shape, output_ecb_path)
print(f"Imagen cifrada con ECB guardada en {output_ecb_path}")

# Cifrado en modo CBC
# Vector de inicialización aleatorio
iv = os.urandom(16)
encrypted_bytes_cbc = encrypt_image_cbc(image_bytes, key, iv)

save_image(encrypted_bytes_cbc, image_shape, output_cbc_path)
print(f"Imagen cifrada con CBC guardada en {output_cbc_path}")
