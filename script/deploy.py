from moccasin.config import get_active_network
from moccasin.boa_tools import VyperContract
from src import buy_me_a_coffee
from script.deploy_mocks import deploy_feed

def deploy_coffee(price_feed: VyperContract) -> VyperContract:
    print(f"using price feed {price_feed.address}")
    coffee: VyperContract = buy_me_a_coffee.deploy(price_feed.address)
    print(f"deployed coffee at : ", coffee.address)
    return coffee

def moccasin_main():
    active_network = get_active_network()
    # [Manifest Named] dives into moccasin.toml to see what appropriate scripts to run and addresses to use.
    # In the case of local networks, it will run deploy_mocks
    price_feed = active_network.manifest_named("price_feed")
    coffee = deploy_coffee(price_feed)
    if active_network.has_explorer() and active_network.is_local_or_is_forked_network() is False:
        print("Verifying contract on explorer...")
        result = active_network.moccasin_verify(coffee)
        result.wait_for_verification()

    print(f"On network {active_network.name}, using price feed at {price_feed.address}")
    return coffee
    