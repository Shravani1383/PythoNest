from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
compiler = Tk()
compiler.title('PythonIDE')
compiler.geometry("700x600")
file_path=''

def set_file_path(path):
    global file_path
    file_path=path

def save_as():
    if file_path=='':
        path=asksaveasfilename(filetypes=[('Python Files','*.py')])
    else:
        path = file_path
    
    with open(path, 'w') as file:
        code=editor.get('1.0',END)
        file.write(code)
        set_file_path(path)
        
        
def save():
    path=asksaveasfilename(filetypes=[('Python Files','*.py')])
    with open(path, 'w') as file:
        code=editor.get('1.0',END)
        file.write(code)
        
def open_file():
    path=askopenfilename(filetypes=[('Python Files','*.py')])
    with open(path, 'r') as file:
        code=file.read()
        editor.delete('1.0',END)
        editor.insert('1.0',code)
        set_file_path(path)    
        

def run():
    code = editor.get("1.0", "end-1c")
    process = subprocess.Popen(["python", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if output:
        code_output.insert("end", output.decode("utf-8") + "\n")
    if error:
        code_output.insert("end", error.decode("utf-8") + "\n")
      
menu_bar= Menu(compiler)

file_bar=Menu(menu_bar, tearoff=0)
file_bar.add_command(label='Open',command=open_file)
file_bar.add_command(label='Save',command=save_as)
file_bar.add_command(label='Save As',command=save_as)
file_bar.add_command(label='Exit',command=exit)
menu_bar.add_cascade(label='File',menu=file_bar)

run_bar=Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run',command=run)
menu_bar.add_cascade(label='Run',menu=run_bar)

compiler.config(menu=menu_bar)

editor = Text()
editor.pack()
code_output = Text(height=10)
code_output.pack()
compiler.mainloop()
