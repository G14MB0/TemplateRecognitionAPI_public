from app import schemas, utils
from app.database import get_db
from app import oauth2
from app import models

from sqlalchemy.orm import Session

#fastAPI things
from fastapi import status, HTTPException, APIRouter, Depends

#pydantic things
from typing import  List #list is used to define a response model that return a list


router = APIRouter(
    prefix="/inventories",
    tags=['Inventories']
)

@router.get("/", response_model=List[schemas.InventoryResponse]) #List say that the response is a list of that PostResponse Class
def get_inventories(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), name: str = ""):
    """Get all the Inventories for that user (users table rows) or filtered by a name

    Returns:
        list[dict]: all the user's inventories
    """    
    if name == "":
        inventories = db.query(models.Inventories).filter(models.Inventories.user_id == current_user.id).all()
        return inventories
    else:
        inventory = db.query(models.Inventories).filter(models.Inventories.user_id == current_user.id, models.Inventories.name == name).first()
        if not inventory:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No inventory named: {name}')
        return [inventory] # return a list to match the response_model


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.InventoryResponse)
def create_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_inventory = models.Inventories(name=inventory.name, description=inventory.description, user_id=current_user.id)

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    return new_inventory



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
