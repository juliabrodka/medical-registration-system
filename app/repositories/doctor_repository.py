from dataclasses import dataclass, field

from app.exceptions.doctor import InvalidDoctorError, DoctorDuplicateError, DoctorNotFoundError, \
    InvalidDoctorStatusError,InvalidSearchError
from app.models.doctor import Doctor, Specialization




@dataclass
class DoctorRepository:
    doctor_list: list[Doctor] =field( default_factory=list)

    def add(self, new_doctor: Doctor):
        if not isinstance(new_doctor, Doctor):
            raise InvalidDoctorError(
                "Doctor must be of type Doctor"
            )
        for doctor in self.doctor_list:
            if doctor.employee_number == new_doctor.employee_number:
                raise DoctorDuplicateError(
                    f"Doctor {new_doctor.employee_number} is already registered"
                )
            if doctor.doctor_id == new_doctor.doctor_id:
                raise DoctorDuplicateError(
                    f"Doctor {new_doctor.doctor_id} is already registered"
                )
        self.doctor_list.append(new_doctor)

    def get_all(self)->list[Doctor]:
        return self.doctor_list.copy()

    def get_by_id(self, doctor_id: int)->Doctor:
        for doctor in self.doctor_list:
            if doctor.doctor_id == doctor_id:
                return doctor
        raise DoctorNotFoundError(
            f"Doctor with id {doctor_id} not found"
        )

    def get_by_last_name(self, last_name: str) -> list[Doctor]:
        if not isinstance(last_name, str):
            raise InvalidSearchError(
                "Search must be a string"
            )
        last_name = last_name.strip()
        if not last_name:
            raise InvalidSearchError(
                "Search cannot be empty"
            )
        if not all(
            char.isalpha() or char in "-' "
            for char in last_name
        ):
            raise InvalidSearchError(
                "Search can contain only letters, spaces, hyphens and apostrophes"
            )
        doctors=[]
        last_name = last_name.casefold()
        for doctor in self.doctor_list:
            if doctor.last_name.casefold().startswith(last_name):
                doctors.append(doctor)
        return doctors

    def get_by_specialization(self, specialization: Specialization) -> list[Doctor]:
        if not isinstance(specialization, Specialization):
            raise InvalidSearchError(
                "Specialization must be of type Specialization"
            )
        doctors=[]
        for doctor in self.doctor_list:
            if doctor.specialization == specialization:
                doctors.append(doctor)
        return doctors

    def get_by_employee_number(self, employee_number: str)->Doctor:
        if not isinstance(employee_number, str):
            raise InvalidSearchError(
                "Search must be a string"
            )
        employee_number = employee_number.strip()
        if not employee_number:
            raise InvalidSearchError(
                "Search cannot be empty"
            )
        for doctor in self.doctor_list:
            if doctor.employee_number == employee_number:
                return doctor
        raise DoctorNotFoundError(
            f"Doctor with employee number {employee_number} not found"
        )

    def activate_by_id(self, doctor_id: int)->None:
        doctor = self.get_by_id(doctor_id)
        if doctor.active:
            raise InvalidDoctorStatusError(
                f"Doctor {doctor.employee_number} is already active"
            )
        doctor.activate()
    def deactivate_by_id(self, doctor_id: int)->None:
        doctor=self.get_by_id(doctor_id)
        if not doctor.active:
            raise InvalidDoctorStatusError(
                f"Doctor {doctor.employee_number} is already inactive"
            )
        doctor.deactivate()

    def __str__(self):
        if len(self.doctor_list) == 0:
         return "No doctors registered"
        return "\n".join(str(doctor) for doctor in self.doctor_list)