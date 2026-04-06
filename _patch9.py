#!/usr/bin/env python3
"""Patch 9: Add Contenedor (4th field P/R/N/C), config settings, two label types.
Uses line-range replacement for JS functions to avoid Unicode escaping issues."""
import sys

with open('mockup.html', 'r', encoding='utf-8') as f:
    content = f.read()

original = len(content)
changes = 0

def do_replace(old, new, desc, count=1):
    global content, changes
    n = content.count(old)
    if n == 0:
        print(f"FAIL [{changes+1}]: {desc} — pattern not found!")
        sys.exit(1)
    if n > 1 and count == 1:
        print(f"WARN [{changes+1}]: {desc} — found {n} matches, replacing first only")
    content = content.replace(old, new, count)
    changes += 1
    print(f"  [{changes}] {desc}")

# ======================================================================
# 1. CSS: Grid 3→4 columns
# ======================================================================
print("\n--- CSS ---")

do_replace(
    "grid-template-columns: 1fr 1fr 1fr;\n            gap: 3px;\n        }",
    "grid-template-columns: 1fr 1fr 1fr 1fr;\n            gap: 3px;\n        }",
    "CSS grid 3→4 columns"
)

# ======================================================================
# 2. Step-1 HTML: Add contenedor + split label buttons
# ======================================================================
print("\n--- Step-1 HTML ---")

do_replace(
    '<label>NIVEL</label>\n                            <input id="prodFormUbiNivel" type="text" maxlength="4" placeholder="N1" style="text-transform:uppercase;">\n                        </div>\n                    </div>\n                    <div id="prodFormUbiCodigoWrap"',
    '<label>NIVEL</label>\n                            <input id="prodFormUbiNivel" type="text" maxlength="4" placeholder="N1" style="text-transform:uppercase;">\n                        </div>\n                        <div class="ubi-cell">\n                            <label>CONT.</label>\n                            <input id="prodFormUbiContenedor" type="text" maxlength="4" placeholder="C1" style="text-transform:uppercase;">\n                        </div>\n                    </div>\n                    <div id="prodFormUbiCodigoWrap"',
    "Step-1: Add contenedor field"
)

do_replace(
    '<button type="button" id="prodFormGenerarEtiquetaBtn" class="btn-generar-etiqueta" disabled>',
    '<div style="display:flex;gap:3px;">\n                        <button type="button" id="prodFormEtiquetaContenedor" class="btn-generar-etiqueta" disabled style="flex:1;font-size:0.48rem;">',
    "Step-1: Start label buttons div"
)

do_replace(
    'Generar etiqueta de ubicaci\u00f3n</button>',
    'Contenedor</button>\n                        <button type="button" id="prodFormEtiquetaProducto" class="btn-generar-etiqueta" disabled style="flex:1;font-size:0.48rem;">Producto</button>\n                    </div>',
    "Step-1: Finish label buttons"
)

# ======================================================================
# 3. Confirmation popup: 3→4 columns + contenedor field
# ======================================================================
print("\n--- Confirmation popup ---")

do_replace(
    "display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;",
    "display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:6px;",
    "Confirm popup: 4 columns"
)

do_replace(
    'input id="confirmUbiNivel" type="text" maxlength="4" style="width:100%;text-align:center;font-size:0.8rem;font-weight:900;border:1px solid #d1d5db;border-radius:4px;padding:4px;text-transform:uppercase;margin-top:2px;">\n                </div>\n            </div>',
    'input id="confirmUbiNivel" type="text" maxlength="4" style="width:100%;text-align:center;font-size:0.72rem;font-weight:900;border:1px solid #d1d5db;border-radius:4px;padding:4px;text-transform:uppercase;margin-top:2px;">\n                </div>\n                <div style="text-align:center;background:#f9fafb;border:1px solid #e5e7eb;border-radius:6px;padding:6px;">\n                    <div style="font-size:0.48rem;font-weight:800;color:#6b7280;text-transform:uppercase;">Contenedor</div>\n                    <input id="confirmUbiContenedor" type="text" maxlength="4" style="width:100%;text-align:center;font-size:0.72rem;font-weight:900;border:1px solid #d1d5db;border-radius:4px;padding:4px;text-transform:uppercase;margin-top:2px;">\n                </div>\n            </div>',
    "Confirm popup: Add contenedor"
)

