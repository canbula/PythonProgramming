class WrongTypeAnnotationError(TypeError):
    pass

class TypeGuard:
    def __init__(self, label: str = "TypeGuard"):
        self.label = label

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(f"{self.label}: Type checking\nFunction: {func.__name__}\nType annotations: {func.__annotations__}")
            
            if bad := next(((k, v, kwargs[k]) for k, v in func.__annotations__.items() if k in kwargs and not isinstance(kwargs[k], v)), None):
                raise WrongTypeAnnotationError(f"Argument '{bad[0]}' must be of type {bad[1].__name__}, but got {type(bad[2]).__name__}")
                
            return func(*args, **kwargs)
        return wrapper

@TypeGuard(label="Custom Type Guard")
def add(*, x: int, y: int) -> int:
    return x + y

def main():
    x = 6
    y = "Canbula"
    try:
        result = add(x=x, y=y)
        print(f"Result: {result}")
    except TypeError as e:
        print(f"TypeError: {e}")
    except Exception as e:
        print(f"Error ({e.__class__.__name__}): {e}")

if __name__ == "__main__":
    main()
