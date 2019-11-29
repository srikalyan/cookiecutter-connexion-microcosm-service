"""
Example controller.

"""
from microcosm.api import binding
from microcosm_logging.decorators import logger
from werkzeug.exceptions import NotFound

from {{ cookiecutter.project_name }}.models.pet import Pet


@binding("pet_controller")
@logger
class PetController(object):

    def __init__(self, graph):
        self.store = graph.pet_store

    def find_pets(self, tags=None, limit=10, offset=0, order_by="created", direction="ASCENDING"):
        total_count = self.store.count(tags=tags)

        if total_count < offset:
            raise ValueError("Offset '{}' is beyond total count '{}'".format(offset, total_count))

        return Pet.to_list_dict(
            items=self.store.find(tags=tags,
                                  limit=limit,
                                  offset=offset,
                                  order_by=order_by,
                                  direction=direction),
            total_count=total_count,
            limit=limit,
            offset=offset,
            order_by=order_by,
            direction=direction,
        ), 200

    def add_pet(self, pet):
        return self.store.create(Pet.from_dict(pet, create=True)).to_dict(), 201

    def find_pet_by_id(self, id_):
        # Note id is known word in python so connexion would add _ to it
        return self.store.retrieve(identifier=id_).to_dict(), 200

    def delete_pet(self, id_):
        # Note id is known word in python so connexion would add _ to it
        existing_pet = self.store.retrieve(identifier=id_)

        if not existing_pet:
            raise NotFound("Pet with id '{id}' not found".format(id=id_))

        self.store.delete(identifier=id_)

        return None, 204
