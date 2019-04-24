def fib(n):
    versiones = dict(python=2.7, zope=2.13, plone=5.1)


    print versiones
    {'zope': 2.13, 'python': 2.7, 'plone': 5.1}
    versiones_adicional = dict(django=2.1)
    print versiones_adicional
    {'django': 2.1}
    versiones.update(versiones_adicional)
