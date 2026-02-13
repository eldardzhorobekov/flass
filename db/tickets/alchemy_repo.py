from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import TicketModel
from tickets.message import TicketComplete


class TicketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_latest_by_routes(
        self, keys: list[tuple], exclude_ids: list[int]
    ) -> list[TicketComplete]:
        """
        Находит последние версии билетов в базе для указанных маршрутов.
        Используется для вычисления prev_price.
        """
        if not keys:
            return []

        # 1. Строим условия для фильтрации по составным ключам
        # Используем .is_(None), чтобы SQLite корректно находил One-Way билеты
        key_conditions = []
        for k in keys:
            # k: (route_from, route_to, date_start, date_end, airline, chat_id)
            cond = and_(
                TicketModel.route_from == k[0],
                TicketModel.route_to == k[1],
                TicketModel.date_start == k[2],
                TicketModel.date_end.is_(None)
                if k[3] is None
                else TicketModel.date_end == k[3],
                TicketModel.airline == k[4],
                TicketModel.chat_id == k[5],
            )
            key_conditions.append(cond)

        # 2. Подзапрос с оконной функцией для нумерации билетов внутри групп
        subq = (
            select(
                TicketModel,
                func.row_number()
                .over(
                    partition_by=[
                        TicketModel.route_from,
                        TicketModel.route_to,
                        TicketModel.date_start,
                        TicketModel.date_end,
                        TicketModel.airline,
                        TicketModel.chat_id,
                    ],
                    order_by=desc(TicketModel.posted_at),
                )
                .label("rn"),
            ).where(and_(or_(*key_conditions), TicketModel.id.notin_(exclude_ids)))
        ).subquery()

        # 3. Выбираем только самые свежие (rn=1)
        # Нам нужны именно объекты модели, поэтому выбираем через aliased или алиас подзапроса
        query = select(TicketModel).from_statement(select(subq).where(subq.c.rn == 1))

        result = await self.session.execute(query)
        db_tickets = result.scalars().all()

        # 4. Мапим TicketModel -> TicketComplete (ручное заполнение для Dataclass)
        return [self._to_complete_dto(t) for t in db_tickets]

    @staticmethod
    def _to_complete_dto(t: TicketModel) -> TicketComplete:
        """Вспомогательный метод для конвертации модели в DTO"""
        return TicketComplete(
            id=t.id,
            chat_id=t.chat_id,
            chat_name=t.chat_name,
            message_id=t.message_id,
            posted_at=t.posted_at,
            route_from=t.route_from,
            route_to=t.route_to,
            date_start=t.date_start,
            date_end=t.date_end,
            price=t.price,
            currency=t.currency,
            airline=t.airline,
            prev_price=None,  # Будет заполнено в контроллере
        )

    async def get_by_ids(self, ticket_ids: list[int]) -> list[TicketComplete]:
        """Получение конкретных билетов по их ID"""
        if not ticket_ids:
            return []

        query = select(TicketModel).where(TicketModel.id.in_(ticket_ids))
        result = await self.session.execute(query)
        return [self._to_complete_dto(t) for t in result.scalars().all()]
