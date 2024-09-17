import requests

API_URL = "https://openexchangerates.org/api/latest.json"
API_KEY = "16d276ef8cd644b7b8ad05f84c52945a"


def get_exchange_rate():
    try:
        response = requests.get(f"{API_URL}?app_id={API_KEY}")
        response.raise_for_status()
        return response.json()["rates"]["GBP"]
    except (requests.RequestException, KeyError):
        return None


def calculate_transfer_amount(withdrawal_amount, usd_to_gbp, fee):
    amount_usd = withdrawal_amount - fee
    amount_gbp = round(amount_usd * usd_to_gbp, 2)
    return amount_gbp


def main():
    while True:
        usd_to_gbp = get_exchange_rate()
        if usd_to_gbp is None:
            usd_to_gbp = float(input("Enter the USD to GBP conversion rate: "))

        try:
            withdrawal_amount = float(input("Enter the amount of money you wish to withdraw: "))

            bank_fee = 5.00
            paypal_fee = min(withdrawal_amount * 0.02 + 1.10, 21.10)
            bank_amount_gbp = calculate_transfer_amount(withdrawal_amount, usd_to_gbp, bank_fee)
            paypal_amount_gbp = calculate_transfer_amount(withdrawal_amount, usd_to_gbp, paypal_fee)

            if bank_amount_gbp > paypal_amount_gbp:
                print(f"Use the bank transfer method. You will receive £{bank_amount_gbp}. The payout with PayPal would have been £{paypal_amount_gbp}.")
            else:
                print(f"Use the PayPal transfer method. You will receive £{paypal_amount_gbp}. The payout with the bank transfer would have been £{bank_amount_gbp}.")

        except ValueError:
            print("Invalid input. Please try again.")

        repeat = input("Do you want to perform another calculation? (y/n) ")
        if repeat.lower() != "y":
            break


if __name__ == "__main__":
    main()
