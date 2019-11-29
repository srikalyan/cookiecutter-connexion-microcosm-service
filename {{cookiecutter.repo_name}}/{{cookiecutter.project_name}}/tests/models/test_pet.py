from uuid import uuid4

from hamcrest import assert_that, is_, equal_to, none, not_none, calling, raises
from microcosm_postgres.models import utcnow
from mock import Mock

from {{ cookiecutter.project_name }}.models.pet import Pet


class TestPet(object):
    def setup(self):
        self.graph = Mock()
        self.name = "some_name"
        self.tag = "some_tag"

        self.dict_without_tag = {
            "name": self.name
        }

    def test_to_dict(self):
        model = Pet(id=uuid4(), name=self.name, tag=self.tag, created_at=utcnow(), updated_at=utcnow())

        actual_dict = model.to_dict()

        assert_that(actual_dict["name"], is_(equal_to(model.name)))
        assert_that(actual_dict["id"], is_(equal_to(model.id)))
        assert_that(actual_dict["tag"], is_(equal_to(model.tag)))
        assert_that(actual_dict["created"], is_(equal_to(int(model.created_timestamp))))
        assert_that(actual_dict["updated"], is_(equal_to(int(model.updated_timestamp))))

    def test_from_dict(self):
        dct = {
            "id": uuid4(),
            "name": self.name,
            "tag": self.tag,
        }

        model = Pet.from_dict(dct=dct, create=False)

        assert_that(model.id, is_(dct["id"]))
        assert_that(model.name, is_(equal_to(self.name)))
        assert_that(model.tag, is_(equal_to(self.tag)))

    def test_from_dict_no_tag(self):
        dct = {
            "id": uuid4(),
            "name": self.name,
        }

        model = Pet.from_dict(dct=dct, create=False)

        assert_that(model.id, is_(dct["id"]))
        assert_that(model.name, is_(equal_to(self.name)))
        assert_that(model.tag, is_(none()))

    def test_from_dict_no_id_without_create(self):
        dct = {
            "name": self.name,
            "tag": self.tag,
        }

        assert_that(calling(Pet.from_dict).with_args(dct=dct, create=False), raises(KeyError))

    def test_from_dict_with_create(self):
        dct = {
            "name": self.name,
            "tag": self.tag,
        }

        model = Pet.from_dict(dct=dct, create=True)

        assert_that(model.id, is_(not_none()))
        assert_that(model.name, is_(equal_to(self.name)))
        assert_that(model.tag, is_(equal_to(self.tag)))

    def test_to_list_dict(self):
        items = [Pet(id=uuid4(), name=self.name, tag=self.tag, created_at=utcnow(), updated_at=utcnow()),
                 Pet(id=uuid4(), name=self.name + "1", tag=self.tag, created_at=utcnow(), updated_at=utcnow())]
        limit = 2
        offset = 0
        total_count = 10
        order_by = "name"
        direction = "ASCENDING"

        actual_dict = Pet.to_list_dict(items, total_count, limit, offset, order_by, direction)

        assert_that(actual_dict,
                    is_(equal_to({
                        "items": [item.to_dict() for item in items],
                        "info": {
                            "totalCount": total_count,
                            "limit": limit,
                            "offset": offset,
                            "orderBy": order_by,
                            "direction": direction,
                        }
                    })))
