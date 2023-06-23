from typing import Any

from sqlalchemy import MetaData, inspect
from sqlalchemy.ext.declarative import as_declarative, declared_attr

meta = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})


def camelcase_to_snake(val: str) -> str:
    """
    Converts CamelCaseString to stake_case_string
    """

    if not val:
        # nothing to change
        return val

    new_val = [val[0].lower()]
    for v in val[1:]:
        new_val.append(v if not v.isalpha() or v.islower() else f"_{v.lower()}")
    return "".join(new_val)


@as_declarative(metadata=meta)
class BaseModel:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:  # noqa
        return camelcase_to_snake(cls.__name__)

    def serialize(self) -> dict:
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }
