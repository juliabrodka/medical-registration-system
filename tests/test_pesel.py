import datetime

import pytest

from app.validators.pesel import validate_pesel_checksum, validate_pesel_format, InvalidPeselError, \
    extract_birth_date


def test_invalid_checksum():
    with pytest.raises(InvalidPeselError):
        validate_pesel_checksum("67100702305")


def test_invalid_birth_month():
    with pytest.raises(InvalidPeselError):
        extract_birth_date("67130702304")


def test_invalid_birth_day():
    with pytest.raises(InvalidPeselError):
        extract_birth_date("67023102304")


@pytest.mark.parametrize(
    "invalid_pesel",
    [
        "1234567890",
        "123456789012",
        "67100A02304",
        "abcdefghijk"
    ]
)
def test_invalid_pesel_format(invalid_pesel):
    with pytest.raises(InvalidPeselError):
        validate_pesel_format(invalid_pesel)


def test_valid_pesel():
    assert extract_birth_date("67100702304") == datetime.date(1967, 10, 7)
    assert validate_pesel_checksum("67100702304") is None
    assert validate_pesel_format("67100702304") is None


@pytest.mark.parametrize(
    "pesel, expected_date",
    [
        ("92052412345", datetime.date(1992, 5, 24)),
        ("01252412345", datetime.date(2001, 5, 24)),
        ("11452412345", datetime.date(2111, 5, 24)),
        ("50652412345", datetime.date(2250, 5, 24)),
        ("60852412345", datetime.date(1860, 5, 24)),
    ]
)
def test_extract_birth_date_centuries(pesel, expected_date):
    assert extract_birth_date(pesel) == expected_date
