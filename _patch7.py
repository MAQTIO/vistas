#!/usr/bin/env python3
"""Patch 7: Redesign ubicación almacén — structured P/R/C fields + etiqueta generator."""
import sys

with open('mockup.html', 'r', encoding='utf-8') as f:
    content = f.read()

original = len(content)
changes = 0

def do_replace(old, new, desc):
    global content, changes
    n = content.count(old)
    if n == 0:
        print(f"FAIL: {desc} — pattern not found!")
        sys.exit(1)
    content = content.replace(old, new, 1)
    changes += 1
    print(f"  [{changes}] {desc} (found {n})")

# ======================================================================
# 1. CSS: Add ubicación styles
# ======================================================================
print("\n--- PART 1: CSS ---")

do_replace(
    """        .prod-photo-pane-extras .photo-pane-separator {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.2);
            margin: 2px 0;
        }""",
    """        .prod-photo-pane-extras .photo-pane-separator {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.2);
            margin: 2px 0;
        }

        .ubicacion-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 3px;
        }

        .ubicacion-grid .ubi-cell {
            display: flex;
            flex-direction: column;
            gap: 1px;
        }

        .ubicacion-grid .ubi-cell label {
            font-size: 0.46rem !important;
            text-align: center;
            margin: 0 !important;
        }

        .ubicacion-grid .ubi-cell select,
        .ubicacion-grid .ubi-cell input {
            text-align: center;
            padding: 3px 2px !important;
            font-size: 0.58rem !important;
            font-weight: 700;
        }

        .ubicacion-codigo {
            background: rgba(0,0,0,0.18);
            border-radius: 5px;
            padding: 4px 6px;
            text-align: center;
            font-family: 'Courier New', monospace;
            font-size: 0.68rem;
            font-weight: 900;
            letter-spacing: 1.5px;
            color: #fff;
            border: 1px solid rgba(255,255,255,0.3);
            min-height: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .ubicacion-codigo.empty {
            font-size: 0.5rem;
            font-weight: 400;
            letter-spacing: 0;
            color: rgba(255,255,255,0.5);
        }

        .btn-generar-etiqueta {
            width: 100%;
            padding: 5px 8px;
            font-size: 0.56rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            border: 1px dashed rgba(255,255,255,0.5);
            border-radius: 5px;
            background: rgba(255,255,255,0.12);
            color: #fff;
            cursor: pointer;
            transition: background 0.15s;
        }

        .btn-generar-etiqueta:hover {
            background: rgba(255,255,255,0.25);
        }

        .btn-generar-etiqueta:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        .ubicacion-pendiente-badge {
            font-size: 0.48rem;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 10px;
            text-align: center;
        }

        .ubicacion-pendiente-badge.pendiente {
            background: rgba(251,191,36,0.25);
            color: #fef3c7;
            border: 1px solid rgba(251,191,36,0.5);
        }

        .ubicacion-pendiente-badge.confirmada {
            background: rgba(34,197,94,0.25);
            color: #dcfce7;
            border: 1px solid rgba(34,197,94,0.5);
        }""",
    "Add ubicación structured CSS"
)

# ======================================================================
# 2. HTML: Replace photo-pane-extras content
# ======================================================================
print("\n--- PART 2: HTML ---")

