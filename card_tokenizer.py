import stripe

# Set your secret key (from Stripe Dashboard)
stripe.api_key = 'sk_test_your_secret_key'

# Function to create a Stripe token from raw card details
def tokenize_card(card_number, exp_month, exp_year, cvc):
    try:
        token = stripe.Token.create(
            card={
                "number": card_number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvc,
            }
        )
        return token.id  # Returns the token ID
    except stripe.error.CardError as e:
        print(f"Card tokenization failed: {e}")
        return None

# Function to charge the card $1 using the token
def charge_card(token):
    try:
        charge = stripe.Charge.create(
            amount=100,  # Amount in cents (100 = $1)
            currency='usd',
            source=token,
            description="Charge for card verification",
        )
        return charge
    except stripe.error.StripeError as e:
        print(f"Charging failed: {e}")
        return None

# Function to save successful raw card details in save.txt
def save_successful_card(raw_card):
    with open("save.txt", "a") as f:
        f.write(raw_card + "\n")

# Function to process a single card
def process_card(raw_card):
    card_number, exp_month, exp_year, cvc = raw_card.split('|')

    print(f"Processing card ending in {card_number[-4:]}...")

    # Step 1: Tokenize the card
    token = tokenize_card(card_number, exp_month, exp_year, cvc)

    if token:
        # Step 2: Charge the card $1
        charge = charge_card(token)

        if charge and charge['status'] == 'succeeded':
            print(f"Card ending in {card_number[-4:]} charged successfully!")

            # Step 3: Save the raw card details in save.txt
            save_successful_card(raw_card)
        else:
            print(f"Card ending in {card_number[-4:]} failed to charge.")
    else:
        print(f"Card ending in {card_number[-4:]} tokenization failed.")

# Main function to handle the card charging workflow for multiple cards
def process_multiple_cards(raw_cards):
    for raw_card in raw_cards:
        process_card(raw_card)

# Example list of raw card data in format: cc|mm|yy|cvc
raw_cards = [
    "4242424242424242|12|2024|123",
    "4000056655665556|11|2025|321"
]

# Start processing the cards
process_multiple_cards(raw_cards)