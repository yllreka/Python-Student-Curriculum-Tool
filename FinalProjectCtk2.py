import customtkinter
from CTkListbox import *
from tkinter import END, messagebox
from tkinter.filedialog import asksaveasfilename


class Courses:

    def __init__(self, root):
        label = customtkinter.CTkLabel(root, text="Provide data path:", )
        label.place(relx=0.09, rely=0.03, )
        label.configure(font=("Montserrat", 15))

        self.entry = customtkinter.CTkEntry(root, placeholder_text="Insert file", width=200)
        self.entry.place(relx=0.2, rely=0.03, )
        self.entry.configure(font=("Karla", 11))

        Yrlabel = customtkinter.CTkLabel(root, text="Year:", )
        Yrlabel.place(relx=0.09, rely=0.1, )
        Yrlabel.configure(font=("Montserrat", 16))

        self.Yrcombobox = customtkinter.CTkComboBox(root, values=["", "1", "2", "3", "4", "5"], )
        self.Yrcombobox.place(relx=0.2, rely=0.1, )

        Deplabel = customtkinter.CTkLabel(root, text="Department:", )
        Deplabel.place(relx=0.6, rely=0.1, )
        Deplabel.configure(font=("Montserrat", 16))

        self.Depcombobox = customtkinter.CTkComboBox(root, values=["", "CHI", "CS", "ECE", "ECON", "EE", "EECS", "ENGR",
                                                                   "FRE", "GER", "IE", "ISE", "LIFE", "MATH", "MGT",
                                                                   "UNI", ], )
        self.Depcombobox.place(relx=0.7, rely=0.1, )
        self.Depcombobox.configure(font=("Karla", 11))

        DspButton = customtkinter.CTkButton(root, text="Display", command=self.Enter_File_dir, )
        DspButton.place(relx=0.2, rely=0.2, )

        ClrButton = customtkinter.CTkButton(root, text="Clear", command=self.Delete)
        ClrButton.place(relx=0.4, rely=0.2, )

        SvButton = customtkinter.CTkButton(root, text="Save", command=self.Save_To_File)
        SvButton.place(relx=0.6, rely=0.2, )

        SelCrsLabel = customtkinter.CTkLabel(root, text="Selected Courses:", )
        SelCrsLabel.place(relx=0.1, rely=0.4, )
        SelCrsLabel.configure(font=("Montserrat", 17))

        self.SelCrsLbx = CTkListbox(root, width=200, height=300)
        self.SelCrsLbx.place(relx=0.1, rely=0.5, )

        CrsLabel = customtkinter.CTkLabel(root, text="Courses:", )
        CrsLabel.place(relx=0.4, rely=0.4, )
        CrsLabel.configure(font=("Montserrat", 17))

        self.CrsLbx = CTkListbox(root, width=550, height=300)
        self.CrsLbx.place(relx=0.4, rely=0.5, )
        self.CrsLbx.bind("<<ListboxSelect>>", self.OnSelect)

        # Store original course details
        self.original_courses = []

    def Enter_File_dir(self):
        filepath = self.entry.get()

        if not filepath:
            messagebox.showwarning("No File Path", "Please provide the file path in the entry field.")
            return

        if not filepath.endswith('.csv'):
            messagebox.showwarning("Invalid File Type", "Only files in '.csv' format are allowed!")
            return

        selected_year = self.Yrcombobox.get()
        selected_dep = self.Depcombobox.get()

        print(filepath)
        print(f"Selected year: {selected_year}")
        print(f"Selected department: {selected_dep}")

        self.CrsLbx.delete(0, END)
        self.original_courses = []

        with open(filepath, "r", encoding="utf-8", errors='ignore') as file:
            for line in file:
                words = line.split()
                if len(words) < 2:
                    continue

                year_match = (selected_year == "" or words[1][0] == selected_year)
                dep_match = (selected_dep == "" or words[0][:4] == selected_dep)

                if year_match and dep_match:
                    self.CrsLbx.insert("end", line)
                    self.original_courses.append(line.strip())

    def Delete(self):
        self.SelCrsLbx.delete(0, END)

    def OnSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        print(value)

        if self.SelCrsLbx.size() >= 6:
            messagebox.showwarning("Limit Reached", "No more than 6 subjects are allowed!")
            return

        self.SelCrsLbx.insert("end", value.split()[0] + " " + value.split()[1][:3])

    def Save_To_File(self):
        selected_courses = []
        for i in range(self.SelCrsLbx.size()):
            selected_course = self.SelCrsLbx.get(i)

            for course in self.original_courses:
                if selected_course in course:
                    selected_courses.append(course)
                    break

        if not selected_courses:
            messagebox.showwarning("No Selection", "There are no subjects selected to save.")
            return

        save_filepath = asksaveasfilename(defaultextension=".csv",
                                          filetypes=[("CSV", ".csv"), ("All files", "*.*")])

        if not save_filepath:
            return

        with open(save_filepath, 'w') as file:
            for course in selected_courses:
                file.write(course + '\n')

        messagebox.showinfo("Saved", f"The subjects were successfully saved to the file {save_filepath}!")


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
root = app
app.geometry("1300x700")
course_app = Courses(root)
app.mainloop()


#  C:\\Users\PowerUser\\Dropbox\\PC\\Downloads\\sampledata (1).csv--##