from model.repositories.shedule_repository import ScheduleRepository
from model.schemas.user_shcema import User


def get_today_schedule():
    user = User()
    instance = ScheduleRepository(user.schedule_url)
    return instance.generate_schedule()