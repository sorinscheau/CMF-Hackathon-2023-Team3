from datetime import timedelta
import logging
import jwt
import bcrypt
from Utils.ValidateToken import *
from DatabaseIntegration import *


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


# Register user
def add_username(username, password):
    hashed_pass = get_hashed_password(str(password)).decode('utf-8')
    add_user(username, hashed_pass)


def login_username(username, password):
    hashed_pass = get_user_hash(username)
    if not hashed_pass:
        logging.warning('Username is not registered, cannot login.')
        return False
    else:
        # Compare sent password with hashed password
        if check_password(password, hashed_pass):
            timestamp_now = int(datetime.timestamp(datetime.utcnow()))
            token_object = {
                "username": username,
                "created_at": timestamp_now,
                "expires_at": timestamp_now + int(timedelta(seconds=3600).total_seconds())
            }
            token = jwt.encode(token_object, hashed_pass, algorithm="HS256")
            return token
        else:
            logging.info('Invalid password')
            return False
