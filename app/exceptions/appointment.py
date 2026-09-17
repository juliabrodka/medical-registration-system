class AppointmentAlreadyBookedError(Exception):
    pass


class InactivePatientError(Exception):
    pass


class InactiveDoctorError(Exception):
    pass


class InvalidStatusError(Exception):
    pass


class InvalidAppointmentError(Exception):
    pass


class AppointmentNotFound(Exception):
    pass


class AppointmentDuplicateError(Exception):
    pass


class AppointmentConflictError(Exception):
    pass


class InvalidDateRangeError(Exception):
    pass


class CollidingAppointmentsError(Exception):
    pass
