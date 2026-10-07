# reports.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from db_connection import get_connection

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ReportsManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Attendance Reports")
        self.geometry("1000x600")
        self.configure(fg_color="#2C3E50")  # Same dark blue theme

        # -------------------- Main Frame --------------------
        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#34495E")
        self.main_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        self.create_widgets()

    def create_widgets(self):
        # -------------------- Top Frame --------------------
        top_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#2C3E50")
        top_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(top_frame, text="Select Course:", font=("Arial", 15), text_color="white") \
            .grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.course_var = ctk.CTkComboBox(top_frame, values=self.load_courses(), width=250)
        self.course_var.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(top_frame, text="Generate Report", command=self.generate_report,
                      fg_color="#3498DB", hover_color="#2E86C1", font=("Arial", 14),
                      width=200).grid(row=0, column=2, padx=20, pady=10)

        # -------------------- Table Frame --------------------
        table_frame = ctk.CTkFrame(self.main_frame, corner_radius=15, fg_color="#2C3E50")
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("ID", "Name", "Total Classes", "Present", "Attendance %")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        style = ttk.Style()
        style.configure("Treeview", background="#34495E", foreground="white",
                        fieldbackground="#34495E", font=("Arial", 11), rowheight=28)
        style.map("Treeview", background=[("selected", "#2980B9")], foreground=[("selected", "white")])

    # -------------------- Load Courses --------------------
    def load_courses(self):
        courses = []
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT course_name FROM courses ORDER BY course_id")
                courses = [row[0] for row in cur]
        except Exception as e:
            messagebox.showerror("DB Error", f"Could not load courses: {e}")
        return courses

    # -------------------- Generate Report --------------------
    def generate_report(self):
        selected_course = self.course_var.get()
        if not selected_course:
            messagebox.showwarning("Validation", "Please select a course.")
            return

        # Clear previous rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            with get_connection() as conn:
                cur = conn.cursor()

                # Get course_id
                cur.execute("SELECT course_id FROM courses WHERE course_name=:course_name",
                            {"course_name": selected_course})
                course_row = cur.fetchone()
                if not course_row:
                    messagebox.showerror("Error", "Selected course not found")
                    return
                course_id = course_row[0]

                # Get students enrolled in this course
                cur.execute("""
                    SELECT s.student_id, s.name
                    FROM students s
                    JOIN enrollments e ON s.student_id = e.student_id
                    WHERE e.course_id = :course_id
                """, {"course_id": course_id})
                students = cur.fetchall()

                for student_id, name in students:
                    # Total classes
                    cur.execute("SELECT COUNT(*) FROM attendance WHERE student_id=:student_id AND course_id=:course_id",
                                {"student_id": student_id, "course_id": course_id})
                    total_classes = cur.fetchone()[0]

                    # Total present
                    cur.execute("""SELECT COUNT(*) FROM attendance 
                                   WHERE student_id=:student_id AND course_id=:course_id AND status='Present'""",
                                {"student_id": student_id, "course_id": course_id})
                    present = cur.fetchone()[0]

                    percentage = (present / total_classes * 100) if total_classes > 0 else 0
                    self.tree.insert("", "end",
                                     values=(student_id, name, total_classes, present, f"{percentage:.2f}%"))

        except Exception as e:
            messagebox.showerror("DB Error", f"Could not generate report: {e}")


if __name__ == "__main__":
    app = ReportsManager()
    app.mainloop()
