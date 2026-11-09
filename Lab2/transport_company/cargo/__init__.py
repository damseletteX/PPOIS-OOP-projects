"""Пакет классов грузов системы управления транспортной компанией."""

from .Cargo import Cargo
from .CargoPackage import CargoPackage
from .DangerousCargo import DangerousCargo
from .FragileCargo import FragileCargo
from .OversizedCargo import OversizedCargo
from .PerishableCargo import PerishableCargo

__all__ = [
    "Cargo",
    "CargoPackage",
    "DangerousCargo",
    "FragileCargo",
    "OversizedCargo",
    "PerishableCargo"
]