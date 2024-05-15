import asyncio
import websockets
import cv2
import base64

# Conversione dell'immagine in BASE64:
def toBase64(path):
    img = cv2.imread(path)
    jpg_img = cv2.imencode('djannis.png', img)
    b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')
    return b64_string

print("Ciro Esposito Caricato.")

# Connessione al ws:
async def connection():
    uri = "ws://localhost:4533"
    async with websockets.connect(uri) as websocket:
        okay = input("Press to send. ")

        # Applico la conversione ed invio l'immagine al server:
        b64_string = toBase64('image.png')
        await websocket.send(b64_string)
        print(f">>> IMG Sent.")

        # In base alla risposta, potrei fare tante altre cose...
        response = await websocket.recv()
        # Ma printo solamente ciò che mi arriva:
        print(f"<<< {response}")


asyncio.run(connection())