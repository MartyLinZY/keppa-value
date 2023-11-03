import pandas as pd

# Load the files
guomai_df = pd.read_excel("果麦订单汇总20231102.xlsx")
export_order_df = pd.read_excel("11.1号订单.xlsx")

# For "果麦订单汇总20231101.xls", if the order number is of the form "xxxxxxxxxxx-yyyyyyyyyy",
# extract the number before "-" as the actual order number.
# If there is no "-", use the entire order number.
def extract_order_number(order):
    if '-' in order:
        return order.split('-')[0]
    else:
        return order

guomai_df['实际订单号'] = guomai_df['订单号'].apply(extract_order_number)

# Extract the actual order numbers from the modified guomai dataframe as strings
actual_guomai_orders_str = set(guomai_df['实际订单号'])

# Convert the order numbers in "ExportOrder.xlsx" to string for comparison
export_orders_str = set(export_order_df['订单编号'].astype(str))

# Identify the orders that are in "ExportOrder.xlsx" but not in the modified "果麦订单汇总20231101.xls"
missing_orders = [order for order in export_orders_str if order not in actual_guomai_orders_str]

print(len(missing_orders))
# Print the result
print(missing_orders)
