import jwt
import logging
from datetime import datetime
from Utils import *


def query_table(query_filter, client, first_entry=True):
    # query_filter example "Username eq 'Abus3r'"
    entities = client.query_entities(query_filter)
    if first_entry:
        for entity in entities:
            username = entity   # ???!
            return username
    else:
        return entities


def validate_token(token):
    # Read token claims
    try:
        claims = jwt.decode(token, options={"verify_signature": False})
    except jwt.DecodeError:
        logging.warning('Failed to decode received token')
        return False
    # Query for specified user in received token
    table_client = create_users_client()
    entity = query_table("Username eq '{0}'".format(claims['username']), table_client)
    # Check username exists
    if not entity:
        logging.warning('Username not found')
        return False
    pass_hash = entity['Password']
    # Decode token
    try:
        decoded_token = jwt.decode(token, pass_hash, algorithms=["HS256"])
    except:
        logging.warning('Invalid token')
        return False
    # Check decoded token is matching claims in received token
    for entry in decoded_token:
        if claims[entry] != decoded_token[entry]:
            logging.warning('Token claims do not match decoded token')
            return False
    # Check expiration time
    if int(datetime.timestamp(datetime.utcnow())) - decoded_token['expires_at'] > 0:
        logging.warning('Token is expired')
        return False
    else:
        logging.info('Token is valid for username {0}'.format(decoded_token['username']))
        return decoded_token['username']
