from app.db.base import Base

# Import models so Alembic can discover tables via Base.metadata
from . import user  # noqa: F401
from . import profile  # noqa: F401
from . import education  # noqa: F401
from . import experience  # noqa: F401
from . import activity  # noqa: F401
from . import certification  # noqa: F401
from . import document  # noqa: F401
from . import company  # noqa: F401
from . import job_posting  # noqa: F401

metadata = Base.metadata