old_extras = """                <div class="prod-photo-pane-extras">
                    <hr class="photo-pane-separator">
                    <div>
                        <label>Etiqueta / Color</label>
                        <select id="prodFormEtiqueta">
                            <option value="">Sin etiqueta</option>
                            <option value="rojo" style="color:#ef4444;">\U0001f534 Rojo \u2014 Urgente</option>
                            <option value="amarillo" style="color:#eab308;">\U0001f7e1 Amarillo \u2014 Revisar</option>
                            <option value="verde" style="color:#22c55e;">\U0001f7e2 Verde \u2014 Listo</option>
                            <option value="azul" style="color:#3b82f6;">\U0001f535 Azul \u2014 Destacado</option>
                            <option value="morado" style="color:#a855f7;">\U0001f7e3 Morado \u2014 Especial</option>
                        </select>
                    </div>
                    <div>
                        <label>Ubicaci\u00f3n / Almac\u00e9n</label>
                        <input id="prodFormUbicacion" type="text" placeholder="Ej: Estante A-3, Bodega 2">
                    </div>
                    <div>
                        <label>Notas internas</label>
                        <textarea id="prodFormNotasInternas" rows="2" placeholder="Notas solo visibles para el equipo..." style="resize:none;"></textarea>
                    </div>
                    <hr class="photo-pane-separator">
                    <label class="photo-pane-toggle">
                        <input type="checkbox" id="prodFormActivo" checked>
                        <span>\u2705 Producto activo</span>
                    </label>
                    <label class="photo-pane-toggle">
                        <input type="checkbox" id="prodFormVisibleCotizador" checked>
                        <span>\U0001f4cb Visible en cotizador</span>
                    </label>
                </div>"""

new_extras = """                <div class="prod-photo-pane-extras">
                    <hr class="photo-pane-separator">
                    <label style="font-size:0.52rem;font-weight:900;letter-spacing:0.3px;color:rgba(255,255,255,0.9);">\U0001f4e6 UBICACI\u00d3N EN ALMAC\u00c9N</label>
                    <div class="ubicacion-grid">
                        <div class="ubi-cell">
                            <label>PASILLO</label>
                            <input id="prodFormUbiPasillo" type="text" maxlength="4" placeholder="P1" style="text-transform:uppercase;">
                        </div>
                        <div class="ubi-cell">
                            <label>RACK</label>
                            <input id="prodFormUbiRack" type="text" maxlength="4" placeholder="R1" style="text-transform:uppercase;">
                        </div>
                        <div class="ubi-cell">
                            <label>NIVEL</label>
                            <input id="prodFormUbiNivel" type="text" maxlength="4" placeholder="N1" style="text-transform:uppercase;">
                        </div>
                    </div>
                    <div id="prodFormUbiCodigoWrap" class="ubicacion-codigo empty">Sin ubicaci\u00f3n asignada</div>
                    <div id="prodFormUbiEstatus" class="ubicacion-pendiente-badge pendiente" style="display:none;">\u23f3 Pendiente de confirmar al guardar</div>
                    <button type="button" id="prodFormGenerarEtiquetaBtn" class="btn-generar-etiqueta" disabled>\U0001f3f7\ufe0f Generar etiqueta de ubicaci\u00f3n</button>
                    <hr class="photo-pane-separator">
                    <div>
                        <label>Notas internas</label>
                        <textarea id="prodFormNotasInternas" rows="2" placeholder="Notas solo visibles para el equipo..." style="resize:none;"></textarea>
                    </div>
                    <hr class="photo-pane-separator">
                    <label class="photo-pane-toggle">
                        <input type="checkbox" id="prodFormActivo" checked>
                        <span>\u2705 Producto activo</span>
                    </label>
                </div>"""

do_replace(old_extras, new_extras, "Replace extras HTML with structured ubicación")

# ======================================================================
# 3. JS: Add ubicación functions + etiqueta generation
# ======================================================================
print("\n--- PART 3: JS ubicación functions ---")

