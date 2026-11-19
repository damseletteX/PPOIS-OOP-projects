"""Пакет классов грузов системы управления транспортной компанией."""

from .cargo import Cargo
from .cargo_document import CargoDocument
from .cargo_package import CargoPackage
from .dangerous_cargo import DangerousCargo
from .fragile_cargo import FragileCargo
from .oversized_cargo import OversizedCargo
from .perishable_cargo import PerishableCargo

__all__ = [
    "Cargo",
    "CargoDocument",
    "CargoPackage",
    "DangerousCargo",
    "FragileCargo",
    "OversizedCargo",
    "PerishableCargo",
]
