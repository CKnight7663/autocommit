y_ = (1
+1
+2
+3)

print(y_)

a = lambda x, **kwargs: x + kwargs.get('y')

b = a(3, y=5)
print(b)