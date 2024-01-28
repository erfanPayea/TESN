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
ALREADY_EXISTS = {
    "status": status.HTTP_400_BAD_REQUEST,
    "data": {
        "code": 3000,
        "message": "requested model already exists"
    }
}
CHAT_NOT_FOUND = {
    "status": status.HTTP_404_NOT_FOUND,
    "data": {
        "code": 3001,
        "message": "chat not found!"
    }
}
MESSAGE_NOT_FOUND = {
    "status": status.HTTP_404_NOT_FOUND,
    "data": {
        "code": 3002,
        "message": "message not found!"
    }
}
