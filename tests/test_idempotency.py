from app.services.idempotency_service import generate_request_hash


def test_request_hash_same_data():
    data = {
        "product_id": 5,
        "quantity": 10
    }

    hash1 = generate_request_hash(data)
    hash2 = generate_request_hash(data)

    assert hash1 == hash2
    
def test_request_hash_different_data():
    data1 = {
        "product_id": 5,
        "quantity": 10
    }

    data2 = {
        "product_id": 5,
        "quantity": 20
    }

    hash1 = generate_request_hash(data1)
    hash2 = generate_request_hash(data2)

    assert hash1 != hash2