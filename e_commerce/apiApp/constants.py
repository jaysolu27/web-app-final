from enum import Enum


class FILTER_KEYWORDS(Enum):
    BRAND_FILTER = 'p_brand__id'
    CATEGORY_FILTER = 'p_category__id'
    PRICE_LESS_THAN_FILTER = "p_price__lte"
    PRICE_GREATER_THAN_FILTER = "p_price__gte"