# Also reduce font-size of Pasillo and Rack inputs in confirm popup
do_replace(
    'input id="confirmUbiPasillo" type="text" maxlength="4" style="width:100%;text-align:center;font-size:0.8rem;',
    'input id="confirmUbiPasillo" type="text" maxlength="4" style="width:100%;text-align:center;font-size:0.72rem;',
    "Confirm popup: Pasillo font size"
)
do_replace(
    'input id="confirmUbiRack" type="text" maxlength="4" style="width:100%;text-align:center;font-size:0.8rem;',
    'input id="confirmUbiRack" type="text" maxlength="4" style="width:100%;text-align:center;font-size:0.72rem;',
    "Confirm popup: Rack font size"
)

# ======================================================================
# 4. Step-2 HTML: Add contenedor
# ======================================================================
print("\n--- Step-2 HTML ---")

do_replace(
    '<input id="prodTabUbiNivel" type="text" maxlength="4" placeholder="N1" style="text-transform:uppercase;" readonly>\n                        </div>\n                    </div>\n                    <hr class="photo-pane-separator">',
    '<input id="prodTabUbiNivel" type="text" maxlength="4" placeholder="N1" style="text-transform:uppercase;" readonly>\n                        </div>\n                        <div class="ubi-cell">\n                            <label>CONT.</label>\n                            <input id="prodTabUbiContenedor" type="text" maxlength="4" placeholder="C1" style="text-transform:uppercase;" readonly>\n                        </div>\n                    </div>\n                    <hr class="photo-pane-separator">',
    "Step-2: Add contenedor field"
)

# ======================================================================
# 5. Config section: Replace almacén tab content
# ======================================================================
print("\n--- Config section ---")

do_replace(
    '<div class="config-tab-panel" id="tabAlmacen" data-tab="almacen">\n                <h3>Configuraci\u00f3n de almac\u00e9n</h3>\n                <div class="popup-panel">\n                    <div class="orden-field">\n                        <label for="configAlmacenUbicacionPorDefecto">Ubicaci\u00f3n por defecto</label>\n                        <select id="configAlmacenUbicacionPorDefecto">\n                            <option value="PISO_1">Piso 1</option>\n                            <option value="PISO_2">Piso 2</option>\n                            <option value="S\u00d3TANO">S\u00f3tano</option>\n                            <option value="MOSTRADOR">Mostrador</option>\n                        </select>\n                    </div>',
    '<div class="config-tab-panel" id="tabAlmacen" data-tab="almacen">\n                <h3>Configuraci\u00f3n de almac\u00e9n y etiquetas</h3>\n                <div class="popup-panel">\n                    <div style="background:#fef3c7;border:1px solid #fbbf24;border-radius:8px;padding:10px;margin-bottom:10px;">\n                        <div style="font-size:0.65rem;font-weight:900;color:#92400e;margin-bottom:6px;">ESTRUCTURA DEL ALMAC\u00c9N</div>\n                        <div style="font-size:0.52rem;color:#78350f;margin-bottom:8px;">Define la capacidad de tu almac\u00e9n. La ubicaci\u00f3n autom\u00e1tica respetar\u00e1 estos l\u00edmites.</div>\n                        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:8px;">\n                            <div class="orden-field" style="margin:0;"><label style="font-size:0.52rem;font-weight:800;color:#92400e;">Pasillos</label><input id="configAlmacenPasillos" type="number" min="1" max="99" step="1" value="5" style="text-align:center;font-weight:700;"></div>\n                            <div class="orden-field" style="margin:0;"><label style="font-size:0.52rem;font-weight:800;color:#92400e;">Racks/pasillo</label><input id="configAlmacenRacks" type="number" min="1" max="99" step="1" value="10" style="text-align:center;font-weight:700;"></div>\n                            <div class="orden-field" style="margin:0;"><label style="font-size:0.52rem;font-weight:800;color:#92400e;">Niveles/rack</label><input id="configAlmacenNiveles" type="number" min="1" max="99" step="1" value="5" style="text-align:center;font-weight:700;"></div>\n                            <div class="orden-field" style="margin:0;"><label style="font-size:0.52rem;font-weight:800;color:#92400e;">Cont./nivel</label><input id="configAlmacenContenedores" type="number" min="1" max="99" step="1" value="4" style="text-align:center;font-weight:700;"></div>\n                        </div>\n                        <div style="margin-top:6px;font-size:0.48rem;color:#92400e;text-align:center;" id="configAlmacenCapacidadTotal">Capacidad total: 1,000 ubicaciones</div>\n                    </div>',
    "Config: Replace almac\u00e9n section"
)

# ======================================================================
# 6. Config defaults
# ======================================================================
print("\n--- Config defaults ---")

