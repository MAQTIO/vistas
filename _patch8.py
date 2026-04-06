#!/usr/bin/env python3
"""Patch 8: 
1. Step-2 photo pane shows same extras (ubicación, notas, activo) — synced from step 1
2. Save button triggers confirmation popup with P/R/N before committing
3. Auto-assign default ubicación (P1-R1-N1 incrementing)
"""
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
# 1. Replace step-2 photo pane HTML — mirror the complete extras panel
# ======================================================================
print("\n--- PART 1: Step-2 photo pane HTML ---")

old_step2_aside = """            <aside class="prod-photo-pane">
                <h4>Foto del producto</h4>
                <div class="prod-foto-principal-box">
                    <div id="prodTabFotoPreview" class="prod-foto-preview">Sin foto principal</div>
                </div>
                
            </aside>"""

new_step2_aside = """            <aside class="prod-photo-pane">
                <h4>\U0001f4f7 Foto del producto</h4>
                <div class="prod-foto-principal-box">
                    <div id="prodTabFotoPreview" class="prod-foto-preview">Sin foto principal</div>
                </div>
                <div class="prod-photo-pane-extras">
                    <hr class="photo-pane-separator">
                    <label style="font-size:0.52rem;font-weight:900;letter-spacing:0.3px;color:rgba(255,255,255,0.9);">\U0001f4e6 UBICACI\u00d3N EN ALMAC\u00c9N</label>
                    <div id="prodTabUbiCodigoWrap" class="ubicacion-codigo empty">Sin ubicaci\u00f3n asignada</div>
                    <div class="ubicacion-grid">
                        <div class="ubi-cell">
                            <label>PASILLO</label>
                            <input id="prodTabUbiPasillo" type="text" maxlength="4" placeholder="P1" style="text-transform:uppercase;" readonly>
                        </div>
                        <div class="ubi-cell">
                            <label>RACK</label>
                            <input id="prodTabUbiRack" type="text" maxlength="4" placeholder="R1" style="text-transform:uppercase;" readonly>
                        </div>
                        <div class="ubi-cell">
                            <label>NIVEL</label>
                            <input id="prodTabUbiNivel" type="text" maxlength="4" placeholder="N1" style="text-transform:uppercase;" readonly>
                        </div>
                    </div>
                    <hr class="photo-pane-separator">
                    <div>
                        <label>Notas internas</label>
                        <div id="prodTabNotasPreview" style="font-size:0.52rem;color:rgba(255,255,255,0.7);min-height:14px;">-</div>
                    </div>
                    <label class="photo-pane-toggle" style="pointer-events:none;opacity:0.7;">
                        <input type="checkbox" id="prodTabActivo" checked disabled>
                        <span>\u2705 Producto activo</span>
                    </label>
                </div>
            </aside>"""

do_replace(old_step2_aside, new_step2_aside, "Replace step-2 photo pane with mirrored extras")

# ======================================================================
# 2. Add confirmation popup HTML — before popupProdTabulador
# ======================================================================
print("\n--- PART 2: Confirmation popup HTML ---")

