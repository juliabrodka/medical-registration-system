from dataclasses import dataclass, field

from app.models.patient import Patient
from app.exceptions.patient import InvalidPatientError, PatientDuplicateError, PatientNotFound, InvalidPatientStatus, InvalidSearchError


@dataclass
class PatientRepository:
    patient_list: list[Patient] =field( default_factory=list)

    def add(self, new_patient: Patient):
        if not isinstance(new_patient, Patient):
            raise InvalidPatientError(
                "Patient must be of type Patient"
            )
        for patient in self.patient_list:
            if patient.pesel == new_patient.pesel:
                raise PatientDuplicateError(
                    f"Patient with pesel {new_patient.pesel} already exists"
                )
            if patient.patient_id == new_patient.patient_id:
                raise PatientDuplicateError(
                    f"Patient with id {new_patient.patient_id} already exists"
                )
        self.patient_list.append(new_patient)

    def get_all(self):
        return self.patient_list.copy()

    def get_by_id(self, patient_id: int) -> Patient:

        for patient in self.patient_list:
            if patient.patient_id == patient_id:
                return patient
        raise PatientNotFound(
            f"Patient with id {patient_id} not found"
        )
    def get_by_pesel(self, pesel: str) -> Patient:
        for patient in self.patient_list:
            if patient.pesel == pesel:
                return patient
        raise PatientNotFound(
            f"Patient with pesel {pesel} not found"
        )

    def get_by_last_name(self, last_name: str) -> list[Patient]:
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
        patients = []
        last_name = last_name.casefold()
        for patient in self.patient_list:
            if patient.last_name.casefold().startswith(last_name):
                patients.append(patient)
        return patients

    def activate_by_id(self, patient_id: int) -> None:
        patient = self.get_by_id(patient_id)
        if patient.active:
            raise InvalidPatientStatus(
                "Patient is already active"
            )
        patient.activate()

    def deactivate_by_id(self, patient_id: int) -> None:
        patient = self.get_by_id(patient_id)
        if not patient.active:
            raise InvalidPatientStatus(
                "Patient is already inactive"
            )
        patient.deactivate()

    def __str__(self) :
        if len(self.patient_list) == 0:
            return "Empty patient list"
        return "\n".join(str(patient) for patient in self.patient_list)