from sqlalchemy.orm import Session

from app.db.models import Application
from app.db.config import LIMIT
from app.db.schemas import ApplicationCreate


class ApplicationDAO:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_application(self, application_id: int) -> Application:
        q = await self.db_session.query(Application) \
            .filter(Application.id == application_id).first()
        return q

    async def get_application_by_path(self, application_path: str) -> Application:
        q = await self.db_session.query(Application) \
            .filter(Application.app_path == application_path).first()
        return q

    async def get_all_applications(self):
        q = await self.db_session.query(Application).limit(LIMIT).all()
        return q

    async def create_application(self, application: ApplicationCreate):
        new_app = Application(app_path=application.app_path)
        self.db_session.add(new_app)
        await self.db_session.commit()
        await self.db_session.refresh(new_app)
        return new_app
