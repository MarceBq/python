from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

class InsufficientStockError(Exception):
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
 
        super().__init__(
            f"Insufficient stock for '{product.name}'. "
            f"Available: {product.stock}, "
            f"Quantity requested: {self.quantity}"
        )

@dataclass(slots=True)
class Product:
    sku: str
    name: str
    stock: int
    price: float

    def __post_init__(self) -> None:
        if self.stock < 0:
            raise ValueError("stock must be positive")
        if self.price < 0:
            raise ValueError("price cannot be negative")

    def reserve(self, quantity: int) -> None:
        if quantity > self.stock:
            raise InsufficientStockError(self, quantity)
        self.stock = self.stock - quantity
            


class ProductRepository(Protocol):
    def save(self, product: Product) -> None: ...
    def get_by_sku(self, product_sku: str) -> Product | None: ...
    def list_all(self) -> list[Product]: ...
    def list_low_stock(self, threshold: int) -> list[Product]: ...

class InMemoryProductRepository:
    def __init__(self) -> None:
        self._products: dict[str, Product] = {}
    
    """
    Stores a product in the repository.

    Products are stored internally using a dictionary where:
        - the key is the product SKU
        - the value is the Product instance

    Example:

    {
        "AB101": Product(...),
        "AB102": Product(...)
    }

    If a product with the same SKU already exists, it is replaced.
    """
    def save(self, product: Product) -> None:
        # Dictionary Assigment
        self._products[product.sku] = product

    """
    Retrieves a product by its SKU.

    Returns:
        The corresponding Product instance if found,
        otherwise None.
    """
    def get_by_sku(self, product_sku: str) -> Product | None:
        return self._products.get(product_sku)

    """
    Retrieves a product by its SKU.

    Returns:
        The corresponding Product instance if found,
        otherwise None.
    """
    def get_by_sku(self, product_sku: str) -> Product | None:
        return self._products.get(product_sku)

    """
    Returns all stored products.

    The repository keeps products internally as a dictionary,
    but this method exposes them as a list containing only the
    Product instances.

    Example:

    [
        Product(...),
        Product(...),
        Product(...)
    ]
    """
    def list_all(self) -> list[Product]:
        return list(self._products.values())

    
    """
    Returns all products whose stock is less than or equal to
    the specified threshold.

    Args:
        threshold: Maximum stock level to consider.

    Returns:
        A list containing all products with low stock.
    """
    def list_low_stock(self, threshold: int) -> list[Product]:
        # result = []
        
        # for product in self.list_all():
        #     if product.stock <= threshold:
        #         result.append(product)
        
        # return result
        return [
            product
            for product in self.list_all()
            if product.stock <= threshold
        ]

    

if __name__  == "__main__":

    # Product
    p1 = Product("AB101", "Camiseta Universitario", 8, 40.99)
    p2 = Product("AB102", "Comiseta Alianza", 5, 30.99)

    # Reserva exitosa

    try: 
        p1.reserve(2)
        print(p1)
        
        p1.reserve(6)
        print(p1)
        
        p1.reserve(1)
        print(p1)
    except InsufficientStockError as e:
        print(f"Error: {e}")

    product_list = InMemoryProductRepository()
     
    product_list.save(p1)
    product_list.save(p2)

    print(product_list.list_all())

    print("Products list with low stock:", product_list.list_low_stock(2))