js_ubicacion = '''
    // === Ubicación de almacén estructurada ===
    function updateUbicacionCodigo() {
        const p = (document.getElementById('prodFormUbiPasillo')?.value || '').trim().toUpperCase();
        const r = (document.getElementById('prodFormUbiRack')?.value || '').trim().toUpperCase();
        const n = (document.getElementById('prodFormUbiNivel')?.value || '').trim().toUpperCase();
        const codigoEl = document.getElementById('prodFormUbiCodigoWrap');
        const estatusEl = document.getElementById('prodFormUbiEstatus');
        const btnEtiqueta = document.getElementById('prodFormGenerarEtiquetaBtn');

        if (!p && !r && !n) {
            if (codigoEl) { codigoEl.textContent = 'Sin ubicaci\\u00f3n asignada'; codigoEl.classList.add('empty'); codigoEl.classList.remove('has-value'); }
            if (estatusEl) estatusEl.style.display = 'none';
            if (btnEtiqueta) btnEtiqueta.disabled = true;
            return '';
        }

        const parts = [];
        if (p) parts.push('P' + p.replace(/^P/i, ''));
        if (r) parts.push('R' + r.replace(/^R/i, ''));
        if (n) parts.push('N' + n.replace(/^N/i, ''));
        const code = parts.join('-');

        if (codigoEl) { codigoEl.textContent = code; codigoEl.classList.remove('empty'); codigoEl.classList.add('has-value'); }

        // Show "pendiente" if the product is being created (no id yet)
        const isNewProduct = !document.getElementById('prodFormCodigo')?.dataset?.editingId;
        if (estatusEl) {
            if (isNewProduct) {
                estatusEl.style.display = 'block';
                estatusEl.className = 'ubicacion-pendiente-badge pendiente';
                estatusEl.textContent = '\\u23f3 Se confirmar\\u00e1 al guardar el producto';
            } else {
                estatusEl.style.display = 'block';
                estatusEl.className = 'ubicacion-pendiente-badge confirmada';
                estatusEl.textContent = '\\u2705 Ubicaci\\u00f3n guardada';
            }
        }
        if (btnEtiqueta) btnEtiqueta.disabled = !isNewProduct ? false : false; // enable if any value
        if (btnEtiqueta) btnEtiqueta.disabled = false;
        return code;
    }

    function generarEtiquetaUbicacion() {
        const p = (document.getElementById('prodFormUbiPasillo')?.value || '').trim().toUpperCase();
        const r = (document.getElementById('prodFormUbiRack')?.value || '').trim().toUpperCase();
        const n = (document.getElementById('prodFormUbiNivel')?.value || '').trim().toUpperCase();
        const nombre = (document.getElementById('prodFormProducto')?.value || '').trim() || 'PRODUCTO';
        const codigo = (document.getElementById('prodFormCodigo')?.value || '').trim() || '000000000000000';

        const parts = [];
        if (p) parts.push('P' + p.replace(/^P/i, ''));
        if (r) parts.push('R' + r.replace(/^R/i, ''));
        if (n) parts.push('N' + n.replace(/^N/i, ''));
        const ubicacionCode = parts.join('-') || 'SIN-UBICACION';

        // Generate printable label in a new window
        const labelHTML = `<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Etiqueta - ${prodEscape(nombre)}</title>
<style>
@media print { body { margin: 0; } .no-print { display: none !important; } }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Arial, Helvetica, sans-serif; display: flex; flex-direction: column; align-items: center; padding: 20px; background: #f3f4f6; }
.label-card { width: 90mm; border: 2px solid #1f2937; border-radius: 8px; padding: 10px; background: #fff; page-break-after: always; }
.label-header { text-align: center; border-bottom: 2px solid #1f2937; padding-bottom: 6px; margin-bottom: 8px; }
.label-empresa { font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; color: #f07a00; }
.label-titulo { font-size: 8px; color: #6b7280; margin-top: 2px; }
.label-ubicacion { text-align: center; font-family: 'Courier New', monospace; font-size: 28px; font-weight: 900; letter-spacing: 3px; padding: 8px 0; color: #1f2937; }
.label-ubicacion-desc { display: flex; justify-content: center; gap: 12px; font-size: 8px; color: #6b7280; margin-bottom: 8px; }
.label-ubicacion-desc span { background: #f3f4f6; padding: 2px 6px; border-radius: 3px; }
.label-producto { text-align: center; font-size: 11px; font-weight: 800; color: #1f2937; padding: 6px 0; border-top: 1px dashed #d1d5db; border-bottom: 1px dashed #d1d5db; text-transform: uppercase; word-break: break-word; }
.label-codigo { text-align: center; font-family: 'Courier New', monospace; font-size: 13px; letter-spacing: 2px; padding: 6px 0; color: #374151; }
.label-barcode { text-align: center; font-family: 'Libre Barcode 39', 'Courier New', monospace; font-size: 36px; letter-spacing: 4px; color: #000; }
.label-footer { text-align: center; font-size: 7px; color: #9ca3af; margin-top: 6px; border-top: 1px solid #e5e7eb; padding-top: 4px; }
.btn-print { margin-top: 16px; padding: 10px 30px; font-size: 14px; font-weight: 700; background: #f07a00; color: #fff; border: none; border-radius: 8px; cursor: pointer; }
.btn-print:hover { background: #d76700; }
</style>
<link href="https://fonts.googleapis.com/css2?family=Libre+Barcode+39&display=swap" rel="stylesheet">
</head><body>
<div class="label-card">
    <div class="label-header">
        <div class="label-empresa">MAQUILEROS PUBLICIDAD</div>
        <div class="label-titulo">ETIQUETA DE UBICACI\\u00d3N</div>
    </div>
    <div class="label-ubicacion">${prodEscape(ubicacionCode)}</div>
    <div class="label-ubicacion-desc">
        ${p ? '<span>Pasillo ' + prodEscape(p.replace(/^P/i,'')) + '</span>' : ''}
        ${r ? '<span>Rack ' + prodEscape(r.replace(/^R/i,'')) + '</span>' : ''}
        ${n ? '<span>Nivel ' + prodEscape(n.replace(/^N/i,'')) + '</span>' : ''}
    </div>
    <div class="label-producto">${prodEscape(nombre)}</div>
    <div class="label-codigo">${prodEscape(codigo)}</div>
    <div class="label-barcode">*${prodEscape(codigo)}*</div>
    <div class="label-footer">Generada: ${new Date().toLocaleDateString('es-MX')} ${new Date().toLocaleTimeString('es-MX', {hour:'2-digit',minute:'2-digit'})}</div>
</div>
<button class="btn-print no-print" onclick="window.print()">\\U0001f5a8\\ufe0f Imprimir etiqueta</button>
</body></html>`;

        const w = window.open('', '_blank', 'width=450,height=600');
        if (w) { w.document.write(labelHTML); w.document.close(); }
    }

'''