popup_confirm = '''
<!-- ============ POPUP: CONFIRMAR UBICACIÓN AL GUARDAR ============ -->
<div id="popupConfirmarUbicacion" class="productos-modal-overlay" aria-hidden="true" style="z-index:2250;">
    <div class="productos-modal-card" role="dialog" aria-modal="true" style="max-width:420px;padding:0;overflow:hidden;border:2px solid #f07a00;">
        <div style="background:linear-gradient(160deg,#f07a00 0%,#d76700 100%);padding:14px 18px;text-align:center;">
            <div style="font-size:1.4rem;">📦</div>
            <h3 style="margin:4px 0 0;font-size:0.82rem;font-weight:900;color:#fff;text-transform:uppercase;letter-spacing:0.5px;">Confirmar ubicación del producto</h3>
        </div>
        <div style="padding:16px 20px;">
            <div style="text-align:center;margin-bottom:12px;">
                <div id="confirmUbiNombreProducto" style="font-size:0.72rem;font-weight:800;color:#1f2937;margin-bottom:4px;">Producto</div>
                <div id="confirmUbiCodigoProducto" style="font-size:0.58rem;color:#6b7280;font-family:monospace;">000000000000000</div>
            </div>
            <div style="background:#fef3c7;border:1px solid #fbbf24;border-radius:8px;padding:10px;margin-bottom:12px;">
                <div style="font-size:0.56rem;font-weight:700;color:#92400e;text-align:center;margin-bottom:6px;">UBICACIÓN ASIGNADA</div>
                <div id="confirmUbiCodigoGrande" style="text-align:center;font-family:'Courier New',monospace;font-size:1.6rem;font-weight:900;letter-spacing:3px;color:#92400e;padding:4px 0;">P1-R1-N1</div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:12px;">
                <div style="text-align:center;background:#f9fafb;border:1px solid #e5e7eb;border-radius:6px;padding:6px;">
                    <div style="font-size:0.48rem;font-weight:800;color:#6b7280;text-transform:uppercase;">Pasillo</div>
                    <input id="confirmUbiPasillo" type="text" maxlength="4" style="width:100%;text-align:center;font-size:0.8rem;font-weight:900;border:1px solid #d1d5db;border-radius:4px;padding:4px;text-transform:uppercase;margin-top:2px;">
                </div>
                <div style="text-align:center;background:#f9fafb;border:1px solid #e5e7eb;border-radius:6px;padding:6px;">
                    <div style="font-size:0.48rem;font-weight:800;color:#6b7280;text-transform:uppercase;">Rack</div>
                    <input id="confirmUbiRack" type="text" maxlength="4" style="width:100%;text-align:center;font-size:0.8rem;font-weight:900;border:1px solid #d1d5db;border-radius:4px;padding:4px;text-transform:uppercase;margin-top:2px;">
                </div>
                <div style="text-align:center;background:#f9fafb;border:1px solid #e5e7eb;border-radius:6px;padding:6px;">
                    <div style="font-size:0.48rem;font-weight:800;color:#6b7280;text-transform:uppercase;">Nivel</div>
                    <input id="confirmUbiNivel" type="text" maxlength="4" style="width:100%;text-align:center;font-size:0.8rem;font-weight:900;border:1px solid #d1d5db;border-radius:4px;padding:4px;text-transform:uppercase;margin-top:2px;">
                </div>
            </div>
            <div style="font-size:0.52rem;color:#6b7280;text-align:center;margin-bottom:4px;">Puedes editar la ubicación antes de confirmar</div>
            <div id="confirmUbiUpdatePreview" style="text-align:center;font-family:monospace;font-size:0.58rem;color:#9ca3af;min-height:14px;"></div>
        </div>
        <div style="display:flex;gap:8px;padding:12px 20px;border-top:1px solid #e5e7eb;background:#f9fafb;">
            <button type="button" id="confirmUbiCancelar" class="productos-btn gray" style="flex:1;padding:8px;font-size:0.65rem;">Cancelar</button>
            <button type="button" id="confirmUbiAceptar" class="productos-btn primary" style="flex:1;padding:8px;font-size:0.65rem;background:#f07a00;">✅ Confirmar y guardar</button>
        </div>
    </div>
</div>
'''

do_replace(
    '<div id="popupProdTabulador" class="productos-modal-overlay" aria-hidden="true">',
    popup_confirm + '\n<div id="popupProdTabulador" class="productos-modal-overlay" aria-hidden="true">',
    "Insert confirmation popup HTML"
)

# ======================================================================
# 3. JS: Sync step-1 values to step-2 when opening tabulador
# ======================================================================
print("\n--- PART 3: Sync values to step-2 ---")

do_replace(
    """        renderProdMainPhotoPreview();
        openProdModal(popupProdTabulador);
    };""",
    """        renderProdMainPhotoPreview();
        syncUbicacionToStep2();
        openProdModal(popupProdTabulador);
    };""",
    "Add syncUbicacionToStep2 call when opening tabulador"
)

# ======================================================================
# 4. JS: Add syncUbicacionToStep2 + auto-assign + confirm functions
# ======================================================================
print("\n--- PART 4: JS functions ---")

