import requests

api_url = "https://openexchangerates.org/api/latest.json"
api_key = "16d276ef8cd644b7b8ad05f84c52945a"

while True:
    try:
        # make an API request for the latest exchange rates
        response = requests.get(f"{api_url}?app_id={api_key}")

        # check if the API request was successful
        if response.status_code == 200:
            # parse the response to get the USD to GBP rate
            usd_to_gbp = response.json()["rates"]["GBP"]
        else:
            raise Exception("API request failed")

    except (requests.RequestException, KeyError, Exception):
        # handle API request failure by asking the user for the conversion rate manually
        usd_to_gbp = float(input("Enter the USD to GBP conversion rate: "))

    try:
        # prompt the user to enter the amount of money they wish to withdraw
        withdrawal_amount = float(input("Enter the amount of money you wish to withdraw: "))

        # calculate the amount of money received from the bank transfer
        bank_fee = 5.00
        bank_amount_usd = withdrawal_amount - bank_fee
        bank_amount_gbp = round(bank_amount_usd * usd_to_gbp, 2)

        # calculate the amount of money received from the PayPal transfer
        paypal_fee = min(withdrawal_amount * 0.02 + 1.00, 21.00)
        paypal_amount_usd = withdrawal_amount - paypal_fee
        paypal_amount_gbp = round(paypal_amount_usd * usd_to_gbp, 2)

        # determine which transfer method to use
        if bank_amount_gbp > paypal_amount_gbp:
            print(f"Use the bank transfer method. You will receive £{bank_amount_gbp}. This is £{round(bank_amount_gbp - paypal_amount_gbp, 2)} GBP more than with PayPal.")
        else:
            print(f"Use the PayPal transfer method. You will receive £{paypal_amount_gbp}. This is £{round(paypal_amount_gbp - bank_amount_gbp, 2)} GBP more than with the bank transfer.")

    except ValueError:
        print("Invalid input. Please try again.")

    repeat = input("Do you want to perform another calculation? (y/n) ")
    if repeat.lower() != "y":
        break
