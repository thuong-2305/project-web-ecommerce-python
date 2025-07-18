from store.models import Product


class Wishlist():
    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get('wishlist_session')

        if 'wishlist_session' not in request.session:
            wishlist = self.session['wishlist_session'] = {}

        self.wishlist = wishlist

    def add_wish(self, product, price):
        product_id = str(product.id)
        product_price = str(price)
        msg = ""
        if product_id in self.wishlist:
            msg = "Sản phẩm đã có trong wishlist"
        else:
            self.wishlist[product_id] = str(product_price)
            msg = "Thêm vào wishlist thành công"

        self.session.modified = True
        return msg

    def get_prods(self):
        product_ids = self.wishlist.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_price(self):
        price = self.wishlist
        return price