js_new = '''
    // === Sync ubicación to step-2 and auto-assign ===
    function syncUbicacionToStep2() {
        const p = (document.getElementById('prodFormUbiPasillo')?.value || '').trim().toUpperCase();
        const r = (document.getElementById('prodFormUbiRack')?.value || '').trim().toUpperCase();
        const n = (document.getElementById('prodFormUbiNivel')?.value || '').trim().toUpperCase();
        const tabP = document.getElementById('prodTabUbiPasillo');
        const tabR = document.getElementById('prodTabUbiRack');
        const tabN = document.getElementById('prodTabUbiNivel');
        const tabCode = document.getElementById('prodTabUbiCodigoWrap');
        const tabNotas = document.getElementById('prodTabNotasPreview');
        const tabActivo = document.getElementById('prodTabActivo');

        if (tabP) tabP.value = p;
        if (tabR) tabR.value = r;
        if (tabN) tabN.value = n;

        const parts = [];
        if (p) parts.push('P' + p.replace(/^P/i, ''));
        if (r) parts.push('R' + r.replace(/^R/i, ''));
        if (n) parts.push('N' + n.replace(/^N/i, ''));
        const code = parts.join('-') || '';

        if (tabCode) {
            if (code) { tabCode.textContent = code; tabCode.classList.remove('empty'); }
            else { tabCode.textContent = 'Sin ubicaci\\u00f3n asignada'; tabCode.classList.add('empty'); }
        }
        if (tabNotas) tabNotas.textContent = (document.getElementById('prodFormNotasInternas')?.value || '').trim() || '-';
        if (tabActivo) tabActivo.checked = document.getElementById('prodFormActivo')?.checked !== false;
    }

    // === Auto-assign next ubicación ===
    function getNextAutoUbicacion() {
        // Parse all existing ubicaciones to find the highest P-R-N
        const maxNivelesPorRack = 5;
        const maxRacksPorPasillo = 10;

        let maxPasillo = 0, maxRack = 0, maxNivel = 0;
        let found = false;

        productosData.forEach(p => {
            const pp = String(p.ubiPasillo || '').replace(/^P/i, '').trim();
            const rr = String(p.ubiRack || '').replace(/^R/i, '').trim();
            const nn = String(p.ubiNivel || '').replace(/^N/i, '').trim();
            if (!pp && !rr && !nn) return;
            found = true;
            const pNum = parseInt(pp) || 0;
            const rNum = parseInt(rr) || 0;
            const nNum = parseInt(nn) || 0;
            // Find the "highest" location using combined value
            const val = pNum * 10000 + rNum * 100 + nNum;
            const curMax = maxPasillo * 10000 + maxRack * 100 + maxNivel;
            if (val > curMax) {
                maxPasillo = pNum;
                maxRack = rNum;
                maxNivel = nNum;
            }
        });

        if (!found) return { pasillo: '1', rack: '1', nivel: '1' };

        // Increment: N+1, if overflow -> R+1 N=1, if overflow -> P+1 R=1 N=1
        let nextN = maxNivel + 1;
        let nextR = maxRack;
        let nextP = maxPasillo;

        if (nextN > maxNivelesPorRack) {
            nextN = 1;
            nextR = maxRack + 1;
        }
        if (nextR > maxRacksPorPasillo) {
            nextR = 1;
            nextP = maxPasillo + 1;
        }

        return { pasillo: String(nextP || 1), rack: String(nextR || 1), nivel: String(nextN || 1) };
    }

    function autoAssignUbicacion() {
        const p = document.getElementById('prodFormUbiPasillo');
        const r = document.getElementById('prodFormUbiRack');
        const n = document.getElementById('prodFormUbiNivel');
        // Only auto-assign if all fields are empty
        if ((p?.value || '').trim() || (r?.value || '').trim() || (n?.value || '').trim()) return;
        const next = getNextAutoUbicacion();
        if (p) p.value = next.pasillo;
        if (r) r.value = next.rack;
        if (n) n.value = next.nivel;
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

        document.getElementById('confirmUbiNombreProducto').textContent = nombre;
        document.getElementById('confirmUbiCodigoProducto').textContent = codigo;
        document.getElementById('confirmUbiPasillo').value = p || '1';
        document.getElementById('confirmUbiRack').value = r || '1';
        document.getElementById('confirmUbiNivel').value = n || '1';
        updateConfirmUbiPreview();

        popup.style.display = 'flex';
        popup.setAttribute('aria-hidden', 'false');
    }

    function updateConfirmUbiPreview() {
        const p = (document.getElementById('confirmUbiPasillo')?.value || '').trim().toUpperCase();
        const r = (document.getElementById('confirmUbiRack')?.value || '').trim().toUpperCase();
        const n = (document.getElementById('confirmUbiNivel')?.value || '').trim().toUpperCase();
        const parts = [];
        if (p) parts.push('P' + p.replace(/^P/i, ''));
        if (r) parts.push('R' + r.replace(/^R/i, ''));
        if (n) parts.push('N' + n.replace(/^N/i, ''));
        const code = parts.join('-') || 'SIN UBICACI\\u00d3N';
        const grande = document.getElementById('confirmUbiCodigoGrande');
        const preview = document.getElementById('confirmUbiUpdatePreview');
        if (grande) grande.textContent = code;
        if (preview) preview.textContent = '';
    }

    function closeConfirmUbicacion(accepted) {
        const popup = document.getElementById('popupConfirmarUbicacion');
        if (popup) { popup.style.display = 'none'; popup.setAttribute('aria-hidden', 'true'); }

        if (accepted && _commitAfterConfirm) {
            // Write confirmed values back to step-1 fields
            const cp = (document.getElementById('confirmUbiPasillo')?.value || '').trim().toUpperCase();
            const cr = (document.getElementById('confirmUbiRack')?.value || '').trim().toUpperCase();
            const cn = (document.getElementById('confirmUbiNivel')?.value || '').trim().toUpperCase();
            const p1 = document.getElementById('prodFormUbiPasillo');
            const r1 = document.getElementById('prodFormUbiRack');
            const n1 = document.getElementById('prodFormUbiNivel');
            if (p1) p1.value = cp;
            if (r1) r1.value = cr;
            if (n1) n1.value = cn;
            updateUbicacionCodigo();
            syncUbicacionToStep2();
            _commitAfterConfirm();
        }
        _commitAfterConfirm = null;
    }

'''

