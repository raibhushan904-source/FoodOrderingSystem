import streamlit as st

MENU = {"Pizza": 8.50, "Burger": 6.00, "Juice": 2.50, "Salad": 5.00, "Pasta": 7.50}

def item_cost(item, quantity):
  if item not in MENU or quantity < 0:
    raise ValueError("Invalid item or quantity")
  return MENU[item] * quantity

def subtotal(order):
  return round(sum(item_cost(item, qty) for item, qty in order.items()), 2)

def discount_amount(amount, code):
  return round(amount * 0.10, 2) if code.strip().upper() == "SAVE10" else 0.0

def delivery_fee(amount, delivery):
  return 0.0 if not delivery or amount >= 25 else 3.50

def order_total(order, code, delivery):
  base = subtotal(order)
  return round(base - discount_amount(base, code) + delivery_fee(base, delivery), 2)

def receipt(order, code, delivery):
  base = subtotal(order)
  return {"Subtotal": base, "Discount": discount_amount(base, code),
          "Delivery": delivery_fee(base, delivery),
          "Total": order_total(order, code, delivery)}

st.title("Online Food Ordering System")
st.write("Choose food, quantities and checkout.")
customer = st.text_input("Customer name")
order = {}
for item, price in MENU.items():
  qty = st.number_input(f"{item} (£{price:.2f})", min_value=0, value=0, step=1)
  if qty:
    order[item] = qty
code = st.text_input("Discount code (try SAVE10)")
delivery = st.checkbox("Delivery required")
if st.button("Place order"):
  if not customer.strip():
    st.error("Enter a customer name")
  elif not order:
    st.error("Choose at least one item")
  else:
    st.success(f"Order confirmed for {customer}!")
    st.table(receipt(order, code, delivery))
    st.write("Items:", order)
