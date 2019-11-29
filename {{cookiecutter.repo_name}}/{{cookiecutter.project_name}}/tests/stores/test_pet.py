"""
Example persistence tests.

Tests cover model-specific constraints under the assumption that framework conventions
handle most boilerplate.

"""
from hamcrest import (
    assert_that,
    equal_to,
    is_,
)
from mock import Mock, patch

from {{ cookiecutter.project_name }}.stores.pet import PetStore


class TestPetStore(object):

    def setup(self):
        self.graph = Mock()
        self.store = PetStore(self.graph)

    @patch("microcosm_postgres.store.SessionContext.session")
    def test_find(self, mock_session):
        tags = ["a", "b"]
        limit = 100
        offset = 200
        order_by = "name"
        direction = "ASCENDING"

        mock_order_by = mock_session.query.return_value.filter.return_value.order_by
        assert_that(self.store.find(tags, limit, offset, order_by, direction), is_(equal_to(
            mock_order_by.return_value.limit.return_value.offset.return_value.all.return_value)))

        mock_session.query.assert_called_once_with(self.store.model_class)
        mock_session.query.return_value.filter.assert_called_once()

        mock_order_by.assert_called_once_with(self.store.model_class.name)

        mock_order_by.return_value.limit.assert_called_once_with(limit)
        mock_order_by.return_value.limit.return_value.offset.assert_called_once_with(offset)
        mock_order_by.return_value.limit.return_value.offset.return_value.all.assert_called_once()

    @patch("microcosm_postgres.store.SessionContext.session")
    def test_find_created(self, mock_session):
        tags = ["a", "b"]
        limit = 100
        offset = 200
        order_by = "created"
        direction = "ASCENDING"

        mock_order_by = mock_session.query.return_value.filter.return_value.order_by
        assert_that(self.store.find(tags, limit, offset, order_by, direction), is_(equal_to(
            mock_order_by.return_value.limit.return_value.offset.return_value.all.return_value)))

        mock_session.query.assert_called_once_with(self.store.model_class)
        mock_session.query.return_value.filter.assert_called_once()

        mock_order_by.assert_called_once_with(self.store.model_class.created_at)

        mock_order_by.return_value.limit.assert_called_once_with(limit)
        mock_order_by.return_value.limit.return_value.offset.assert_called_once_with(offset)
        mock_order_by.return_value.limit.return_value.offset.return_value.all.assert_called_once()

    @patch("microcosm_postgres.store.SessionContext.session")
    def test_find_updated(self, mock_session):
        tags = ["a", "b"]
        limit = 100
        offset = 200
        order_by = "updated"
        direction = "ASCENDING"

        mock_order_by = mock_session.query.return_value.filter.return_value.order_by

        assert_that(self.store.find(tags, limit, offset, order_by, direction), is_(equal_to(
            mock_order_by.return_value.limit.return_value.offset.return_value.all.return_value)))

        mock_session.query.assert_called_once_with(self.store.model_class)
        mock_session.query.return_value.filter.assert_called_once()

        mock_order_by.assert_called_once_with(self.store.model_class.updated_at)

        mock_order_by.return_value.limit.assert_called_once_with(limit)
        mock_order_by.return_value.limit.return_value.offset.assert_called_once_with(offset)
        mock_order_by.return_value.limit.return_value.offset.return_value.all.assert_called_once()

    @patch("microcosm_postgres.store.SessionContext.session")
    def test_count(self, mock_session):
        tags = ["a", "b"]

        mock_count = mock_session.query.return_value.filter.return_value.count
        assert_that(self.store.count(tags), is_(equal_to(mock_count.return_value)))

        mock_session.query.assert_called_once_with(self.store.model_class)
        mock_session.query.return_value.filter.assert_called_once()
        mock_count.assert_called_once()
