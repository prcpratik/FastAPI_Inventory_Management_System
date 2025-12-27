
from fastapi import FastAPI,Depends
from models import Product
from database import session,engine
import database_models
from  sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

#created objec from fast api 
app = FastAPI()

#for solving cross origin problem
app.add_middleware(
     CORSMiddleware,
     allow_origins = ["http://localhost:3000"],
     allow_methods=["*"]

)


database_models.Base.metadata.create_all(bind=engine)



products = [
    Product(id=1,name="phone",description="budget phone",price=99,quantity=10),
    Product(id=2,name="laptop",description="budget laptop",price=15.5,quantity=100)

    
]

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()



def init_db():
    db = session()

    count=db.query(database_models.Product).count
    
    if count==0:
        for product in products:
            db.add(database_models.Product(**(product.model_dump())))
    
        db.commit()


init_db()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    #db connection
    #db = session()
    #db.query()
    #query
    db_products = db.query(database_models.Product).all()

    return db_products

@app.get("/products/{id}")
def get_product_by_id(id:int,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    
    if db_product:
        
       return db_product
        
    return "product not found"    


@app.post("/products")
def add_product(product:Product,db:Session = Depends(get_db)):
     
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    #products.append(product)
    return product

@app.put("/products/{id}")
def update_product(id:int,product:Product,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    
    if db_product:
        db_product.name=product.name

        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "product added successfully"
    else:
        return "No product found"    

    
@app.delete("/products/{id}")
def delete_product(id : int , db : Session = Depends(get_db)):
    print("@SS in delete route")
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
       db.delete(db_product)
       db.commit()
    else:
        return "product not found"    

