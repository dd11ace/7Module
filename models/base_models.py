from datetime import datetime

from pydantic import BaseModel, Field, field_validator, field_serializer, EmailStr
from typing import Optional

from enums.roles import Roles


class UserData(BaseModel):
    id: Optional[str | int] = None
    email: EmailStr
    fullName: str
    password: str
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    passwordRepeat: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="passwordRepeat должен вполностью совпадать с полем password",
    )
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        # Проверяем, совпадение паролей
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    @field_serializer("roles")
    def serialize_roles(self, roles: list[Roles | str]) -> list[str]:
        """Сериализует роли в строки, принимает как Enum, так и строки."""
        if not roles:
            return []

        result = []
        for role in roles:
            match role:
                case Roles():
                    result.append(role.value)
                case str():
                    result.append(role)
                case other:
                    result.append(str(other))

        return result

    def get_roles_as_strings(self) -> list[str]:
        """Возвращает роли в виде списка строк."""
        return self.serialize_roles(self.roles)
