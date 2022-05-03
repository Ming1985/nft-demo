import time
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from brownie import network, AdvancedCollectible
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible_integration():
    # arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip('only for integration testing')
    # acting
    advanced_collectible, creation_transaction = deploy_and_create()
    time.sleep(200)
    # assert
    assert advanced_collectible.tokenCounter() == 1
