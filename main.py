from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont
from tkinter import filedialog, ttk

FONT_NAME = "Courier"

colors = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'grey': (128, 128, 128),
    'blue': (0, 0, 255),
    'pink': (255, 0, 255),
    'red': (255, 0, 0)
}

def coef_photo_size(height, width):
    return width/height
def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename
def open_img():
    x = openfn()
    img = Image.open(x)
    img.save("photo_for_watermarking.jpg")
    width, height = img.size
    print(f'images width: {width} and height: {height}')
    pic_width = round(width/height*400)
    img = img.resize((pic_width, 400), Image.LANCZOS)
    img = img.convert('RGBA')
    img = ImageTk.PhotoImage(img)
    panel.config(text="", image=img)
    panel.image = img


def open_logo():
    y = openfn()
    logo = Image.open(y)
    logo.save('opened_logo.png')
    logo_width, logo_height = logo.size
    pic_width = round(logo_width/logo_height * 160)
    logo = logo.resize((pic_width, 160), Image.LANCZOS)
    logo = logo.convert('RGBA')
    logo = ImageTk.PhotoImage(logo)
    panel_logo.config(text="", image=logo)
    panel_logo.image = logo


def count_pos(width, height, text_width, text_height, pos):
    if pos == 'down right':
        x = width - text_width - text_width/10  # right pad
        y = height - text_height - text_height/2  # down pad
    elif pos == 'up left':
        x = 10
        y = 10
    elif pos == 'center':
        x = width/2 - text_width/2
        y = height/2 - text_height/2
    position = (round(x), round(y))
    return position

def save():
    im = Image.open('photo_with_watermarking.png')
    filename = filedialog.asksaveasfile(mode='wb', defaultextension=".png")
    if filename is None:
        return
    im.save(filename)

def show_text_watermark():
    #get data from Comboxes and Entries
    text = entry_watermark.get()
    transparency = int(transparency_entry.get())
    color = tuple(list(colors[combo_color.get()]) + [transparency]) #add transparecy into the tuple
    choosen_font = combo_font.get() + ".ttf"
    pos = combo_position.get()
    font_size = int(size_entry.get())
    #open photo
    photo = Image.open('photo_for_watermarking.jpg')
    photo = photo.convert('RGBA')

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new("RGBA", photo.size, (255, 255, 255, 0))

    # get a drawing context
    drawing = ImageDraw.Draw(txt)

    font = ImageFont.truetype(choosen_font.lower(), font_size)
    #count photo width and height, text width and height to count position
    width, height = photo.size
    text_box = font.getbbox(text)
    text_width = text_box[2] - text_box[0]
    text_height = text_box[3] - text_box[1]
    position = count_pos(width=width, height=height, text_width=text_width, text_height=text_height, pos=pos)
    #adding watermark
    drawing.text(position, text, fill=color, font=font)
    photo = Image.alpha_composite(photo, txt)
    # (local) save and show new photo
    photo.save("photo_with_watermarking.png")
    width, height = photo.size
    pic_width = round(width / height * 400)
    photo = photo.resize((pic_width, 400), Image.LANCZOS)
    photo = photo.convert('RGB')
    photo = ImageTk.PhotoImage(photo)
    panel.config(image=photo)
    panel.image = photo


def show_logo_watermark():
    #get data from Comboxes and Entries
    angle = int(angle_entry.get())
    pos = combo_logo_position.get()
    size_logo = int(size_logo_entry.get())

    #open photo
    photo = Image.open('photo_for_watermarking.jpg')
    photo = photo.convert('RGBA')
    width, height = photo.size
    pic_width = round(width / height * 400)

    #open logo
    logo = Image.open('opened_logo.png')
    logo = logo.convert('RGBA')
    width_logo, height_logo = logo.size

    #resize logo and rotation
    width_logo = round(width_logo * size_logo/100)
    height_logo = round(height_logo * size_logo/100)
    logo = logo.rotate(angle)
    logo = logo.resize((width_logo, height_logo))

    # count position
    position = count_pos(width=width, height=height, text_width=width_logo, text_height=height_logo, pos=pos)
    # adding watermark
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 150))
    transparent.paste(photo, (0, 0))
    transparent.paste(logo, position, mask=logo)

    # (local) save and show new photo
    transparent.save("photo_with_watermarking.png")
    transparent = transparent.resize((pic_width, 400), Image.LANCZOS)
    transparent = transparent.convert('RGB')
    transparent = ImageTk.PhotoImage(transparent)
    panel.config(image=transparent)
    panel.image = transparent



