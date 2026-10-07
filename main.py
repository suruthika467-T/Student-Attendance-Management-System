import customtkinter as ctk
from tkinter import messagebox
import os
 
class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Attendance Management System")
        self.geometry("900x600")
        self.configure(fg_color="#0b253e")  # Keep your original background color

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_widgets()

    # ======================================================
    # Create all buttons
    # ======================================================
    def create_widgets(self):
        title_label = ctk.CTkLabel(
            self,
            text="📘 Attendance Management System",
            font=("Arial Rounded MT Bold", 28),
            text_color="white",
        )
        title_label.pack(pady=40)

        button_frame = ctk.CTkFrame(self, fg_color="#0b253e")
        button_frame.pack(pady=30)

        # --- Buttons ---
        btn_students = ctk.CTkButton(
            button_frame,
            text="👩‍🎓 Manage Students",
            command=self.open_students,
            fg_color="#0b80ff",
            hover_color="#0066cc",
            width=250,
            height=45,
            corner_radius=10,
        )
        btn_students.pack(pady=10)

        btn_courses = ctk.CTkButton(
            button_frame,
            text="📗 Manage Courses",
            command=self.open_courses,
            fg_color="#2e8b57",
            hover_color="#256d45",
            width=250,
            height=45,
            corner_radius=10,
        )
        btn_courses.pack(pady=10)

        btn_enrollments = ctk.CTkButton(
            button_frame,
            text="🎓 Enroll Students",
            command=self.open_enrollments,
            fg_color="#8a2be2",
            hover_color="#6a1db9",
            width=250,
            height=45,
            corner_radius=10,
        )
        btn_enrollments.pack(pady=10)

        btn_attendance = ctk.CTkButton(
            button_frame,
            text="🕒 Mark Attendance",
            command=self.open_attendance,
            fg_color="#ff8c00",
            hover_color="#e67300",
            width=250,
            height=45,
            corner_radius=10,
        )
        btn_attendance.pack(pady=10)

        btn_reports = ctk.CTkButton(
            button_frame,
            text="📊 View Reports",
            command=self.open_reports,
            fg_color="#ff4040",
            hover_color="#cc0000",
            width=250,
            height=45,
            corner_radius=10,
        )
        btn_reports.pack(pady=10)

    
    def open_students(self):
        try:
            from students import StudentManager
            StudentManager()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Students module:\n{e}")

    def open_courses(self):
        try:
            from courses import CourseManager
            CourseManager()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Courses module:\n{e}")

    def open_enrollments(self):
        try:
            from enrollments import EnrollManager
            EnrollManager()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Enroll module:\n{e}")

    def open_attendance(self):
        try:
            from attendance import AttendanceManager
            AttendanceManager()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Attendance module:\n{e}")

    def open_reports(self):
        try:
            from reports import ReportsManager
            ReportsManager()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Reports module:\n{e}")


 
if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()

