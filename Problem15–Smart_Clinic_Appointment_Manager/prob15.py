import streamlit as st
import datetime
import re
import time

# Initializing appointment data list, because we need to save appointent for later
if "appoinment_data" not in st.session_state:
    st.session_state.appoinment_data = []


# Title
st.title(" Smart Clinic Appointment Manager 🏥", text_alignment="center")
st.divider()


def side_bar():
    """Defines Sidebar Code (User Guide), so the user understands everything"""
    with st.sidebar:
        st.header("Clinic Data")

        # Clinic Name
        st.subheader("Clinic Name: ")
        st.info("Hana's Clinic")

        # Current Date
        st.subheader("Current Date: ")
        st.info(datetime.date.today())

        # Information Section
        st.subheader("Navigation/information section: ")
        st.markdown("""
        - The Receptionist Can:
            - Book appointments.\n
            - View all appointments.\n
            - Search for appointments.\n
            - Cancel appointments.\n
            - View today's schedule.\n
            - View clinic statistics.\n
            - Prevent appointment conflicts.
        """)


def time_check(text):
    pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
    return bool(re.match(pattern, text))


def validation(patient_name, reason_for_visit, appointment_time, appointment_date):
    if patient_name == "":
        return "Cannot Leave Space Empty"

    if not time_check(appointment_time):
        return "Please Enter Time in a Clear Format"

    if reason_for_visit == "":
        return "Cannot Leave Space Empty"

    if appointment_date < datetime.date.today():
        return "Cannot Book An Appointment For The Past"

    return True


def book_appointment_tab():
    with st.form("Enter Info"):
        patient_name = st.text_input("Patient Name: ")

        doctor_name = st.selectbox(
            "Doctor Name: ",
            [
                "DR. Marwa",
                "Dr. Aya",
                "Dr. Ahmed"
            ]
        )

        appointment_date = st.date_input("Appointment Date: ")
        appointment_time = st.text_input("Appointment Time: ")
        reason_for_visit = st.text_input("Reason For Visit: ")

        book_appointment = st.form_submit_button(
            "Book Appointment",
            type="primary"
        )

        if book_appointment == True:

            if validation(
                patient_name,
                reason_for_visit,
                appointment_time,
                appointment_date
            ) != True:

                st.error(
                    validation(
                        patient_name,
                        reason_for_visit,
                        appointment_time,
                        appointment_date
                    )
                )

            else:
                result = False

                for user in st.session_state.appoinment_data:

                    if (
                        user.get("doctor") == doctor_name
                        and user.get("date") == appointment_date
                        and user.get("time") == appointment_time
                    ):
                        st.warning(
                            "An Appointment At The Same Time Is Scheduled"
                        )
                        result = True
                        break

                if not result:
                    st.session_state.appoinment_data.append(
                        {
                            "name": patient_name,
                            "doctor": doctor_name,
                            "date": appointment_date,
                            "time": appointment_time,
                            "reason": reason_for_visit,
                            "status": "Scheduled"
                        }
                    )

                    st.spinner(" ")
                    time.sleep(2)
                    st.success("Appointment Booked Successfully")


def search_tab():
    patient = st.checkbox("Patient")
    doctor = st.checkbox("Doctor")
    date = st.checkbox("Date")

    if(patient):
        patient_name = st.text_input("Enter Patient Name: ")

    if(doctor):
        doctor_name = st.selectbox(
            "Enter Doctor Name: ",
            [
                "DR. Marwa",
                "Dr. Aya",
                "Dr. Ahmed"
            ]
        )

    if(date):
        appointment_date = st.date_input("Enter Appointment Date: ")

    submit = st.button("Submit")

    search_list = []

    if submit:

        for user in st.session_state.appoinment_data:

            match = True

            if patient:
                if user.get("name") != patient_name:
                    match = False

            if doctor:
                if user.get("doctor") != doctor_name:
                    match = False

            if date:
                if user.get("date") != appointment_date:
                    match = False

            if match:
                search_list.append(
                    {
                        "name": user.get("name"),
                        "doctor": user.get("doctor"),
                        "date": user.get("date"),
                        "time": user.get("time"),
                        "reason": user.get("reason"),
                        "status": user.get("status")
                    }
                )

        if search_list == []:
            st.info("No Matching Appointments")
        else:
            st.table(search_list)


