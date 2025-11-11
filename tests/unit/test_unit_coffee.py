import boa
from eth_utils import to_wei
from eth_utils import from_wei

SEND_VALUE = to_wei(1, "ether")
RANDOM_USER = boa.env.generate_address("non-owner")

def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.price_feed() == eth_usd.address

def test_starting_values(coffee):
    assert coffee.MINIMUM_USD() == to_wei(50, "ether")

def test_starting_owner(coffee, account):
    assert coffee.OWNER() == account.address

def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts("You must spend more ETH!"):
        coffee.fund()

def test_fund_with_money(coffee, account):
    # Arrange
    boa.env.set_balance(account.address, SEND_VALUE * 2 )
    # Act
    coffee.fund(value=SEND_VALUE)
    account_balance = boa.env.get_balance(account.address)
    print(f"the account_balance is : {account_balance}")
    # Assert
    funder = coffee.funders(0)
    amount_that_funder_funded = coffee.address_to_amount_funded(funder)
    assert funder == account.address
    assert amount_that_funder_funded == SEND_VALUE

def test_non_owner_cannot_withdraw(coffee_funded):
    with boa.reverts("Not the contract owner!"):
        with boa.env.prank(RANDOM_USER):
            coffee_funded.withdraw()

def test_owner_can_withdraw_successfully(coffee_funded):
    coffee_owner = coffee_funded.OWNER()
    with boa.env.prank(coffee_owner):
        coffee_funded.withdraw()
    ending_owner_balance = boa.env.get_balance(coffee_owner)
    ending_coffee_balance = boa.env.get_balance(coffee_funded.address)
    assert ending_owner_balance == SEND_VALUE * 2
    assert ending_coffee_balance == 0

def test_adds_funder_to_array_successfully(coffee):
    boa.env.set_balance(RANDOM_USER, SEND_VALUE)
    with boa.env.prank(RANDOM_USER):
        coffee.fund(value=SEND_VALUE)
    funder = coffee.funders(0)
    assert funder == RANDOM_USER

def test_updates_hashMap_successfully_with_funder_amount(coffee_funded):
    coffee_owner_who_already_funded_in_the_fixture = coffee_funded.OWNER()
    amount_funded = coffee_funded.address_to_amount_funded(coffee_owner_who_already_funded_in_the_fixture)
    assert amount_funded == SEND_VALUE

def test_withdraw_from_several_funders(coffee_funded):
    coffee_owner = coffee_funded.OWNER()
    number_of_funders = 10
    for i in range(number_of_funders):
        user = boa.env.generate_address(i)
        boa.env.set_balance(user, SEND_VALUE * 2)
        with boa.env.prank(user):
            coffee_funded.fund(value=SEND_VALUE)
    starting_fund_me_balance = boa.env.get_balance(coffee_funded.address)
    starting_owner_balance = boa.env.get_balance(coffee_owner)

    with boa.env.prank(coffee_owner):
        coffee_funded.withdraw()

    assert boa.env.get_balance(coffee_funded.address) == 0
    assert starting_fund_me_balance + starting_owner_balance == boa.env.get_balance(coffee_owner)

def test_get_rate(coffee):
    # us_dollar_of_one_eth = coffee.get_eth_to_usd_rate(SEND_VALUE) # 1 ETHER is how many us dollars?
    us_dollar_of_one_eth = coffee.get_rate(SEND_VALUE)
    print(f"the amount of dolllars you get for 1 ETH is : {from_wei(us_dollar_of_one_eth, "ether")} dollars")

def test_get_owner_returns_owner(coffee):
    expected_coffee_owner = coffee.OWNER()
    coffee_owner = coffee.get_owner()
    assert expected_coffee_owner == coffee_owner

def test_get_version_gets_price_feed_version(coffee):
    price_feed_version = coffee.get_version()
    print(f"the price feed version is {price_feed_version}")

def test_get_funder_array_returns_funder_successfully(coffee_funded):
    coffee_first_funder = coffee_funded.funders(0)
    coffee_owner = coffee_funded.OWNER()
    assert coffee_first_funder == coffee_owner
