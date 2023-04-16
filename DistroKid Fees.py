while True:
    try:
        # prompt the user to enter the current USD to GBP conversion rate
        usd_to_gbp = float(input("Enter the current USD to GBP conversion rate: "))

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
    except:
        print("An error occurred. Please try again.")
    else:
        repeat = input("Do you want to perform another calculation? (y/n) ")
        if repeat.lower() != "y":
            break
