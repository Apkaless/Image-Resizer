import PIL
from PIL import Image, ImageTk
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread



img_extensions = ['png', 'jpg', 'jpeg', 'gif']
FONT_STYLE = "Helvetica"
FONT_SIZE = 20


class ResizerGUI(tkinter.Tk):
    image_to_resize = None
    img_format = None

    def __init__(self):
        super().__init__()
        self.geometry('800x800')
        self.title('Image Resizer')
        self.resizable(width=False, height=False)
        self.configure(bg='white')

        self.f1 = tkinter.Frame(self, width=800, height=200, background='black')
        self.f1.grid(row=0, column=0, sticky='ew')
        self.logo_text = tkinter.Label(self.f1, text='Image Resizer', font=(FONT_STYLE, FONT_SIZE, 'bold'),
                                       foreground='black', background='white')
        self.logo_text.place(x=0, y=0, relwidth=1, relheight=1)

        self.image_f2 = tkinter.Frame(self, width=800, height=300, background='white')
        self.image_f2.grid(column=0, row=2)

        self.img_btn_browser = tkinter.Button(self.image_f2, text='Browse Image', command=self.load_image)
        self.img_btn_browser.configure(relief='flat', borderwidth=2, highlightbackground='red', highlightthickness=2)
        self.img_btn_browser.grid(column=1, row=1, pady=(20, 0))

        self.img_info_f3 = tkinter.Frame(self, width=800, height=300, background='white')
        self.img_info_f3.grid(column=0, row=3, pady=(100, 0))

        self.width_label = tkinter.Label(self.img_info_f3, text='Width:', font=(FONT_STYLE, 10, 'bold'),
                                         background='white')
        self.width_label.place(x=0, y=0, relx=0.4, rely=0)

        self.height_label = tkinter.Label(self.img_info_f3, text='Height:', font=(FONT_STYLE, 10, 'bold'),
                                          background='white')
        self.height_label.place(x=0, y=0, relx=0.4, rely=0.1)

        self.width_entry = tkinter.Entry(self.img_info_f3, font=(FONT_STYLE, 10, 'bold'), background='white')
        self.width_entry.configure(relief='flat', borderwidth=2, highlightbackground='black', highlightthickness=2)
        self.width_entry.place(x=0, y=0, relx=0.5, rely=0)

        self.height_entry = tkinter.Entry(self.img_info_f3, font=(FONT_STYLE, 10, 'bold'), background='white')
        self.height_entry.configure(relief='flat', borderwidth=2, highlightbackground='black', highlightthickness=2)
        self.height_entry.place(x=0, y=0, relx=0.5, rely=0.1)

        self.img_btn_resize = tkinter.Button(self.img_info_f3, text='Resize Image', command=self.resizer)
        self.img_btn_resize.configure(relief='flat', borderwidth=2, highlightbackground='black', highlightthickness=2)
        self.img_btn_resize.place(x=0, y=0, relx=0.5, rely=0.6, anchor='center')

    def load_image(self):
        loading_thread = Thread(target=self.browser)
        loading_thread.start()

    def browser(self):
        img_path = filedialog.askopenfilename()
        if img_path:
            try:

                img = Image.open(img_path, mode='r')
                ResizerGUI.image_to_resize = img
                ResizerGUI.img_format = img.format
                img = img.resize((150, 150))
                tkimg = ImageTk.PhotoImage(img)
                display_img = tkinter.Label(self.image_f2, image=tkimg, compound='bottom', background='white')
                display_img.image = tkimg
                display_img.grid(row=0, column=1)
                return True
            except PIL.UnidentifiedImageError:
                print('Image Not Supported')
                return False
        else:
            print('No Image')
            return False

    def resizer(self):
        width = self.width_entry.get()
        height = self.height_entry.get()

        if ResizerGUI.image_to_resize is None:
            messagebox.showerror(title='Image', message='Please select an image')
            return False

        if width.isdigit() and height.isdigit():
            try:
                img = ResizerGUI.image_to_resize
                img = img.resize((int(width), int(height)))
                if str(ResizerGUI.img_format).lower() in img_extensions:
                    img.save('resized_img.' + ResizerGUI.img_format)
                    messagebox.showinfo(title='Image Resized', message='Image resized Successfully!')
                    return True
                else:
                    messagebox.showerror(title='Format Type', message='Format Type Not Supported!')
                    print('Image Format not supported')
                    return False
            except Exception as e:
                print(e)
                messagebox.showerror(title='Error Resizing', message='Error Resizing')
                return False
        else:
            messagebox.showerror(title='Value Error', message='Please make sure you entered the correct width and height')
            return False


if __name__ == '__main__':
    root = ResizerGUI()
    root.mainloop()
