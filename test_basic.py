import cv2
import tkinter as tk
from PIL import Image, ImageTk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("识别人类")
        
        self.cap = None
        
        btn = tk.Button(root, text="启动", command=self.start)
        btn.pack(pady=10)
        
        self.label = tk.Label(root)
        self.label.pack()
    
    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.update_frame()
    
    def update_frame(self):
        if not self.cap:
            return
        
        ret, frame = self.cap.read()
        if ret:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img = img.resize((640, 480))
            img_tk = ImageTk.PhotoImage(image=img)
            self.label.config(image=img_tk)
            self.label.image = img_tk
        
        self.root.after(30, self.update_frame)

root = tk.Tk()
app = App(root)
root.mainloop()
