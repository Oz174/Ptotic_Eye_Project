import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from matplotlib import pyplot as plt
from utility import final_utils as fu

process_preop_clicked = False
process_postop_clicked = False

def show_plots():
    """
    Shows the plots of the selected files.
    """
    if not process_preop_clicked or not process_postop_clicked:
        tk.messagebox.showerror("Error", "Please process the preoperative and postoperative files first")
        return

    plt.show()

def process_preop():
    """
    Returns the values of the selected files and radio buttons.
    """
    global process_preop_clicked
    file1 = file_label.cget("text")
    # try to open the file1 and file2 , if no then put label as empty 
    if not os.path.exists(file1):
       tk.messagebox.showerror("Error", "Please select a file")
       return

    try:
        split_index_preop = int(split_idx_preop.get())
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid split index")
        return

    ptotic = ptotic_side.get()

    try:
        degree = int(degree_entry.get())
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid degree")
        return
    

    upper_right_contour,upper_left_contour,right_pupil,left_pupil = fu.read_coordinates(file1,split_index_preop)
    fx,gx,mrdr,mrdl,pmr,pml= fu.plot_contour(upper_right_contour,upper_left_contour,right_pupil,left_pupil,ptotic,degree,"Preoperative")
    new_root = tk.Tk()
    new_root.title("Preoperative Stats")
    table = ttk.Treeview(new_root,columns=( "Feature", "Value"), show= 'headings')
    table.heading("Feature", text="Feature")
    table.heading("Value", text="Value")

    table.pack(fill='both', expand=True)
    table.insert("","end",values=("Equation of Right Eye",[round(aarg,2) for aarg in list(fx.coefficients)]))
    table.insert("","end",values=("Equation of Left Eye",[round(aarg,2) for aarg in list(gx.coefficients)]))
    table.insert("","end",values=("MRD1 Right(mm)",mrdr))
    table.insert("","end",values=("MRD1 Left(mm)",mrdl))
    table.insert("","end",values=("PHUL-MRD1 right eye(mm)",pmr))
    table.insert("","end",values=("PHUL-MRD1 left eye(mm)",pml))
    table.insert("","end",values=("Similarity MRD1",fu.compute_similarity(mrdr,mrdl,ptotic)))
    table.insert("","end",values=("Similarity PHUL-MRD1",fu.compute_similarity(pmr,pml,ptotic)))
    process_preop_clicked = not process_preop_clicked

def process_postop():
    """
    Returns the values of the selected files and radio buttons.
    """
    global process_postop_clicked
    file2 = file_label2.cget("text")
    # try to open the file1 and file2 , if no then put label as empty 
    if not os.path.exists(file2):
       tk.messagebox.showerror("Error", "Please select a file")
       return
       
    try:
        split_index_postop = int(split_idx_postop.get())
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid split index")
        return
    
    ptotic = ptotic_side.get()

    try:
        degree = int(degree_entry.get())
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid degree")
        return

    upper_right_contour,upper_left_contour,right_pupil,left_pupil = fu.read_coordinates(file2,split_index_postop)
    fx,gx,mrdr,mrdl,pmr,pml= fu.plot_contour(upper_right_contour,upper_left_contour,right_pupil,left_pupil,ptotic,degree,"Postoperative")
    new_root2 = tk.Tk()
    new_root2.title("Postoperative Stats")
    
    table = ttk.Treeview(new_root2, columns=("Feature","Value"), show='headings')
    table.heading("Feature", text="Feature")
    table.heading("Value", text="Value")

    table.pack(fill='both', expand=True)
    table.insert("","end",values=("Equation of Right Eye",[round(aarg,2) for aarg in list(fx.coefficients)]))
    table.insert("","end",values=("Equation of Left Eye",[round(aarg,2) for aarg in list(gx.coefficients)]))
    table.insert("","end",values=("MRD1 Right",mrdr))
    table.insert("","end",values=("MRD1 Left",mrdl))
    table.insert("","end",values=("PHUL-MRD1 right eye",pmr))
    table.insert("","end",values=("PHUL-MRD1 left eye",pml))
    table.insert("","end",values=("Similarity MRD1",fu.compute_similarity(mrdr,mrdl,ptotic)))
    table.insert("","end",values=("Similarity PHUL-MRD1",fu.compute_similarity(pmr,pml,ptotic)))
    process_postop_clicked = not process_postop_clicked

def browse_files(label):
  """
  Opens a file dialog and displays the selected file path in the label.
  """
  filename = filedialog.askopenfilename(initialdir=".", title="Select a File", filetypes=(("All Files", "*.*"),))
  if filename:
    label.config(text=f"{os.path.basename(filename)}")

root = tk.Tk()
root.geometry("600x480")
root.title("Eye Surgery Analysis Tool")

# Label to display file information
file_label = tk.Label(root, text="Preoperative Coordinates Text File: ")
file_label.grid(column=0, row=0)

# Browse button to open file dialog
browse_button = tk.Button(root, text="Browse", command=lambda : browse_files(file_label))
browse_button.grid(column=1,row=0)

# entry text with label 'split index'
split_idx_preop_lbl = tk.Label(root, text="Split Index :")
split_idx_preop_lbl.grid(column=2, row=0)
split_idx_preop = tk.Entry(root)
split_idx_preop.grid(column=3, row=0)

# entry text with label 'split index'
split_idx_postop_lbl = tk.Label(root, text="Split Index :")
split_idx_postop_lbl.grid(column=2, row=1)
split_idx_postop = tk.Entry(root)
split_idx_postop.grid(column=3, row=1)

# entry text with label 'degree'
degree_label = tk.Label(root, text="Degree:")
degree_label.grid(column=0, row=3)
degree_entry = tk.Entry(root)
degree_entry.grid(column=1, row=3)

# label file 2 (because I want to select two files)
file_label2 = tk.Label(root, text="Postoperative Coordinates Text File:")
file_label2.grid(column=0, row=1)

# Browse button to open file dialog
browse_button2 = tk.Button(root, text="Browse", command=lambda: browse_files(file_label2))
browse_button2.grid(column=1,row=1)


# Two radio buttons for left and right with label named ptotic 
ptotic_label = tk.Label(root, text="Ptotic Side:")
ptotic_label.grid(column=0, row=2)

# Radio buttons for left and right
ptotic_side = tk.StringVar()
ptotic_side.set("Left")
radio_left = tk.Radiobutton(root, text="Left", variable=ptotic_side, value="l")
radio_left.grid(column=1, row=2)
radio_right = tk.Radiobutton(root, text="Right", variable=ptotic_side, value="r")
radio_right.grid(column=2, row=2)




# submit button that shows the values of the selected files and radio buttons
preop_button = tk.Button(root, text="Show PreOp Stats", command=process_preop)
preop_button.grid(column=0, row=5)

postop_button = tk.Button(root, text="Show PostOp Stats", command=process_postop)
postop_button.grid(column=1, row=5)

show_plots_btn = tk.Button(root, text="Show All Plots", command=lambda: plt.show())
show_plots_btn.grid(column=2, row=5)    

root.mainloop()