from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from db_helper import get_order_status , get_next_order_id , insert_order_item,insert_order_tracking, fetch_food_item_id,get_total_order_price
import generic_helper
import re
import sqlite3
app = FastAPI()
inprogress_orders={}


@app.get("/new")
async def func():
    return {"Hello world"}


@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()
    
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_context = payload['queryResult']['outputContexts']
    session_id  = generic_helper.extract_session_id(output_context[0]['name'])
    intent_handler_dict = {
        'order.add - context: ongoing-tracking': add_to_order,
        'order.remove - context: ongoing-tracking': remove_from_order,
        'order.complete - context: ongoing-tracking': complete_order,
        'track.order -context: Ongoing-order': track_order
    }
    
    return intent_handler_dict[intent](parameters,session_id)
       
       
def add_to_order(parameters: dict,session_id:str):
    food_items = parameters["food-item"]
    quantities = [int(q) for q in parameters["number"]]
    
    if(len(food_items)!=len(quantities)):
        fulfillment_text = f"Sorry , I did't understand. Can you please specify food items and quantities correctly"
    else:
        new_food_dict = dict(zip(food_items,quantities))
        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
        else:
            inprogress_orders[session_id]=new_food_dict
        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text =f"So far you have: {order_str}. Do you need anything else?"
    return JSONResponse(content={"fulfillmentText":fulfillment_text})


# def remove_from_order(parameters: dict, session_id: str):
#     if session_id not in inprogress_orders:
#         return JSONResponse(content={
#             "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
#         })
    
#     food_items = parameters["food-item"]
#     quantities = [int(q) for q in parameters["number"]]
#     current_order = inprogress_orders[session_id]

#     removed_items = []
#     no_such_items = []
#     partially_removed = []
#     for idx, item in enumerate(food_items):
#         if item not in current_order:
#             no_such_items.append(item)
#         else:
#             if quantities[idx]!="":
#                 remove_qty = quantities[idx]
#             else:
#                 remove_qty = current_order[item]
#             if remove_qty >= current_order[item]:
#                 removed_items.append(item)
#                 del current_order[item]
#             else:
#                 partially_removed.append((item, remove_qty, current_order[item] - remove_qty))
#                 current_order[item] -= remove_qty

#     if len(removed_items) > 0:
#         fulfillment_text = f'Removed {",".join(removed_items)} from your order!\n'

#     if len(no_such_items) > 0:
#         fulfillment_text += f' Your current order does not have {",".join(no_such_items)}\n'
#     if len(partially_removed)>0:
#         for item, removed_qty, remaining_qty in partially_removed:
#             fulfillment_text += f"Removed {removed_qty} from {item}, {remaining_qty} left.\n"
#     if len(current_order.keys()) == 0:
#         fulfillment_text += " Your order is empty!\n"
#     else:
#         order_str = generic_helper.get_str_from_food_dict(current_order)
#         fulfillment_text += f" Here is what is left in your order: {order_str}\n"

#     return JSONResponse(content={
#         "fulfillmentText": fulfillment_text
#     })
def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having trouble finding your order. Sorry! Can you place a new order, please?"
        })
    
    food_items = parameters.get("food-item", [])  # Default to empty list if not provided
    quantities = parameters["number"]
    current_order = inprogress_orders[session_id]
    removed_items = []
    no_such_items = []
    partially_removed = []
    
    for idx, item in enumerate(food_items):
        if item not in current_order:
            no_such_items.append(item)
            continue

        # Determine the quantity to remove
        remove_qty = int(quantities[idx]) if quantities[idx]!="" else current_order[item]
        print(remove_qty)
        if remove_qty >= current_order[item]:  # Remove completely
            removed_items.append(item)
            del current_order[item]
        else:  # Partial removal
            partially_removed.append((item, remove_qty, current_order[item] - remove_qty))
            current_order[item] -= remove_qty
            print(current_order[item])
    # Construct fulfillment text
    fulfillment_text = ""
    if removed_items:
        fulfillment_text += f"Removed {', '.join(removed_items)} from your order!\n"
    if no_such_items:
        fulfillment_text += f"Your current order does not have {', '.join(no_such_items)}\n"
    if partially_removed:
        for item, removed_qty, remaining_qty in partially_removed:
            fulfillment_text += f"Removed {removed_qty} from {item}, {remaining_qty} left.\n"
    
    if not current_order:
        fulfillment_text += "Your order is empty!\n"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"Here is what is left in your order: {order_str}\n"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})

def complete_order(parameters: dict, session_id: str):
    """Handles order completion by inserting into database and updating tracking."""
    if session_id not in inprogress_orders:
        return JSONResponse(content={"fulfillmentText": "I'm having trouble finding your order. Can you place a new order?"})

    order = inprogress_orders[session_id]
    order_id = get_next_order_id()   # order id for placing order

    for food_item, quantity in order.items():
        food_id = fetch_food_item_id(food_item)
        if food_id:
            # Fetch price of the food item
            conn = sqlite3.connect("Food_chatbot.db")
            cursor = conn.cursor()
            cursor.execute("SELECT price FROM food_items WHERE item_id = ?", (food_id,))
            price = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            total_price = price * quantity
            insert_order_item(order_id, food_id, quantity, total_price)

    total_order_price = get_total_order_price(order_id)
    insert_order_tracking(order_id, "progress")
    print("********************************************")
    print(inprogress_orders) 
    print("********************************************")
    fulfillment_text = f"Your order (ID: {order_id}) is confirmed! The total price is ₹{total_order_price}. We'll notify you when it's ready."
    del inprogress_orders[session_id]
    return JSONResponse(content={"fulfillmentText": fulfillment_text})

def track_order(parameters: dict,session_id:str):
        order_id = int(parameters['number'])
        
        # Fetch order status from SQLite
        order_status = get_order_status(order_id)

        if order_status:
            fulfillment_text = f"The order status for order id {order_id} is {order_status}."
        else:
            fulfillment_text = f"No order found with order id {order_id}."
        
        return JSONResponse(content={"fulfillmentText": fulfillment_text})
