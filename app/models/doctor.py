from dataclasses import dataclass
from enum import Enum
from app.exceptions.doctor import InvalidSpecializationError

class Specialization(Enum):
    CARDIOLOGY = "Cardiology"
    DERMATOLOGY = "Dermatology"
    NEUROLOGY = "Neurology"
    PEDIATRICS = "Pediatrics"
    INTERNAL_MEDICINE = "Internal Medicine"
    GYNECOLOGY = "Gynecology"


@dataclass
class Doctor:
    doctor_id: int
    employee_number: str
    first_name: str
    last_name: str

    specialization: Specialization

    room: str | None = None

    active: bool = True

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_status(self):
        if self.active:
            return "Active"
        else:
            return "Inactive"

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def change_room(self, new_room):
        self.room = new_room

    def change_specialization(self, new_specialization):
        if not isinstance(new_specialization, Specialization):
            raise InvalidSpecializationError(
                "Specialization must be of type Specialization"
            )

        self.specialization = new_specialization

    def __str__(self):
        return (
            f"---Doctor INFO---\n"
            f"{self.get_status()} Doctor\n"
            f"Employee Number: {self.employee_number}\n"
            f"Name: {self.first_name} {self.last_name}\n"
            f"Specialization: {self.specialization.value}\n"
            f"Room: {self.room}\n"
        )

    def __post_init__(self):
        if not isinstance(self.specialization, Specialization):
            raise InvalidSpecializationError(
                "Specialization must be of type Specialization"
            )
