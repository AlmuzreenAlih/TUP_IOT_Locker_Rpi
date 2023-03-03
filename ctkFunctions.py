
from PIL import Image

def tkShow(ctk,Widget,SourceImage, Percentage):
    img = Image.open(SourceImage)
    my_image = ctk.CTkImage(light_image=img, dark_image=img, size=(Percentage*img.width, Percentage*img.height))
    Widget.configure(image=my_image)

def tkPack(Widget):
    Widget.place(relx=0.5, rely=0.5, anchor="center")

def tkHide(Widget):
    Widget.place_forget()
    
import shutil
import os

def copy(file_path, to_folder, renamed=None):
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")

    # Create the destination folder if it doesn't exist
    os.makedirs(to_folder, exist_ok=True)

    # Get the base name of the file (i.e. the file name without the path)
    if renamed is None:
        file_name = os.path.basename(file_path)
    else:
        file_name = renamed

    # Copy the file to the destination folder
    shutil.copy2(file_path, os.path.join(to_folder, file_name))

    print(f"{file_path} copied to {os.path.join(to_folder, file_name)}.")
