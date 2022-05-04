def extract_dash_strings(val_product_id):
    product_id_spl = val_product_id.split('-')
    product_id = product_id_spl[1] if len(product_id_spl) >= 1 else None

    return product_id