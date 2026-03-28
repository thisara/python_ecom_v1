"""
from api.utils._response import Client_Response
from product import ProductOrderItem
from uowProductItem import product_order_reservation
from service import get_product

def create_product_order_item(productOrderItem: ProductOrderItem) -> Client_Response:

    response_message = ""
    source_product = get_product(productOrderItem.code)

    if source_product != None:
        
        response_message = product_order_reservation(source_product, productOrderItem)

    return Client_Response(response_message, {})

"""

"""
        product_code = source_product['code']
        product_name = source_product['name']
        curr_product_version = source_product['version']
        curr_product_stock = source_product['stock']
#version check
        if curr_product_stock > productOrderItem.stock:
            
            with client.start_session() as session:
                
                try:
                    with client.start_session() as session:

                        new_product_version = curr_product_version + 1
                        new_product_stock = curr_product_stock - productOrderItem.stock

                        productData = ProductData(product_code,product_name,new_product_stock,new_product_version)
                        
                        with session.start_transaction():    

                            result1 = update_product(productData, session)

                            is_product_updated = result1.raw_result.get('updatedExisting')
    
                            print(is_product_updated)

                            #if is_product_updated == True:

                            product_order_item_data = ProductOderItemData(productOrderItem.code, productOrderItem.stock, productOrderItem.orderRef, new_product_version)
                        
                            result2 = create_product_item(product_order_item_data, session)

                            print(result2)

                            session.commit_transaction()

                            response_message = global_messages['SUCCESS_SAVE']
                            print("commited")

                            #else:
                             #   print("rollback")
                              #  session.rollback_transaction()

                except Exception as e:
                    print("exception")
                    response_message = global_messages['ERROR_SAVE']
                finally:
                    print("end")
                    session.end_session()

        else:
            response_message = "Low stock !"
"""

    

"""
        with client.start_session() as session:

            if curr_product_stock > productOrderItem.stock:

                try:

                    new_product_version = curr_product_version + 1
                    new_product_stock = curr_product_stock - productOrderItem.stock

                    with session.start_transaction():

                        db = get_db_conn(client)

                        db.product.update_one(
                            { "code": product_code},
                            { "$set":{"stock": new_product_stock, "version": new_product_version}},
                            session=session
                        )

                        product_order_item_data = ProductOderItemData(productOrderItem.code, productOrderItem.stock, productOrderItem.orderRef, new_product_version)
                        
                        result = create_product_item(product_order_item_data, session)

                        print(result)
                        #db.product_order_item.insert_one(product_order_item_data.__dict__, session=session)

                        session.commit_transaction()

                        response_message = global_messages['SUCCESS_SAVE']
                
                except Exception as e:
                    respose_message = global_messages['ERROR_SAVE']
                finally:
                    session.end_session()
                
            else:
                response_message = "Low stock !"
"""
    

