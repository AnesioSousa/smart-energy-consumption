def get_dict_key(d):
    return frozenset(d.items())


my_dict = {"a": 1, "b": 2}
other_dict = {"b": 2, "a": 1}

print(get_dict_key(my_dict))  # Output: frozenset({('a', 1), ('b', 2)})
print(get_dict_key(other_dict))  # Output: frozenset({('a', 1), ('b', 2)})

my_dict2 = {"c": 3}
my_dict3 = {"a": 1, "b": 2, "c": 3}

my_dict_set = get_dict_key(my_dict)
my_dict2_set = get_dict_key(my_dict2)
my_dict3_set = get_dict_key(my_dict3)

d = {}
d[my_dict_set] = "my_dict"
d[my_dict2_set] = "my_dict2"
d[my_dict3_set] = "my_dict3"

print(d)  # Output: {frozenset({('a', 1), ('b', 2)}): 'my_dict', frozenset({('c', 3)}): 'my_dict2', frozenset({('a', 1), ('b', 2), ('c', 3)}): 'my_dict3'}
