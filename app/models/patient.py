from dataclasses import dataclass,field
from datetime import date
from app.validators.pesel import validate_pesel, extract_birth_date, extract_gender, Gender
from app.exceptions.patient import MissingContactError



@dataclass
class Patient:
    patient_id: int
    first_name: str
    last_name: str
    pesel: str

    phone: str | None=None
    email: str | None=None
    address: str | None=None

    active: bool=True

    birth_date: date=field(init=False)
    gender: Gender=field(init=False)

    def deactivate(self)->None:
        self.active = False
    def activate(self)->None:
        self.active = True


    def verify_contact(self)->None:
        phone_missing = self.phone is None or not self.phone.strip()
        email_missing = self.email is None or not self.email.strip()

        if phone_missing and email_missing:
            raise MissingContactError(
                "Patient must have at least a phone number or email."
            )
    def get_full_name(self)->str:
        return f"{self.first_name} {self.last_name}"

    def get_status(self) -> str:
        if self.active:
            return "ACTIVE"
        return "INACTIVE"
    def __str__(self)->str:
        return(
            "---Patient INFO---\n"
            f"{self.get_status()} Patient\n"
            f"Name: {self.get_full_name()}\n"
            f"PESEL: {self.pesel}\n"
            f"Date of birth: {self.birth_date}\n"
            f"Gender: {self.gender.value}\n"
            f"Phone number: {self.phone}\n"
            f"Email: {self.email}\n"
            f"Address: {self.address}\n"
        )
    def __post_init__(self):
        self.verify_contact()
        validate_pesel(self.pesel)
        self.birth_date = extract_birth_date(self.pesel)
        self.gender=extract_gender(self.pesel)

