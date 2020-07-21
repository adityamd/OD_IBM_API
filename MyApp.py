
import tkinter as tk
import json
from watson_developer_cloud import VisualRecognitionV3
from PIL import ImageTk,Image

def get_keywords(path):
    visual_recognition = VisualRecognitionV3(
        '2018-03-19',
        iam_apikey='{api_key}')

    with open(path, 'rb') as images_file:
        classes = visual_recognition.classify(
            images_file,
            threshold='0.6',
        classifier_ids='default').get_result()
    return classes
    
class dialogBox:
    win=None
    def __init__(self,root,head,icon):
        self.win=tk.Toplevel(root)
        self.win.configure(bg="#087BA8",width=400)
        self.win.wm_maxsize(800,800)
        self.win.resizable(1,1)
        self.win.focus()
        self.win.grab_set()
        self.win.title(head)
        self.win.iconbitmap(icon)
    def display(self,classes,path):
        img = ImageTk.PhotoImage(Image.open(path))
        panel = tk.Label(self.win, image = img)
        panel.image=img
        panel.pack(fill='x')
        table_head=tk.Label(self.win,text='Class : Score',font=('Times',15,'bold','underline'))
        table_head.pack(fill='x')
        for cl in classes:
            table_data=tk.Label(self.win,font=('Courier',10,'italic'))
            table_data.configure(text=(cl['class']+' : '+str(cl['score'])))
            table_data.pack(fill='x')

class basicWindow:
    strings=[]
    integers=[]
    root=tk.Tk()
    icons=""
    def __init__(self,icon,head,Strvars,IntVars):
        self.icons=icon
        self.root.title(head)
        self.root.iconbitmap(icon)
        self.root.wm_minsize(400,400)
        self.root.configure(bg='#087BA8')
        heading=tk.Label(self.root,text=head,bg="#087BA8",fg="white",font=50)
        heading.pack(anchor='n',pady=30)
        for i in range(Strvars):
            self.strings.append(tk.StringVar());
        for i in range(IntVars):
            self.integers.append(i)
        
    def fill_window(self,mess,submes):
        s=0
        i=0
        main_frame=tk.Frame(self.root)
        main_frame.pack(ipadx=30,ipady=30)
        mess=tk.Label(main_frame,text=mess,font=("Courier",10))
        mess.pack(expand=True)
        def get_path(event=None):
            path=path_entry.get()
            classes=get_keywords(path)
            classes=classes['images'][0]['classifiers'][0]['classes']
            print(classes)
            window=dialogBox(self.root,"Result",self.icons)
            window.display(classes,path)
            path_entry.delete(0,tk.END)
            
        path_entry=tk.Entry(main_frame,textvariable=self.strings[s],font=('Courier',10,'italic'))
        s+=1
        path_entry.pack(expand=True)
        path_entry.bind("<Return>",get_path)
        submit=tk.Button(self.root,text=submes,command=get_path)
        submit.pack(expand=True)
    
    def mainlop(self):
        self.root.mainloop()
if __name__=='__main__':
    homeWin=basicWindow('myapp_icon.ico','Object Detection',1,0)
    homeWin.fill_window("Enter path:",'Submit')
    homeWin.mainlop()
