#!/usr/bin/env python3
"""Patch 10: 
1. P/R/N/C select-all on focus
2. Thermal printer labels (no colors, minimal, clean)
3. Improve tabulador step-2 layout (photo pane consistent, better space usage)
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
# 1. P/R/N/C select-all on focus — add focus listeners
# ======================================================================
print("\n--- PART 1: Select-all on focus for P/R/N/C ---")

do_replace(
    "    // Ubicación de almacén — auto update code\n    ['prodFormUbiPasillo', 'prodFormUbiRack', 'prodFormUbiNivel', 'prodFormUbiContenedor'].forEach(id => {\n        const el = document.getElementById(id);\n        if (el) el.addEventListener('input', () => updateUbicacionCodigo());\n    });",
    """    // Ubicación de almacén — auto update code + select-all on focus
    ['prodFormUbiPasillo', 'prodFormUbiRack', 'prodFormUbiNivel', 'prodFormUbiContenedor'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', () => updateUbicacionCodigo());
            el.addEventListener('focus', () => { setTimeout(() => el.select(), 0); });
        }
    });""",
    "Add select-all on focus for step-1 P/R/N/C fields"
)

do_replace(
    "    ['confirmUbiPasillo', 'confirmUbiRack', 'confirmUbiNivel', 'confirmUbiContenedor'].forEach(id => {\n        const el = document.getElementById(id);\n        if (el) el.addEventListener('input', () => updateConfirmUbiPreview());\n    });",
    """    ['confirmUbiPasillo', 'confirmUbiRack', 'confirmUbiNivel', 'confirmUbiContenedor'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', () => updateConfirmUbiPreview());
            el.addEventListener('focus', () => { setTimeout(() => el.select(), 0); });
        }
    });""",
    "Add select-all on focus for confirm P/R/N/C fields"
)

# ======================================================================
# 2. Replace _labelCSS + label functions for thermal printer
# ======================================================================
print("\n--- PART 2: Thermal printer labels ---")

# Find and replace the entire _labelCSS, _ubicDescHTML, generarEtiquetaContenedor, generarEtiquetaProducto block
lines = content.split('\n')

# Find _labelCSS start
label_start = -1
for i, l in enumerate(lines):
    if 'function _labelCSS()' in l:
        label_start = i
        break

# Find generarEtiquetaProducto end
label_end = -1
for i, l in enumerate(lines):
    if 'function generarEtiquetaProducto()' in l:
        # Find the closing brace
        brace_count = 0
        for j in range(i, i + 40):
            brace_count += lines[j].count('{') - lines[j].count('}')
            if brace_count == 0 and j > i:
                label_end = j
                break
        break

if label_start == -1 or label_end == -1:
    print(f"FAIL: Could not find label functions block start={label_start} end={label_end}")
    sys.exit(1)

print(f"  Found label block: lines {label_start+1}-{label_end+1}")

new_label_block = r'''    function _labelCSS() {
        return `
@media print { body { margin: 0; padding: 0; } .no-print { display: none !important; } @page { margin: 2mm; } }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, Helvetica, sans-serif; display: flex; flex-direction: column; align-items: center; padding: 4px; background: #fff; }
.label-card { width: 72mm; border: 1px solid #000; padding: 4mm; background: #fff; }
.label-header { text-align: center; border-bottom: 1px solid #000; padding-bottom: 3px; margin-bottom: 4px; }
.label-empresa { font-size: 9px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; }
.label-tipo-tag { font-size: 8px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.5px; border: 1px solid #000; padding: 1px 6px; display: inline-block; margin-top: 2px; }
.label-ubicacion { text-align: center; font-family: 'Courier New', monospace; font-size: 22px; font-weight: 900; letter-spacing: 2px; padding: 4px 0; }
.label-desc-row { display: flex; justify-content: center; gap: 6px; font-size: 7px; margin-bottom: 4px; }
.label-desc-row span { border: 1px solid #999; padding: 1px 4px; border-radius: 2px; }
.label-producto { text-align: center; font-size: 10px; font-weight: 800; padding: 4px 0; border-top: 1px dashed #000; border-bottom: 1px dashed #000; text-transform: uppercase; word-break: break-word; }
.label-codigo { text-align: center; font-family: 'Courier New', monospace; font-size: 12px; letter-spacing: 2px; padding: 3px 0; }
.label-barcode { text-align: center; font-family: 'Libre Barcode 39', 'Courier New', monospace; font-size: 40px; letter-spacing: 3px; }
.label-footer { text-align: center; font-size: 6px; margin-top: 3px; border-top: 1px solid #ccc; padding-top: 2px; }
.btn-print { margin-top: 12px; padding: 8px 24px; font-size: 13px; font-weight: 700; background: #000; color: #fff; border: none; border-radius: 6px; cursor: pointer; }`;
    }

    function _ubicDescHTML(v) {
        let h = '';
        if (v.p) h += '<span>P' + prodEscape(v.p.replace(/^P/i,'')) + '</span>';
        if (v.r) h += '<span>R' + prodEscape(v.r.replace(/^R/i,'')) + '</span>';
        if (v.n) h += '<span>N' + prodEscape(v.n.replace(/^N/i,'')) + '</span>';
        if (v.c) h += '<span>C' + prodEscape(v.c.replace(/^C/i,'')) + '</span>';
        return h;
    }

    function generarEtiquetaContenedor() {
        const v = _getUbiFormValues();
        const ubicacionCode = buildUbiCode(v.p, v.r, v.n, v.c) || 'SIN-UBICACION';
        const fecha = new Date().toLocaleDateString('es-MX');
        const html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>' + prodEscape(ubicacionCode) + '</title><style>' + _labelCSS() + '</style><link href="https://fonts.googleapis.com/css2?family=Libre+Barcode+39&display=swap" rel="stylesheet"></head><body>' +
            '<div class="label-card">' +
            '<div class="label-header"><div class="label-empresa">MAQUILEROS PUBLICIDAD</div><div class="label-tipo-tag">CONTENEDOR</div></div>' +
            '<div class="label-ubicacion">' + prodEscape(ubicacionCode) + '</div>' +
            '<div class="label-desc-row">' + _ubicDescHTML(v) + '</div>' +
            '<div class="label-barcode">*' + prodEscape(ubicacionCode.replace(/-/g,'')) + '*</div>' +
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
            '<div style="font-size:7px;font-weight:800;text-transform:uppercase;">UBICACI\u00d3N</div>' +
            '<div style="font-family:monospace;font-size:14px;font-weight:900;letter-spacing:1px;">' + prodEscape(ubicacionCode) + '</div>' +
            '<div class="label-desc-row" style="margin-top:2px;">' + _ubicDescHTML(v) + '</div>' +
            '</div>' +
            '<div class="label-footer">' + fecha + '</div>' +
            '</div>' +
            '<button class="btn-print no-print" onclick="window.print()">Imprimir</button></body></html>';
        const w = window.open('', '_blank', 'width=380,height=480');
        if (w) { w.document.write(html); w.document.close(); }
    }'''

new_label_lines = new_label_block.split('\n')
lines[label_start:label_end+1] = new_label_lines
content = '\n'.join(lines)
changes += 1
print(f"  [{changes}] Replaced label functions ({label_end - label_start + 1} lines -> {len(new_label_lines)} lines)")

# ======================================================================
# 3. Step-2 tabulador layout improvements
# ======================================================================
print("\n--- PART 3: Step-2 tabulador layout ---")

# Make the tabulador card use the same photo-pane width as step-1 (180px)
# and make the layout stretch vertically to fill the card
do_replace(
    """.prod-tab-step-layout {
            display: grid;
            grid-template-columns: 180px minmax(0, 1fr);
            gap: 10px;
            align-items: stretch;
        }

        .prod-tab-step-main {
            min-width: 0;
            display: grid;
            gap: 10px;
        }""",
    """.prod-tab-step-layout {
            display: grid;
            grid-template-columns: 180px minmax(0, 1fr);
            gap: 8px;
            align-items: stretch;
            flex: 1 1 0;
            min-height: 0;
            overflow: hidden;
        }

        .prod-tab-step-main {
            min-width: 0;
            display: flex;
            flex-direction: column;
            gap: 8px;
            overflow: auto;
        }""",
    "Step-2 layout: flex fill + scroll"
)

# Make the tabulador card flex column stretch properly 
# The popupProdTabulador uses .productos-modal-card.wide which already has flex column
# We need to make the inner content stretch

# Add an ID to the tabulador card for specific CSS targeting
do_replace(
    '<div id="popupProdTabulador" class="productos-modal-overlay" aria-hidden="true">\n    <div class="productos-modal-card wide" role="dialog"',
    '<div id="popupProdTabulador" class="productos-modal-overlay" aria-hidden="true">\n    <div id="prodTabCard" class="productos-modal-card wide" role="dialog"',
    "Add ID to tabulador card"
)

# Add CSS for the tabulador card to properly fill and scroll
do_replace(
    """/* ID selector — máxima especificidad CSS para fijar tamaño */
        #prodFormCard {""",
    """/* ID selectors — máxima especificidad CSS para fijar tamaño */
        #prodTabCard {
            width: min(98vw, 1120px) !important;
            height: min(96vh, 780px) !important;
            height: min(96dvh, 780px) !important;
            min-height: min(96vh, 780px) !important;
            min-height: min(96dvh, 780px) !important;
            max-height: min(96vh, 780px) !important;
            max-height: min(96dvh, 780px) !important;
            overflow: hidden !important;
            box-sizing: border-box !important;
            display: flex !important;
            flex-direction: column !important;
        }

        #prodFormCard {""",
    "Add #prodTabCard CSS for fixed sizing"
)

# Make the photo pane in step-2 not overflow - it should scroll internally
do_replace(
    """.prod-photo-pane {
            background: linear-gradient(160deg, #f07a00 0%, #d76700 100%);
            border-radius: 10px;""",
    """.prod-photo-pane {
            background: linear-gradient(160deg, #f07a00 0%, #d76700 100%);
            border-radius: 10px;
            overflow-y: auto;""",
    "Photo pane: add internal scroll"
)

# Make the tabulador sections fill available space
do_replace(
    """.prod-tabulador-layout {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .prod-tabulador-section {
            border: 1px solid #dbe4f2;
            border-radius: 8px;
            overflow: hidden;
            background: #fff;
        }""",
    """.prod-tabulador-layout {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            flex: 1 1 0;
            min-height: 0;
        }

        .prod-tabulador-section {
            border: 1px solid #dbe4f2;
            border-radius: 8px;
            overflow: auto;
            background: #fff;
            min-height: 0;
        }""",
    "Tabulador sections: scroll + flex fill"
)

# ======================================================================
# WRITE
# ======================================================================
with open('mockup.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n=== DONE: {changes} changes. Size: {original} -> {len(content)} ===")
