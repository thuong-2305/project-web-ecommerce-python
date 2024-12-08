from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exist
        cart = self.session.get('session_key')

        # If the user is new, no session key!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of site
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        msg = ""
        if product_id in self.cart:
            msg = "Sản phẩm đã có trong giả hàng" 
        else:
            self.cart[product_id] = int(product_qty)
            msg = "Thêm vào giỏ hàng thành công" 

        self.session.modified = True
        return msg

    def __len__(self):
        return len(self.cart)
    
    def total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0

        for key, val in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price*val
                    else:
                        total += product.price*val

        # shipping_method = request.POST.get('shipping_method', 'normal')
        #
        # # Thêm phí giao hàng nếu chọn Express
        # if shipping_method == 'express':
        #     total += 500_000
        return total

    
    def get_prods(self):
        #get ids from cart
        product_ids = self.cart.keys()
        #use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity) :
        product_id = str(product)
        product_qty = int(quantity)
        
        ourcart = self.cart

        ourcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
