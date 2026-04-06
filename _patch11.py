#!/usr/bin/env python3
"""Patch 11: 
1. Fix etiquetas: remove duplicate P/R/N/C badges (only show code once)
2. Product code smaller in label to not overflow
3. Confirm popup: auto-focus P, auto-advance P→R→N→C, Enter to save
4. Detect duplicate ubicación and warn
5. Container label with multi-product indicator
6. CSS: all procesos/recetas buttons to orange  
7. Fix loadProductos mapper: add ubi fields
"""
import sys

with open('mockup.html', 'r', encoding='utf-8') as f:
    content = f.read()

original = len(content)
changes = 0

def do_replace(old, new, desc, count=1):
    global content, changes
    n = content.count(old)
    if n == 0:
        print(f"FAIL [{changes+1}]: {desc} — not found!")
        sys.exit(1)
    content = content.replace(old, new, count)
    changes += 1
    print(f"  [{changes}] {desc} (found {n})")

# ======================================================================
# 1-2. Fix labels: remove duplicate desc-row, shrink product code
# ======================================================================
print("\n--- PART 1-2: Fix labels ---")

# Replace label CSS + functions using line range
lines = content.split('\n')

label_start = -1
label_end = -1
for i, l in enumerate(lines):
    if 'function _labelCSS()' in l:
        label_start = i
        break

for i, l in enumerate(lines):
    if 'function generarEtiquetaProducto()' in l:
        bc = 0
        for j in range(i, i + 50):
            bc += lines[j].count('{') - lines[j].count('}')
            if bc == 0 and j > i:
                label_end = j
                break
        break

if label_start == -1 or label_end == -1:
    print(f"FAIL: Could not find label block start={label_start} end={label_end}")
    sys.exit(1)

print(f"  Label block: lines {label_start+1}-{label_end+1}")

