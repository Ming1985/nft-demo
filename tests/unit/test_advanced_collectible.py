from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from brownie import network, AdvancedCollectible
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    # arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # acting
    advanced_collectible, creation_transaction = deploy_and_create()
    # get an event from a transaction
    # format: tx.events[eventname][eventvariable]
    requestId = creation_transaction.events["requestedCollectible"]["requestId"]
    random_number = 777
    # vrf coordinator call back function
    # requestId, randomness number, and consumer contract address
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible, {"from": get_account()}
    )
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
