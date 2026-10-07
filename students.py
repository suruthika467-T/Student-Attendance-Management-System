import customtkinter as ctk
from tkinter import messagebox
from db_connection import get_connection


# ✅ CTkToplevel → works as a child window (for main.py)
class StudentManager(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("900x550")

        # Appearance Settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # Background color
        self.configure(bg="#2C3E50")

        # Title Label
        title = ctk.CTkLabel(self, text="🎓 College Student Management System",
                             font=ctk.CTkFont(size=24, weight="bold"),
                             text_color="#F1C40F")
        title.pack(pady=20)

        # Main Frame
        main_frame = ctk.CTkFrame(self, fg_color="#34495E", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Input Fields
        labels = ["Student ID", "Name", "Department", "Year", "Email", "Phone"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(main_frame, text=label_text + ":", text_color="#ECF0F1")
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            entry = ctk.CTkEntry(main_frame, placeholder_text=f"Enter {label_text}")
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
            self.entries[label_text.lower().replace(" ", "_")] = entry

        main_frame.columnconfigure(1, weight=1)

        # Button Frame
        btn_frame = ctk.CTkFrame(main_frame, fg_color="#2C3E50")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ctk.CTkButton(btn_frame, text="Add Student", fg_color="#1ABC9C",
                      hover_color="#16A085", command=self.add_student).grid(row=0, column=0, padx=15)
        ctk.CTkButton(btn_frame, text="Update Student", fg_color="#3498DB",
                      hover_color="#2980B9", command=self.update_student).grid(row=0, column=1, padx=15)
        ctk.CTkButton(btn_frame, text="Delete Student", fg_color="#E74C3C",
                      hover_color="#C0392B", command=self.delete_student).grid(row=0, column=2, padx=15)
        ctk.CTkButton(btn_frame, text="Clear Form", fg_color="#9B59B6",
                      hover_color="#8E44AD", command=self.clear_form).grid(row=0, column=3, padx=15)

    # ------------------ CRUD Operations ------------------

    def validate_form(self):
        data = {}
        for key, entry in self.entries.items():
            value = entry.get().strip()
            if not value:
                messagebox.showwarning("Validation", f"Please enter {key.replace('_', ' ').title()}.")
                return None
            data[key] = value
        return data

    def add_student(self):
        data = self.validate_form()
        if not data:
            return
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO students (student_id, name, department, year, email, phone) VALUES (:1,:2,:3,:4,:5,:6)",
                    (data['student_id'], data['name'], data['department'], data['year'], data['email'], data['phone'])
                )
                conn.commit()
                messagebox.showinfo("Success", "Student added successfully.")
                self.clear_form()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not add student: {e}")

    def update_student(self):
        data = self.validate_form()
        if not data:
            return
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE students SET name=:1, department=:2, year=:3, email=:4, phone=:5 WHERE student_id=:6",
                    (data['name'], data['department'], data['year'], data['email'], data['phone'], data['student_id'])
                )
                if cur.rowcount == 0:
                    messagebox.showwarning("Not Found", "No student with that ID exists.")
                else:
                    conn.commit()
                    messagebox.showinfo("Success", "Student updated successfully.")
                    self.clear_form()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not update student: {e}")

    def delete_student(self):
        sid = self.entries["student_id"].get().strip()
        if not sid:
            messagebox.showwarning("Validation", "Enter Student ID to delete.")
            return
        if not messagebox.askyesno("Confirm", "Delete this student? This action cannot be undone."):
            return
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM students WHERE student_id = :1", (sid,))
                if cur.rowcount == 0:
                    messagebox.showwarning("Not Found", "No student with that ID exists.")
                else:
                    conn.commit()
                    messagebox.showinfo("Success", "Student deleted successfully.")
                    self.clear_form()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not delete student: {e}")

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, "end")


# ✅ This allows standalone testing too
if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()  # hide root window
    app = StudentManager()
    app.mainloop()
