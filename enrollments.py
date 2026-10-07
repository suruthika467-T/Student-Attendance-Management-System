import customtkinter as ctk
from tkinter import messagebox
from db_connection import get_connection

ctk.set_appearance_mode("Dark")  # Unified dark theme
ctk.set_default_color_theme("blue")


class EnrollManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Enrollment")
        self.geometry("800x500")
        self.configure(fg_color="#2C3E50")  # Same as courses.py background

        # Title
        ctk.CTkLabel(
            self,
            text="🎓 Student Enrollment",
            font=("Arial", 22, "bold"),
            text_color="#F1C40F"  # Golden title
        ).pack(pady=20)

        # Outer frame (center content)
        outer_frame = ctk.CTkFrame(self, fg_color="#2C3E50")
        outer_frame.pack(expand=True)

        # Inner frame (form)
        form_frame = ctk.CTkFrame(outer_frame, fg_color="#34495E", corner_radius=15)
        form_frame.pack(padx=20, pady=20)

        # --- Enrollment ID ---
        ctk.CTkLabel(form_frame, text="Enrollment ID:", text_color="#ECF0F1").grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )
        self.enroll_id = ctk.CTkEntry(form_frame, placeholder_text="Enter Enrollment ID", width=200)
        self.enroll_id.grid(row=0, column=1, padx=10, pady=10)

        # --- Student ID ---
        ctk.CTkLabel(form_frame, text="Student ID:", text_color="#ECF0F1").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )
        self.student_id = ctk.CTkEntry(form_frame, placeholder_text="Enter Student ID", width=200)
        self.student_id.grid(row=1, column=1, padx=10, pady=10)

        # --- Course ID ---
        ctk.CTkLabel(form_frame, text="Course ID:", text_color="#ECF0F1").grid(
            row=2, column=0, padx=10, pady=10, sticky="e"
        )
        self.course_id = ctk.CTkEntry(form_frame, placeholder_text="Enter Course ID", width=200)
        self.course_id.grid(row=2, column=1, padx=10, pady=10)

        # Buttons Frame
        btn_frame = ctk.CTkFrame(form_frame, fg_color="#34495E")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        # --- Buttons ---
        ctk.CTkButton(btn_frame, text="Add Enrollment",
                      fg_color="#1ABC9C", hover_color="#16A085",
                      command=self.add_enrollment, width=130).grid(row=0, column=0, padx=10)

        ctk.CTkButton(btn_frame, text="Update Enrollment",
                      fg_color="#F39C12", hover_color="#D68910",
                      command=self.update_enrollment, width=130).grid(row=0, column=1, padx=10)

        ctk.CTkButton(btn_frame, text="Delete Enrollment",
                      fg_color="#E74C3C", hover_color="#C0392B",
                      command=self.delete_enrollment, width=130).grid(row=0, column=2, padx=10)

        ctk.CTkButton(btn_frame, text="Clear Fields",
                      fg_color="#5DADE2", hover_color="#3498DB",
                      command=self.clear_fields, width=130).grid(row=0, column=3, padx=10)

    # ---------------- Database Operations ----------------
    def add_enrollment(self):
        eid = self.enroll_id.get().strip()
        sid = self.student_id.get().strip()
        cid = self.course_id.get().strip()

        if not eid or not sid or not cid:
            messagebox.showwarning("Validation", "All fields are required!")
            return

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO enrollments (enrollment_id, student_id, course_id) VALUES (:1, :2, :3)",
                    (eid, sid, cid)
                )
                conn.commit()
                messagebox.showinfo("Success", "Enrollment added successfully.")
                self.clear_fields()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def update_enrollment(self):
        eid = self.enroll_id.get().strip()
        sid = self.student_id.get().strip()
        cid = self.course_id.get().strip()

        if not eid:
            messagebox.showwarning("Validation", "Enter Enrollment ID to update.")
            return

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE enrollments SET student_id=:1, course_id=:2 WHERE enrollment_id=:3",
                    (sid, cid, eid)
                )
                conn.commit()
                messagebox.showinfo("Success", "Enrollment updated successfully.")
                self.clear_fields()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def delete_enrollment(self):
        eid = self.enroll_id.get().strip()

        if not eid:
            messagebox.showwarning("Validation", "Enter Enrollment ID to delete.")
            return

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM enrollments WHERE enrollment_id=:1", (eid,))
                conn.commit()
                messagebox.showinfo("Deleted", "Enrollment deleted successfully.")
                self.clear_fields()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def clear_fields(self):
        self.enroll_id.delete(0, "end")
        self.student_id.delete(0, "end")
        self.course_id.delete(0, "end")


if __name__ == "__main__":
    app = EnrollManager()
    app.mainloop()
