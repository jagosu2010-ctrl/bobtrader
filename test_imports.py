#!/usr/bin/env python
"""Quick import verification script."""
import sys
import traceback

modules_to_test = [
    'pt_config',
    'pt_exchanges',
    'pt_logging',
    'pt_analytics',
    'pt_notifications',
    'pt_volume',
    'pt_correlation',
    'pt_position_sizing',
    'pt_volume_dashboard',
    'pt_risk_dashboard',
    'pt_panic',
]

print("=" * 60)
print("IMPORT TEST RESULTS")
print("=" * 60)

results = {'ok': [], 'warning': [], 'error': []}

for module_name in modules_to_test:
    try:
        __import__(module_name)
        results['ok'].append(module_name)
        print(f"✓ {module_name}: OK")
    except ImportError as e:
        # Check if this is an optional dependency
        error_msg = str(e)
        if 'pandas' in error_msg or 'numpy' in error_msg or 'alpaca' in error_msg or 'robin_stocks' in error_msg:
            results['warning'].append((module_name, error_msg))
            print(f"⚠ {module_name}: OPTIONAL DEP MISSING - {error_msg}")
        else:
            results['error'].append((module_name, error_msg))
            print(f"✗ {module_name}: FAILED - {error_msg}")
    except Exception as e:
        results['error'].append((module_name, str(e)))
        print(f"✗ {module_name}: ERROR - {str(e)}")
        traceback.print_exc()

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"✓ OK: {len(results['ok'])}")
print(f"⚠ WARNINGS (optional deps): {len(results['warning'])}")
print(f"✗ ERRORS: {len(results['error'])}")

if results['error']:
    print("\nFAILED MODULES:")
    for mod, err in results['error']:
        print(f"  - {mod}: {err}")

sys.exit(0 if not results['error'] else 1)
