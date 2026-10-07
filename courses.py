import customtkinter as ctk
from tkinter import messagebox
from db_connection import get_connection

ctk.set_appearance_mode("Dark")  # Unified dark theme
ctk.set_default_color_theme("blue")

class CourseManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Course Management")
        self.geometry("800x500")
        self.configure(fg_color="#2C3E50")  # Dark blue background

        # Title
        ctk.CTkLabel(
            self,
            text="Course Management",
            font=("Arial", 22, "bold"),
            text_color="#F1C40F"
        ).pack(pady=20)

        # Outer frame (to center content)
        outer_frame = ctk.CTkFrame(self, fg_color="#2C3E50")
        outer_frame.pack(expand=True)  # expands & centers in window

        # Inner form frame
        form_frame = ctk.CTkFrame(outer_frame, fg_color="#34495E", corner_radius=15)
        form_frame.pack(padx=20, pady=20)

        # Course ID
        ctk.CTkLabel(form_frame, text="Course ID:", text_color="#ECF0F1").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.course_id = ctk.CTkEntry(form_frame, placeholder_text="Enter Course ID", width=200)
        self.course_id.grid(row=0, column=1, padx=10, pady=10)

        # Course Name
        ctk.CTkLabel(form_frame, text="Course Name:", text_color="#ECF0F1").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.course_name = ctk.CTkEntry(form_frame, placeholder_text="Enter Course Name", width=200)
        self.course_name.grid(row=1, column=1, padx=10, pady=10)

        # Department
        ctk.CTkLabel(form_frame, text="Department:", text_color="#ECF0F1").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.department = ctk.CTkEntry(form_frame, placeholder_text="Enter Department", width=200)
        self.department.grid(row=2, column=1, padx=10, pady=10)

        # Buttons
        btn_frame = ctk.CTkFrame(form_frame, fg_color="#34495E")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ctk.CTkButton(btn_frame, text="Add Course", fg_color="#1ABC9C", hover_color="#16A085",
                      command=self.add_course, width=130).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="Update Course", fg_color="#F39C12", hover_color="#D68910",
                      command=self.update_course, width=130).grid(row=0, column=1, padx=10)
        ctk.CTkButton(btn_frame, text="Delete Course", fg_color="#E74C3C", hover_color="#C0392B",
                      command=self.delete_course, width=130).grid(row=0, column=2, padx=10)
        ctk.CTkButton(btn_frame, text="Clear Fields", fg_color="#5DADE2", hover_color="#3498DB",
                      command=self.clear_fields, width=130).grid(row=0, column=3, padx=10)

    # Database Operations
    def add_course(self):
        cid = self.course_id.get().strip()
        name = self.course_name.get().strip()
        dept = self.department.get().strip()

        if not cid or not name or not dept:
            messagebox.showwarning("Validation", "All fields are required!")
            return

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO courses (course_id, course_name, department) VALUES (:1, :2, :3)",
                    (cid, name, dept)
                )
                conn.commit()
                messagebox.showinfo("Success", "Course added successfully.")
                self.clear_fields()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def update_course(self):
        cid = self.course_id.get().strip()
        name = self.course_name.get().strip()
        dept = self.department.get().strip()

        if not cid:
            messagebox.showwarning("Validation", "Enter Course ID to update.")
            return

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""UPDATE courses SET course_name=:1, department=:2 WHERE course_id=:3""",
                            (name, dept, cid))
                conn.commit()
                messagebox.showinfo("Success", "Course updated successfully.")
                self.clear_fields()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def delete_course(self):
        cid = self.course_id.get().strip()
        if not cid:
            messagebox.showwarning("Validation", "Enter Course ID to delete.")
            return
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM courses WHERE course_id=:1", (cid,))
                conn.commit()
                messagebox.showinfo("Deleted", "Course deleted successfully.")
                self.clear_fields()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def clear_fields(self):
        self.course_id.delete(0, "end")
        self.course_name.delete(0, "end")
        self.department.delete(0, "end")


if __name__ == "__main__":
    app = CourseManager()
    app.mainloop()  