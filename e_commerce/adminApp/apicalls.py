import requests
import logging
from adminApp.constants import UrlConst


def login_api(payload=None):
    try:
        reponse =requests.post(
            url=f"{UrlConst.PRODUCT_LIST.value}/users/login/",
            data=payload
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def register_api(payload=None):
    try:
        reponse =requests.post(
            url=f"{UrlConst.PRODUCT_LIST.value}/users/register/",
            data=payload,
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e
    

def fetch_products_api(token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.PRODUCT_LIST.value}/product-list-create/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def fetch_brand_list_api(token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.PRODUCT_LIST.value}/brand-list-create/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def fetch_order_list_api(token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.PRODUCT_LIST.value}/create-order/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def fetch_category_list_api(token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.PRODUCT_LIST.value}/category-list-create/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def create_brand_api(payload=None, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.post(
            url=f"{UrlConst.PRODUCT_LIST.value}/brand-list-create/",
            data=payload,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def create_category_api(payload=None, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.post(
            url=f"{UrlConst.PRODUCT_LIST.value}/category-list-create/",
            data=payload,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def create_product_api(payload=None, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.post(
            url=f"{UrlConst.PRODUCT_LIST.value}/product-list-create/",
            data=payload,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def update_brand_api(payload=None, id=None, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.put(
            url=f"{UrlConst.PRODUCT_LIST.value}/brand-detail-delete-update/{id}/",
            data=payload,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def update_category_api(payload=None, id=None, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.put(
            url=f"{UrlConst.PRODUCT_LIST.value}/category-detail-delete-update/{id}/",
            data=payload,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def update_product_api(payload=None, id=None, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.put(
            url=f"{UrlConst.PRODUCT_LIST.value}/product-detail-delete-update/{id}/",
            data=payload,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def delete_brand_api(id=None, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.delete(
            url=f"{UrlConst.PRODUCT_LIST.value}/brand-detail-delete-update/{id}/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def delete_category_api(id=None, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.delete(
            url=f"{UrlConst.PRODUCT_LIST.value}/category-detail-delete-update/{id}/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def delete_product_api(id=None, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.delete(
            url=f"{UrlConst.PRODUCT_LIST.value}/product-detail-delete-update/{id}/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def fetch_user_list_api(token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.get(
            url=f"{UrlConst.PRODUCT_LIST.value}/user-list/",
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e


def change_user_status_api(payload=None, token=None):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
        }
        reponse =requests.post(
            url=f"{UrlConst.PRODUCT_LIST.value}/user-list/",
            data=payload,
            headers=headers
        )
        return reponse
    except Exception as e:
        logging.error(f'Error while fetching product list {e}')
        return e
