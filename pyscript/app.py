from pyscript import display, document, window
from js import Uint8Array, File, URL, document
import asyncio
import numpy
import io

from PIL import Image, ImageFilter
from pyodide.ffi import create_proxy
from pyweb import pydom

async def execute(e):
    print("Python Funziona...")
    # aaa

        
def clear(event):
    toEliminate = document.getElementById("blank")
    toEliminate.removeChild(toEliminate.firstElementChild)

    toEliminate = document.getElementById("inputSpace")
    toEliminate.removeChild(toEliminate.firstElementChild)

    newSpace = document.createElement("input")
    newSpace.type = "file"
    newSpace.id = "file-upload"
    toEliminate.appendChild(newSpace)

    upload_file = create_proxy(_upload_file_and_show)
    document.getElementById("file-upload").addEventListener("change", upload_file)

    print("IMG Deleted.")


def _upload_file_and_show(e):

    print("Attempted file upload: " + e.target.value)
    file_list = e.target.files
    first_item = file_list.item(0)

    new_image = document.createElement('img')
    new_image.src = window.URL.createObjectURL(first_item)
    document.getElementById("blank").appendChild(new_image)


upload_file = create_proxy(_upload_file_and_show)
document.getElementById("file-upload").addEventListener("change", upload_file)


async def _upload_change_and_show(e):
    #Get the first file from upload
    file_list = e.target.files
    first_item = file_list.item(0)

    # PRENDO IN INGRESSO L'IMMAGINE!
    array_buf = await first_item.arrayBuffer()
    array_galli = Uint8Array.new(array_buf)
    bytes_list = bytearray(array_galli)
    my_bytes = io.BytesIO(bytes_list) 
    my_image = Image.open(my_bytes)

    # INFO DELL'IMMAGINE!
    print("{} - {} - {}".format(my_image.format, my_image.width, my_image.height))

    # PROCESSING ALL'IMMAGINE!
    my_image = my_image.filter(ImageFilter.EMBOSS).resize((500, 500))

    # RISPUTO FUORI L'IMMAGINE
    my_stream = io.BytesIO()
    my_image.save(my_stream, format="PNG")

    image_file = File.new([Uint8Array.new(my_stream.getvalue())], "new_image_file.png", {type: "image/png"})

    new_image = document.createElement('img')
    new_image.src = window.URL.createObjectURL(image_file)
    document.getElementById("output_upload_pillow").appendChild(new_image)


# Run image processing code above whenever file is uploaded    
upload_file = create_proxy(_upload_change_and_show)
document.getElementById("file-upload-pillow").addEventListener("change", upload_file)
