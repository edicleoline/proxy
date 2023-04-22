import importlib
import logging

def class_factory(module_class_string, **kwargs):
    """
    :param module_class_string: full name of the class to create an object of
    :param kwargs: parameters to pass
    :return:
    """
    module_name, class_name = module_class_string.rsplit(".", 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    obj = cls(**kwargs)
    return obj