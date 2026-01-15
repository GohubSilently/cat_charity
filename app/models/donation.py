from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import InvestmentInformation


class Donation(InvestmentInformation):
    comment: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id'),
    )

    def __repr__(self) -> str:
        return f'{super().__repr__()}, comment={self.comment}'  # noqa: FCS100
