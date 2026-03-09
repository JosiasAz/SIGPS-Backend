# Importar os modelos aqui para que o Alembic os detecte
from app.db.base import Base  # noqa
from app.models.user import User  # noqa
from app.models.patient import Patient  # noqa
from app.models.specialist import Specialist  # noqa
from app.models.schedule import Schedule  # noqa
from app.models.appointment import Appointment  # noqa
