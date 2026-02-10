import importlib,sys,traceback,pathlib

# Ensure project root is on sys.path so imports find top-level modules
root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

p = root
modules = []
for f in p.glob('*.py'):
    if f.name == '__init__.py' or f.parent.name == 'tools' or f.stem.startswith('test_'):
        continue
    modules.append(f.stem)

# Skip very heavy modules that run on import or require live exchange SDKs
SKIP_ON_IMPORT = {"pt_trainer", "pt_trader", "pt_thinker", "pt_backtester"}
modules = [m for m in modules if m not in SKIP_ON_IMPORT]

ok=[]
err=[]
print('Modules to import:', modules)
for name in sorted(modules):
    try:
        importlib.import_module(name)
        ok.append(name)
    except Exception as e:
        err.append((name,traceback.format_exc()))

print('IMPORT_CHECK_OK_COUNT=',len(ok))
print('IMPORT_CHECK_ERR_COUNT=',len(err))
for n in ok:
    print('OK:',n)
for n,exc in err:
    print('ERR:',n)
    print(exc)
