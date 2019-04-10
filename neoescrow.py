'''
# Build & run
sc build_run /smart-contracts/scescrow/neoescrow.py True False True 0710 05 register_escrow ['seller_addr']
sc build_run /smart-contracts/scescrow/neoescrow.py True False True 0710 05 accept_escrow ['seller_addr']
# Build
sc build /smart-contracts/scescrow/neoescrow.py
# Deploy
sc deploy /smart-contracts/scescrow/neoescrow.avm True False True 0710 05
# Invoke

# Convert result to string
In python cli: bytes.fromhex('4675636b796f75')
'''

from boa.interop.Neo.Runtime import Notify, CheckWitness, Serialize, Deserialize
from boa.interop.Neo.Storage import Get, Put, Delete, GetContext
from boa.interop.Neo.Transaction import GetTXHash, GetOutputs
from boa.interop.Neo.Output import GetValue
from boa.interop.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash

# Errors
ARG_ERROR = 'Wrong number of arguments'
INVALID_OPERATION = 'Invalid operation'
UNEXISTING_ESCROW = 'Invalid escrowId'

def main(op, args):
    context = GetContext()

    if op == 'register_escrow':
        if len(args) == 1:
            return register_escrow(context, args[0])
        else:
            Notify(ARG_ERROR)
            return False
    elif op == 'accept_escrow':
        if len(args) == 1:
            return accept_escrow(context, args[0])
        else:
            Notify(ARG_ERROR)
            return False
    else:
        Notify(INVALID_OPERATION)
        return False

def register_escrow(context, seller_addr):
    """
    register_escrow(seller_addr) -> escrow_id
    The buyer send some coins to the contract and receives an unique id for the escrow
    """
    container = GetScriptContainer()

    # Use invocation tx hash as escrow_id
    tx_hash = GetTXHash(container)

    # Calculate the assets value
    outputs = GetOutputs(container)
    value = 0
    for output in outputs:
        v = GetValue(output)
        value += v

    escrow = {
        'seller_addr': seller_addr,
        'amount': value
    }
    escrow = Serialize(escrow)

    Put(context, tx_hash, escrow)

    return tx_hash

def accept_escrow(context, escrow_id):
    """
    accept_escrow(escrow_id)
    The moderator accepts the escrow request.
    The timestamp of the last block is saved
    """
    # Check if the escrow exists
    if not Get(escrow_id):
        Notify(UNEXISTING_ESCROW)
        return False

def moderate(context, escrow_id, to):
    """
    moderate(escrow_id, to)
    The buyer or the seller did not release the escrow,
    the moderator decides who deserves the coins
    """
    Notify('TODO')

def refund(context, escrow_id):
    """
    refund(escrow_id)
    Buyer claim a refund, the coins are sent back to him if
    more than one month is passed
    """
    Notify('TODO')

def release_escrow(context, escrow_id):
    """
    releaseEscrow(escrow_id)
    The buyer invoke this function, the funds are sent to the seller
    """
    Notify('TODO')
