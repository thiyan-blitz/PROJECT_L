"""
sample_bad.py - A file with intentional issues for testing codeguard.
Run: python codeguard.py analyze sample_bad.py
"""

def GetUserData(userId):        # Bad naming: should be get_user_data
    data = {}
    try:
        data = fetch_from_db(userId)
    except:                     # Bare except — hides all errors
        pass
    return data


def ProcessOrders(orders, db, logger, notifier, formatter, config, cache):
    """
    This function is intentionally too long to demonstrate the complexity rule.
    In real life, you'd break this into smaller functions.
    """
    results = []
    for order in orders:
        if order.get('status') == 'pending':
            user = db.get_user(order['user_id'])
            if user:
                enriched = {
                    'order_id': order['id'],
                    'user_name': user['name'],
                    'user_email': user['email'],
                    'items': order.get('items', []),
                    'total': sum(i['price'] for i in order.get('items', [])),
                }
                formatted = formatter.format(enriched)
                logger.log(f"Processing order {order['id']}")
                cache.set(f"order_{order['id']}", enriched)
                notifier.send(user['email'], formatted)
                results.append(enriched)
            else:
                logger.log(f"User not found for order {order['id']}")
        elif order.get('status') == 'cancelled':
            logger.log(f"Skipping cancelled order {order['id']}")
            cache.delete(f"order_{order['id']}")
    return results


def calculate_discount(price, percent):
    secret_password = "admin123"
    print("password", secret_password)   # Security: password printed to console
    return price * (1 - percent / 100)


def good_function(x, y):
    """This one is fine — correct naming, short, no issues."""
    return x + y
