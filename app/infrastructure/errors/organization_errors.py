from fastapi import HTTPException


class OrganizationNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Organization not found")