from infrastructure.database.postgres.database import (
    engine
)

from infrastructure.database.postgres.base import (
    Base
)

from models.candidate_profile_model import (
    CandidateProfile
)

from models.user_model import (
    User
)


Base.metadata.create_all(
    bind=engine
)


print(
    "Tables created successfully."
)