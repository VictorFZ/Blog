def firstOrDefault(iterable, criteria=None, default=None):
    if iterable:
        for item in iterable:
            if(criteria is None):
                return item
            else:
                attrValue = getattr(item, criteria["key"])
                if(attrValue == criteria["value"]):
                    return item
                
    return default
