from fastapi import APIRouter, HTTPException, Request, Depends, Form
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.schema_user import User, UserCreate
from app.crud import crud_user

# Server-side rendering
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["users"], default_response_class=HTMLResponse)
templates = Jinja2Templates(directory="app/templates")


# --------------- USER CREATION endpoint "/signup" ---------------
# Define a GET route for the sign-up page with csrf_token
@router.get("/signup/", name="signup")
def get_signup_page(request: Request):
    csrf_token = request.cookies.get("csrf_token")
    return templates.TemplateResponse(
        "signup.html", {"request": request, "csrf_token": csrf_token}
    )


# Define a POST route to create a new user
@router.post(
    "/signup/",
    response_class=HTMLResponse,
    response_model=UserCreate,
    name="create_user",
)
def create_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Create new user

    Args:
        username (str, optional): username given from HTML form
        email (str, optional): email given from HTML form
        password (str, optional): password given from HTML form
        csrf_token (str, optional): token from cookies
        db (Session, optional)
    """
    user = UserCreate(
        username=username,
        email=email,
        password=password,
    )
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud_user.create_user(db=db, user=user)
    context = {"request": request, "new_user": new_user, "csrf_token": csrf_token}
    return templates.TemplateResponse("signup.html", context)
