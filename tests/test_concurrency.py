import threading

from app.database import SessionLocal
from app.services.inventory_service import reserve_inventory


def reserve_stock():
    db = SessionLocal()

    try:
        reserve_inventory(
            db=db,
            product_id=5,
            warehouse_id=2,
            quantity=1,
            order_id=999,
            user_id=1,
        )

        db.commit()
        print("Reservation successful")

    except Exception as e:
        db.rollback()
        print(f"Reservation failed: {e}")

    finally:
        db.close()


def test_concurrent_reservation():
    thread1 = threading.Thread(target=reserve_stock)
    thread2 = threading.Thread(target=reserve_stock)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()