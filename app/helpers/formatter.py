def setting(obj):
    """
    Format Setting Objects
    :param obj:
    :return:
    """
    if obj:
        if obj.type == 'str':
            return str(obj.value)
        elif obj.type == 'bool':
            return bool(obj.value)
        elif obj.type == 'int':
            return int(obj.value)
        elif obj.type == 'float':
            return float(obj.value)
    return None
