import os
import pytest


files = [f for f in os.listdir(os.path.dirname(__file__)) if f.startswith("emails")]
for f in files:
    exec("import " + f[:-3] + " as " + f[:-3])


# test the file if it has the Emails class
def test_names():
    for f in files:
        assert "Emails" in dir(eval(f[:-3])), "Emails is not defined in " + f[:-3]


# test the Emails class if it is a subclass of list
def test_subclass():
    for f in files:
        assert issubclass(eval(f[:-3]).Emails, list), (
            "Emails is not a subclass of list in " + f[:-3]
        )


# check if the Emails class is an instance of the list class
def test_instance():
    for f in files:
        assert isinstance(eval(f[:-3]).Emails([]), list), (
            "Emails is not an instance of list in " + f[:-3]
        )


# test the Emails class if it has the validate method
def test_validate():
    for f in files:
        assert "validate" in dir(eval(f[:-3]).Emails), (
            "validate is not defined in " + f[:-3]
        )
        assert callable(eval(f[:-3]).Emails.validate), (
            "validate is not callable in " + f[:-3]
        )


# test the Emails class if it has the __init__ method
def test_init():
    for f in files:
        assert "__init__" in dir(eval(f[:-3]).Emails), (
            "__init__ is not defined in " + f[:-3]
        )
        assert callable(eval(f[:-3]).Emails.__init__), (
            "__init__ is not callable in " + f[:-3]
        )


# test the Emails class if it has the __repr__ method
def test_repr():
    for f in files:
        assert "__repr__" in dir(eval(f[:-3]).Emails), (
            "__repr__ is not defined in " + f[:-3]
        )
        assert callable(eval(f[:-3]).Emails.__repr__), (
            "__repr__ is not callable in " + f[:-3]
        )


# check Emails class can reproduce itself with the __repr__ method
def test_repr_output():
    for f in files:
        assert (
            repr(eval(f[:-3]).Emails(["bora.canbula@cbu.edu.tr", "bora@canbula.com"]))
            == (
                eval(f[:-3]).Emails(["bora.canbula@cbu.edu.tr", "bora@canbula.com"])
            ).__repr__()
        ), (
            "The Emails class does not reproduce itself with the __repr__ method in "
            + f[:-3]
        )


# test the Emails class if it has the __str__ method
def test_str():
    for f in files:
        assert "__str__" in dir(eval(f[:-3]).Emails), (
            "__str__ is not defined in " + f[:-3]
        )
        assert callable(eval(f[:-3]).Emails.__str__), (
            "__str__ is not callable in " + f[:-3]
        )


# check if the validate method allows only strings
def test_validate_strings():
    for f in files:
        with pytest.raises(ValueError) as e:
            eval(f[:-3]).Emails([1, 2, 3])
            assert str(e.type) == "<class 'ValueError'>", (
                "The validate method does not allow only strings in " + f[:-3]
            )


# check if the validate method allows only valid email addresses, and raises ValueError otherwise
def test_validate_emails():
    for f in files:
        with pytest.raises(ValueError) as e:
            eval(f[:-3]).Emails(["bora.canbula@cbu.edu.tr", "canbula.com"])
            assert str(e.type) == "<class 'ValueError'>", (
                "The validate method does not allow only valid email addresses in "
                + f[:-3]
            )
        with pytest.raises(ValueError) as e:
            eval(f[:-3]).Emails(["bora@canbulacom"])
            assert str(e.type) == "<class 'ValueError'>", (
                "The validate method does not allow only valid email addresses in "
                + f[:-3]
            )


# check Emails class does not allow duplicate email addresses, the order is not important
def test_validate_duplicates():
    for f in files:
        assert (
            eval(f[:-3])
            .Emails(
                [
                    "bora.canbula@cbu.edu.tr",
                    "bora@canbula.com",
                    "bora.canbula@cbu.edu.tr",
                ]
            )
            .data.count("bora.canbula@cbu.edu.tr")
            == 1
        ), (
            "The Emails class does not allow duplicate email addresses in " + f[:-3]
        )
