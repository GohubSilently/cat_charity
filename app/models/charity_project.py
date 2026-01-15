from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import InvestmentInformation


class CharityProject(InvestmentInformation):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f'{super().__repr__()}, name={self.name}'  # noqa: FCS100
