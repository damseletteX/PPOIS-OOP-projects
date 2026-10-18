import unittest
from transport_company import TransportOrder, Vehicle, ASSOCIATIONS


class SkeletonTests(unittest.TestCase):
    def test_order_can_be_created(self):
        order = TransportOrder("ORD-1", "2026-10-18", "draft", "normal")
        self.assertEqual(order.order_number, "ORD-1")

    def test_vehicle_can_be_created(self):
        vehicle = Vehicle("AB12 CDE", "Example", "Van", 1000)
        self.assertEqual(vehicle.capacity_kg, 1000)

    def test_associations_catalogue_has_at_least_30_entries(self):
        self.assertGreaterEqual(len(ASSOCIATIONS), 30)


if __name__ == "__main__":
    unittest.main()
