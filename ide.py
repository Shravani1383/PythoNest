from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import os
import tkinter.filedialog
import tkinter.messagebox
import subprocess
root = Tk()
# root.iconbitmap('icons/python.png')
image_icon=PhotoImage(file="icons/icon1.png")
root.iconphoto(False, image_icon)

PROGRAM_NAME = "PythoNest"
root.title(PROGRAM_NAME)
file_name = None
root.geometry('800x600')

#all codes goes here
file_path=''

def set_file_path(path):
    global file_path
    file_path=path

#FILE MENU
def new_file(event=None):
    root.title("Untitled")
    global file_name
    file_name = None
    content_text.delete(1.0, END)
    on_content_changed()

def open_file(event=None):
    input_file_name = tkinter.filedialog.askopenfilename(defaultextension="*.py*",filetypes=[("Python Files", "*.py")])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
        content_text.delete(1.0, END)
        with open(file_name) as _file:
            content_text.insert(1.0, _file.read())
    
    on_content_changed()
     
def write_to_file(file_name):
    try:
        content = content_text.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass  


def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(filetypes=[('Python Files','*.py')])
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
    return "break"
    

def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"



#EDIT MENU
def cut():
    content_text.event_generate("<<Cut>>")
    on_content_changed()
    return "break"
def copy():
    content_text.event_generate("<<Copy>>")
    on_content_changed()
    return "break"
def paste():
    content_text.event_generate("<<Paste>>")
    on_content_changed()
    return "break"

def selectall(event=None):
    content_text.tag_add('sel','1.0','end')
    return "break"

   
def find_text(event=None):
    search_toplevel = Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(search_toplevel, text="Find All", underline=0,
           command=lambda: search_output(
               search_entry_widget.get(), ignore_case_value.get(),
               content_text, search_toplevel, search_entry_widget)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def close_search_window():
        content_text.tag_remove('match', '1.0', END)
        search_toplevel.destroy()
    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return "break"

def search_output(needle,if_ignore_case, content_text, search_toplevel, search_box):
    content_text.tag_remove('match','1.0', END)
    matches_found=0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle,start_pos, nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break

            end_pos = '{} + {}c'. format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found +=1
            start_pos = end_pos
        content_text.tag_config('match', background='yellow', foreground='blue')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))

#ABOUT MENU

def display_about(event=None):
    tkinter.messagebox.showinfo(
        "About", PROGRAM_NAME + "\nPython Code editor\n -Shravani Jagtap")


def display_help(event=None):
    tkinter.messagebox.showinfo(
        "Help", "This is a Python code Editor",
        icon='question')


def exit_editor(event=None):
    if tkinter.messagebox.askokcancel("Exit", "Are you sure you want to Quit?"):
        root.destroy()

#adding Line Numbers Functionality
def get_line_numbers():
    output = ''
    if show_line_number.get():
        row, col = content_text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output

def on_content_changed(event=None):
    update_line_numbers()
    update_cursor()

def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')

# Adding Cursor Functionality
def show_cursor():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()


def update_cursor(event=None):
    row, col = content_text.index(INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col) + 1)  # col starts at 0
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)


#Adding Text Highlight Functionality
def highlight_line(interval=100):
    content_text.tag_remove("active_line", 1.0, "end")
    content_text.tag_add(
        "active_line", "insert linestart", "insert lineend+1c")
    content_text.after(interval, toggle_highlight)


def undo_highlight():
    content_text.tag_remove("active_line", 1.0, "end")


def toggle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()


#Adding Change Theme Functionality
def change_theme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    foreground_color, background_color = fg_bg_colors.split('.')
    content_text.config(
        background=background_color, fg=foreground_color)

#pop-up menu
def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root, event.y_root)

