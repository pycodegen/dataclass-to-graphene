from py_type_extractor.type_extractor.nodes.BaseOption import BaseTempOption


class IsSubscription(BaseTempOption):
    def __hash__(self):
        return hash(IsSubscription)


is_subscription_flag = IsSubscription()
