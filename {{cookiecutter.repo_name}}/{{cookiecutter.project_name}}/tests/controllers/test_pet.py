from hamcrest import assert_that, is_, equal_to, calling, raises
from mock import Mock, patch
from werkzeug.exceptions import NotFound

from {{ cookiecutter.project_name }}.controllers.pet import PetController


class TestPetController(object):
    def setup(self):
        self.graph = Mock()
        self.controller = PetController(self.graph)

    @patch("{{ cookiecutter.project_name }}.controllers.pet.Pet.to_list_dict")
    def test_find_pets(self, mock_to_list_dict):
        tags = ["a", "b"]
        limit = 10
        offset = 0
        order_by = "created"
        direction = "ASCENDING"
        total_count = 100

        self.controller.store.count.return_value = total_count

        assert_that(self.controller.find_pets(tags, limit, offset, order_by, direction),
                    is_(equal_to((mock_to_list_dict.return_value, 200))))

        mock_to_list_dict.assert_called_once_with(items=self.controller.store.find.return_value,
                                                  total_count=total_count,
                                                  limit=limit,
                                                  offset=offset,
                                                  order_by=order_by,
                                                  direction=direction)

        self.controller.store.find.assert_called_once_with(tags=tags,
                                                           limit=limit,
                                                           offset=offset,
                                                           order_by=order_by,
                                                           direction=direction)

        self.controller.store.count.assert_called_once_with(tags=tags)

    def test_find_pets_with_offset_beyond_total_count(self):
        tags = ["a", "b"]
        limit = 10
        order_by = "created"
        direction = "ASCENDING"
        total_count = 100
        offset = total_count + 1

        self.controller.store.count.return_value = total_count

        assert_that(calling(self.controller.find_pets).with_args(tags, limit, offset, order_by, direction),
                    raises(ValueError))

    @patch("{{ cookiecutter.project_name }}.controllers.pet.Pet.from_dict")
    def test_add_pet(self, mock_from_dict):
        pet = Mock()

        assert_that(self.controller.add_pet(pet),
                    is_(equal_to((self.controller.store.create.return_value.to_dict.return_value, 201))))

        self.controller.store.create.assert_called_once_with(mock_from_dict.return_value)
        self.controller.store.create.return_value.to_dict.assert_called_once_with()

        mock_from_dict.assert_called_once_with(pet, create=True)

    def test_find_pet_by_id(self):
        id_ = "some_id"

        assert_that(self.controller.find_pet_by_id(id_=id_),
                    is_(equal_to((self.controller.store.retrieve.return_value.to_dict.return_value, 200))))

        self.controller.store.retrieve.assert_called_once_with(identifier=id_)
        self.controller.store.retrieve.return_value.to_dict.assert_called_once_with()

    def test_delete_pet(self):
        id_ = "some_id"
        assert_that(self.controller.delete_pet(id_=id_), is_(equal_to((None, 204))))

        self.controller.store.retrieve.assert_called_once_with(identifier=id_)
        self.controller.store.delete.assert_called_once_with(identifier=id_)

    def test_delete_pet_not_existing(self):
        id_ = "some_id"
        self.controller.store.retrieve.return_value = None

        assert_that(calling(self.controller.delete_pet).with_args(id_=id_), raises(NotFound))
        self.controller.store.retrieve.assert_called_once_with(identifier=id_)
