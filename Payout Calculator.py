import requests

API_URL = "https://openexchangerates.org/api/latest.json"
API_KEY = "16d276ef8cd644b7b8ad05f84c52945a"


def get_exchange_rate():
    try:
        response = requests.get(f"{API_URL}?app_id={API_KEY}")
        if response.status_code == 200:
            return response.json()["rates"]["GBP"]
        raise Exception("API request failed")
    except (requests.RequestException, KeyError, Exception):
        return None


def calculate_bank_transfer_amount(withdrawal_amount, usd_to_gbp, bank_fee):
    bank_amount_usd = withdrawal_amount - bank_fee
    bank_amount_gbp = round(bank_amount_usd * usd_to_gbp, 2)
    return bank_amount_gbp


def calculate_paypal_transfer_amount(withdrawal_amount, usd_to_gbp, paypal_fee):
    paypal_amount_usd = withdrawal_amount - paypal_fee
    paypal_amount_gbp = round(paypal_amount_usd * usd_to_gbp, 2)
    return paypal_amount_gbp


def main():
    while True:
        usd_to_gbp = get_exchange_rate()
        if usd_to_gbp is None:
            usd_to_gbp = float(input("Enter the USD to GBP conversion rate: "))

        try:
            withdrawal_amount = float(input("Enter the amount of money you wish to withdraw: "))

            symphonic_bank_fee = 5.00
            symphonic_paypal_fee = min(withdrawal_amount * 0.02 + 1.10, 21.10)
            symphonic_bank_amount_gbp = calculate_bank_transfer_amount(withdrawal_amount, usd_to_gbp, symphonic_bank_fee)
            symphonic_paypal_amount_gbp = calculate_paypal_transfer_amount(withdrawal_amount, usd_to_gbp, symphonic_paypal_fee)

            if symphonic_bank_amount_gbp > symphonic_paypal_amount_gbp:
                print(f"Use the bank transfer method. You will receive £{symphonic_bank_amount_gbp}. The payout with PayPal would have been £{symphonic_paypal_amount_gbp}.")
            else:
                print(f"Use the PayPal transfer method. You will receive £{symphonic_paypal_amount_gbp}. The payout with the bank transfer would have been £{symphonic_bank_amount_gbp}.")

        except ValueError:
            print("Invalid input. Please try again.")

        repeat = input("Do you want to perform another calculation? (y/n) ")
        if repeat.lower() != "y":
            break


if __name__ == "__main__":
    main()