do_replace(
    "almacen: { ubicacionPorDefecto: 'PISO_1', stockMinimoAlerta: 20, aceptarStockNegativo: false, overstockAlerta: true }",
    "almacen: { pasillos: 5, racks: 10, niveles: 5, contenedores: 4, stockMinimoAlerta: 20, aceptarStockNegativo: false, overstockAlerta: true }",
    "Config: Update defaults"
)

# ======================================================================
# 7. Config load - replace ubicacionPorDefecto with new fields
# ======================================================================
print("\n--- Config load ---")

do_replace(
    "configAlmacenUbicacionPorDefecto) configAlmacenUbicacionPorDefecto.value = getConfigValue('almacen', 'ubicacionPorDefecto')",
    "cfgP_REMOVED_PLACEHOLDER) { /* removed */ }; if (false",
    "Config: Remove old ubicacion load (temp)"
)

# Actually, let me do a cleaner approach - find and replace the whole load block
# First, restore
content = content.replace(
    "cfgP_REMOVED_PLACEHOLDER) { /* removed */ }; if (false",
    "configAlmacenUbicacionPorDefecto) configAlmacenUbicacionPorDefecto.value = getConfigValue('almacen', 'ubicacionPorDefecto')"
)

# Let me find the exact lines of config load
lines = content.split('\n')
config_load_line = -1
for i, l in enumerate(lines):
    if "configAlmacenUbicacionPorDefecto" in l and "getConfigValue" in l:
        config_load_line = i
        break

if config_load_line == -1:
    print("FAIL: Could not find config load line for ubicacionPorDefecto")
    sys.exit(1)

print(f"  Found config load at line {config_load_line + 1}: {lines[config_load_line].strip()[:60]}...")

# Replace that single line with the new config load lines
old_line = lines[config_load_line]
indent = '        '
new_load_lines = [
    f"{indent}const cfgAlmPasillos = document.getElementById('configAlmacenPasillos');",
    f"{indent}const cfgAlmRacks = document.getElementById('configAlmacenRacks');",
    f"{indent}const cfgAlmNiveles = document.getElementById('configAlmacenNiveles');",
    f"{indent}const cfgAlmContenedores = document.getElementById('configAlmacenContenedores');",
    f"{indent}if (cfgAlmPasillos) cfgAlmPasillos.value = getConfigValue('almacen', 'pasillos') || 5;",
    f"{indent}if (cfgAlmRacks) cfgAlmRacks.value = getConfigValue('almacen', 'racks') || 10;",
    f"{indent}if (cfgAlmNiveles) cfgAlmNiveles.value = getConfigValue('almacen', 'niveles') || 5;",
    f"{indent}if (cfgAlmContenedores) cfgAlmContenedores.value = getConfigValue('almacen', 'contenedores') || 4;",
    f"{indent}updateConfigCapacidadTotal();",
]
lines[config_load_line:config_load_line+1] = new_load_lines
changes += 1
print(f"  [{changes}] Config: Replace load ubicacionPorDefecto with 4 new fields")

# Rejoin
content = '\n'.join(lines)

# ======================================================================
# 8. Config save - replace ubicacionPorDefecto
# ======================================================================
print("\n--- Config save ---")

do_replace(
    "setConfigValue('almacen', 'ubicacionPorDefecto', configAlmacenUbicacionPorDefecto",
    "setConfigValue('almacen', 'pasillos', Number(document.getElementById('configAlmacenPasillos')?.value) || 5);\n        setConfigValue('almacen', 'racks', Number(document.getElementById('configAlmacenRacks')?.value) || 10);\n        setConfigValue('almacen', 'niveles', Number(document.getElementById('configAlmacenNiveles')?.value) || 5);\n        setConfigValue('almacen', 'contenedores', Number(document.getElementById('configAlmacenContenedores')?.value) || 4);\n        // removed old ubicacionPorDefecto: (false && configAlmacenUbicacionPorDefecto",
    "Config: Replace save"
)

# ======================================================================
# 9. Remove old configAlmacenUbicacionPorDefecto JS variable
# ======================================================================
print("\n--- Remove old config var ---")

do_replace(
    "const configAlmacenUbicacionPorDefecto = document.getElementById('configAlmacenUbicacionPorDefecto');\n    const configAlmacenStockMinimoAlerta",
    "const configAlmacenStockMinimoAlerta",
    "Remove old configAlmacenUbicacionPorDefecto variable"
)

# ======================================================================
# 10-14. JS FUNCTIONS: Replace entire block using line-range replacement
# ======================================================================
print("\n--- JS Functions (line-range replacement) ---")

lines = content.split('\n')

# Find the comment line that starts the block
start_line = -1
end_line = -1
for i, l in enumerate(lines):
    if 'Ubicaci' in l and 'almac' in l and 'estructurada' in l and l.strip().startswith('//'):
        start_line = i
        break

