from app import schemas, utils
from app.database import get_db
from app import oauth2
from app import models

from sqlalchemy.orm import Session

#fastAPI things
from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.exc import IntegrityError

#pydantic things
from typing import  List #list is used to define a response model that return a list


router = APIRouter(
    prefix="/data",
    tags=['Data']
)

@router.get("/", response_model=List[schemas.DataResponse])
def get_data(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), name: str = ""):
    """Get all the data for that user (users table rows) or filtered by a name

    Returns:
        list[dict]: all the user's inventories
    """    
    if name == "":
        data = db.query(models.Data).filter(models.Data.owner_id == current_user.id).all()
        return data
    else:
        data = db.query(models.Data).filter(models.Data.owner_id == current_user.id, models.Data.name == name).first()
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No data named: {name}')
        return [data] # return a list to match the response_model even if it's only one



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DataResponse)
def create_data(data: schemas.DataCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    try:
        new_data = models.Data(name=data.name, data=data.data, owner_id=current_user.id)

        db.add(new_data)
        db.commit()
        db.refresh(new_data)

        return new_data
    
    except IntegrityError as e:
        db.rollback()  # Rollback the session to a clean state
        # Check if the exception is due to a unique constraint violation
        if "unique" in str(e.orig) or "duplicat" in str(e.orig):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duplicate data name")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    except Exception as e:
        db.rollback()  # Ensure the session is rolled back in case of any other exceptions
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{name}")
def delete_data(name: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if name != "":
        data = data = db.query(models.Data).filter(models.Data.owner_id == current_user.id, models.Data.name == name).first()
        if data is None:
            raise HTTPException(status_code=404, detail="Data not found")
        else:
            # If data exists, delete it
            db.delete(data)
            db.commit()
    else:
        raise HTTPException(status_code=404, detail="No data name has been passed")
    
    return {"message": f"data with name {name} correctly deleted"}


# @router.get("/{name}", response_model=schemas.InventoryResponse)
# def get_inventory_name(name: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     """get user's inventory by name

#     Args:
#         name (str): name

#     Raises:
#         HTTPException: name doesn't exists

#     Returns:
#         inventory: class InventoryResponse(BaseModel):
#     """    

    
#     inventory = db.query(models.Inventories).where(models.Inventories.name == name, models.Inventories.user_id == current_user.id).first()

#     if not inventory:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'inventory with name {name} does not exist')

#     return inventory


# @router.put("/", response_model=schemas.UserResponse)
# def modify_user(updated_user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     """_summary_

#     Args:
#         updated_user (schemas.UserUpdate): class UserUpdate(BaseModel):
#                                                 id: Optional[int] = None
#                                                 email: Optional[EmailStr] = None
#                                                 name: Optional[str]
#                                                 role: Optional[str]

#     Raises:
#         HTTPException: if missing ID and email, at lease one of them must be provided
#         HTTPException: if the user doesn't exists, so nothing to modify

#     Returns:
#         user: class UserResponse(BaseModel):
#                 created_at: datetime
#                 email: EmailStr
#                 name: str
#                 id: int
#                 role: str
#     """    
#     # cursor.execute(f'SELECT * FROM users WHERE id = {id}')
#     # user = cursor.fetchone()
    
#     if updated_user.email is None and updated_user.id is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Need to provide user ID or user email!')
    
#     if current_user.role != "administrator" and updated_user.role == "administrator":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Need privileged access to get this data. your role: {current_user.role}")


#     if current_user.role != "administrator" and \
#             ((updated_user.id and current_user.id != updated_user.id) or \
#              (updated_user.email and current_user.email != updated_user.email)):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Need privileged access to modify this data. your role: {current_user.role}")

#     # Construct the query based on email or id
#     user_query = None
#     if updated_user.id:
#         user_query = db.query(models.Users).filter(models.Users.id == updated_user.id)
#         # Check if the user exist
#         user = user_query.first()
#         if user == None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {updated_user.id} does not exist')
#     else:
#         user_query = db.query(models.Users).filter(models.Users.email == updated_user.email)
#         # Check if the user exist
#         user = user_query.first()
#         if user == None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with email {updated_user.email} does not exist')

    

#     # Update the user's attributes
#     user_data = updated_user.model_dump()
#     # Remove 'id' and 'email' keys if they exist to NOT update them
#     user_data.pop('id', None)
#     user_data.pop('email', None)

#     user_query.update(user_data)

#     db.commit()

#     return user_query.first()
