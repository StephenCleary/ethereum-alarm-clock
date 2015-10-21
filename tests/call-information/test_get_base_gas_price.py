from populus.contracts import get_max_gas
from populus.utils import wait_for_transaction


deploy_contracts = [
    "Alarm",
    "NoArgs",
]


def test_getting_base_gas_used(deploy_client, deployed_contracts):
    alarm = deployed_contracts.Alarm
    client_contract = deployed_contracts.NoArgs

    deposit_amount = get_max_gas(deploy_client) * deploy_client.get_gas_price() * 20
    alarm.deposit.sendTransaction(client_contract._meta.address, value=deposit_amount)

    txn_hash = client_contract.scheduleIt.sendTransaction(alarm._meta.address)
    wait_for_transaction(deploy_client, txn_hash)
    txn = deploy_client.get_transaction_by_hash(txn_hash)

    call_key = alarm.getLastCallKey()
    assert call_key is not None

    assert alarm.getCallBaseGasPrice(call_key) == int(txn['gasPrice'], 16)