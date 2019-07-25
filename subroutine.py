def baz():
    print("baz") # <-- PC 
    # return
    
def bar():
    print("Hello")
    baz()
    print("World")
    baz()
    # return
    
def foo():
    print("Hi")
    bar()
    print("there")
    # return
    
print("Main 1")
foo()
print("Main 2")