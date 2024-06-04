def parent():
    def nested():
        print("Nested")

    parent.external_nested = nested

    print("Parent")


parent()
parent.external_nested()
