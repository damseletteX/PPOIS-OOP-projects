"""Domain-specific exceptions for the transport company."""

class TransportCompanyError(Exception):
    """Base exception for transport company domain errors."""
    pass

class InvalidOrderError(Exception):
    """Raised when an order fails domain validation."""
    pass

class CustomerNotFoundError(Exception):
    """Raised when a customer cannot be found."""
    pass

class VehicleUnavailableError(Exception):
    """Raised when a vehicle cannot be assigned."""
    pass

class DriverUnavailableError(Exception):
    """Raised when a driver is unavailable."""
    pass

class CapacityExceededError(Exception):
    """Raised when cargo exceeds vehicle or storage capacity."""
    pass

class RouteNotFeasibleError(Exception):
    """Raised when a route cannot be operated safely or legally."""
    pass

class DeliveryWindowError(Exception):
    """Raised when a delivery window cannot be met."""
    pass

class PaymentProcessingError(Exception):
    """Raised when payment processing fails."""
    pass

class InvoiceStateError(Exception):
    """Raised when an invoice transition is invalid."""
    pass

class MaintenanceRequiredError(Exception):
    """Raised when a vehicle requires maintenance before use."""
    pass

class PermitExpiredError(Exception):
    """Raised when a required permit is expired."""
    pass

class DangerousGoodsComplianceError(Exception):
    """Raised when dangerous-goods requirements are not met."""
    pass

class TemperatureExcursionError(Exception):
    """Raised when cargo temperature leaves its permitted range."""
    pass

class DuplicateReferenceError(Exception):
    """Raised when a unique business reference already exists."""
    pass

class ResourceConflictError(Exception):
    """Raised when a resource is double-booked."""
    pass

