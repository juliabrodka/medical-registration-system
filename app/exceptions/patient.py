class InvalidPeselError(Exception):
    pass


class MissingContactError(Exception):
    pass


class InvalidPatientError(Exception):
    pass


class PatientDuplicateError(Exception):
    pass


class PatientNotFound(Exception):
    pass


class InvalidSearchError(Exception):
    pass


class InvalidPatientStatus(Exception):
    pass