if start_line == -1:
    print("FAIL: Could not find ubicación functions block start")
    sys.exit(1)

# Find closeConfirmUbicacion function and its closing brace
for i in range(start_line, min(start_line + 300, len(lines))):
    if 'function closeConfirmUbicacion' in lines[i]:
        brace_count = 0
        for j in range(i, i + 40):
            brace_count += lines[j].count('{') - lines[j].count('}')
            if brace_count == 0 and j > i:
                end_line = j
                break
        break

if end_line == -1:
    print("FAIL: Could not find ubicación functions block end")
    sys.exit(1)

print(f"  Found JS block: lines {start_line+1}-{end_line+1}")

# Build new JS block
# IMPORTANT: Use \\u for JS unicode escapes so Python keeps them as literal \u
new_js_block = r'''    // === Ubicación de almacén estructurada P/R/N/C ===
    function buildUbiCode(p, r, n, c) {
        const parts = [];
        if (p) parts.push('P' + p.replace(/^P/i, ''));
        if (r) parts.push('R' + r.replace(/^R/i, ''));
        if (n) parts.push('N' + n.replace(/^N/i, ''));
        if (c) parts.push('C' + c.replace(/^C/i, ''));
        return parts.join('-');
    }

    function getAlmacenConfig() {
        return {
            pasillos: Number(getConfigValue('almacen', 'pasillos')) || 5,
            racks: Number(getConfigValue('almacen', 'racks')) || 10,
            niveles: Number(getConfigValue('almacen', 'niveles')) || 5,
            contenedores: Number(getConfigValue('almacen', 'contenedores')) || 4
        };
    }

    function updateConfigCapacidadTotal() {
        const pp = Number(document.getElementById('configAlmacenPasillos')?.value) || 5;
        const rr = Number(document.getElementById('configAlmacenRacks')?.value) || 10;
        const nn = Number(document.getElementById('configAlmacenNiveles')?.value) || 5;
        const cc = Number(document.getElementById('configAlmacenContenedores')?.value) || 4;
        const total = pp * rr * nn * cc;
        const el = document.getElementById('configAlmacenCapacidadTotal');
        if (el) el.textContent = 'Capacidad total: ' + total.toLocaleString('es-MX') + ' ubicaciones';
    }

    function updateUbicacionCodigo() {
        const p = (document.getElementById('prodFormUbiPasillo')?.value || '').trim().toUpperCase();
        const r = (document.getElementById('prodFormUbiRack')?.value || '').trim().toUpperCase();
        const n = (document.getElementById('prodFormUbiNivel')?.value || '').trim().toUpperCase();
        const c = (document.getElementById('prodFormUbiContenedor')?.value || '').trim().toUpperCase();
        const codigoEl = document.getElementById('prodFormUbiCodigoWrap');
        const estatusEl = document.getElementById('prodFormUbiEstatus');
        const btnCont = document.getElementById('prodFormEtiquetaContenedor');
        const btnProd = document.getElementById('prodFormEtiquetaProducto');

        if (!p && !r && !n && !c) {
            if (codigoEl) { codigoEl.textContent = 'Sin ubicaci\u00f3n asignada'; codigoEl.classList.add('empty'); codigoEl.classList.remove('has-value'); }
            if (estatusEl) estatusEl.style.display = 'none';
            if (btnCont) btnCont.disabled = true;
            if (btnProd) btnProd.disabled = true;
            return '';
        }

        const code = buildUbiCode(p, r, n, c);
        if (codigoEl) { codigoEl.textContent = code; codigoEl.classList.remove('empty'); codigoEl.classList.add('has-value'); }

        const isNewProduct = !document.getElementById('prodFormCodigo')?.dataset?.editingId;
        if (estatusEl) {
            if (isNewProduct) {
                estatusEl.style.display = 'block';
                estatusEl.className = 'ubicacion-pendiente-badge pendiente';
                estatusEl.textContent = '\u23f3 Se confirmar\u00e1 al guardar el producto';
            } else {
                estatusEl.style.display = 'block';
                estatusEl.className = 'ubicacion-pendiente-badge confirmada';
                estatusEl.textContent = '\u2705 Ubicaci\u00f3n guardada';
            }
        }
        if (btnCont) btnCont.disabled = false;
        if (btnProd) btnProd.disabled = false;
        return code;
    }

    function _getUbiFormValues() {
        return {
            p: (document.getElementById('prodFormUbiPasillo')?.value || '').trim().toUpperCase(),
            r: (document.getElementById('prodFormUbiRack')?.value || '').trim().toUpperCase(),
            n: (document.getElementById('prodFormUbiNivel')?.value || '').trim().toUpperCase(),
            c: (document.getElementById('prodFormUbiContenedor')?.value || '').trim().toUpperCase(),
            nombre: (document.getElementById('prodFormProducto')?.value || '').trim() || 'PRODUCTO',
            codigo: (document.getElementById('prodFormCodigo')?.value || '').trim() || '000000000000000'
        };
    }

    function _labelCSS() {
        return `
@media print { body { margin: 0; } .no-print { display: none !important; } }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, Helvetica, sans-serif; display: flex; flex-direction: column; align-items: center; padding: 20px; background: #f3f4f6; }
.label-card { width: 90mm; border: 2px solid #1f2937; border-radius: 8px; padding: 10px; background: #fff; page-break-after: always; }
.label-header { text-align: center; border-bottom: 2px solid #1f2937; padding-bottom: 6px; margin-bottom: 8px; }
.label-empresa { font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; color: #f07a00; }
.label-titulo { font-size: 8px; color: #6b7280; margin-top: 2px; }
.label-ubicacion { text-align: center; font-family: 'Courier New', monospace; font-size: 22px; font-weight: 900; letter-spacing: 2px; padding: 6px 0; color: #1f2937; }
.label-ubicacion-desc { display: flex; justify-content: center; gap: 8px; font-size: 7px; color: #6b7280; margin-bottom: 6px; flex-wrap: wrap; }
.label-ubicacion-desc span { background: #f3f4f6; padding: 2px 5px; border-radius: 3px; }
.label-producto { text-align: center; font-size: 11px; font-weight: 800; color: #1f2937; padding: 6px 0; border-top: 1px dashed #d1d5db; border-bottom: 1px dashed #d1d5db; text-transform: uppercase; word-break: break-word; }
.label-codigo { text-align: center; font-family: 'Courier New', monospace; font-size: 13px; letter-spacing: 2px; padding: 6px 0; color: #374151; }
.label-barcode { text-align: center; font-family: 'Libre Barcode 39', 'Courier New', monospace; font-size: 36px; letter-spacing: 4px; color: #000; }
.label-footer { text-align: center; font-size: 7px; color: #9ca3af; margin-top: 6px; border-top: 1px solid #e5e7eb; padding-top: 4px; }
.btn-print { margin-top: 16px; padding: 10px 30px; font-size: 14px; font-weight: 700; background: #f07a00; color: #fff; border: none; border-radius: 8px; cursor: pointer; }
.btn-print:hover { background: #d76700; }
.label-tipo { font-size: 9px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; padding: 3px 10px; border-radius: 4px; display: inline-block; margin-top: 4px; }
.label-tipo.contenedor { background: #fef3c7; color: #92400e; border: 1px solid #fbbf24; }
.label-tipo.producto { background: #ede9fe; color: #5b21b6; border: 1px solid #a78bfa; }`;
    }

    function _ubicDescHTML(v) {
        let h = '';
        if (v.p) h += '<span>Pasillo ' + prodEscape(v.p.replace(/^P/i,'')) + '</span>';
        if (v.r) h += '<span>Rack ' + prodEscape(v.r.replace(/^R/i,'')) + '</span>';
        if (v.n) h += '<span>Nivel ' + prodEscape(v.n.replace(/^N/i,'')) + '</span>';
        if (v.c) h += '<span>Cont. ' + prodEscape(v.c.replace(/^C/i,'')) + '</span>';
        return h;
    }

    function generarEtiquetaContenedor() {
        const v = _getUbiFormValues();
        const ubicacionCode = buildUbiCode(v.p, v.r, v.n, v.c) || 'SIN-UBICACION';
        const fecha = new Date().toLocaleDateString('es-MX') + ' ' + new Date().toLocaleTimeString('es-MX', {hour:'2-digit',minute:'2-digit'});
        const html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Contenedor - ' + prodEscape(ubicacionCode) + '</title><style>' + _labelCSS() + '</style><link href="https://fonts.googleapis.com/css2?family=Libre+Barcode+39&display=swap" rel="stylesheet"></head><body>' +
            '<div class="label-card">' +
            '<div class="label-header"><div class="label-empresa">MAQUILEROS PUBLICIDAD</div><div class="label-titulo">ETIQUETA DE CONTENEDOR</div></div>' +
            '<div style="text-align:center;"><span class="label-tipo contenedor">\ud83d\udce6 CONTENEDOR</span></div>' +
            '<div class="label-ubicacion">' + prodEscape(ubicacionCode) + '</div>' +
            '<div class="label-ubicacion-desc">' + _ubicDescHTML(v) + '</div>' +
            '<div style="border-top:1px dashed #d1d5db;padding-top:6px;text-align:center;font-size:9px;color:#6b7280;">Este contenedor puede albergar m\u00faltiples productos.<br>Escanea el c\u00f3digo para identificar la ubicaci\u00f3n.</div>' +
            '<div class="label-barcode">*' + prodEscape(ubicacionCode.replace(/-/g,'')) + '*</div>' +
            '<div class="label-footer">Generada: ' + fecha + '</div>' +
            '</div>' +
            '<button class="btn-print no-print" onclick="window.print()">\ud83d\udda8\ufe0f Imprimir etiqueta</button></body></html>';
        const w = window.open('', '_blank', 'width=450,height=600');
        if (w) { w.document.write(html); w.document.close(); }
    }

    function generarEtiquetaProducto() {
        const v = _getUbiFormValues();
        const ubicacionCode = buildUbiCode(v.p, v.r, v.n, v.c) || 'SIN-UBICACION';
        const fecha = new Date().toLocaleDateString('es-MX') + ' ' + new Date().toLocaleTimeString('es-MX', {hour:'2-digit',minute:'2-digit'});
        const html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Producto - ' + prodEscape(v.nombre) + '</title><style>' + _labelCSS() + '</style><link href="https://fonts.googleapis.com/css2?family=Libre+Barcode+39&display=swap" rel="stylesheet"></head><body>' +
            '<div class="label-card">' +
            '<div class="label-header"><div class="label-empresa">MAQUILEROS PUBLICIDAD</div><div class="label-titulo">ETIQUETA DE PRODUCTO</div></div>' +
            '<div style="text-align:center;"><span class="label-tipo producto">\ud83c\udff7\ufe0f PRODUCTO</span></div>' +
            '<div class="label-producto">' + prodEscape(v.nombre) + '</div>' +
            '<div class="label-codigo">' + prodEscape(v.codigo) + '</div>' +
            '<div class="label-barcode">*' + prodEscape(v.codigo) + '*</div>' +
            '<div style="border-top:1px dashed #d1d5db;padding:6px 0 2px;text-align:center;">' +
            '<div style="font-size:8px;font-weight:800;color:#6b7280;text-transform:uppercase;margin-bottom:2px;">Ubicaci\u00f3n en almac\u00e9n</div>' +
            '<div style="font-family:monospace;font-size:16px;font-weight:900;letter-spacing:2px;color:#1f2937;">' + prodEscape(ubicacionCode) + '</div>' +
            '<div class="label-ubicacion-desc" style="margin-top:4px;">' + _ubicDescHTML(v) + '</div>' +
            '</div>' +
            '<div class="label-footer">Generada: ' + fecha + '</div>' +
            '</div>' +
            '<button class="btn-print no-print" onclick="window.print()">\ud83d\udda8\ufe0f Imprimir etiqueta</button></body></html>';
        const w = window.open('', '_blank', 'width=450,height=600');
        if (w) { w.document.write(html); w.document.close(); }
    }

    function syncUbicacionToStep2() {
        const p = (document.getElementById('prodFormUbiPasillo')?.value || '').trim().toUpperCase();
        const r = (document.getElementById('prodFormUbiRack')?.value || '').trim().toUpperCase();
        const n = (document.getElementById('prodFormUbiNivel')?.value || '').trim().toUpperCase();
        const c = (document.getElementById('prodFormUbiContenedor')?.value || '').trim().toUpperCase();
        const tabP = document.getElementById('prodTabUbiPasillo');
        const tabR = document.getElementById('prodTabUbiRack');
        const tabN = document.getElementById('prodTabUbiNivel');
        const tabC = document.getElementById('prodTabUbiContenedor');
        const tabCode = document.getElementById('prodTabUbiCodigoWrap');
        const tabNotas = document.getElementById('prodTabNotasPreview');
        const tabActivo = document.getElementById('prodTabActivo');
        if (tabP) tabP.value = p;
        if (tabR) tabR.value = r;
        if (tabN) tabN.value = n;
        if (tabC) tabC.value = c;
        const code = buildUbiCode(p, r, n, c);
        if (tabCode) {
            if (code) { tabCode.textContent = code; tabCode.classList.remove('empty'); }
            else { tabCode.textContent = 'Sin ubicaci\u00f3n asignada'; tabCode.classList.add('empty'); }
        }
        if (tabNotas) tabNotas.textContent = (document.getElementById('prodFormNotasInternas')?.value || '').trim() || '-';
        if (tabActivo) tabActivo.checked = document.getElementById('prodFormActivo')?.checked !== false;
    }

    // === Auto-assign next ubicación P/R/N/C ===
    function getNextAutoUbicacion() {
        const cfg = getAlmacenConfig();
        let maxVal = 0;
        let maxP = 0, maxR = 0, maxN = 0, maxC = 0;
        let found = false;

        productosData.forEach(prod => {
            const pp = parseInt(String(prod.ubiPasillo || '').replace(/^P/i, '').trim()) || 0;
            const rr = parseInt(String(prod.ubiRack || '').replace(/^R/i, '').trim()) || 0;
            const nn = parseInt(String(prod.ubiNivel || '').replace(/^N/i, '').trim()) || 0;
            const cc = parseInt(String(prod.ubiContenedor || '').replace(/^C/i, '').trim()) || 0;
            if (!pp && !rr && !nn && !cc) return;
            found = true;
            const val = pp * 1000000 + rr * 10000 + nn * 100 + cc;
            if (val > maxVal) { maxVal = val; maxP = pp; maxR = rr; maxN = nn; maxC = cc; }
        });

        if (!found) return { pasillo: '1', rack: '1', nivel: '1', contenedor: '1' };

        let nC = maxC + 1, nN = maxN, nR = maxR, nP = maxP;
        if (nC > cfg.contenedores) { nC = 1; nN = maxN + 1; }
        if (nN > cfg.niveles) { nN = 1; nR = maxR + 1; }
        if (nR > cfg.racks) { nR = 1; nP = maxP + 1; }

        return { pasillo: String(nP || 1), rack: String(nR || 1), nivel: String(nN || 1), contenedor: String(nC || 1) };
    }

    function autoAssignUbicacion() {
        const p = document.getElementById('prodFormUbiPasillo');
        const r = document.getElementById('prodFormUbiRack');
        const n = document.getElementById('prodFormUbiNivel');
        const c = document.getElementById('prodFormUbiContenedor');
        if ((p?.value || '').trim() || (r?.value || '').trim() || (n?.value || '').trim() || (c?.value || '').trim()) return;
        const next = getNextAutoUbicacion();
        if (p) p.value = next.pasillo;
        if (r) r.value = next.rack;
        if (n) n.value = next.nivel;
        if (c) c.value = next.contenedor;
        updateUbicacionCodigo();
    }

    // === Confirmation popup for ubicación before save ===
    let _commitAfterConfirm = null;

    function showConfirmUbicacion(onConfirm) {
        const popup = document.getElementById('popupConfirmarUbicacion');
        if (!popup) { onConfirm(); return; }
        _commitAfterConfirm = onConfirm;
        const nombre = (document.getElementById('prodFormProducto')?.value || '').trim() || 'Producto';
        const codigo = (document.getElementById('prodFormCodigo')?.value || '').trim() || '-';
        const p = (document.getElementById('prodFormUbiPasillo')?.value || '').trim().toUpperCase();
        const r = (document.getElementById('prodFormUbiRack')?.value || '').trim().toUpperCase();
        const n = (document.getElementById('prodFormUbiNivel')?.value || '').trim().toUpperCase();
        const c = (document.getElementById('prodFormUbiContenedor')?.value || '').trim().toUpperCase();
        document.getElementById('confirmUbiNombreProducto').textContent = nombre;
        document.getElementById('confirmUbiCodigoProducto').textContent = codigo;
        document.getElementById('confirmUbiPasillo').value = p || '1';
        document.getElementById('confirmUbiRack').value = r || '1';
        document.getElementById('confirmUbiNivel').value = n || '1';
        document.getElementById('confirmUbiContenedor').value = c || '1';
        updateConfirmUbiPreview();
        popup.style.display = 'flex';
        popup.setAttribute('aria-hidden', 'false');
    }

    function updateConfirmUbiPreview() {
        const p = (document.getElementById('confirmUbiPasillo')?.value || '').trim().toUpperCase();
        const r = (document.getElementById('confirmUbiRack')?.value || '').trim().toUpperCase();
        const n = (document.getElementById('confirmUbiNivel')?.value || '').trim().toUpperCase();
        const c = (document.getElementById('confirmUbiContenedor')?.value || '').trim().toUpperCase();
        const code = buildUbiCode(p, r, n, c) || 'SIN UBICACI\u00d3N';
        const grande = document.getElementById('confirmUbiCodigoGrande');
        if (grande) grande.textContent = code;
    }

    function closeConfirmUbicacion(accepted) {
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
    }'''

