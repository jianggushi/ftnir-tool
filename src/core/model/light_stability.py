from datetime import datetime

from sqlalchemy import Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class LightStability(Base):
    __tablename__ = "light_stability"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    interference_max_max: Mapped[float] = mapped_column(Float)
    interference_max_min: Mapped[float] = mapped_column(Float)
    interference_max_mean: Mapped[float] = mapped_column(Float)
    interference_max_std: Mapped[float] = mapped_column(Float)

    check_start_time: Mapped[datetime] = mapped_column(DateTime)
    check_end_time: Mapped[datetime] = mapped_column(DateTime)
