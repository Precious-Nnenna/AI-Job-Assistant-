from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Tells FastAPI docs where clients can log in to get a token.
# Also used to read the token from the Authorization header on protected routes.