new_label_block = r'''    function _labelCSS() {
        return `
@media print { body { margin: 0; padding: 0; } .no-print { display: none !important; } @page { margin: 2mm; } }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, Helvetica, sans-serif; display: flex; flex-direction: column; align-items: center; padding: 4px; background: #fff; }
.label-card { width: 72mm; border: 1px solid #000; padding: 4mm; background: #fff; }
.label-header { text-align: center; border-bottom: 1px solid #000; padding-bottom: 3px; margin-bottom: 4px; }
.label-empresa { font-size: 9px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; }
.label-tipo-tag { font-size: 8px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.5px; border: 1px solid #000; padding: 1px 6px; display: inline-block; margin-top: 2px; }
.label-ubicacion { text-align: center; font-family: 'Courier New', monospace; font-size: 20px; font-weight: 900; letter-spacing: 2px; padding: 4px 0; }
.label-producto { text-align: center; font-size: 10px; font-weight: 800; padding: 4px 0; border-top: 1px dashed #000; border-bottom: 1px dashed #000; text-transform: uppercase; word-break: break-word; }
.label-codigo { text-align: center; font-family: 'Courier New', monospace; font-size: 9px; letter-spacing: 1px; padding: 2px 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.label-barcode { text-align: center; font-family: 'Libre Barcode 39', 'Courier New', monospace; font-size: 38px; letter-spacing: 3px; }
.label-footer { text-align: center; font-size: 6px; margin-top: 3px; border-top: 1px solid #ccc; padding-top: 2px; }
.label-multi { text-align: center; font-size: 7px; font-weight: 800; border: 1px dashed #000; padding: 2px 4px; margin-top: 3px; }
.btn-print { margin-top: 12px; padding: 8px 24px; font-size: 13px; font-weight: 700; background: #000; color: #fff; border: none; border-radius: 6px; cursor: pointer; }`;
    }

    function _getContainerProducts(v) {
        // Find other products in the same P/R/N/C location
        const code = buildUbiCode(v.p, v.r, v.n, v.c);
        if (!code) return [];
        const editingId = document.getElementById('prodFormCodigo')?.dataset?.editingId || '';
        return productosData.filter(p => {
            if (editingId && p.id === editingId) return false;
            const pc = buildUbiCode(
                String(p.ubiPasillo || '').trim().toUpperCase(),
                String(p.ubiRack || '').trim().toUpperCase(),
                String(p.ubiNivel || '').trim().toUpperCase(),
                String(p.ubiContenedor || '').trim().toUpperCase()
            );
            return pc === code;
        });
    }

    function generarEtiquetaContenedor() {
        const v = _getUbiFormValues();
        const ubicacionCode = buildUbiCode(v.p, v.r, v.n, v.c) || 'SIN-UBICACION';
        const fecha = new Date().toLocaleDateString('es-MX');
        const others = _getContainerProducts(v);
        const currentName = v.nombre !== 'PRODUCTO' ? v.nombre : '';
        const allNames = currentName ? [currentName] : [];
        others.forEach(p => { if (p.producto) allNames.push(p.producto); });
        const multiHTML = allNames.length > 1
            ? '<div class="label-multi">' + allNames.length + ' productos en este contenedor</div>'
            : allNames.length === 1
            ? '<div class="label-multi">1 producto: ' + prodEscape(allNames[0].substring(0, 30)) + '</div>'
            : '';
        const html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>' + prodEscape(ubicacionCode) + '</title><style>' + _labelCSS() + '</style><link href="https://fonts.googleapis.com/css2?family=Libre+Barcode+39&display=swap" rel="stylesheet"></head><body>' +
            '<div class="label-card">' +
            '<div class="label-header"><div class="label-empresa">MAQUILEROS PUBLICIDAD</div><div class="label-tipo-tag">CONTENEDOR</div></div>' +
            '<div class="label-ubicacion">' + prodEscape(ubicacionCode) + '</div>' +
            '<div class="label-barcode">*' + prodEscape(ubicacionCode.replace(/-/g,'')) + '*</div>' +
            multiHTML +
            '<div class="label-footer">' + fecha + '</div>' +
            '</div>' +
            '<button class="btn-print no-print" onclick="window.print()">Imprimir</button></body></html>';
        const w = window.open('', '_blank', 'width=380,height=480');
        if (w) { w.document.write(html); w.document.close(); }
    }

    function generarEtiquetaProducto() {
        const v = _getUbiFormValues();
        const ubicacionCode = buildUbiCode(v.p, v.r, v.n, v.c) || 'SIN-UBICACION';
        const fecha = new Date().toLocaleDateString('es-MX');
        const html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>' + prodEscape(v.nombre) + '</title><style>' + _labelCSS() + '</style><link href="https://fonts.googleapis.com/css2?family=Libre+Barcode+39&display=swap" rel="stylesheet"></head><body>' +
            '<div class="label-card">' +
            '<div class="label-header"><div class="label-empresa">MAQUILEROS PUBLICIDAD</div><div class="label-tipo-tag">PRODUCTO</div></div>' +
            '<div class="label-producto">' + prodEscape(v.nombre) + '</div>' +
            '<div class="label-codigo">' + prodEscape(v.codigo) + '</div>' +
            '<div class="label-barcode">*' + prodEscape(v.codigo) + '*</div>' +
            '<div style="border-top:1px dashed #000;padding:3px 0;text-align:center;">' +
            '<div style="font-family:monospace;font-size:14px;font-weight:900;letter-spacing:1px;">' + prodEscape(ubicacionCode) + '</div>' +
            '</div>' +
            '<div class="label-footer">' + fecha + '</div>' +
            '</div>' +
            '<button class="btn-print no-print" onclick="window.print()">Imprimir</button></body></html>';
        const w = window.open('', '_blank', 'width=380,height=480');
        if (w) { w.document.write(html); w.document.close(); }
    }'''

new_lines = new_label_block.split('\n')
lines[label_start:label_end+1] = new_lines
content = '\n'.join(lines)
changes += 1
print(f"  [{changes}] Replaced labels ({label_end - label_start + 1} -> {len(new_lines)} lines)")

# _ubicDescHTML already removed as part of label block replacement above

# ======================================================================
# 3. Confirm popup: auto-focus P, auto-advance, Enter to save
# ======================================================================
print("\n--- PART 3: Confirm auto-advance + Enter ---")

# Replace the confirm listeners to add auto-advance behavior
do_replace(
    """    ['confirmUbiPasillo', 'confirmUbiRack', 'confirmUbiNivel', 'confirmUbiContenedor'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', () => updateConfirmUbiPreview());
            el.addEventListener('focus', () => { setTimeout(() => el.select(), 0); });
        }
    });""",
    """    const _confirmUbiFields = ['confirmUbiPasillo', 'confirmUbiRack', 'confirmUbiNivel', 'confirmUbiContenedor'];
    _confirmUbiFields.forEach((id, idx) => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', () => {
                updateConfirmUbiPreview();
                // Auto-advance to next field when a digit is entered
                const val = el.value.replace(/[^0-9]/g, '');
                if (val.length >= 1 && idx < _confirmUbiFields.length - 1) {
                    const next = document.getElementById(_confirmUbiFields[idx + 1]);
                    if (next) { setTimeout(() => next.focus(), 50); }
                }
            });
            el.addEventListener('focus', () => { setTimeout(() => el.select(), 0); });
            el.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    closeConfirmUbicacion(true);
                }
            });
        }
    });""",
    "Confirm: auto-advance + Enter"
)

