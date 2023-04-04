import requests
import logging
from userApp.constants import UrlConst



def login_api(payload=None):
    try:
        reponse =requests.post(
            url=f"{UrlConst.API_URL.value}/users/login/",
            data=payload
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def register_api(payload=None):
    try:
        reponse =requests.post(
            url=f"{UrlConst.API_URL.value}/users/register/",
            data=payload
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e
    

def fetch_products_api(token=None):
    headers = {
        "Authorization": f"Bearer {token}",
    }
    try:
        reponse =requests.get(
            url=f"{UrlConst.API_URL.value}/product-list-create/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def fetch_all_brands_api(token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.API_URL.value}/brand-list-create/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def fetch_all_reviews_api(user_id, product_id, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.API_URL.value}/reviw-list/{user_id}/{product_id}",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def create_review_api(payload, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.post(
            url=f"{UrlConst.API_URL.value}/reviw-list/",
            data=payload,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e




def fetch_all_category_api(token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.API_URL.value}/category-list-create/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def fetch_filter_product_api(payload, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.post(
            url=f"{UrlConst.API_URL.value}/product-filter/",
            data=payload,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def fetch_product_detail_api(id, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.API_URL.value}/product-detail-delete-update/{id}",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def add_to_cart_api(payload, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.post(
            url=f"{UrlConst.API_URL.value}/add-to-cart-api/",
            data=payload,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def fetch_cart_product_api(id, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.API_URL.value}/add-to-cart-api/{id}",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def fetch_top_products(token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.API_URL.value}/top-products/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def search_products_api(payoad, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.post(
            url=f"{UrlConst.API_URL.value}/seach-products/",
            data=payoad,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def delete_cart_item_api(id=None, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.delete(
            url=f"{UrlConst.API_URL.value}/add-to-cart-api/{id}/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e
    

def create_order_api(payload, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.post(
            url=f"{UrlConst.API_URL.value}/create-order/",
            data=payload,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def delete_cart(id, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.API_URL.value}/delete-cart/{id}/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def list_order_api(id, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.API_URL.value}/create-order/{id}/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e