def run():
    code = content_text.get("1.0", "end-1c")
    process = subprocess.Popen(["python", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if output:
        code_output.insert("end", output.decode("utf-8") + "\n")
    if error:
        code_output.insert("end", error.decode("utf-8") + "\n")
    
    
# ICONS for the compound menu
new_file_icon = PhotoImage(file='icons/new_file.png')
open_file_icon = PhotoImage(file='icons/Open_file.png')
save_file_icon = PhotoImage(file='icons/save.png')
cut_icon = PhotoImage(file='icons/cut.png')
copy_icon = PhotoImage(file='icons/copy.png')
paste_icon = PhotoImage(file='icons/paste.png')
find_icon = PhotoImage(file='icons/find_text.png')
run_icon=PhotoImage(file='icons/run.png')

#MENU CODES GOES HERE
menu_bar = Menu(root) #menu begins

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left', image=new_file_icon, underline=0, command=new_file)
file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left', image=open_file_icon, underline=0, command=open_file)
file_menu.add_command(label="Save", accelerator='Ctrl+S', compound='left', image=save_file_icon, underline=0, command=save)
file_menu.add_command(label="Save As", accelerator='Ctrl+Shift+S', compound='left', underline=0, command = save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator='Alt+F4', compound='left', underline=0, command=exit_editor)
menu_bar.add_cascade(label='File', menu=file_menu)
# end of File Menu

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label='Cut', accelerator='Ctrl+X', compound='left',  image=cut_icon, underline=0, command=cut) 
edit_menu.add_command(label='Copy', accelerator='Ctrl+C', compound='left', image=copy_icon, underline=0, command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl+V', compound='left',  image=paste_icon, underline=0, command=paste)
edit_menu.add_separator()
edit_menu.add_command(label='Find', accelerator='Ctrl+F', compound='left',  image=find_icon, underline=0, command=find_text)
edit_menu.add_separator()
edit_menu.add_command(label='Select All', accelerator='Ctrl+A', compound='left', underline=0, command=selectall) 
menu_bar.add_cascade(label='Edit', menu=edit_menu)
#end of Edit Menu

run_bar=Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run',image=run_icon,compound='left',command=run)
menu_bar.add_cascade(label='Run',menu=run_bar)
#end of run Menu
view_menu = Menu(menu_bar, tearoff=0)
show_line_number=IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label="Show Line Number", variable=show_line_number)
show_cursor_info=IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(label='Show Cursor Location at Bottom', variable=show_cursor_info, command=show_cursor)
to_highlight_line=IntVar()
view_menu.add_checkbutton(label='Highlight Current Line', variable=to_highlight_line, onvalue=1, offvalue=0,command=toggle_highlight)
themes_menu=Menu(menu_bar, tearoff=0)
view_menu.add_cascade(label='Themes', menu=themes_menu, command=change_theme)

''' THEMES OPTIONS'''
color_schemes = {
    'Default': '#000000.#FFFFFF',
    
    'Night Mode': '#FFFFFF.#2b2e2e',
}

theme_choice=StringVar()
theme_choice.set('Default')
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(label=k, variable=theme_choice, command=change_theme)

menu_bar.add_cascade(label='View', menu=view_menu)


#start of About Menu
about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='About', menu=about_menu)
about_menu.add_command(label='About', underline=0, command=display_about)
about_menu.add_command(label='Help', underline=0, command=display_help)
#end of About Menu


root.config(menu=menu_bar)

#adding top shortcut bar and left line number bar
shortcut_bar=Frame(root, height=25)
shortcut_bar.pack(expand='no', fill='x')

#adding shortcut icons
icons=('new_file', 'open_file', 'save', 'cut', 'copy', 'paste', 'find_text','run')
for i, icon in enumerate(icons):
    tool_bar_icon = PhotoImage(file='icons/{}.png'.format(icon)).zoom(1,1)
    cmd = eval(icon)
    tool_bar = Button(shortcut_bar, image=tool_bar_icon, height=23,width=30, command=cmd)
    tool_bar.image = tool_bar_icon
    tool_bar.pack(side='left')


line_number_bar = Text(root, width=4, padx=3, takefocus=0, fg='white', border=0, background='#282828', state='disabled',  wrap='none')
line_number_bar.pack(side='left', fill='y')

#adding the main context Text widget and Scrollbar Widget
content_text = Text(root, wrap='word')
content_text.pack(expand='yes', fill='both')

scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side='right', fill='y')

# addind cursor info label
cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')

# setting up the pop-up menu
popup_menu = Menu(content_text)
for i in ('cut', 'copy', 'paste'):
    cmd = eval(i)
    popup_menu.add_command(label=i, compound='left', command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label='Select All', underline=7, command=selectall)
content_text.bind('<Button-3>', show_popup_menu)


#handling binding

content_text.bind('<Control-N>', new_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-S>', save)
content_text.bind('<Control-s>', save)

content_text.bind('<Control-A>',selectall)
content_text.bind('<Control-a>',selectall)
content_text.bind('<Control-F>',find_text)
content_text.bind('<Control-f>',find_text)

content_text.bind('<KeyPress-F1>', display_help)

content_text.bind('<Any-KeyPress>', on_content_changed)
content_text.tag_configure('active_line', background='ivory2')

content_text.bind('<Button-3>', show_popup_menu)
content_text.focus_set()

code_output = Text(height=10)
code_output.pack()
#END OF MENU

root.protocol('WM_DELETE_WINDOW', exit_editor)
root.mainloop()