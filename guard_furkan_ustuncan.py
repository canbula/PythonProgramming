class WrongTypeAnnotationError(TypeError):
    pass


class TypeGuard:
    def __init__(self, label: str = "TypeGuard"):
        self.label = label

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(f"{self.label}: Type checking")
            print(f"Function: {func.__name__}")
            print(f"Type annotations: {func.__annotations__}")
            for k, v in func.__annotations__.items():
                if k in kwargs:
                    if not isinstance(kwargs[k], v):
                        raise WrongTypeAnnotationError(
                            f"Argument '{k}' must be of type {v.__name__}, "
                            f"but got {type(kwargs[k]).__name__}"
                        )
            result = func(*args, **kwargs)
            return result

        return wrapper


@TypeGuard(label="Custom Type Guard")
def add(*, x: int, y: int) -> int:
    return x + y


def main():
    x = 22
    y = "Furkan"
    try:
        result = add(x=x, y=y)
        print(f"Result: {result}")
    except TypeError as e:
        print(f"TypeError: {e}")
    except Exception as e:
        print(f"Error ({e.__class__.__name__}): {e}")


if __name__ == "__main__":
    main()
