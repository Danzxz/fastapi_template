import uuid
from decimal import Decimal

import factory
from core.example.dto.check_db import EntityNameBaseSchema


class EntityNameFactory(factory.Factory):
    name = "Name"
    city_id = factory.sequence(lambda _: uuid.uuid4())
    latitude = Decimal("10")
    longitude = Decimal("10")
    subway_line_id = factory.sequence(lambda _: uuid.uuid4())

    class Meta:
        model = EntityNameBaseSchema
