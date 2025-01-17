import asyncio
import kaiscr_speed as kaiscr
import os
import tkinter
from PIL import Image
from PIL import ImageTk
from io import BytesIO

os.system('adb root && adb forward tcp:6000 localfilesystem:/data/local/debugger-socket')

width = 480
height = 960

# Scale factor needed to fit on smaller desktop displays
scale_factor = 0.8

root = tkinter.Tk()
root.title('KaiLive')
root.geometry('x'.join([str(int(width * scale_factor)), str(int(height * scale_factor))]))
cv = tkinter.Canvas(root, width=width, height=height, background='white')
cv.pack(fill=tkinter.BOTH, expand=tkinter.YES)

takescreenshot = kaiscr.TakeScreenshot()
screenshot = takescreenshot.screenshotSpeed
bye = takescreenshot.close
stop = False

def quit(*args):
    global stop
    stop = True
    bye()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", quit)

async def update_pic():
    global cv,root
    global takescreenshot
    try:
        while not stop:
            png =await screenshot()
            im = Image.open(BytesIO(png))
            # Resize to fit the screen
            im = im.resize((int(width * scale_factor), int(height * scale_factor)))
            img = ImageTk.PhotoImage(image=im)
            # Anchor image top-left/ Northwest (NW)
            cv.create_image(0, 0, image=img, anchor='nw')
            root.update()

    except Exception as e:
        print(e)

loop = asyncio.get_event_loop()
results = loop.run_until_complete(update_pic())

loop.close()
