import asyncio
import websockets
import cv2
import numpy
import base64
import io
from PIL import Image
import cv2

# Ingresso dell'immagine BASE64, CONVERSIONE in CV2 Image.
def stringToRGB(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    img = Image.open(io.BytesIO(imgdata))
    opencv_img = cv2.cvtColor(numpy.array(img), cv2.COLOR_BGR2RGB)

    # ELABORAZIONE DELL'IMMAGINE:
    for i in range(0, 3):
        ret, thresh = cv2.threshold(opencv_img[:,:,i], 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(opencv_img, contours, -1, (0,255,0), 3)

    cv2.imwrite("ricciHappy.png", opencv_img)

    return opencv_img

async def logic(websocket):
    ricciMsg = await websocket.recv()
    print("MSG RECV --> {}".format(ricciMsg))

    # Decodifico l'immagine, applico un semplice algoritmo:
    recvImg = stringToRGB(ricciMsg)

    # Qui posso anche ri-spedire l'immagine indietro al client...
    # reply = "{}".format(recvImg)  # <--- Questo sarebbe un esempio!
    # await websocket.send(reply)   # <--- Questo sarebbe un esempio!

    # Invece, preparo un semplice messaggio come risposta:
    reply = "Ricci è omozigote {}".format("Successo!")
    await websocket.send(reply)

async def main():
    async with websockets.serve(logic, "localhost", 4533):
        await asyncio.Future()

asyncio.run(main())