window = Tk()
window.title("Watermaker Desctop App")
window.geometry("1350x600")
window.config(pady=50, padx=50, bg='white')


start_img = Image.open('start.jpg')
start_img = start_img.resize((600, 400), Image.LANCZOS)
start_img = ImageTk.PhotoImage(start_img)
start_logo = Image.open('logo.jpg')
start_logo = start_logo.resize((240, 160), Image.LANCZOS)
start_logo = ImageTk.PhotoImage(start_logo)

panel = Label(padx=2, pady=2, image=start_img, text='Upload your photo', font=(FONT_NAME, 20, "bold"), compound=CENTER)
panel.image = start_img
panel.grid(column=0, row=1, columnspan=2, rowspan=12, padx=20)

btn_open = Button(window, text='Open Image', command=open_img, padx=10)
btn_open.grid(column=0, row=0, pady=20, padx=20)

btn_save = Button(window, text='Save Image', padx=10, command=save)
btn_save.grid(column=1, row=0, pady=20, padx=20)

btn_show_text = Button(window, text='Show Text Watermark', padx=10, command=show_text_watermark)
btn_show_text.grid(column=2, row=0)

watermark_label = Label(text='Enter your watermark text', bg='white')
watermark_label.grid(column=2, row=1)

entry_watermark = Entry(window, width=50, borderwidth=2)
entry_watermark.grid(column=2, row=2)
entry_watermark.insert(END, string="Example")

font_label = Label(text='Choose a font style', bg='white')
font_label.grid(column=2, row=3)

combo_font = ttk.Combobox(window, width=47, values=["Times", "Arial", "Georgia", "Verdana"])
combo_font.grid(column=2, row=4)

size_label = Label(text='Enter font size', bg='white')
size_label.grid(column=2, row=5)

size_entry = Entry(window, width=50, borderwidth=2)
size_entry.grid(column=2, row=6)
size_entry.insert(END, string="0")

type_label = Label(text='Choose watermark color', bg='white')
type_label.grid(column=2, row=7, padx=5)

combo_color = ttk.Combobox(window, width=47, values=['white', 'black', 'grey', 'blue', 'pink', 'red'])
combo_color.grid(column=2, row=8, padx=5)

position_label = Label(text='Choose position', bg='white')
position_label.grid(column=2, row=9, padx=5)

combo_position = ttk.Combobox(window, width=47, values=['center', 'down right', 'up left'])
combo_position.grid(column=2, row=10, padx=5)

transparency_label = Label(text=f'Enter text transparency level. \n0 - Full Transparency, 255 - Full Opacity', bg='white')
transparency_label.grid(column=2, row=11, padx=5)

transparency_entry = Entry(window, width=50, borderwidth=2)
transparency_entry.grid(column=2, row=12, padx=5)
transparency_entry.insert(END, string="150")

btn_show_logo = Button(window, text='Show Logo Watermark', padx=10, command=show_logo_watermark)
btn_show_logo.grid(column=3, row=0)

btn_open_logo = Button(window, text='Open Logo', command=open_logo, padx=10)
btn_open_logo.grid(column=3, row=1)

panel_logo = Label(padx=2, pady=2, image=start_logo, text='Upload your logo', font=(FONT_NAME, 10, "bold"), compound=CENTER)
panel_logo.image = start_logo
panel_logo.grid(column=3, row=2, rowspan=5, padx=2, pady=2)

angle_label = Label(window, text='Enter the angle of rotation', bg='white')
angle_label.grid(column=3, row=7)

angle_entry = Entry(window, width=40, borderwidth=2)
angle_entry.grid(column=3, row=8)
angle_entry.insert(END, string="0")

position_logo = Label(text='Choose Logo position', bg='white')
position_logo.grid(column=3, row=9)

combo_logo_position = ttk.Combobox(window, width=40, values=['center', 'down right', 'up left'])
combo_logo_position.grid(column=3, row=10)

logo_size_label = Label(text=f'Enter logo size in %', bg='white')
logo_size_label.grid(column=3, row=11)

size_logo_entry = Entry(window, width=42, borderwidth=2)
size_logo_entry.grid(column=3, row=12)
size_logo_entry.insert(END, string="100")


window.mainloop()
