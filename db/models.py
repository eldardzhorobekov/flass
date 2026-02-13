import datetime

from sqlalchemy import BigInteger, DateTime, Index, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TicketModel(Base):
    __tablename__ = "tickets"

    # Основные поля (Primary Key и Telegram метаданные)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    chat_name: Mapped[str] = mapped_column(String(255), nullable=False)
    message_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Данные о маршруте
    route_from: Mapped[str] = mapped_column(String(10), nullable=False)  # IATA коды
    route_to: Mapped[str] = mapped_column(String(10), nullable=False)

    # Даты и цены
    date_start: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    date_end: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    price: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="KZT")
    airline: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Служебные поля
    posted_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    # --- ИНДЕКСЫ ДЛЯ ОПТИМИЗАЦИИ ---
    __table_args__ = (
        # Индекс для быстрого поиска истории по составному ключу
        Index(
            "idx_history_lookup",
            "route_from",
            "route_to",
            "date_start",
            "date_end",
            "airline",
            "chat_id",
            posted_at.desc(),  # Сортировка внутри индекса для ускорения ROW_NUMBER()
        ),
        # Индекс для получения билетов по списку ID
        Index("idx_tickets_ids", "id"),
        {"schema": "flass"},
    )

    def __repr__(self) -> str:
        return (
            f"<Ticket {self.route_from}-{self.route_to} {self.price} {self.currency}>"
        )