do_replace(
    "    // === Costo promedio autom\u00e1tico para insumos ===",
    js_new + "    // === Costo promedio autom\u00e1tico para insumos ===",
    "Insert sync/autoAssign/confirm JS functions"
)

# ======================================================================
# 5. Intercept save button to show confirmation popup
# ======================================================================
print("\n--- PART 5: Intercept save ---")

do_replace(
    """    if (prodTabGuardarProducto) {
        prodTabGuardarProducto.addEventListener('click', () => {
            if (!prodPendingTabuladorId) {
                alert('Selecciona un tabulador.');
                return;
            }
            commitPendingProduct();
        });
    }""",
    """    if (prodTabGuardarProducto) {
        prodTabGuardarProducto.addEventListener('click', () => {
            if (!prodPendingTabuladorId) {
                alert('Selecciona un tabulador.');
                return;
            }
            showConfirmUbicacion(() => commitPendingProduct());
        });
    }""",
    "Intercept save with confirmation popup"
)

# ======================================================================
# 6. Event listeners for confirmation popup
# ======================================================================
print("\n--- PART 6: Confirmation popup listeners ---")

do_replace(
    """    const etiquetaBtn = document.getElementById('prodFormGenerarEtiquetaBtn');
    if (etiquetaBtn) etiquetaBtn.addEventListener('click', () => generarEtiquetaUbicacion());""",
    """    const etiquetaBtn = document.getElementById('prodFormGenerarEtiquetaBtn');
    if (etiquetaBtn) etiquetaBtn.addEventListener('click', () => generarEtiquetaUbicacion());

    // Confirmation popup listeners
    const confirmUbiAceptar = document.getElementById('confirmUbiAceptar');
    const confirmUbiCancelar = document.getElementById('confirmUbiCancelar');
    if (confirmUbiAceptar) confirmUbiAceptar.addEventListener('click', () => closeConfirmUbicacion(true));
    if (confirmUbiCancelar) confirmUbiCancelar.addEventListener('click', () => closeConfirmUbicacion(false));
    ['confirmUbiPasillo', 'confirmUbiRack', 'confirmUbiNivel'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('input', () => updateConfirmUbiPreview());
    });
    const popupConfirmUbi = document.getElementById('popupConfirmarUbicacion');
    if (popupConfirmUbi) popupConfirmUbi.addEventListener('click', (e) => { if (e.target === popupConfirmUbi) closeConfirmUbicacion(false); });""",
    "Add confirmation popup event listeners"
)

# ======================================================================
# 7. Auto-assign ubicación when opening NEW product form
# ======================================================================
print("\n--- PART 7: Auto-assign on new product ---")

# Find where the new product form opens — resetProdForm is called
do_replace(
    "        updateRecetaResumen();\n        updateProcesosResumen();\n        updateProcesoInsumosResumen();\n        if (prodGfCobroTipo) prodGfCobroTipo.value = 'm2';",
    "        updateRecetaResumen();\n        updateProcesosResumen();\n        updateProcesoInsumosResumen();\n        autoAssignUbicacion();\n        if (prodGfCobroTipo) prodGfCobroTipo.value = 'm2';",
    "Auto-assign ubicación on new product creation"
)

# ======================================================================
# 8. Widen step-2 photo pane to match step-1
# ======================================================================
print("\n--- PART 8: Widen step-2 layout ---")

do_replace(
    """        .prod-tab-step-layout {
            display: grid;
            grid-template-columns: 280px minmax(0, 1fr);
            gap: 12px;
            align-items: start;
        }""",
    """        .prod-tab-step-layout {
            display: grid;
            grid-template-columns: 180px minmax(0, 1fr);
            gap: 10px;
            align-items: stretch;
        }""",
    "Widen step-2 to match step-1 photo pane width"
)

# ======================================================================
# WRITE
# ======================================================================
with open('mockup.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n=== {changes} changes applied. Size: {original} -> {len(content)} ===")
