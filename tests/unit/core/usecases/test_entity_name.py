import pytest


@pytest.mark.anyio
class TestEntityNameUserCase:
    @pytest.fixture(scope="session")
    def data(self):
        return "123"

    async def test_entity_use_case(self, data):
        assert data == "123"
