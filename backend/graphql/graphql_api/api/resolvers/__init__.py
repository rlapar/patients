from functools import wraps


def apply_basic_args(model):
    def decorator(f):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            limit = kwargs.pop("limit")
            offset = kwargs.pop("offset")
            order = kwargs.pop("order")

            if not kwargs:
                raise ValueError("Not enough arguments.")

            created_from = kwargs.pop("created_from", None)
            created_to = kwargs.pop("created_to", None)
            updated_from = kwargs.pop("updated_from", None)
            updated_to = kwargs.pop("updated_to", None)

            q = f(*args, **kwargs)

            if order not in ["asc", "desc", "no"]:
                raise ValueError('Invalid "order" value, possible values are ["asc", "desc", "no"].')
            elif order == "asc":
                q = q.order_by(model.created.asc())
            elif order == "desc":
                q = q.order_by(model.created.desc())

            q = q.limit(limit).offset(offset)

            if created_from:
                q = q.filter(model.created >= created_from)

            if created_to:
                q = q.filter(model.created <= created_to)

            if updated_from:
                q = q.filter(model.updated >= updated_from)

            if updated_to:
                q = q.filter(model.updated <= updated_to)

            return q

        return _wrapper

    return decorator
