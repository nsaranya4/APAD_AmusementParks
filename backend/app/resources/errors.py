class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class BadRequestError(Exception):
    pass


class EntityNotFoundError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
    "BadRequestError": {
        "message": "Incorrect data provided",
        "status": 400
    },
    "EntityNotFoundError": {
        "message": "Entity Not Found",
        "status": 404
    }

}