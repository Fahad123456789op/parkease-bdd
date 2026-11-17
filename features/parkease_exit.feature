Feature: Automatic wallet payment at exit gate
  As a registered ParkEase driver, I want my parking fee to be charged automatically
  from my wallet when I exit, so that I can leave the plaza without queuing at a payment booth.

  @smoke
  Scenario: Successful exit payment for a registered electric vehicle
    Given registered driver "fahad" is logged in to the ParkEase app
    And the electric vehicle "EV-2026" is linked to the driver's account
    And the driver's wallet balance is Rs. 1,000
    And the vehicle "EV-2026" entered the parking plaza at "10:00"
    When the vehicle "EV-2026" exits the parking plaza at "13:40" (after 220 minutes)
    Then the app should display "Payment successful – gate opening"
    And the receipt should show a capped parking fee of Rs. 280
    And the receipt should show an EV discount of Rs. 70
    And the receipt should show a service charge of Rs. 20
    And the total amount paid should be Rs. 230
    And the updated wallet balance should be Rs. 770
    And the exit gate should be open

  @smoke @boundary
  Scenario: Registered electric vehicle reaches the daily cap (discount applied after cap)
    Given registered driver "fahad" is logged in to the ParkEase app
    And the electric vehicle "EV-CAP" is linked to the driver's account
    And the driver's wallet balance is Rs. 1,000
    When the vehicle "EV-CAP" exits the parking plaza after 780 minutes
    Then the app should display "Payment successful – gate opening"
    And the receipt should show a capped parking fee of Rs. 800
    And the receipt should show an EV discount of Rs. 200
    And the receipt should show a service charge of Rs. 20
    And the total amount paid should be Rs. 620
    And the updated wallet balance should be Rs. 380
    And the exit gate should be open

  @boundary
  Scenario Outline: Petrol car fee calculation across grace period, hourly rounding, and daily cap
    Given registered driver "fahad" is logged in to the ParkEase app
    And the petrol vehicle "ICT-505" is linked to the driver's account
    And the driver's wallet balance is Rs. 1,000
    When the vehicle "ICT-505" exits the parking plaza after <minutes_parked> minutes
    Then the app should display "Payment successful – gate opening"
    And the receipt should show a capped parking fee of <parking_fee>
    And the receipt should show a service charge of <service_charge>
    And the total amount paid should be <total_payable>
    And the updated wallet balance should be <final_wallet>

    Examples: Free and rounding
      | minutes_parked | parking_fee | service_charge | total_payable | final_wallet |
      | 15             | Rs. 0       | Rs. 0          | Rs. 0         | Rs. 1,000    |
      | 16             | Rs. 100     | Rs. 20         | Rs. 120       | Rs. 880      |
      | 60             | Rs. 100     | Rs. 20         | Rs. 120       | Rs. 880      |
      | 61             | Rs. 160     | Rs. 20         | Rs. 180       | Rs. 820      |

    Examples: Daily cap
      | minutes_parked | parking_fee | service_charge | total_payable | final_wallet |
      | 720            | Rs. 760     | Rs. 20         | Rs. 780       | Rs. 220      |
      | 721            | Rs. 800     | Rs. 20         | Rs. 820       | Rs. 180      |
      | 900            | Rs. 800     | Rs. 20         | Rs. 820       | Rs. 180      |

  @negative
  Scenario: Exit denied when wallet balance is Rs. 1 short of total payable
    Given registered driver "fahad" is logged in to the ParkEase app
    And the petrol vehicle "RWP-786" is linked to the driver's account
    And the driver's wallet balance is Rs. 239
    When the vehicle "RWP-786" exits the parking plaza after 130 minutes
    Then the app should display "Insufficient wallet balance"
    And the total amount paid should be Rs. 0
    And the updated wallet balance should be Rs. 239
    And the exit gate should remain closed