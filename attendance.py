import customtkinter as ctk
from tkinter import ttk, messagebox
from db_connection import get_connection
from datetime import date

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AttendanceManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Attendance Management")
        self.geometry("1000x600")
        self.configure(fg_color="#2C3E50")  # Dark blue theme

        # Title
        ctk.CTkLabel(
            self,
            text="🕒 Attendance Management",
            font=("Arial", 24, "bold"),
            text_color="#F1C40F"
        ).pack(pady=15)

        # Main Frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#34495E")
        self.main_frame.place(relx=0.02, rely=0.08, relwidth=0.96, relheight=0.9)

        self.create_widgets()

    def create_widgets(self):
        # Top Frame
        top_frame = ctk.CTkFrame(self.main_frame, fg_color="#2C3E50", corner_radius=15)
        top_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(top_frame, text="Course:", text_color="white").grid(row=0, column=0, padx=10, pady=10)
        self.course_var = ctk.CTkComboBox(top_frame, values=self.load_courses(), width=200)
        self.course_var.grid(row=0, column=1, padx=10)

        ctk.CTkLabel(top_frame, text="Date:", text_color="white").grid(row=0, column=2, padx=10)
        self.date_entry = ctk.CTkEntry(top_frame, width=150)
        self.date_entry.grid(row=0, column=3, padx=10)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))

        ctk.CTkButton(top_frame, text="Load Students", command=self.load_students,
                      fg_color="#1ABC9C", hover_color="#16A085", width=150).grid(row=0, column=4, padx=10)

        # Table Frame
        table_frame = ctk.CTkFrame(self.main_frame, fg_color="#2C3E50", corner_radius=15)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Status"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in ("ID", "Name", "Status"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=200)

        style = ttk.Style()
        style.configure("Treeview", background="#34495E", foreground="white",
                        fieldbackground="#34495E", rowheight=28, font=("Arial", 11))
        style.map('Treeview', background=[('selected', '#2980B9')])

        # Bottom Buttons
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="#2C3E50", corner_radius=15)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Mark Present", fg_color="#27AE60", hover_color="#1E8449",
                      command=lambda: self.mark_attendance("Present")).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkButton(btn_frame, text="Mark Absent", fg_color="#E74C3C", hover_color="#C0392B",
                      command=lambda: self.mark_attendance("Absent")).grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(btn_frame, text="Save Attendance", fg_color="#3498DB", hover_color="#2E86C1",
                      command=self.save_attendance).grid(row=0, column=2, padx=10, pady=10)

        ctk.CTkButton(btn_frame, text="Clear", fg_color="#7F8C8D", hover_color="#707B7C",
                      command=self.clear_selection).grid(row=0, column=3, padx=10, pady=10)

    def load_courses(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT course_name FROM courses ORDER BY course_id")
                return [row[0] for row in cur]
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        return []

    def load_students(self):
        self.tree.delete(*self.tree.get_children())
        course = self.course_var.get()
        if not course:
            messagebox.showwarning("Select Course", "Please select a course.")
            return

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT s.student_id, s.name
                    FROM students s
                    JOIN enrollments e ON s.student_id = e.student_id
                    JOIN courses c ON e.course_id = c.course_id
                    WHERE c.course_name = :course_name
                """, {"course_name": course})
                students = cur.fetchall()
                if not students:
                    messagebox.showinfo("No Students", "No students found for this course.")
                    return
                for row in students:
                    self.tree.insert("", "end", values=(row[0], row[1], "Absent"))
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def mark_attendance(self, status):
        for item in self.tree.selection():
            self.tree.set(item, "Status", status)

    def save_attendance(self):
        course = self.course_var.get()
        adate = self.date_entry.get().strip()
        if not course or not adate:
            messagebox.showwarning("Validation", "Course and date required")
            return

        try:
            with get_connection() as conn:
                cur = conn.cursor()
                
                # Get course_id
                cur.execute("SELECT course_id FROM courses WHERE course_name=:course_name", {"course_name": course})
                result = cur.fetchone()
                if not result:
                    messagebox.showerror("Error", "Selected course not found in database")
                    return
                course_id = result[0]

                # Save attendance for each student
                for item in self.tree.get_children():
                    student_id, _, status = self.tree.item(item, "values")
                    cur.execute("""
                        MERGE INTO attendance a
                        USING dual
                        ON (
                            a.student_id = :student_id 
                            AND a.course_id = :course_id 
                            AND a.attendance_date = TO_DATE(:adate,'YYYY-MM-DD')
                        )
                        WHEN MATCHED THEN 
                            UPDATE SET a.status = :status
                        WHEN NOT MATCHED THEN 
                            INSERT (student_id, course_id, attendance_date, status)
                            VALUES (:student_id, :course_id, TO_DATE(:adate,'YYYY-MM-DD'), :status)
                    """, {
                        "student_id": student_id,
                        "course_id": course_id,
                        "adate": adate,
                        "status": status
                    })
                conn.commit()
            messagebox.showinfo("Success", "Attendance Saved Successfully ✅")
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def clear_selection(self):
        for item in self.tree.get_children():
            self.tree.set(item, "Status", "Absent")


if __name__ == "__main__":
    app = AttendanceManager()
    app.mainloop()
