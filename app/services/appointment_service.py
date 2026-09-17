from dataclasses import dataclass
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.patient_repository import PatientRepository
from app.repositories.doctor_repository import DoctorRepository
from app.models.appointment import Appointment, AppointmentStatus
from app.exceptions.appointment import CollidingAppointmentsError, InvalidDateRangeError
import datetime


@dataclass
class AppointmentService:
    appointments: AppointmentRepository
    patients: PatientRepository
    doctors: DoctorRepository

    def book_appointment(self, appointment_id: int, patient_id: int) -> None:
        appointment = self.appointments.get_by_id(appointment_id)
        patient = self.patients.get_by_id(patient_id)
        appointments = self.appointments.get_by_patient_id(patient_id)
        for app in appointments:
            if (app.date == appointment.date
                    and app.time == appointment.time
                    and app.status == AppointmentStatus.BOOKED
                    and app.appointment_id != appointment.appointment_id):
                raise CollidingAppointmentsError(
                    "Appointments are colliding"
                )
        appointment.book_appointment(patient)

    def cancel_booking(self, appointment_id) -> None:
        appointment = self.appointments.get_by_id(appointment_id)
        appointment.cancel_booking()

    def cancel_appointment(self, appointment_id: int) -> None:
        appointment = self.appointments.get_by_id(appointment_id)
        appointment.cancel_appointment()

    def get_doctor_schedule(self, doctor_id: int) -> list[Appointment]:
        self.doctors.get_by_id(doctor_id)
        return self.appointments.get_by_doctor_id(doctor_id)

    def handle_doctor_absence(self, doctor_id: int, start: datetime.date, end: datetime.date) -> None:
        if start > end:
            raise InvalidDateRangeError(
                "Invalid date range"
            )
        self.doctors.get_by_id(doctor_id)
        appointments = self.appointments.get_by_doctor_id(doctor_id)
        for appointment in appointments:
            if start <= appointment.date <= end:
                if appointment.status != AppointmentStatus.CANCELLED:
                    appointment.cancel_appointment()