new_js_lines = new_js_block.split('\n')
lines = content.split('\n')
lines[start_line:end_line+1] = new_js_lines
content = '\n'.join(lines)
changes += 1
print(f"  [{changes}] Replaced JS functions block ({end_line - start_line + 1} lines -> {len(new_js_lines)} lines)")

# ======================================================================
# 15. Event listeners
# ======================================================================
print("\n--- Event listeners ---")

do_replace(
    "'prodFormUbiPasillo', 'prodFormUbiRack', 'prodFormUbiNivel'].forEach",
    "'prodFormUbiPasillo', 'prodFormUbiRack', 'prodFormUbiNivel', 'prodFormUbiContenedor'].forEach",
    "Add C to ubi input listeners"
)

do_replace(
    "const etiquetaBtn = document.getElementById('prodFormGenerarEtiquetaBtn');\n    if (etiquetaBtn) etiquetaBtn.addEventListener('click', () => generarEtiquetaUbicacion());",
    "const etiquetaContBtn = document.getElementById('prodFormEtiquetaContenedor');\n    const etiquetaProdBtn = document.getElementById('prodFormEtiquetaProducto');\n    if (etiquetaContBtn) etiquetaContBtn.addEventListener('click', () => generarEtiquetaContenedor());\n    if (etiquetaProdBtn) etiquetaProdBtn.addEventListener('click', () => generarEtiquetaProducto());",
    "Replace label button listeners"
)

