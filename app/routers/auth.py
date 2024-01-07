# Copyright (c) 2023 Gianmaria Castaldini

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from app import schemas, utils, oauth2
from app.database import get_db

from sqlalchemy.orm import Session
from app import models

#fastAPI things
from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)

@router.post("/")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """the login endpoint. it first select the user from the database if exist, then
    get it's saved hashed password and compare it with the plain password provided by
    the user using utils.verifyPassowrd.

    If good, create a JWT token and return it.

    Args:
        user_credential (_type_, optional): _description_. Defaults to Depends()):#:schemas.UserLogin.

    Raises:
        HTTPException: User not exists
        HTTPException: User password not match

    Returns:
        _type_: token and token type
    """    
    user = db.query(models.Users).filter(
    models.Users.email == user_credentials.username).first()
    # user = schemas.UserLogin.parse_obj(user) #this convert the RealDictRow to use as user.pass etc

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verifyPassword(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    #create the jwt token
    ######################################################
    # Now I'm creating a token containing the user.id
    # So when parsing the token to retrive the user info
    # I'll only get the user id!!!
    ######################################################
    access_token = oauth2.create_access_token(data={"user_id": user.id})  
    return {"access_token": access_token, "token_type": "bearer"}