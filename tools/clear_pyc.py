import os, pathlib
p=pathlib.Path(__file__).resolve().parent.parent / '__pycache__'
if p.exists():
    for f in p.glob('*.pyc'):
        try:
            f.unlink()
            print('deleted',f)
        except Exception as e:
            print('failed',f,e)
else:
    print('no __pycache__')