do_replace(
    "'confirmUbiPasillo', 'confirmUbiRack', 'confirmUbiNivel'].forEach",
    "'confirmUbiPasillo', 'confirmUbiRack', 'confirmUbiNivel', 'confirmUbiContenedor'].forEach",
    "Add C to confirm listeners"
)

# ======================================================================
# 16. Payload
# ======================================================================
print("\n--- Payload ---")

do_replace(
    "ubiNivel: (document.getElementById('prodFormUbiNivel')?.value || '').trim().toUpperCase(),",
    "ubiNivel: (document.getElementById('prodFormUbiNivel')?.value || '').trim().toUpperCase(),\n            ubiContenedor: (document.getElementById('prodFormUbiContenedor')?.value || '').trim().toUpperCase(),",
    "Add contenedor to payload"
)

# ======================================================================
# 17. Reset
# ======================================================================
print("\n--- Reset ---")

do_replace(
    "const ubiRClear = document.getElementById('prodFormUbiRack');\n        const ubiNClear = document.getElementById('prodFormUbiNivel');",
    "const ubiRClear = document.getElementById('prodFormUbiRack');\n        const ubiNClear = document.getElementById('prodFormUbiNivel');\n        const ubiCClear = document.getElementById('prodFormUbiContenedor');",
    "Reset: Add C var"
)

