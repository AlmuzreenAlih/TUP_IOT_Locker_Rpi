
from PIL import Image

def tkShow(ctk,Widget,SourceImage, Percentage):
    img = Image.open(SourceImage)
    my_image = ctk.CTkImage(light_image=img, dark_image=img, size=(Percentage*img.width, Percentage*img.height))
    Widget.configure(image=my_image)

def tkPack(Widget):
    Widget.place(relx=0.5, rely=0.5, anchor="center")

def tkHide(Widget):
    Widget.place_forget()