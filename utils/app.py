from fastapi import Depends, HTTPException, status, FastAPI, Request, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import uuid
import os
from services.jwt_ser import hash_password
from sqlalchemy.future import select
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from config.database import engine, get_db, Base
from models.user_model import User
import schemas.products as product_schema
import services.product_service as product_service
import services.db_auth as db_auth
import schemas.orders as order_schema
import services.order_service as order_service
import schemas.user as user_schema
import schemas.payments as payment_schema
import services.payment_service as payment_service
from services.dependencies import get_current_user, get_current_active_superuser
from services.db_auth import limiter

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# app.add_middleware(HTTPSRedirectMiddleware) # Commented out for local testing without HTTPS

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://final-prj-onxi.onrender.com",
        "https://final-frontend-mu-five.vercel.app/",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Mount uploads directory for static file serving
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
@limiter.limit("5/minute")
async def root(request: Request):
    return {"message": "Hello"}


# Auth routes
@app.post("/auth/register")
async def auth_register(
    user: user_schema.UserCreate, db: AsyncSession = Depends(get_db)
):
    return await db_auth.register(user, db)


@app.post("/auth/login")
async def auth_login(user: user_schema.UserLogin, db: AsyncSession = Depends(get_db)):
    return await db_auth.login(user, db)


@app.post("/auth/refresh")
async def auth_refresh(
    body: user_schema.RefreshTokenRequest, db: AsyncSession = Depends(get_db)
):
    return await db_auth.refresh(body.refresh_token, db)


@app.post("/auth/logout")
async def auth_logout(
    body: user_schema.RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await db_auth.logout(body.refresh_token, db)


# Product routes
@app.get("/product/list", response_model=list[product_schema.ProductResponse])
async def list_products(
    category_id: Optional[int] = Query(None),
    min_price: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
    available: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await product_service.get_products(
        category_id, min_price, max_price, available, db
    )


@app.get("/product/{product_id}", response_model=product_schema.ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy.future import select
    from models.user_model import Product

    stmt = select(Product).filter(Product.id == product_id)
    result = await db.execute(stmt)
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product have been deleted")
    return product


@app.post("/product/create")
async def create_product(
    product: product_schema.ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    return await product_service.create(product, db)


@app.put("/product/update")
async def update_product(
    product: product_schema.ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    return await product_service.update(product, db)


@app.delete("/product/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    return await product_service.delete(product_id, db)


@app.get("/product/all")
async def get_all_products(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    return await product_service.get_all_products(db)


@app.post("/product/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_superuser)
):
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = f"uploads/{filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"image_url": f"/{file_path}"}


@app.get("/init-admin")
async def init_admin(db: AsyncSession = Depends(get_db)):
    stmt = select(User).filter(User.username == "admin")
    result = await db.execute(stmt)
    admin_user = result.scalars().first()
    
    if admin_user:
        return {"message": "Admin user already exists!", "email": "admin@example.com"}
        
    hashed = hash_password("admin123")
    admin_user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hashed,
        is_admin=True,
        is_active=True
    )
    db.add(admin_user)
    await db.commit()
    
    return {
        "message": "Admin user created successfully on Render!",
        "email": "admin@example.com",
        "password": "admin123"
    }

# Order routes
@app.get("/orders/me")
async def get_my_orders(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return await order_service.get_user_orders(current_user.id, db)


@app.get("/order/all")
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    return await order_service.get_all_orders(db)


@app.get("/order/{order_id}")
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await order_service.get_order(order_id, db)


@app.post("/order/place")
async def place_order(
    order: order_schema.PlaceOrderRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await order_service.place_order(order, db)


@app.patch("/order/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: order_schema.OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    return await order_service.update_order_status(order_id, status.status, db)


# Payment routes
@app.post("/payments/confirm")
async def confirm_payment(
    payment: payment_schema.PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await payment_service.process_payment(payment, db)


@app.get("/payments/{payment_id}", response_model=payment_schema.PaymentResponse)
async def get_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await payment_service.get_payment(payment_id, db)


@app.patch("/payments/{payment_id}/status")
async def update_payment_status(
    payment_id: int,
    status: payment_schema.PaymentStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    return await payment_service.update_payment_status(payment_id, status, db)
