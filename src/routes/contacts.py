from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel
from src.repository import contacts as repository_contacts
import src.services.auth as auth_service


router = APIRouter(prefix='/contacts')


@router.get("/", response_model=List[ContactModel])
async def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactModel)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact


@router.post("/new", response_model=ContactModel, status_code=status.HTTP_201_CREATED)
async def create_contact(
        body: ContactModel,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}/update", response_model=ContactModel)
async def update_contact(
        body: ContactModel,
        contact_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact


@router.delete("/{contact_id}/delete", response_model=ContactModel)
async def remove_contact(
        contact_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contact


@router.get('/by_name/{name}', response_model=List[ContactModel])
async def search_by_name(
        name: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):
    contacts = await repository_contacts.search_by_name(name, current_user, db)
    if len(contacts) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contacts


@router.get('/by_surname/{surname}', response_model=List[ContactModel])
async def search_by_surname(
        surname: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):
    contacts = await repository_contacts.search_by_surname(surname, current_user, db)
    if len(contacts) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contacts


@router.get('/by_email/{email}', response_model=List[ContactModel])
async def search_by_email(
        email: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):
    contacts = await repository_contacts.search_by_email(email, current_user, db)
    if len(contacts) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contacts


@router.get('/next_week_birthdays/', response_model=List[ContactModel])
async def next_week_birthdays(db: Session = Depends(get_db)):
    current_user: User = Depends(auth_service.get_current_user)
    contacts = await repository_contacts.upcoming_birthdays(current_user, db)
    if len(contacts) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    return contacts