from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from app.database import get_db

from sqlalchemy.orm import Session
from app import models

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.config import settings

#this line of code simply create a scheme for the password automatically checking 
#from the login API requestForm
oaut2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/login')  ## this must coincide with the ./login endopoint without the ./

#SECRET_KEY
#Algorithm
#Expiration time
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    """This methon create the jwt token 
        based on payload "data" using the jose library
    Args:
        data (dict): payload to use in jwt token creation

    Returns:
        _type_: the jwt token
    """    
    to_encode = data.copy() #this sore a new variable insted of link them

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt



def verify_access_token(token: str, credentials_exception):
    """This method verify that the token is properly formed
    by decoding it and then checking if there is the payload
    used to create the token.
    If there is a problem, it raise a credential exception

    Args:
        token (str): the jwt token      
        credentials_exception (_type_): still dunno

    Raises:
        credentials_exception: still dunno
        credentials_exception: still dunno
    """    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        #in questo passaggio sto "estraendo" il payload che gli ho messo prima
        #questo significa che se cambio/aggiungo roba prima (in auth.py) anche qui devo modificare
        id = payload.get("user_id") 

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oaut2_scheme), db: Session = Depends(get_db)):
    """
    *** Use this method to parse the token and get the logged user ***

    This method define a credential exception and then pass it, both with the token
    to the verify_access_token to validate the user login. if the access token is correct,
    it proceed with getting the user from the Database

    The method can be used to know what user is communicating by parsing the bearer token.

    Args:
        token (str, optional): the token. Defaults to Depends(oaut2_scheme).

    Returns:
        _type_: a raise if there is a login problem
    """    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="could not validate credentials",
                                         headers={"WWW-Autenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    # retrive the user and return it
    user = db.query(models.Users).where(models.Users.id == token.id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Error with this user")
    return user