do_replace(
    "if (ubiNClear) ubiNClear.value = '';",
    "if (ubiNClear) ubiNClear.value = '';\n        if (ubiCClear) ubiCClear.value = '';",
    "Reset: Add C clear"
)

# ======================================================================
# 18. Edit load
# ======================================================================
print("\n--- Edit load ---")

do_replace(
    "const ubiREdit = document.getElementById('prodFormUbiRack');\n        const ubiNEdit = document.getElementById('prodFormUbiNivel');",
    "const ubiREdit = document.getElementById('prodFormUbiRack');\n        const ubiNEdit = document.getElementById('prodFormUbiNivel');\n        const ubiCEdit = document.getElementById('prodFormUbiContenedor');",
    "Edit: Add C var"
)

do_replace(
    "if (ubiNEdit) ubiNEdit.value = row.ubiNivel || '';",
    "if (ubiNEdit) ubiNEdit.value = row.ubiNivel || '';\n        if (ubiCEdit) ubiCEdit.value = row.ubiContenedor || '';",
    "Edit: Add C load"
)

# ======================================================================
# 19. Config capacity listeners
# ======================================================================
print("\n--- Config capacity listeners ---")

do_replace(
    "if (confirmUbiAceptar) confirmUbiAceptar.addEventListener('click', () => closeConfirmUbicacion(true));",
    "if (confirmUbiAceptar) confirmUbiAceptar.addEventListener('click', () => closeConfirmUbicacion(true));\n\n    ['configAlmacenPasillos', 'configAlmacenRacks', 'configAlmacenNiveles', 'configAlmacenContenedores'].forEach(id => {\n        const el = document.getElementById(id);\n        if (el) el.addEventListener('input', () => updateConfigCapacidadTotal());\n    });",
    "Add config capacity listeners"
)

# ======================================================================
# WRITE
# ======================================================================
with open('mockup.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n=== DONE: {changes} changes applied. Size: {original} -> {len(content)} ===")
