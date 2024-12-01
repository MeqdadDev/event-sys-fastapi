from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from app.config import settings
from app.models import User
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.routers.auth import oauth2_scheme


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token",
            )
        # Query the user asynchronously
        user_id = int(user_id)
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User not found"
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
