import base64
import uuid
import hashlib

def password_hashing(password, salt):
        print "Start Password hashing";
        if salt is None:
            salt = uuid.uuid4().hex
        password_hash = hashlib.sha512(password + salt).hexdigest()
        print "End Password hashing";
        return (password_hash, salt);


def check_password(password, hashed_password, salt):
        rehashing, salt = password_hashing(password, salt);
        return rehashing == hashed_password