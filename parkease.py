from dataclasses import dataclass
import math


@dataclass
class ExitResult:
    message: str
    parking_fee: int
    ev_discount: int
    service_charge: int
    total_paid: int
    gate_open: bool


class ParkEase:
    DAILY_CAP = 800
    FIRST_HOUR_FEE = 100
    ADDITIONAL_HOUR_FEE = 60
    SERVICE_CHARGE = 20
    GRACE_MINUTES = 15

    def __init__(self):
        self.logged_in_driver = None
        self.vehicles = {}  # plate -> is_electric (bool)
        self.wallet = 0

    def login(self, driver: str) -> None:
        self.logged_in_driver = driver

    def link_vehicle(self, plate: str, electric: bool) -> None:
        self.vehicles[plate] = electric

    def set_wallet(self, rupees: int) -> None:
        self.wallet = rupees

    def wallet_balance(self) -> int:
        return self.wallet

    def exit(self, plate: str, minutes_parked: int) -> ExitResult:
        # R1: Only logged-in drivers with linked vehicle can pay by wallet
        if not self.logged_in_driver or plate not in self.vehicles:
            return ExitResult(
                message="Driver not logged in or vehicle not linked",
                parking_fee=0, ev_discount=0, service_charge=0,
                total_paid=0, gate_open=False
            )

        # R2: Exiting within the first 15 minutes (<= 15) is free
        if minutes_parked <= self.GRACE_MINUTES:
            return ExitResult(
                message="Payment successful – gate opening",
                parking_fee=0, ev_discount=0, service_charge=0,
                total_paid=0, gate_open=True
            )

        # R3: First hour Rs. 100, each additional started hour Rs. 60 (rounded up)
        started_hours = math.ceil(minutes_parked / 60.0)
        raw_fee = self.FIRST_HOUR_FEE + max(0, started_hours - 1) * self.ADDITIONAL_HOUR_FEE

        # R4: Cap parking fee at Rs. 800
        capped_fee = min(raw_fee, self.DAILY_CAP)

        # R5: Registered EVs get 25% discount applied AFTER the cap
        is_ev = self.vehicles[plate]
        ev_discount = int(round(capped_fee * 0.25)) if is_ev else 0

        # R6: Fixed service charge of Rs. 20 on every paid visit (not discounted)
        service_charge = self.SERVICE_CHARGE

        # Total payable = (capped parking fee - EV discount) + service charge
        total_payable = (capped_fee - ev_discount) + service_charge

        # R7: Wallet must cover total payable
        if self.wallet < total_payable:
            return ExitResult(
                message="Insufficient wallet balance",
                parking_fee=capped_fee, ev_discount=ev_discount,
                service_charge=service_charge, total_paid=0, gate_open=False
            )

        # R8: Successful deduction and gate opening
        self.wallet -= total_payable
        return ExitResult(
            message="Payment successful – gate opening",
            parking_fee=capped_fee, ev_discount=ev_discount,
            service_charge=service_charge, total_paid=total_payable, gate_open=True
        )