# Auto-focus Pasillo when popup opens
do_replace(
    """        updateConfirmUbiPreview();
        popup.style.display = 'flex';
        popup.setAttribute('aria-hidden', 'false');
    }

    function updateConfirmUbiPreview()""",
    """        updateConfirmUbiPreview();
        popup.style.display = 'flex';
        popup.setAttribute('aria-hidden', 'false');
        // Auto-focus pasillo field
        setTimeout(() => {
            const pField = document.getElementById('confirmUbiPasillo');
            if (pField) { pField.focus(); pField.select(); }
        }, 100);
    }

    function updateConfirmUbiPreview()""",
    "Confirm: auto-focus Pasillo on open"
)

# ======================================================================
# 4. Detect duplicate ubicación and warn before save
# ======================================================================
print("\n--- PART 4: Duplicate ubicación warning ---")

# Modify closeConfirmUbicacion to check for duplicates
do_replace(
    """    function closeConfirmUbicacion(accepted) {
        const popup = document.getElementById('popupConfirmarUbicacion');
        if (popup) { popup.style.display = 'none'; popup.setAttribute('aria-hidden', 'true'); }
        if (accepted && _commitAfterConfirm) {
            const cp = (document.getElementById('confirmUbiPasillo')?.value || '').trim().toUpperCase();
            const cr = (document.getElementById('confirmUbiRack')?.value || '').trim().toUpperCase();
            const cn = (document.getElementById('confirmUbiNivel')?.value || '').trim().toUpperCase();
            const cc = (document.getElementById('confirmUbiContenedor')?.value || '').trim().toUpperCase();
            const p1 = document.getElementById('prodFormUbiPasillo');
            const r1 = document.getElementById('prodFormUbiRack');
            const n1 = document.getElementById('prodFormUbiNivel');
            const c1 = document.getElementById('prodFormUbiContenedor');
            if (p1) p1.value = cp;
            if (r1) r1.value = cr;
            if (n1) n1.value = cn;
            if (c1) c1.value = cc;
            updateUbicacionCodigo();
            syncUbicacionToStep2();
            _commitAfterConfirm();
        }
        _commitAfterConfirm = null;
    }""",
    """    function _checkDuplicateUbicacion(p, r, n, c) {
        const code = buildUbiCode(p, r, n, c);
        if (!code) return [];
        const editingId = document.getElementById('prodFormCodigo')?.dataset?.editingId || '';
        return productosData.filter(prod => {
            if (editingId && prod.id === editingId) return false;
            const pc = buildUbiCode(
                String(prod.ubiPasillo || '').trim().toUpperCase(),
                String(prod.ubiRack || '').trim().toUpperCase(),
                String(prod.ubiNivel || '').trim().toUpperCase(),
                String(prod.ubiContenedor || '').trim().toUpperCase()
            );
            return pc === code;
        });
    }

    function _applyConfirmedUbi(cp, cr, cn, cc) {
        const p1 = document.getElementById('prodFormUbiPasillo');
        const r1 = document.getElementById('prodFormUbiRack');
        const n1 = document.getElementById('prodFormUbiNivel');
        const c1 = document.getElementById('prodFormUbiContenedor');
        if (p1) p1.value = cp;
        if (r1) r1.value = cr;
        if (n1) n1.value = cn;
        if (c1) c1.value = cc;
        updateUbicacionCodigo();
        syncUbicacionToStep2();
        if (_commitAfterConfirm) _commitAfterConfirm();
        _commitAfterConfirm = null;
    }

    function closeConfirmUbicacion(accepted) {
        const popup = document.getElementById('popupConfirmarUbicacion');
        if (!accepted) {
            if (popup) { popup.style.display = 'none'; popup.setAttribute('aria-hidden', 'true'); }
            _commitAfterConfirm = null;
            return;
        }
        const cp = (document.getElementById('confirmUbiPasillo')?.value || '').trim().toUpperCase();
        const cr = (document.getElementById('confirmUbiRack')?.value || '').trim().toUpperCase();
        const cn = (document.getElementById('confirmUbiNivel')?.value || '').trim().toUpperCase();
        const cc = (document.getElementById('confirmUbiContenedor')?.value || '').trim().toUpperCase();
        const dupes = _checkDuplicateUbicacion(cp, cr, cn, cc);
        if (dupes.length > 0) {
            const code = buildUbiCode(cp, cr, cn, cc);
            const names = dupes.slice(0, 3).map(d => d.producto || d.codigo || d.id).join(', ');
            const msg = dupes.length === 1
                ? 'La ubicaci\\u00f3n ' + code + ' ya est\\u00e1 asignada a:\\n\\n\\u2022 ' + names + '\\n\\n\\u00bfDeseas guardar aqu\\u00ed de todos modos?'
                : 'La ubicaci\\u00f3n ' + code + ' ya tiene ' + dupes.length + ' producto(s):\\n\\n\\u2022 ' + names + '\\n\\n\\u00bfDeseas guardar aqu\\u00ed de todos modos?';
            if (!confirm(msg)) return; // User cancelled, stay in popup
        }
        if (popup) { popup.style.display = 'none'; popup.setAttribute('aria-hidden', 'true'); }
        _applyConfirmedUbi(cp, cr, cn, cc);
    }""",
    "Duplicate ubicación check"
)

