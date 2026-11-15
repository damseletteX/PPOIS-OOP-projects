"""Пакет классов грузов системы управления транспортной компанией."""

from .Cargo import Cargo
from .CargoDocument import CargoDocument
from .CargoPackage import CargoPackage
from .DangerousCargo import DangerousCargo
from .FragileCargo import FragileCargo
from .OversizedCargo import OversizedCargo
from .PerishableCargo import PerishableCargo

__all__ = [
    "Cargo",
    "CargoDocument",
    "CargoPackage",
    "DangerousCargo",
    "FragileCargo",
    "OversizedCargo",
    "PerishableCargo",
]
