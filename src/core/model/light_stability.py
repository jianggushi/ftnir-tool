from datetime import datetime

from sqlalchemy import Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class LightStabilityResult(Base):
    __tablename__ = "light_stability"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    interference_max_max: Mapped[float] = mapped_column(
        Float, comment="干涉最大强度的最大值"
    )
    spectrum_max_max: Mapped[float] = mapped_column(
        Float, comment="光谱最大强度的最大值"
    )

    check_start_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, comment="检查开始时间"
    )

    check_end_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, comment="检查结束时间"
    )
