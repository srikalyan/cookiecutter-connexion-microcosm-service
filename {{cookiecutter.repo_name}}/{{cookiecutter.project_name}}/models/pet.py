from uuid import uuid4

from sqlalchemy import Column, String

from microcosm_postgres.models import EntityMixin, Model


class Pet(EntityMixin, Model):
    """
    ORM model for Pet.
    """
    __tablename__ = "pet"

    name = Column(String, nullable=False, unique=True)

    tag = Column(String, nullable=True, unique=False, index=True)

    def to_dict(self):
        """
        Creates the diction version of the model which can be used service response.

        :return: dict
        """
        return {
            "id": self.id,
            "name": self.name,
            "tag": self.tag,
            "created": int(self.created_timestamp),
            "updated": int(self.updated_timestamp),
        }

    @staticmethod
    def from_dict(dct, create=False):
        """
        Generates an instance from the dict

        :param dct: dictionary of the
        :param create: boolean when true, id of the object would be initialized to UUId
        :return: instance of the Pet
        """
        return Pet(
            id=uuid4() if create else dct["id"],
            name=dct["name"],
            tag=dct.get("tag"),
        )

    @staticmethod
    def to_list_dict(items, total_count, limit, offset, order_by, direction):
        """
        Generates a list instance for list of pets

        :param items: list of pets
        :param total_count: total number of instances that exists for the search criteria
        :param limit: number of pet instances requested
        :param offset: offset fr
        :param order_by:
        :param direction:
        :return:
        """
        return {
            "items": [item.to_dict() for item in items],
            "info": {
                "totalCount": total_count,
                "limit": limit,
                "offset": offset,
                "orderBy": order_by,
                "direction": direction,
            }
        }
