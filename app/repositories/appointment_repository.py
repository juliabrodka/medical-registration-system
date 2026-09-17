import datetime
from dataclasses import dataclass, field

from app.exceptions.appointment import InvalidAppointmentError, InactiveDoctorError, AppointmentDuplicateError, \
    AppointmentConflictError, AppointmentNotFound
from app.models.appointment import Appointment, AppointmentStatus


@dataclass
class AppointmentRepository:
    appointment_list: list[Appointment] = field(default_factory=list)

    def add(self, new_appointment: Appointment):
        if not isinstance(new_appointment, Appointment):
            raise InvalidAppointmentError(
                "Appoinment must be of type Appoinment"
            )
        if not new_appointment.doctor.active:
            raise InactiveDoctorError(
                "Cannot add appointment with inactive doctor."
            )
        for appointment in self.appointment_list:
            if appointment.appointment_id == new_appointment.appointment_id:
                raise AppointmentDuplicateError(
                    f'Appointment with id {new_appointment.appointment_id} already exists.'
                )
            if (appointment.date == new_appointment.date
                    and appointment.time == new_appointment.time
                    and appointment.doctor.doctor_id == new_appointment.doctor.doctor_id):
                raise AppointmentConflictError(
                    f"Appointment with doctor {new_appointment.doctor} on {new_appointment.date} {new_appointment.time} already exists."
                )

        self.appointment_list.append(new_appointment)

    def get_all(self) -> list[Appointment]:
        return self.appointment_list.copy()

    def get_by_id(self, appointment_id: int) -> Appointment:
        for appointment in self.appointment_list:
            if appointment.appointment_id == appointment_id:
                return appointment
        raise AppointmentNotFound(
            f"Appointment with id {appointment_id} was not found."
        )

    def get_by_date(self, date: datetime.date) -> list[Appointment]:
        appointments = []
        for appointment in self.appointment_list:
            if date == appointment.date:
                appointments.append(appointment)
        return appointments

    def get_by_doctor_id(self, doctor_id: int) -> list[Appointment]:
        appointments = []
        for appointment in self.appointment_list:
            if doctor_id == appointment.doctor.doctor_id:
                appointments.append(appointment)
        return appointments

    def get_by_patient_id(self, patient_id: int) -> list[Appointment]:
        appointments = []
        for appointment in self.appointment_list:
            if (appointment.patient is not None
                    and appointment.patient.patient_id == patient_id):
                appointments.append(appointment)
        return appointments

    def get_by_status(self, status: AppointmentStatus) -> list[Appointment]:
        appointments = []
        for appointment in self.appointment_list:
            if appointment.status == status:
                appointments.append(appointment)
        return appointments