def cancel_appointment_tab():
    patient_name = st.text_input("Patient Name: ")

    doctor_name = st.selectbox(
        "Doctor Name: ",
        [
            "DR. Marwa",
            "Dr. Aya",
            "Dr. Ahmed"
        ]
    )

    appointment_date = st.date_input("Appointment Date: ")
    appointment_time = st.text_input("Appointment Time: ")

    cancel = st.button("Cancel")

    if cancel:

        for user in st.session_state.appoinment_data:

            if (
                user.get("name") == patient_name
                and user.get("doctor") == doctor_name
                and user.get("date") == appointment_date
                and user.get("time") == appointment_time
            ):

                user["status"] = "Cancelled"

                st.spinner(" ")
                time.sleep(2)

                st.error("Appointment Cancelled Successfully")

                time.sleep(2)
                st.rerun()

                break

        else:
            st.warning("No Matching Appointemnts")


def todays_schedule():

    today_list = []

    for user in st.session_state.appoinment_data:

        if user.get("date") == datetime.date.today():

            today_list.append(
                {
                    "name": user.get("name"),
                    "doctor": user.get("doctor"),
                    "time": user.get("time"),
                    "reason": user.get("reason"),
                    "status": user.get("status")
                }
            )

    if today_list != []:
        st.table(today_list)
    else:
        st.info("No Appointments Today")


def statistics():

    active_appointments = 0
    today_appointments = 0

    dr_marwa_appointments = 0
    dr_aya_appointments = 0
    dr_ahmed_appointments = 0

    most_appoinments_doctor = ""

    for i in st.session_state.appoinment_data:

        if i.get("status") == "Scheduled":
            active_appointments += 1

        if i.get("date") == datetime.date.today():
            today_appointments += 1

        if i.get("doctor") == "DR. Marwa":
            dr_marwa_appointments += 1

        if i.get("doctor") == "Dr. Aya":
            dr_aya_appointments += 1

        if i.get("doctor") == "Dr. Ahmed":
            dr_ahmed_appointments += 1

    st.write("Active Appointments: ", active_appointments)
    st.write("Today's Appointments: ", today_appointments)

    st.write(
        "Dr. Marwa's Appointments: ",
        dr_marwa_appointments
    )

    st.write(
        "Dr. Aya's Appointments: ",
        dr_aya_appointments
    )

    st.write(
        "Dr. Ahmed's Appointments: ",
        dr_ahmed_appointments
    )

    if (
        dr_marwa_appointments > dr_aya_appointments
        and dr_marwa_appointments > dr_ahmed_appointments
    ):
        most_appoinments_doctor = "Dr. Marwa"

    if (
        dr_aya_appointments > dr_marwa_appointments
        and dr_aya_appointments > dr_ahmed_appointments
    ):
        most_appoinments_doctor = "Dr. Aya"

    if (
        dr_ahmed_appointments > dr_aya_appointments
        and dr_ahmed_appointments > dr_marwa_appointments
    ):
        most_appoinments_doctor = "Dr. Ahmed"

    st.subheader("Doctor with most appointments")
    st.code(most_appoinments_doctor)


def group_by_date():

    sorted_appointments = sorted(
        st.session_state.appoinment_data,
        key=lambda user: user.get("date")
    )

    current_date = None
    who = []

    for user in sorted_appointments:

        appointment_date = user.get("date")

        if appointment_date != current_date:

            if who:
                st.table(who)

            st.subheader(appointment_date)

            who = []
            current_date = appointment_date

        who.append(user)

    if who:
        st.table(who)

def doctor_weekly_schedule():

    today = datetime.date.today()

    start_of_this_week = (
        today - datetime.timedelta(days=today.weekday())
    )

    end_of_this_week = (
        start_of_this_week + datetime.timedelta(days=6)
    )

    doctors = [
        "DR. Marwa",
        "Dr. Aya",
        "Dr. Ahmed"
    ]

    for doctor in doctors:

        doctor_list = []

        for appointment in st.session_state.appoinment_data:

            if (
                appointment.get("doctor") == doctor
                and start_of_this_week
                <= appointment.get("date")
                <= end_of_this_week
            ):

                doctor_list.append(appointment)

        if doctor_list:

            # Sort doctor's appointments by date and time
            doctor_list = sorted(
                doctor_list,
                key=lambda appointment: (
                    appointment.get("date"),
                    appointment.get("time")
                )
            )

            st.subheader(doctor)
            st.table(doctor_list)


side_bar()


tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "Book Appointment",
        "View Appointments",
        "Search",
        "Cancel Appointments",
        "Today's Schedule",
        "Statistics",
        "Weekly Clinic Management System"
    ]
)


with tab1:
    book_appointment_tab()


with tab2:

    if st.session_state.appoinment_data != []:
        st.table(st.session_state.appoinment_data)
    else:
        st.info("No Appointments Booked Yet")


with tab3:
    search_tab()


with tab4:
    cancel_appointment_tab()


with tab5:
    todays_schedule()


with tab6:
    statistics()


with tab7:
    group_by_date()
    doctor_weekly_schedule()
