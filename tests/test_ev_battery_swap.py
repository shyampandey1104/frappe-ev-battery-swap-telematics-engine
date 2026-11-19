import unittest
from ev_battery_swap.engine import SmartBatteryPack, EVBatterySwappingStationEngine

class TestEVBatterySwappingStationEngine(unittest.TestCase):
    def setUp(self):
        self.station = EVBatterySwappingStationEngine("STATION-DEL-CONNAUGHT-01", rate_per_kwh_inr=15.0)

    def test_battery_swapping_workflow(self):
        # Add ready battery
        p1 = SmartBatteryPack("BAT-3KWH-001", 3.0, 95.0, 98.0, 32.0)
        self.station.register_battery_telemetry(p1)

        # Add drained battery
        p2 = SmartBatteryPack("BAT-3KWH-002", 3.0, 15.0, 95.0, 35.0)
        self.station.register_battery_telemetry(p2)

        swap = self.station.execute_battery_swap("EV-AUTO-DL-12-9901", "BAT-3KWH-002", driver_wallet_balance_inr=200.0)
        self.assertEqual(swap["dispensed_battery_id"], "BAT-3KWH-001")
        self.assertGreater(swap["billed_amount_inr"], 0)

    def test_thermal_safety_hold(self):
        hot_pack = SmartBatteryPack("BAT-HOT-999", 3.0, 92.0, 90.0, 62.0) # > 55 C
        res = self.station.register_battery_telemetry(hot_pack)
        self.assertTrue(res["thermal_alarm"])
        self.assertEqual(res["status"], "MAINTENANCE")

if __name__ == "__main__":
    unittest.main()
