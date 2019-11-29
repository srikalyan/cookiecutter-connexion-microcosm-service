from microcosm.api import binding
from microcosm_postgres.store import Store

from {{ cookiecutter.project_name }}.models.pet import Pet as PetModel


@binding("pet_store")
class PetStore(Store):

    def __init__(self, graph):
        """
        Persistence layer for Pet
        :param graph: microcosm graph instance
        """
        super().__init__(graph, PetModel)

    def find(self, tags, limit, offset, order_by, direction):
        """
        finds pets based on the search criteria

        :param tags: list of tags to be used for searching
        :param limit: Max number of pet instances to return
        :param offset: offset from which the pet instances should be returned
        :param order_by: The property on Pet to be used for sorting the list
        :param direction: Direction of the sort either ASCENDING or DESCENDING
        :return: list of pets
        """
        real_order_by = order_by

        if order_by == "created":
            real_order_by = "created_at"
        elif order_by == "updated":
            real_order_by = "updated_at"

        order_by_property = getattr(self.model_class, real_order_by)

        query = self.session.query(
            self.model_class
        )

        if tags:
            query = query.filter(self.model_class.tag.in_(tags))

        return query.order_by(
            order_by_property if direction == "ASCENDING" else order_by_property.desc()
        ).limit(
            limit
        ).offset(
            offset
        ).all()

    def count(self, tags):
        """
        Counts the number of pets in store matching the criteria
        :param tags: list of tags on which pets needs to be searched
        :return: number of pets in the store matching the criteria
        """
        query = self.session.query(
            self.model_class
        )

        if tags:
            query = query.filter(self.model_class.tag.in_(tags))

        return query.count()
