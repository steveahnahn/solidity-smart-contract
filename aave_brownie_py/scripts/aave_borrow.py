from scripts.helpful_scripts import get_account
from brownie import network, config, interface
from scripts import get_weth


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork-dev"]:
        get_weth()
    # ABI
    # ADDRESS
    lending_pool = get_lending_pool()
    print(lending_pool)


def get_lending_pool():
    # ABI
    # ADDRESS
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
