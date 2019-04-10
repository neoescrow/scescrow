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
from boa.interop.Neo.Blockchain import GetHeight, GetHeader
from boa.interop.Neo.Runtime import Notify, CheckWitness, Serialize, Deserialize
from boa.interop.Neo.Storage import Get, Put, Delete, GetContext
from boa.interop.Neo.Transaction import GetTXHash, GetOutputs, GetScriptHash, GetReferences
from boa.interop.Neo.Output import GetValue
from boa.interop.System.ExecutionEngine import GetScriptContainer, GetExecutingScriptHash

# Errors
ARG_ERROR = 'Wrong number of arguments'
NOT_SENDER = 'You should input the right sender'
INVALID_OPERATION = 'Invalid operation'
UNEXISTING_ESCROW = 'Invalid escrowId'
WRONG_USER = 'Invalid address'
NOT_EXPIRY = 'Funds are still locked up'

context = GetContext()

def main(op, args):

    if op == 'register_escrow':
        if len(args) == 2:
            return register_escrow(args[0], args[1])
        else:
            Notify(ARG_ERROR)
            return False
    elif op == 'accept_escrow':
        if len(args) == 2:
            return accept_escrow(args[0], args[1])
        else:
            Notify(ARG_ERROR)
            return False
    elif op == 'moderate':
        if len(args) == 3:
            return accept_escrow(args[0], args[1], args[2])
        else:
            Notify(ARG_ERROR)
            return False
    elif op == 'release_escrow':
        if len(args) == 3:
            return accept_escrow(args[0], args[1], args[2])
        else:
            Notify(ARG_ERROR)
            return False
    elif op == 'refund':
        if len(args) == 2:
            return accept_escrow(args[0], args[1])
        else:
            Notify(ARG_ERROR)
            return False
    else:
        Notify(INVALID_OPERATION)
        return False

def register_escrow(sender, seller_addr):
    """
    register_escrow(seller_addr) -> escrow_id
    The buyer send some coins to the contract and receives an unique id for the escrow
    """

    #check if sender is correct
    if not CheckWitness(sender):
        Notify(NOT_SENDER)
        return False

    container = GetScriptContainer()

    #get current block
    c = GetHeight()

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
        'buyer_addr': sender,
        'amount': value,
        'moderator': None,
        'expiry': c + (10950),
    }
    escrow = Serialize(escrow)

    Put(context, tx_hash, escrow)

    return tx_hash



def accept_escrow( sender, escrow_id):
    """
    accept_escrow(escrow_id)
    The moderator accepts the escrow request.
    The timestamp of the last block is saved
    """

    #check if sender is correct
    if not CheckWitness(sender):
        Notify(NOT_SENDER)
        return False

    # Check if the escrow exists
    escrow = Get(context, escrow_id)
    if not escrow:
        Notify(UNEXISTING_ESCROW)
        return False

    escrow = Deserialize(escrow)

    #store new moderator
    escrow.moderator = sender

    escrow = Serialize(escrow)

    Put(context, escrow_id, escrow)

    return True




def moderate(sender, to, escrow_id):
    """
    moderate(escrow_id, to)
    The buyer or the seller did not release the escrow,
    the moderator decides who deserves the coins
    """

    #check if sender is correct
    if not CheckWitness(sender):
        Notify(NOT_SENDER)
        return False

    # Check if the escrow exists
    escrow = Get(context, escrow_id)
    if not escrow:
        Notify(UNEXISTING_ESCROW)
        return False

    escrow = Deserialize(escrow)

    #get current block
    c = GetHeight()
    
    # Check if sender is moderator
    if escrow['moderator'] != sender:
        Notify(WRONG_USER)
        return False

    #check if time-lock is over
    if escrow['expiry'] >= c:
        Notify(NOT_EXPIRY)
        return False

    # Check that moderator can only send funds to either buyer or seller
    if escrow['seller_addr'] != to or escrow['buyer_addr'] != to:
        Notify(WRONG_USER)
        return False

def refund(sender, escrow_id):
    """
    refund(escrow_id)
    Buyer claim a refund, the coins are sent back to him if
    more than one month is passed
    """
    #check if sender is correct
    if not CheckWitness(sender):
        Notify(NOT_SENDER)
        return False

    # Check if the escrow exists
    escrow = Get(context, escrow_id)
    if not escrow:
        Notify(UNEXISTING_ESCROW)
        return False

    escrow = Deserialize(escrow)

    #get current block
    c = GetHeight()
    
    # Check if sender is moderator
    if escrow['buyer_addr'] != sender:
        Notify(WRONG_USER)
        return False

    #check if time-lock is over
    if escrow['expiry'] >= c:
        Notify(NOT_EXPIRY)
        return False

def release_escrow(sender, to,  escrow_id):
    """
    releaseEscrow(escrow_id)
    The buyer invoke this function, the funds are sent to the seller
    """

    #check if sender is correct
    if not CheckWitness(sender):
        Notify(NOT_SENDER)
        return False

    # Check if the escrow exists
    escrow = Get(context, escrow_id)
    if not escrow:
        Notify(UNEXISTING_ESCROW)
        return False

    escrow = Deserialize(escrow)
    
    # Check if sender is buyer
    if escrow['buyer_addr'] != sender:
        Notify(WRONG_USER)
        return False

    # Check if reciever is seller
    if escrow['seller_addr'] != to:
        Notify(WRONG_USER)
        return False
    
