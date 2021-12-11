#0.0121
#12100000000000000

from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    #Arrange
    lottery = deploy_lottery()
    #Act
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    #Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_starter():
    #Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    #Act/Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from":get_account(), "value": lottery.getEntranceFee()})