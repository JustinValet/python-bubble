from bubble.api import Api

API_KEY = "14339304d3832596f14b657e2b1072a7"
bubble_object = "Collecte_order"
env = "dev"
website = "optimtri.com"
params = {"api_token": API_KEY}


class_bubble = Api(params, website, env)

res = class_bubble.get(bubble_object="collecte_order")