# Insert before "// === Costo promedio"
do_replace(
    "    // === Costo promedio autom\u00e1tico para insumos ===",
    js_ubicacion + "    // === Costo promedio autom\u00e1tico para insumos ===",
    "Insert ubicación JS functions"
)

# ======================================================================
# 4. JS: Event listeners for ubicación fields
# ======================================================================
print("\n--- PART 4: Event listeners ---")

# Find where the prodFormActivo listener area would be — after the proceso insumos listeners
# Let's insert after the seleccion insumo proc listeners
do_replace(
    """    const popupSelIns = document.getElementById('popupSeleccionInsumoProc');
    if (popupSelIns) popupSelIns.addEventListener('click', (e) => { if (e.target === popupSelIns) cancelSeleccionInsumoProc(); });""",
    """    const popupSelIns = document.getElementById('popupSeleccionInsumoProc');
    if (popupSelIns) popupSelIns.addEventListener('click', (e) => { if (e.target === popupSelIns) cancelSeleccionInsumoProc(); });

    // Ubicación de almacén — auto update code
    ['prodFormUbiPasillo', 'prodFormUbiRack', 'prodFormUbiNivel'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('input', () => updateUbicacionCodigo());
    });
    const etiquetaBtn = document.getElementById('prodFormGenerarEtiquetaBtn');
    if (etiquetaBtn) etiquetaBtn.addEventListener('click', () => generarEtiquetaUbicacion());""",
    "Add ubicación event listeners"
)

# ======================================================================
# 5. JS: Update payload — replace etiqueta + ubicacion + visibleCotizador
# ======================================================================
print("\n--- PART 5: Update payload ---")

