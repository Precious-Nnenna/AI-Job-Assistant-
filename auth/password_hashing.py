from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$V7GHdeReanrWv/ZA9sszrw$2JNMLY+PjjZ1bYn4t719jGInCyhGH4qLaCz9ptcNosU"

def hash_password(password):
    hashed_password = password_hash.hash(password)
    return hashed_password

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)










