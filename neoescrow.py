'''
# Build & run
sc build_run /smart-contracts/neoescrow.py True False True 0710 05 registerEscrow ['sellerAddr']
sc build_run /smart-contracts/neoescrow.py True False True 0710 05 acceptEscrow ['asdasd']
# Build
sc build /smart-contracts/neoescrow.py
# Deploy
sc deploy /smart-contracts/neoescrow.avm True False True 0710 05
# Invoke

# Convert result to string
In python cli: bytes.fromhex('4675636b796f75')
'''

from boa.interop.Neo.Runtime import Notify, CheckWitness, Serialize, Deserialize
from boa.interop.Neo.Storage import Get, Put, Delete, GetContext
from boa.interop.System.ExecutionEngine import GetCallingScriptHash

# Errors
ARG_ERROR = 'Wrong number of arguments'
INVALID_OPERATION = 'Invalid operation'
UNEXISTING_ESCROW = 'Invalid escrowId'

def Main(op, args):
    context = GetContext()

    if op == 'registerEscrow':
        if len(args) == 1:
            return registerEscrow(context, args[0])
        else:
            Notify(ARG_ERROR)
            return False
    elif op == 'acceptEscrow':
        if len(args) == 1:
            return acceptEscrow(context, args[0])
        else:
            Notify(ARG_ERROR)
            return False
    else:
        Notify(INVALID_OPERATION)
        return False

'''
registerEscrow(sellerAddr) -> escrowId
The buyer send some coins to the contract and receives an unique id for the escrow
'''
def registerEscrow(context, sellerAddr):
    # Use invocation tx hash as key and escrowId?
    tx = 'asdasd'
    escrow = {'test': 'testtest'}
    escrow = Serialize(escrow)
    Put(context, tx, escrow)
    return True

'''
acceptEscrow(escrowId)
The moderator accepts the escrow request. The timestamp of the last block is saved
'''
def acceptEscrow(context, escrowId):
    # Check if the escrow exists
    if not Get(escrowId):
        Notify(UNEXISTING_ESCROW)
        return False

'''
moderate(escrowId, to)
The buyer or the seller did not release the escrow,
the moderator decides who deserves the coins
'''
def moderate(context, escrowId, to):
    Notify('TODO')

'''
refund(escrowId)
Buyer claim a refund, the coins are sent back to him if
more than one month is passed or the third person decides this.
A % fee is sent to the moderator
'''
def refund(context, escrowId):
    Notify('TODO')

'''
releaseEscrow(escrowId)
Both buyer and seller can invoke this function, when both have done it,
the funds are sent to the seller
'''
def releaseEscrow(context, escrowId):
    Notify('TODO')