do_replace(
    """            etiqueta: String(document.getElementById('prodFormEtiqueta')?.value || ''),
            ubicacion: String(document.getElementById('prodFormUbicacion')?.value || '').trim(),
            notasInternas: String(document.getElementById('prodFormNotasInternas')?.value || '').trim(),
            activo: document.getElementById('prodFormActivo')?.checked !== false,
            visibleCotizador: document.getElementById('prodFormVisibleCotizador')?.checked !== false""",
    """            ubicacion: updateUbicacionCodigo() || '',
            ubiPasillo: (document.getElementById('prodFormUbiPasillo')?.value || '').trim().toUpperCase(),
            ubiRack: (document.getElementById('prodFormUbiRack')?.value || '').trim().toUpperCase(),
            ubiNivel: (document.getElementById('prodFormUbiNivel')?.value || '').trim().toUpperCase(),
            notasInternas: String(document.getElementById('prodFormNotasInternas')?.value || '').trim(),
            activo: document.getElementById('prodFormActivo')?.checked !== false""",
    "Update payload with structured ubicación"
)

# ======================================================================
# 6. JS: Update reset
# ======================================================================
print("\n--- PART 6: Update reset ---")

do_replace(
    """        const etiquetaClear = document.getElementById('prodFormEtiqueta');
        const ubicacionClear = document.getElementById('prodFormUbicacion');
        const notasInternasClear = document.getElementById('prodFormNotasInternas');
        const activoClear = document.getElementById('prodFormActivo');
        const visibleCotClear = document.getElementById('prodFormVisibleCotizador');
        if (etiquetaClear) etiquetaClear.value = '';
        if (ubicacionClear) ubicacionClear.value = '';
        if (notasInternasClear) notasInternasClear.value = '';
        if (activoClear) activoClear.checked = true;
        if (visibleCotClear) visibleCotClear.checked = true;""",
    """        const ubiPClear = document.getElementById('prodFormUbiPasillo');
        const ubiRClear = document.getElementById('prodFormUbiRack');
        const ubiNClear = document.getElementById('prodFormUbiNivel');
        const notasInternasClear = document.getElementById('prodFormNotasInternas');
        const activoClear = document.getElementById('prodFormActivo');
        if (ubiPClear) ubiPClear.value = '';
        if (ubiRClear) ubiRClear.value = '';
        if (ubiNClear) ubiNClear.value = '';
        if (notasInternasClear) notasInternasClear.value = '';
        if (activoClear) activoClear.checked = true;
        updateUbicacionCodigo();""",
    "Update reset for structured ubicación"
)

# ======================================================================
# 7. JS: Update edit load
# ======================================================================
print("\n--- PART 7: Update edit load ---")

do_replace(
    """        const etiquetaEdit = document.getElementById('prodFormEtiqueta');
        const ubicacionEdit = document.getElementById('prodFormUbicacion');
        const notasInternasEdit = document.getElementById('prodFormNotasInternas');
        const activoEdit = document.getElementById('prodFormActivo');
        const visibleCotEdit = document.getElementById('prodFormVisibleCotizador');
        if (etiquetaEdit) etiquetaEdit.value = row.etiqueta || '';
        if (ubicacionEdit) ubicacionEdit.value = row.ubicacion || '';
        if (notasInternasEdit) notasInternasEdit.value = row.notasInternas || '';
        if (activoEdit) activoEdit.checked = row.activo !== false;
        if (visibleCotEdit) visibleCotEdit.checked = row.visibleCotizador !== false;""",
    """        const ubiPEdit = document.getElementById('prodFormUbiPasillo');
        const ubiREdit = document.getElementById('prodFormUbiRack');
        const ubiNEdit = document.getElementById('prodFormUbiNivel');
        const notasInternasEdit = document.getElementById('prodFormNotasInternas');
        const activoEdit = document.getElementById('prodFormActivo');
        if (ubiPEdit) ubiPEdit.value = row.ubiPasillo || '';
        if (ubiREdit) ubiREdit.value = row.ubiRack || '';
        if (ubiNEdit) ubiNEdit.value = row.ubiNivel || '';
        if (notasInternasEdit) notasInternasEdit.value = row.notasInternas || '';
        if (activoEdit) activoEdit.checked = row.activo !== false;
        updateUbicacionCodigo();""",
    "Update edit load for structured ubicación"
)

# ======================================================================
# WRITE
# ======================================================================
with open('mockup.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n=== {changes} changes applied. Size: {original} -> {len(content)} ===")
