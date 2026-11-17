import parse
from behave import given, when, then, register_type
from parkease import ParkEase


# Custom parameter type: converts "Rs. 1,000" or "Rs. 280" into int (1000, 280)
@parse.with_pattern(r"Rs\.\s*[\d,]+")
def parse_rupees(text: str) -> int:
    cleaned = text.replace("Rs.", "").replace(",", "").strip()
    return int(cleaned)


register_type(Rupees=parse_rupees)


@given('registered driver "{driver}" is logged in to the ParkEase app')
def step_driver_logged_in(context, driver):
    context.park_ease = ParkEase()
    context.park_ease.login(driver)


@given('the electric vehicle "{plate}" is linked to the driver\'s account')
def step_link_ev(context, plate):
    context.park_ease.link_vehicle(plate, electric=True)


@given('the petrol vehicle "{plate}" is linked to the driver\'s account')
def step_link_petrol(context, plate):
    context.park_ease.link_vehicle(plate, electric=False)


@given("the driver's wallet balance is {amount:Rupees}")
def step_set_wallet(context, amount):
    context.park_ease.set_wallet(amount)


@given('the vehicle "{plate}" entered the parking plaza at "{entry_time}"')
def step_entry_time(context, plate, entry_time):
    context.entry_time = entry_time


@when('the vehicle "{plate}" exits the parking plaza at "{exit_time}" (after {minutes:d} minutes)')
def step_exit_with_timestamp(context, plate, exit_time, minutes):
    context.result = context.park_ease.exit(plate, minutes)


@when('the vehicle "{plate}" exits the parking plaza after {minutes:d} minutes')
def step_exit_after_minutes(context, plate, minutes):
    context.result = context.park_ease.exit(plate, minutes)


@then('the app should display "{expected_message}"')
def step_verify_message(context, expected_message):
    actual = context.result.message
    assert actual == expected_message, (
        f"Expected message '{expected_message}', but got '{actual}'"
    )


@then("the receipt should show a capped parking fee of {expected_fee:Rupees}")
def step_verify_parking_fee(context, expected_fee):
    actual = context.result.parking_fee
    assert actual == expected_fee, (
        f"Expected capped parking fee Rs. {expected_fee}, but got Rs. {actual}"
    )


@then("the receipt should show an EV discount of {expected_discount:Rupees}")
def step_verify_ev_discount(context, expected_discount):
    actual = context.result.ev_discount
    assert actual == expected_discount, (
        f"Expected EV discount Rs. {expected_discount}, but got Rs. {actual}"
    )


@then("the receipt should show a service charge of {expected_service:Rupees}")
def step_verify_service_charge(context, expected_service):
    actual = context.result.service_charge
    assert actual == expected_service, (
        f"Expected service charge Rs. {expected_service}, but got Rs. {actual}"
    )


@then("the total amount paid should be {expected_total:Rupees}")
def step_verify_total_paid(context, expected_total):
    actual = context.result.total_paid
    assert actual == expected_total, (
        f"Expected total paid Rs. {expected_total}, but got Rs. {actual}"
    )


@then("the updated wallet balance should be {expected_balance:Rupees}")
def step_verify_wallet_balance(context, expected_balance):
    actual = context.park_ease.wallet_balance()
    assert actual == expected_balance, (
        f"Expected wallet balance Rs. {expected_balance}, but got Rs. {actual}"
    )


@then("the exit gate should be open")
def step_verify_gate_open(context):
    assert context.result.gate_open is True, (
        f"Expected exit gate to be open (True), but gate_open was {context.result.gate_open}"
    )


@then("the exit gate should remain closed")
def step_verify_gate_closed(context):
    assert context.result.gate_open is False, (
        f"Expected exit gate to remain closed (False), but gate_open was {context.result.gate_open}"
    )
