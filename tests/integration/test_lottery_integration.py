from asyncio.constants import LOG_THRESHOLD_FOR_CONNLOST_WRITES
from brownie import network
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
)
from scripts.deploy_lottery import deploy_lottery
import time


def test_can_pick_winner1():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    # wait for chainlink node to response on test net
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
