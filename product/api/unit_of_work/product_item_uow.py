from api.utils._db_client import get_mongo_client, get_db_conn, DBConnection

from api.models.product import ProductData, ProductOderItemData
from api.dto.product import Product, ProductOrderItem

from api.repository.product_item_repository import repo_create_product_item
from api.repository.product_repository import repo_update_product
from api.utils._message import get_global_messages

def product_order_reservation(product: Product, productOrderItem: ProductOrderItem) -> str:
    
    try:

        db_connection = DBConnection()
        client = db_connection.get_client()
        #client = get_mongo_client()

        product_code = product['code']
        product_name = product['name']
        curr_product_version = product['version']
        curr_product_stock = product['stock']

        global_messages = get_global_messages()

        #if curr_product_version == productOrderItem.version:
        if curr_product_stock > productOrderItem.stock:
            
                with client.start_session() as session:

                    new_product_version = curr_product_version + 1
                    new_product_stock = curr_product_stock - productOrderItem.stock

                    productData = ProductData(product_code,product_name,new_product_stock,new_product_version)
                    
                    with session.start_transaction():    

                        repo_update_product(productData, client, session)

                        product_order_item_data = ProductOderItemData(productOrderItem.code, productOrderItem.stock, productOrderItem.orderRef, new_product_version)
                    
                        repo_create_product_item(product_order_item_data, client, session)
                        #print(c)

                        session.commit_transaction()

                        response_message = global_messages['SUCCESS_SAVE']

        else:
            response_message = "Low stock !"

    except Exception as e:
        print(e)
        response_message = global_messages['ERROR_SAVE']
    finally:
        session.end_session()

    
    return response_message