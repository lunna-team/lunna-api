from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.dependencies import get_db, get_current_user
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.models.user import User
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserResponse

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    request: LoginRequest, 
    db: AsyncSession = Depends(get_db)
):
    """
    Autenticar usuário com email e senha.
    """
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token = create_access_token(subject=user.id, role=user.role)
    refresh_token = create_refresh_token(subject=user.id, role=user.role)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Finalizar sessão. No caso de JWT stateless, geralmente apenas avisamos o cliente para deletar o token,
    ou implementamos uma blacklist com Redis.
    """
    return {"message": "Logged out successfully"}
