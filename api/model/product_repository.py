"""It contains UserRepository class."""

from .models import Product, Category, User
from .repository import Repository


class ProductRepository(Repository):
    """It Contains specific method related to de product
        model to do operation in the database.
        """

    def __init__(self):
        Repository.__init__(self, Product)

    def get_tree(self):
        return self.session.query(Product).all()

    def get_all_products(self) -> Product:
        return self.session.query(Product).all()

    def is_invalid(self, product: Product) -> list:
        invalid = list()

        return invalid
