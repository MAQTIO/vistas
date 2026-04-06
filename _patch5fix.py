#!/usr/bin/env python3
"""Fix: move row.insumosEnlazados from reset to edit, remove duplicate updateProcesoInsumosResumen."""
import sys

with open('mockup.html', 'r', encoding='utf-8') as f:
    content = f.read()

original = len(content)
changes = 0

def do_replace(old, new, desc):
    global content, changes
    n = content.count(old)
    if n == 0:
        print(f"FAIL: {desc} — not found!")
        sys.exit(1)
    if n > 1:
        print(f"WARN: {desc} — found {n} times, replacing first only")
    content = content.replace(old, new, 1)
    changes += 1
    print(f"  [{changes}] {desc}")

# 1. Remove the misplaced row.insumosEnlazados line + duplicate updateProcesoInsumosResumen from reset
do_replace(
    "        procesoInsumosDraft = Array.isArray(row.insumosEnlazados) ? row.insumosEnlazados.map(i => ({insumoId: i.insumoId || '', insumoNombre: i.insumoNombre || i.insumoId || '', insumoCode: i.insumoCode || i.insumoId || '', categoria: i.categoria || ''})) : [];\n        updateRecetaResumen();\n        updateProcesosResumen();\n        updateProcesoInsumosResumen();\n        updateProcesoInsumosResumen();",
    "        updateRecetaResumen();\n        updateProcesosResumen();\n        updateProcesoInsumosResumen();",
    "Remove misplaced row.insumosEnlazados and duplicate resumen from reset"
)

# 2. Add procesoInsumosDraft load + updateProcesoInsumosResumen to the edit function
do_replace(
    "        updateRecetaResumen();\n        updateProcesosResumen();\n        // recetaDraft loaded above",
    "        procesoInsumosDraft = Array.isArray(row.insumosEnlazados) ? row.insumosEnlazados.map(i => ({insumoId: i.insumoId || '', insumoNombre: i.insumoNombre || i.insumoId || '', insumoCode: i.insumoCode || i.insumoId || '', categoria: i.categoria || ''})) : [];\n        updateRecetaResumen();\n        updateProcesosResumen();\n        updateProcesoInsumosResumen();\n        // recetaDraft loaded above",
    "Add procesoInsumosDraft load to edit function"
)

# 3. Fix the access-api-client.js 404 — check if there's a script reference to it
if 'access-api-client.js' in content:
    # Remove the script tag
    import re
    old_tag = re.search(r'<script[^>]*access-api-client\.js[^>]*></script>\n?', content)
    if old_tag:
        content = content.replace(old_tag.group(0), '', 1)
        changes += 1
        print(f"  [{changes}] Removed access-api-client.js script tag")
    else:
        print("  INFO: access-api-client.js referenced but not as a standard script tag")
else:
    print("  INFO: access-api-client.js not found in file (404 may be from external source)")

with open('mockup.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n=== {changes} fixes applied. Size: {original} -> {len(content)} ===")
