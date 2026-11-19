"""Electric Vehicle (EV) Smart Battery Swapping Station & BMS Telematics Engine."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class SmartBatteryPack:
    battery_pack_id: str
    capacity_kwh: float
    state_of_charge_pct: float       # SoC %
    state_of_health_pct: float       # SoH %
    pack_temperature_celsius: float
    status: str = "CHARGING"         # CHARGING, READY_TO_SWAP, IN_VEHICLE, MAINTENANCE

class EVBatterySwappingStationEngine:
    def __init__(self, station_id: str, rate_per_kwh_inr: float = 14.50):
        self.station_id = station_id
        self.rate_per_kwh = rate_per_kwh_inr
        self.inventory: Dict[str, SmartBatteryPack] = {}
        self.swaps: List[Dict[str, Any]] = []

    def register_battery_telemetry(self, pack: SmartBatteryPack) -> Dict[str, Any]:
        # Safety check: Thermal runaway warning (>55C)
        if pack.pack_temperature_celsius > 55.0:
            pack.status = "MAINTENANCE"
            thermal_alarm = True
        elif pack.state_of_charge_pct >= 90.0:
            pack.status = "READY_TO_SWAP"
            thermal_alarm = False
        else:
            pack.status = "CHARGING"
            thermal_alarm = False

        self.inventory[pack.battery_pack_id] = pack
        return {
            "battery_pack_id": pack.battery_pack_id,
            "status": pack.status,
            "thermal_alarm": thermal_alarm
        }

    def execute_battery_swap(self, vehicle_id: str, returned_pack_id: str, driver_wallet_balance_inr: float) -> Dict[str, Any]:
        if returned_pack_id not in self.inventory:
            raise ValueError(f"Returned pack {returned_pack_id} not registered.")
        
        # Find a ready battery
        ready_packs = [p for p in self.inventory.values() if p.status == "READY_TO_SWAP"]
        if not ready_packs:
            raise ValueError("No fully charged battery packs ready for swap at this station.")

        dispensed_pack = ready_packs[0]
        returned_pack = self.inventory[returned_pack_id]

        energy_dispensed_kwh = round(dispensed_pack.capacity_kwh * (dispensed_pack.state_of_charge_pct / 100.0) - 
                                     returned_pack.capacity_kwh * (returned_pack.state_of_charge_pct / 100.0), 2)
        swap_fee = round(max(0.0, energy_dispensed_kwh) * self.rate_per_kwh, 2)

        if driver_wallet_balance_inr < swap_fee:
            raise ValueError(f"Insufficient driver wallet balance ₹{driver_wallet_balance_inr} for swap fee ₹{swap_fee}")

        dispensed_pack.status = "IN_VEHICLE"
        returned_pack.status = "CHARGING"

        swap_record = {
            "swap_id": f"SWP-{self.station_id}-{len(self.swaps) + 1:04d}",
            "vehicle_id": vehicle_id,
            "returned_battery_id": returned_pack_id,
            "dispensed_battery_id": dispensed_pack.battery_pack_id,
            "energy_consumed_kwh": energy_dispensed_kwh,
            "billed_amount_inr": swap_fee,
            "timestamp": datetime.now().isoformat()
        }
        self.swaps.append(swap_record)
        return swap_record
