import contextlib
with contextlib.redirect_stdout(None):
    print("this is not printed")
print("this is printed")
# >>> this is printed
