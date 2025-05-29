from hashids import Hashids

hashids = Hashids(min_length=30, salt="mySecretSalt")

def encode_id(customer_id):
    return hashids.encode(customer_id)

def decode_id(encoded_id):
    decoded = hashids.decode(encoded_id)
    if decoded:
        return decoded[0]
    raise ValueError("Invalid encoded ID")
