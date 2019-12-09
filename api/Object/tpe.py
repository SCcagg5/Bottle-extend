import stripe
from .sql import sql

stripe.api_key = 'sk_test_0rg4e2dv9iOAxFCDrWMRgVqg'


class tpe:
    def addcard(token, user_id):
        card = {}
        stripe_id = tpe.__getcus(user_id)
        if stripe_id is None:
            res = sql.get("SELECT `email` FROM `user` WHERE `id` = %s", (user_id))
            if len(res) == 0:
                return [False, "invalid user", None]
            email = str(res[0][0])
            customer = stripe.Customer.create(source=token, email=email)
            succes = sql.input("INSERT INTO `userstripes` (`id`, `user_id`, `stripe_id`) VALUES (NULL, %s, %s)", \
            (user_id, customer["id"]))
            if not succes:
                return [False, "data input error", 500]
            card = customer["sources"]["data"][0]
        else:
            card = stripe.Customer.create_source(stripe_id, source=token)
        return [True, {'card': stripe.formatcard(card)}, None]

    def userdetails(user_id):
        card = {}
        stripe_id = tpe.__getcus(user_id)
        cards = stripe.Customer.retrieve(stripe_id)["sources"]["data"]
        return [True, {"cards": tpe.__formatcards(cards)}, None]

    def __getcus(user_id):
        res = sql.get("SELECT `stripe_id` FROM `userstripes` WHERE `user_id` = %s", (user_id))
        if len(res) == 0:
            return None
        return str(res[0][0])

    def __formatcards(cards):
        ret = []
        for i in cards:
            ret.append(tpe.__formatcard(i))
        return ret

    def __formatcard(card):
        card = {
        "brand": card["brand"],
        "country": card["country"],
        "exp_month": card["exp_month"],
        "exp_year": card["exp_year"],
        "last4": card["last4"],
        }
        return card

# # Charge the Customer instead of the card:
# charge = stripe.Charge.create(
#   amount=1000,
#   currency='usd',
#   customer=customer.id,
# )
#
# # YOUR CODE: Save the customer ID and other info in a database for later.
#
# # When it's time to charge the customer again, retrieve the customer ID.
# charge = stripe.Charge.create(
#   amount=1500, # $15.00 this time
#   currency='usd',
#   customer=customer_id, # Previously stored, then retrieved
# )
