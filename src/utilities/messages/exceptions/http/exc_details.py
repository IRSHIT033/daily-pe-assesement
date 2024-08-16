from typing import List
from uuid import UUID

def http_400_username_details(username: str) -> str:
    return f"The username {username} is taken! Be creative and choose another one!"


def http_400_email_details(email: str) -> str:
    return f"The email {email} is already registered! Be creative and choose another one!"

def http_404_user_not_found() -> str:
    return " User not found "

def http_404_users_not_found(missing_ids:List[UUID]) -> str:
    return f" User_IDS not found : {', '.join([str(i) for i in missing_ids])}"

def http_404_manager_not_found() -> str:
    return " Manager not found "

def http_400_bulk_update_extra_keys(extra_keys:List[str]) -> str:
    return f"Cannot bulk update {', '.join(extra_keys)}. These can be updated individually only."

def http_400_user_ids_not_Provided() -> str:
    return " User ids not provided "

def http_400_signup_credentials_details() -> str:
    return "Signup failed! Recheck all your credentials!"


def http_400_sigin_credentials_details() -> str:
    return "Signin failed! Recheck all your credentials!"


def http_401_unauthorized_details() -> str:
    return "Refused to complete request due to lack of valid authentication!"


def http_403_forbidden_details() -> str:
    return "Refused access to the requested resource!"


def http_404_id_details(id: int) -> str:
    return f"Either the account with id `{id}` doesn't exist, has been deleted, or you are not authorized!"


def http_404_username_details(username: str) -> str:
    return f"Either the account with username `{username}` doesn't exist, has been deleted, or you are not authorized!"


def http_404_email_details(email: str) -> str:
    return f"Either the account with email `{email}` doesn't exist, has been deleted, or you are not authorized!"
