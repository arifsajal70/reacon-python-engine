def check_if_db_operator_exists(operator):
    """
    Check Search Operator
    :param operator:
    :return:
    """
    ol = ['ne', 'lt', 'lte', 'gt', 'gte', 'in', 'nin', 'all', 'size', 'exists', 'exact', 'iexact', 'contains',
          'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith', 'match']
    if operator in ol:
        return True
    return False
