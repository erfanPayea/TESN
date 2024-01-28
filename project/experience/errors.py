from rest_framework import status

INVALID_ARGUMENTS = {
    "status": status.HTTP_400_BAD_REQUEST,
    "data": {
        "code": 1000,
        "message": "please provide necessary arguments"
    }
}

CITY_NOT_FOUND = {
    "status": status.HTTP_404_NOT_FOUND,
    "data": {
        "code": 4001,
        "message": "city not found!"
    }
}

ATTRACTION_NOT_FOUND = {
    "status": status.HTTP_404_NOT_FOUND,
    "data": {
        "code": 4002,
        "message": "attraction not found!"
    }
}

POST_NOT_FOUND = {
    "status": status.HTTP_404_NOT_FOUND,
    "data": {
        "code": 4003,
        "message": "post not found!"
    }
}

REVIEW_NOT_FOUND = {
    "status": status.HTTP_404_NOT_FOUND,
    "data": {
        "code": 4004,
        "message": "review not found!"
    }
}

COMMENT_NOT_FOUND = {
    "status": status.HTTP_404_NOT_FOUND,
    "data": {
        "code": 4005,
        "message": "comment not found!"
    }
}
