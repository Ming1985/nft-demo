# utility scripts.
from brownie import (
    accounts,
    network,
    config,
    Contract,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
)

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache-local",
    "mainnet-fork",
    "hardhat",
    "local-ganache",
]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0:"PUG", 1: "SHIBA_INU",2: "ST_BERNARD"}

def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


# get account according to current network
def get_account(index=None, id=None):

    # accounts.add(config)
    # accounts.load("id")
    if index:
        return accounts[index]  # accounts is imported from brownie, test account array
    if id:
        return accounts.load(id)  # accounts.load, load preset id from brownie. see roam
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(
        config["wallets"]["from_key"]
    )  # load from config file, brownie-config.yaml


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """this function will grabe the contract addresses from the brownie config
    if defined, otherwise it will deploy a mock version of that contract, and
    return that mock contract,

        Args:
            contract_name (string)

        returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
            eg. MockV3Aggregator[-1]
    """
    contract_type = contract_to_mock[contract_name]  # 获取
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:  # 是否有已经部署的Mock合约
            deploy_mocks()
        contract = contract_type[-1]  # 获取最新的一个合约
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # Load a contract need abi and address.
        # address is provided in config file.
        # abi and name is provided by contract object. like VRFCoordinator.
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    """use this script if you want to deploy mocks to a testnet"""
    print(f"the active network is {network.show_active()}")
    print("deploying mocks")
    account = get_account()
    print("deploying mock linktoken")
    link_token = LinkToken.deploy({"from": account})
    print("deploying mock vrf coordinator")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRFCoordinator deployed at {vrf_coordinator.address}")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=300000000000000000
):
    account = (
        account if account else get_account()
    )  # if give account use it else load one
    link_token = link_token if link_token else get_contract("link_token")
    # transfer $amount link to contract_address, from account.
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # tx = interface.LinkTokenInterface.transfer(contract_address, amount, {"from": account})

    # another way to use the function, through interface
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from":account})
    tx.wait(1)
    print(f"Fund contract with: {amount / (10 ** 18)} LINK")
    return tx
