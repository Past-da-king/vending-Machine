"""
Drink models implementing an inheritance hierarchy.
Demonstrates polymorphism and the Open/Closed Principle.
"""
from abc import ABC, abstractmethod


class Drink(ABC):
    """
    Abstract base class for all drinks.
    
    Provides a template for drink products with common attributes
    and enforces implementation of specific methods in subclasses.
    """
    
    def __init__(self, code: str, name: str, price: float):
        """
        Initialize a Drink.
        
        Args:
            code: Unique product code (e.g., "A1")
            name: Display name of the drink
            price: Price in dollars
        """
        if price < 0:
            raise ValueError("Price cannot be negative")
        self._code = code
        self._name = name
        self._price = price
    
    @property
    def code(self) -> str:
        """Get the drink's product code."""
        return self._code
    
    @property
    def name(self) -> str:
        """Get the drink's name."""
        return self._name
    
    @property
    def price(self) -> float:
        """Get the drink's price."""
        return self._price
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Get a description of the drink.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def get_category(self) -> str:
        """
        Get the drink category.
        Must be implemented by subclasses.
        """
        pass
    
    def __str__(self) -> str:
        return f"{self.name} (${self.price:.2f})"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code='{self.code}', name='{self.name}', price={self.price})"


class Soda(Drink):
    """Carbonated soft drink."""
    
    def __init__(self, code: str, name: str, price: float, is_diet: bool = False):
        super().__init__(code, name, price)
        self._is_diet = is_diet
    
    @property
    def is_diet(self) -> bool:
        return self._is_diet
    
    def get_description(self) -> str:
        diet_str = "Diet " if self._is_diet else ""
        return f"{diet_str}Carbonated soft drink"
    
    def get_category(self) -> str:
        return "Soda"


class Juice(Drink):
    """Fruit juice drink."""
    
    def __init__(self, code: str, name: str, price: float, fruit_type: str = "Mixed"):
        super().__init__(code, name, price)
        self._fruit_type = fruit_type
    
    @property
    def fruit_type(self) -> str:
        return self._fruit_type
    
    def get_description(self) -> str:
        return f"Fresh {self._fruit_type} juice"
    
    def get_category(self) -> str:
        return "Juice"


class Water(Drink):
    """Bottled water."""
    
    def __init__(self, code: str, name: str, price: float, is_sparkling: bool = False):
        super().__init__(code, name, price)
        self._is_sparkling = is_sparkling
    
    @property
    def is_sparkling(self) -> bool:
        return self._is_sparkling
    
    def get_description(self) -> str:
        water_type = "Sparkling" if self._is_sparkling else "Still"
        return f"{water_type} mineral water"
    
    def get_category(self) -> str:
        return "Water"