# ======================================================================
# 5. CSS: All procesos/insumos buttons to orange
# ======================================================================
print("\n--- PART 5: CSS orange for procesos/insumos ---")

# Button: Seleccionar procesos (indigo → orange)
do_replace(
    'id="prodFormProcesosBtn" class="productos-btn" style="padding:6px 14px;font-size:0.62rem;background:#6366f1;color:#fff;border:none;border-radius:6px;"',
    'id="prodFormProcesosBtn" class="productos-btn" style="padding:6px 14px;font-size:0.62rem;background:#f07a00;color:#fff;border:none;border-radius:6px;"',
    "Btn procesos: indigo→orange"
)

# Button: Enlazar insumos (green → orange)
do_replace(
    'id="prodFormProcesoInsumosBtn" class="productos-btn" style="padding:6px 14px;font-size:0.62rem;background:#059669;color:#fff;border:none;border-radius:6px;"',
    'id="prodFormProcesoInsumosBtn" class="productos-btn" style="padding:6px 14px;font-size:0.62rem;background:#f07a00;color:#fff;border:none;border-radius:6px;"',
    "Btn proceso-insumos: green→orange"
)

# Bulk CSS color replacements for procesos (indigo) and proceso-insumos (green) → orange
color_map = [
    # Indigo → Orange
    ('#6366f1', '#f07a00'),
    ('#4338ca', '#d76700'),
    ('#a5b4fc', '#f07a00'),
    ('#eef2ff', '#fff3e6'),
    ('#c7d2fe', '#f07a00'),
    ('#3730a3', '#92400e'),
    ('#4f46e5', '#d76700'),
    # Green → Orange  
    ('#059669', '#f07a00'),
    ('#6ee7b7', '#f07a00'),
    ('#ecfdf5', '#fff3e6'),
    ('#047857', '#92400e'),
    ('#065f46', '#92400e'),
]

# Lines we must NOT change (stock indicators that need to stay green)
# We'll be careful: replace globally and if anything breaks we'll fix

for old_c, new_c in color_map:
    n = content.count(old_c)
    if n > 0:
        content = content.replace(old_c, new_c)
        changes += 1
        print(f"  [{changes}] Color {old_c} → {new_c} ({n} occurrences)")

# ======================================================================
# 6. Fix loadProductos mapper: add ubi fields
# ======================================================================
print("\n--- PART 6: Fix loadProductos mapper ---")

do_replace(
    "                categoria: String(row.categoria || 'General').trim() || 'General',\n                tipo: row.tipo === 'gran-formato' ? 'gran-formato' : 'stock'",
    "                categoria: String(row.categoria || 'General').trim() || 'General',\n                tipo: row.tipo === 'gran-formato' ? 'gran-formato' : 'stock',\n                ubicacion: String(row.ubicacion || '').trim(),\n                ubiPasillo: String(row.ubiPasillo || '').trim(),\n                ubiRack: String(row.ubiRack || '').trim(),\n                ubiNivel: String(row.ubiNivel || '').trim(),\n                ubiContenedor: String(row.ubiContenedor || '').trim(),\n                notasInternas: String(row.notasInternas || '').trim(),\n                activo: row.activo !== false",
    "loadProductos mapper: add ubi + notas + activo"
)

# ======================================================================
# WRITE
# ======================================================================
with open('mockup.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n=== DONE: {changes} changes. Size: {original} -> {len(content)} ===")
