from rest_framework import status

INVALID_ARGUMENTS = {
    "status": status.HTTP_400_BAD_REQUEST,
    "data": {
        "code": 1000,
        "message": "please provide necessary arguments"
    }
}
USER_NOT_FOUND = {
    "status": status.HTTP_404_NOT_FOUND,
    "data": {
        "code": 1001,
        "message": "user not found"
    }
}
OTP_NOT_VALID = {
    "status": status.HTTP_400_BAD_REQUEST,
    "data": {
        "code": 2000,
        "message": "otp is not valid"
    }
}
OTP_EXPIRED = {
    "status": status.HTTP_400_BAD_REQUEST,
    "data": {
        "code": 2001,
        "message": "please provide necessary arguments"
    }
}
OTP_WAIT = {
    "status": status.HTTP_400_BAD_REQUEST,
    "data": {
        "code": 2002,
        "message": "wait 2 minutes and try again "
    }
}
DUPLICATE_USERNAME = {
    "status": status.HTTP_400_BAD_REQUEST,
    "data": {
        "code": 2003,
        "message": "username already exists."
    }
}
DUPLICATE_EMAIL = {
    "status": status.HTTP_400_BAD_REQUEST,
    "data": {
        "code": 2004,
        "message": "a user with this email already exists."
    }
}
