
from PIL import Image

def tkRender(ctk,Widget,SourceImage, Percentage):
    if isinstance(SourceImage, str):
        img = Image.open(SourceImage)
    else:
        pass
        # img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        # pil_image = Image.fromarray(img_rgb)
    my_image = ctk.CTkImage(light_image=img, dark_image=img, size=(Percentage*img.width, Percentage*img.height))
    Widget.configure(image=my_image)

def tkPack(Widget):
    Widget.place(relx=0.5, rely=0.5, anchor="center")

def tkHide(Widget):
    try:
        Widget.place_forget()
    except:
        pass
    
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

def SortingLH(List,Axis):
    return sorted(List,key=lambda x: x[Axis])
    
class inverse_str(str):
    """
    A string that sorts in inverse order.
    """
    def __lt__(self, rhs):
        return not super().__lt__(rhs)

def SortingHL(List,Axis):
    # x = sorted(List,key=lambda x: (-x[Axis],inverse_str(x[1]))) #or sort them from the tertiary to primary
    # x = sorted(List,key=lambda x: (-x[Axis],x[1])) #this also works for max/min, kung ano una niyang nakitang max or min, yun pa rin kasi
    x = sorted(List,key=lambda x: (-x[Axis]))
    return x

# def haha():
#     for i in GUI3.winfo_children():
#         if isinstance(i, ctk.CTkButton) and i.cget("text").isdecimal():
#             print(i.cget("text"), ())

def Send(SerialData, character, Description):
    SerialData.write(bytes(character, "utf-8"))
    print("ARDUINO SEND: ", Description)

def SendWait(SerialData, character, timeout, Description):
    SerialData.write(bytes(character, "utf-8"))
    reading = SerialData.read().decode("utf-8")
    ST = time.time()
    while True:
        if reading != "":
            break
        if time.time() - ST > timeout:
            break
    print("ARDUINO SEND: ", Description)