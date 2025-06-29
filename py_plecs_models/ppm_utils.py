def add_key_prefix_dict(_dict, prefix):

    new_dict = {}
    for key, val in _dict.items():
        new_dict[f"{prefix}{key}"] = val

    return new_dict
