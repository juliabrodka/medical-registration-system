import datetime
from enum import Enum

from app.exceptions.patient import InvalidPeselError


class Gender(Enum):
    FEMALE = "Female"
    MALE = "Male"


def validate_pesel_format(pesel):
    if len(pesel) != 11:
        raise InvalidPeselError(
            "Patient's PESEL must be 11 digits"
        )

    if not pesel.isdigit():
        raise InvalidPeselError(
            "Patient's PESEL must contain only digits"
        )


def validate_pesel_checksum(pesel):
    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]

    checksum = 0

    for i in range(len(weights)):
        checksum += weights[i] * int(pesel[i])

    control_digit = (10 - checksum % 10) % 10

    if control_digit != int(pesel[10]):
        raise InvalidPeselError(
            "Invalid PESEL: checksum error"
        )


def extract_birth_date(pesel):
    year = pesel[:2]
    month = int(pesel[2:4])
    day = int(pesel[4:6])

    if 1 <= month <= 12:
        year = "19" + year

    elif 21 <= month <= 32:
        year = "20" + year
        month -= 20

    elif 41 <= month <= 52:
        year = "21" + year
        month -= 40

    elif 61 <= month <= 72:
        year = "22" + year
        month -= 60

    elif 81 <= month <= 92:
        year = "18" + year
        month -= 80

    else:
        raise InvalidPeselError(
            "Invalid PESEL: invalid month"
        )

    try:
        return datetime.date(
            int(year),
            month,
            day
        )
    except ValueError:
        raise InvalidPeselError(
            "Invalid PESEL: invalid birth date"
        )


def extract_gender(pesel: str) -> Gender:
    gender = int(pesel[9])
    if gender % 2 == 0:
        return Gender.FEMALE
    else:
        return Gender.MALE


def validate_pesel(pesel):
    validate_pesel_format(pesel)
    validate_pesel_checksum(pesel)
    extract_birth_date(pesel)
