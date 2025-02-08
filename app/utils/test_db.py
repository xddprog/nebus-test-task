from sqlalchemy import select
from app.infrastructure.database.models.activity import Activity
from app.infrastructure.database.models.building import Building
from app.infrastructure.database.models.organization import Organization, OrganizationActivity, OrganizationPhone
from app.infrastructure.database.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


async def test_db(session: AsyncSession):
    try:
        is_exist = (await session.execute(select(Building))).scalars().all()
        if is_exist:
            return
        buildings = [
            Building(address="ул. Ленина, 10", latitude=55.76, longitude=37.62),
            Building(address="ул. Гагарина, 5", latitude=55.75, longitude=37.60),
            Building(address="пр-т Мира, 15", latitude=55.78, longitude=37.64),
        ]
        session.add_all(buildings)
        await session.flush()

        organizations = [
            Organization(name="Магазин Продукты", building_id=buildings[0].id),
            Organization(name="СТО Автосервис", building_id=buildings[1].id),
            Organization(name="Кафе Дружба", building_id=buildings[0].id),
            Organization(name="Магазин Автозапчасти", building_id=buildings[2].id),
            Organization(name="Супермаркет 24", building_id=buildings[1].id),
        ]
        session.add_all(organizations)
        await session.flush()

        activities = [
            Activity(name="Еда"),
            Activity(name="Мясная продукция", parent_id=1),
            Activity(name="Молочная продукция", parent_id=1),
            Activity(name="Автомобили"),
            Activity(name="Грузовые", parent_id=4),
            Activity(name="Легковые", parent_id=4),
            Activity(name="Запчасти", parent_id=4),
            Activity(name="Аксессуары", parent_id=4),
        ]
        session.add_all(activities)
        await session.flush()

        org_activities = [
            OrganizationActivity(organization_id=organizations[0].id, activity_id=1),
            OrganizationActivity(organization_id=organizations[1].id, activity_id=4),
            OrganizationActivity(organization_id=organizations[2].id, activity_id=1),
            OrganizationActivity(organization_id=organizations[3].id, activity_id=7),
            OrganizationActivity(organization_id=organizations[4].id, activity_id=1),
        ]
        session.add_all(org_activities)

        phones = [
            OrganizationPhone(organization_id=organizations[0].id, phone_number="+79991112233"),
            OrganizationPhone(organization_id=organizations[1].id, phone_number="+78882223344"),
            OrganizationPhone(organization_id=organizations[2].id, phone_number="+79995556677"),
            OrganizationPhone(organization_id=organizations[3].id, phone_number="+77778889900"),
            OrganizationPhone(organization_id=organizations[4].id, phone_number="+76667778899"),
        ]
        session.add_all(phones)

        users = [
            User(email="user1@example.com", password="hashed_password_1", token="token_1"),
            User(email="user2@example.com", password="hashed_password_2", token="token_2"),
            User(email="user3@example.com", password="hashed_password_3", token="token_3"),
        ]
        session.add_all(users)

        await session.commit()
    except Exception as e:
        raise e
    finally:
        await session.close()
