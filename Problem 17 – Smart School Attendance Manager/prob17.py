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

