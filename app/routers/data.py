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
        # Check if the data already exists based on name and owner_id
        existing_data = db.query(models.Data).filter(models.Data.name == data.name, models.Data.owner_id == current_user.id).first()
        
        if existing_data:
            # If data exists, update it
            existing_data.data = data.data
            db.commit()
            db.refresh(existing_data)
            return existing_data
        else:
            # If data does not exist, create a new record
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


