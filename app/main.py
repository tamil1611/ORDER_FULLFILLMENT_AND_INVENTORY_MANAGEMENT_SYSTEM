from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.product import router as product_router
from app.routers.warehouse import router as warehouse_router
from app.routers.inventory import router as inventory_router
from app.routers.order import router as order_router
from app.routers.notification import router as notification_router
from app.routers.dashboard import router as  dashboard_router
from app.routers.audit_log import router as  audit_log_router
from app.routers.return_router import router as return_router

app = FastAPI(
    title="Order Fulfillment & Inventory Management API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(warehouse_router)
app.include_router(inventory_router)
app.include_router(order_router)
app.include_router(notification_router)
app.include_router(dashboard_router)
app.include_router(audit_log_router)
app.include_router(return_router)
@app.get("/")
def root():
    return {
        "message": "Order Fulfillment API is running"
    }