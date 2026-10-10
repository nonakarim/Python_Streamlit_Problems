import streamlit as st
import datetime

students = []

class StudentDetails:
    def record_attendance(self, id, name, date, cls, status):
        self.id = id
        self.name = name
        self.date = date
        self.cls = cls
        self.status = status

        students.append({
            "ID": self.id,
            "Name": self.name, 
            "Date": self.date, 
            "Class": self.cls,
            "Status": self.status
        })

    def correct_attendance(self, name, date, status):
        for student in students:
            if student.get("Name") == name and student.get("Date") == date:
                self.status = status
                student.get("Status") = self.status

class StudentDirectory:
    def view_students(self):
        st.table(students)

    #Search Student Still Under Progress

class SearchHistoryTracker:
    def attendance_history(self, id):
        for student in students:
            if student.get("ID") == id:
                st.table(student)

    def today_attendance(self):
        today = datetime.date.today()

        absent=[]
        present=[]

        for student in students:
            if student.get("Date") == today:
                if student.get("Status") == "Absent":
                    absent.append(student)
                else:
                    present.append(student)

        isAbsent=True
        isPresent = True

        if absent != []:
            st.subheader("🔴Absent Students")
            st.table(absent)
        else:
            isAbsent = False

        if present != []:
            st.subheader("🟢Present Students")
            st.table(present)
        else:
            isPresent = False

        if not isAbsent and isPresent:
            st.info("No absence has been recorded today.")
        elif not isPresent and isAbsent:
            st.info("No attendance has been recorded today.")
        elif not isPresent and not isAbsent:
            st.info("No Student Records Today YET")

class OverallStatistics:
    def total_students(self):
        total_students = set()

        for student in students:
            total_students.add(student.get("Name"))

        st.write(f"👩🏻‍🎓Total Students: {len(total_students)}")

    def total_attendance_records(self):
        st.write(f"📋Total Attendance Records {len(students)}")

    def absent_present(self):
        absent=[]
        present=[]

        for student in students:
            if student.get("Status") == "Absent":
                absent.append(student)
            else:
                present.append(student)

        st.write(f"🟢Total Present Students {len(present)}")
        st.write(f"🔴Total Absent Students {len(absent)}")

        st.write(f"📈Total Attendance Percentage: {len(present)/len(students)*100}%")
