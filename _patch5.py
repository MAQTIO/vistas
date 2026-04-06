#!/usr/bin/env python3
"""Patch 5: Add insumos enlazados to Proceso type + prompt in order flow."""
import sys

with open('mockup.html', 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)
changes = 0

def do_replace(old, new, desc, count=1):
    global content, changes
    n = content.count(old)
    if n == 0:
        print(f"FAIL [{changes+1}] {desc}: pattern not found!")
        sys.exit(1)
    content = content.replace(old, new, count) if count == 1 else content.replace(old, new)
    changes += 1
    print(f"  [{changes}] {desc} (found {n})")

# ======================================================================
# 1. Add "Insumos enlazados" button+summary to the Proceso form
#    Insert it in the HTML before the Descripcion field, only for proceso
# ======================================================================
print("\n--- PART 1: HTML button for Insumos del Proceso ---")

# Insert after the "Desgaste" field (data-nat="insumo"), before Descripcion
old_before_desc = '                    <div class="orden-field prod-stock-only productos-field-span3" data-nat="producto,fabricado,insumo,proceso,servicio"><label for="prodFormDescripcion">Descripci\u00f3n</label>'

new_proceso_insumos_btn = '''                    <div class="orden-field productos-field-span3" data-nat="proceso"><label style="margin-bottom:2px;">\U0001f9f0 Insumos del proceso</label><div style="display:flex;align-items:center;gap:6px;"><button type="button" id="prodFormProcesoInsumosBtn" class="productos-btn" style="padding:6px 14px;font-size:0.62rem;background:#059669;color:#fff;border:none;border-radius:6px;">\U0001f9f0 Enlazar insumos</button><span id="prodFormProcesoInsumosResumen" style="font-size:0.55rem;color:#9ca3af;flex:1;">Sin insumos enlazados</span></div><div id="prodFormProcesoInsumosPreview" style="margin-top:4px;font-size:0.6rem;"></div></div>
                    <div class="orden-field prod-stock-only productos-field-span3" data-nat="producto,fabricado,insumo,proceso,servicio"><label for="prodFormDescripcion">Descripci\u00f3n</label>'''

do_replace(old_before_desc, new_proceso_insumos_btn, "Add Insumos del proceso button to form")

# ======================================================================
# 2. Add popup HTML for Insumos del Proceso (reuse pattern from Receta)
# ======================================================================
print("\n--- PART 2: Popup HTML for Insumos del Proceso ---")

popup_proceso_insumos = '''
<!-- ============ POPUP: INSUMOS DEL PROCESO ============ -->
<div id="popupProcesoInsumos" class="productos-modal-overlay" aria-hidden="true" style="z-index:2200;">
    <div class="productos-modal-card wide" role="dialog" aria-modal="true" style="max-width:980px;padding:0;overflow:hidden;border:1px solid #e5e7eb;max-height:92dvh;display:flex;flex-direction:column;">
        <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 18px 10px;border-bottom:2px solid #059669;background:#fff;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:1rem;">\U0001f9f0</span>
                <h3 style="margin:0;font-size:0.82rem;font-weight:900;color:#1f2937;text-transform:uppercase;letter-spacing:0.2px;">Insumos del proceso</h3>
            </div>
            <div style="display:flex;gap:6px;align-items:center;">
                <span id="procInsumoBadge" style="background:#ecfdf5;color:#059669;padding:2px 10px;border-radius:20px;font-size:0.58rem;font-weight:700;border:1px solid #6ee7b7;">0 insumos</span>
                <button type="button" id="procInsumoPopupClose" style="background:none;border:none;font-size:1.1rem;cursor:pointer;color:#6b7280;padding:4px;">\u2715</button>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;flex:1;min-height:0;overflow:hidden;">
            <!-- LEFT: Buscar insumos -->
            <div style="display:flex;flex-direction:column;border-right:1px solid #e5e7eb;overflow:hidden;">
                <div style="padding:8px 12px;background:#f9fafb;border-bottom:1px solid #eee;">
                    <div style="font-size:0.68rem;font-weight:800;color:#374151;margin-bottom:4px;">\U0001f50d Buscar insumos disponibles</div>
                    <input id="procInsumoSearchInput" type="text" placeholder="Buscar por nombre, c\u00f3digo o categor\u00eda..." style="width:100%;padding:6px 10px;border:1px solid #d1d5db;border-radius:6px;font-size:0.65rem;">
                </div>
                <div style="flex:1;overflow-y:auto;min-height:0;">
                    <table style="width:100%;border-collapse:collapse;">
                        <thead style="position:sticky;top:0;background:#f3f4f6;z-index:1;">
                            <tr>
                                <th style="padding:6px 8px;font-size:0.58rem;text-align:left;color:#6b7280;border-bottom:1px solid #e5e7eb;">C\u00f3digo</th>
                                <th style="padding:6px 8px;font-size:0.58rem;text-align:left;color:#6b7280;border-bottom:1px solid #e5e7eb;">Insumo</th>
                                <th style="padding:6px 8px;font-size:0.58rem;text-align:center;color:#6b7280;border-bottom:1px solid #e5e7eb;">Existencias</th>
                                <th style="padding:6px 8px;font-size:0.58rem;text-align:center;color:#6b7280;border-bottom:1px solid #e5e7eb;">Acci\u00f3n</th>
                            </tr>
                        </thead>
                        <tbody id="procInsumoAvailableBody"></tbody>
                    </table>
                </div>
            </div>
            <!-- RIGHT: Insumos enlazados -->
            <div style="display:flex;flex-direction:column;overflow:hidden;">
                <div style="padding:8px 12px;background:#ecfdf5;border-bottom:1px solid #6ee7b7;">
                    <div style="font-size:0.68rem;font-weight:800;color:#065f46;">\u2705 Insumos enlazados al proceso</div>
                    <div style="font-size:0.52rem;color:#047857;margin-top:2px;">Al asignar este proceso a un producto, el cotizador pedir\u00e1 seleccionar cu\u00e1l insumo usar</div>
                </div>
                <div style="flex:1;overflow-y:auto;min-height:0;">
                    <table style="width:100%;border-collapse:collapse;">
                        <thead style="position:sticky;top:0;background:#d1fae5;z-index:1;">
                            <tr>
                                <th style="padding:6px 8px;font-size:0.58rem;text-align:left;color:#065f46;border-bottom:1px solid #6ee7b7;">Insumo</th>
                                <th style="padding:6px 8px;font-size:0.58rem;text-align:center;color:#065f46;border-bottom:1px solid #6ee7b7;">Categor\u00eda</th>
                                <th style="padding:6px 8px;font-size:0.58rem;text-align:center;color:#065f46;border-bottom:1px solid #6ee7b7;">Quitar</th>
                            </tr>
                        </thead>
                        <tbody id="procInsumoLinkedBody"></tbody>
                    </table>
                </div>
                <div id="procInsumoLinkedEmpty" style="flex:1;display:flex;align-items:center;justify-content:center;color:#9ca3af;font-size:0.65rem;padding:20px;">
                    Agrega insumos desde la tabla de la izquierda
                </div>
            </div>
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between;padding:10px 18px;border-top:1px solid #e5e7eb;background:#f9fafb;">
            <span id="procInsumoTotalInfo" style="font-size:0.6rem;color:#6b7280;">0 insumos enlazados</span>
            <div style="display:flex;gap:6px;">
                <button type="button" id="procInsumoAceptar" class="productos-btn primary" style="padding:6px 18px;font-size:0.68rem;background:#059669;">Aceptar</button>
                <button type="button" id="procInsumoCancelar" class="productos-btn gray" style="padding:6px 18px;font-size:0.68rem;">Cancelar</button>
            </div>
        </div>
    </div>
</div>

<!-- ============ POPUP: SELECCION DE INSUMO DEL PROCESO EN COTIZADOR ============ -->
<div id="popupSeleccionInsumoProc" class="productos-modal-overlay" aria-hidden="true" style="z-index:2220;">
    <div class="productos-modal-card" role="dialog" aria-modal="true" style="max-width:520px;padding:0;overflow:hidden;border:1px solid #e5e7eb;max-height:70dvh;display:flex;flex-direction:column;">
        <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 18px 10px;border-bottom:2px solid #059669;background:#fff;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:1rem;">\U0001f9f0</span>
                <h3 id="selInsProcTitulo" style="margin:0;font-size:0.78rem;font-weight:900;color:#1f2937;">Seleccionar insumo para el proceso</h3>
            </div>
            <button type="button" id="selInsProcClose" style="background:none;border:none;font-size:1.1rem;cursor:pointer;color:#6b7280;padding:4px;">\u2715</button>
        </div>
        <div id="selInsProcSubtitle" style="padding:8px 18px;font-size:0.6rem;color:#6b7280;background:#f9fafb;border-bottom:1px solid #eee;">
            Este producto requiere que elijas un insumo para cada proceso asignado.
        </div>
        <div style="flex:1;overflow-y:auto;min-height:0;padding:0;">
            <table style="width:100%;border-collapse:collapse;">
                <thead style="position:sticky;top:0;background:#ecfdf5;z-index:1;">
                    <tr>
                        <th style="padding:8px 12px;font-size:0.6rem;text-align:left;color:#065f46;border-bottom:1px solid #6ee7b7;">Insumo</th>
                        <th style="padding:8px 12px;font-size:0.6rem;text-align:center;color:#065f46;border-bottom:1px solid #6ee7b7;">Existencias</th>
                        <th style="padding:8px 12px;font-size:0.6rem;text-align:center;color:#065f46;border-bottom:1px solid #6ee7b7;">Seleccionar</th>
                    </tr>
                </thead>
                <tbody id="selInsProcBody"></tbody>
            </table>
        </div>
        <div style="padding:10px 18px;border-top:1px solid #e5e7eb;background:#f9fafb;display:flex;justify-content:flex-end;">
            <button type="button" id="selInsProcCancelar" class="productos-btn gray" style="padding:6px 18px;font-size:0.68rem;">Cancelar</button>
        </div>
    </div>
</div>
'''

# Insert before popupProdTabulador
anchor = '<div id="popupProdTabulador" class="productos-modal-overlay" aria-hidden="true">'
do_replace(anchor, popup_proceso_insumos + '\n' + anchor, "Insert Proceso Insumos + Selector popups")

# ======================================================================
# 3. Add JS functions for proceso insumos popup
# ======================================================================
print("\n--- PART 3: JS functions for proceso insumos ---")

js_proc_insumos = '''
    // === Insumos enlazados al Proceso — Popup-based ===
    let procesoInsumosDraft = []; // [{insumoId, insumoNombre, insumoCode, categoria}]
    let procesoInsumosDraftBackup = [];

    function openProcesoInsumosPopup() {
        const popup = document.getElementById('popupProcesoInsumos');
        if (!popup) return;
        procesoInsumosDraftBackup = JSON.parse(JSON.stringify(procesoInsumosDraft));
        popup.style.display = 'flex';
        popup.setAttribute('aria-hidden', 'false');
        renderProcInsumoAvailable();
        renderProcInsumoLinked();
    }

    function closeProcesoInsumosPopup(accept) {
        const popup = document.getElementById('popupProcesoInsumos');
        if (!popup) return;
        if (!accept) procesoInsumosDraft = procesoInsumosDraftBackup;
        popup.style.display = 'none';
        popup.setAttribute('aria-hidden', 'true');
        updateProcesoInsumosResumen();
    }

    function renderProcInsumoAvailable(filter) {
        const tbody = document.getElementById('procInsumoAvailableBody');
        if (!tbody) return;
        const term = (filter || document.getElementById('procInsumoSearchInput')?.value || '').trim().toLowerCase();
        const insumos = productosData.filter(p => p.naturaleza === 'insumo');
        const filtered = term ? insumos.filter(p =>
            [p.codigo, p.producto, p.categoria].some(v => String(v || '').toLowerCase().includes(term))
        ) : insumos;
        if (!filtered.length) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:20px;color:#9ca3af;font-size:0.6rem;">No se encontraron insumos</td></tr>';
            return;
        }
        tbody.innerHTML = filtered.map(ins => {
            const code = ins.codigo || ins.id || '';
            const nombre = ins.producto || ins.id || '';
            const exist = Number(ins.existencias || 0);
            const already = procesoInsumosDraft.some(r => r.insumoId === code);
            return '<tr style="cursor:pointer;' + (already ? 'background:#ecfdf5;' : '') + '">' +
                '<td style="padding:5px 8px;font-size:0.6rem;color:#6b7280;border-bottom:1px solid #f1f5f9;">' + prodEscape(code) + '</td>' +
                '<td style="padding:5px 8px;font-size:0.62rem;font-weight:700;color:#1f2937;border-bottom:1px solid #f1f5f9;">' + prodEscape(nombre) + '</td>' +
                '<td style="padding:5px 8px;font-size:0.6rem;text-align:center;color:' + (exist < 0 ? '#dc2626' : '#059669') + ';font-weight:700;border-bottom:1px solid #f1f5f9;">' + exist + '</td>' +
                '<td style="padding:5px 8px;text-align:center;border-bottom:1px solid #f1f5f9;">' +
                    (already
                        ? '<span style="color:#059669;font-size:0.58rem;font-weight:700;">\\u2713 Enlazado</span>'
                        : '<button type="button" onclick="addInsumoProceso(\\'' + prodEscape(code).replace(/'/g, "\\\\'") + '\\')" class="productos-btn" style="padding:3px 10px;font-size:0.58rem;background:#059669;color:#fff;border:none;border-radius:4px;">+ Enlazar</button>'
                    ) +
                '</td></tr>';
        }).join('');
    }

    window.addInsumoProceso = function(code) {
        const ins = productosData.find(p => p.naturaleza === 'insumo' && (p.codigo === code || p.id === code));
        if (!ins) return;
        if (procesoInsumosDraft.some(r => r.insumoId === code)) return;
        procesoInsumosDraft.push({
            insumoId: code,
            insumoNombre: ins.producto || ins.id || code,
            insumoCode: code,
            categoria: ins.categoria || ''
        });
        renderProcInsumoAvailable();
        renderProcInsumoLinked();
    };

    window.removeInsumoProceso = function(idx) {
        procesoInsumosDraft.splice(idx, 1);
        renderProcInsumoAvailable();
        renderProcInsumoLinked();
    };

    function renderProcInsumoLinked() {
        const tbody = document.getElementById('procInsumoLinkedBody');
        const emptyDiv = document.getElementById('procInsumoLinkedEmpty');
        const badge = document.getElementById('procInsumoBadge');
        const totalInfo = document.getElementById('procInsumoTotalInfo');
        if (!tbody) return;
        if (!procesoInsumosDraft.length) {
            tbody.innerHTML = '';
            if (emptyDiv) emptyDiv.style.display = 'flex';
            if (badge) badge.textContent = '0 insumos';
            if (totalInfo) totalInfo.textContent = '0 insumos enlazados';
            return;
        }
        if (emptyDiv) emptyDiv.style.display = 'none';
        tbody.innerHTML = procesoInsumosDraft.map((r, idx) =>
            '<tr>' +
            '<td style="padding:5px 8px;font-size:0.62rem;font-weight:700;color:#1f2937;border-bottom:1px solid #6ee7b7;">' + prodEscape(r.insumoNombre) + '<div style="font-size:0.5rem;color:#6b7280;">' + prodEscape(r.insumoCode || r.insumoId) + '</div></td>' +
            '<td style="padding:5px 8px;font-size:0.58rem;text-align:center;color:#6b7280;border-bottom:1px solid #6ee7b7;">' + prodEscape(r.categoria || '-') + '</td>' +
            '<td style="padding:5px 8px;text-align:center;border-bottom:1px solid #6ee7b7;"><button type="button" onclick="removeInsumoProceso(' + idx + ')" style="background:none;border:none;color:#ef4444;cursor:pointer;font-size:0.75rem;padding:2px 6px;" title="Quitar">\\u2715</button></td>' +
            '</tr>'
        ).join('');
        if (badge) badge.textContent = procesoInsumosDraft.length + ' insumo' + (procesoInsumosDraft.length !== 1 ? 's' : '');
        if (totalInfo) totalInfo.textContent = procesoInsumosDraft.length + ' insumo' + (procesoInsumosDraft.length !== 1 ? 's' : '') + ' enlazados';
    }

    function updateProcesoInsumosResumen() {
        const resumen = document.getElementById('prodFormProcesoInsumosResumen');
        const preview = document.getElementById('prodFormProcesoInsumosPreview');
        if (resumen) {
            resumen.textContent = procesoInsumosDraft.length
                ? procesoInsumosDraft.length + ' insumo' + (procesoInsumosDraft.length !== 1 ? 's' : '') + ' enlazados'
                : 'Sin insumos enlazados';
            resumen.style.color = procesoInsumosDraft.length ? '#059669' : '#9ca3af';
            resumen.style.fontWeight = procesoInsumosDraft.length ? '700' : '400';
        }
        if (preview) {
            preview.innerHTML = procesoInsumosDraft.map(r =>
                '<span style="display:inline-block;padding:2px 8px;margin:1px 2px;background:#ecfdf5;border:1px solid #6ee7b7;border-radius:12px;font-size:0.55rem;font-weight:600;color:#065f46;">' +
                prodEscape(r.insumoNombre) + '</span>'
            ).join('');
        }
    }

    // === Selector de insumo del proceso en el cotizador ===
    let _selInsProcCallback = null;
    let _selInsProcPending = []; // [{procesoId, procesoNombre, insumosEnlazados, selected}]
    let _selInsProcCurrentIdx = 0;

    function promptSeleccionInsumosProcesos(producto, onComplete) {
        // producto = modelo completo del producto con procesosDetalle
        const procesos = Array.isArray(producto.procesosDetalle) ? producto.procesosDetalle : [];
        if (!procesos.length) { onComplete([]); return; }

        // For each proceso, find the proceso model and its insumosEnlazados
        _selInsProcPending = [];
        procesos.forEach(pd => {
            const procModel = productosData.find(p => p.naturaleza === 'proceso' && (p.producto === pd.procesoId || p.id === pd.procesoId));
            const enlazados = Array.isArray(procModel?.insumosEnlazados) ? procModel.insumosEnlazados : [];
            if (enlazados.length > 0) {
                _selInsProcPending.push({
                    procesoId: pd.procesoId,
                    procesoNombre: pd.procesoNombre || pd.procesoId,
                    insumosEnlazados: enlazados,
                    selected: null
                });
            }
        });

        if (!_selInsProcPending.length) { onComplete([]); return; }

        _selInsProcCallback = onComplete;
        _selInsProcCurrentIdx = 0;
        showNextProcesoInsumoSelection();
    }

    function showNextProcesoInsumoSelection() {
        if (_selInsProcCurrentIdx >= _selInsProcPending.length) {
            // All done
            const popup = document.getElementById('popupSeleccionInsumoProc');
            if (popup) { popup.style.display = 'none'; popup.setAttribute('aria-hidden', 'true'); }
            if (_selInsProcCallback) {
                _selInsProcCallback(_selInsProcPending.map(p => ({
                    procesoId: p.procesoId,
                    procesoNombre: p.procesoNombre,
                    insumoSeleccionado: p.selected
                })));
            }
            return;
        }

        const current = _selInsProcPending[_selInsProcCurrentIdx];
        const popup = document.getElementById('popupSeleccionInsumoProc');
        const titulo = document.getElementById('selInsProcTitulo');
        const subtitle = document.getElementById('selInsProcSubtitle');
        const tbody = document.getElementById('selInsProcBody');

        if (!popup || !tbody) return;

        if (titulo) titulo.textContent = 'Proceso: ' + current.procesoNombre;
        if (subtitle) subtitle.textContent = 'Selecciona el insumo que se usar\\u00e1 en el proceso "' + current.procesoNombre + '" (' + (_selInsProcCurrentIdx + 1) + ' de ' + _selInsProcPending.length + ')';

        tbody.innerHTML = current.insumosEnlazados.map(ins => {
            // Find current stock
            const model = productosData.find(p => p.naturaleza === 'insumo' && (p.codigo === ins.insumoId || p.id === ins.insumoId));
            const nombre = ins.insumoNombre || model?.producto || ins.insumoId;
            const exist = model ? Number(model.existencias || 0) : 0;
            return '<tr style="cursor:pointer;" onclick="selectInsumoForProceso(\\'' + prodEscape(ins.insumoId).replace(/'/g, "\\\\'") + '\\', \\'' + prodEscape(nombre).replace(/'/g, "\\\\'") + '\\')">' +
                '<td style="padding:8px 12px;font-size:0.65rem;font-weight:700;color:#1f2937;border-bottom:1px solid #e5e7eb;">' + prodEscape(nombre) + '</td>' +
                '<td style="padding:8px 12px;font-size:0.62rem;text-align:center;color:' + (exist < 0 ? '#dc2626' : '#059669') + ';font-weight:700;border-bottom:1px solid #e5e7eb;">' + exist + '</td>' +
                '<td style="padding:8px 12px;text-align:center;border-bottom:1px solid #e5e7eb;"><button type="button" class="productos-btn" style="padding:4px 12px;font-size:0.6rem;background:#059669;color:#fff;border:none;border-radius:4px;">Usar este</button></td>' +
                '</tr>';
        }).join('');

        popup.style.display = 'flex';
        popup.setAttribute('aria-hidden', 'false');
    }

    window.selectInsumoForProceso = function(insumoId, insumoNombre) {
        if (_selInsProcCurrentIdx < _selInsProcPending.length) {
            _selInsProcPending[_selInsProcCurrentIdx].selected = { insumoId, insumoNombre };
        }
        _selInsProcCurrentIdx++;
        showNextProcesoInsumoSelection();
    };

    function cancelSeleccionInsumoProc() {
        const popup = document.getElementById('popupSeleccionInsumoProc');
        if (popup) { popup.style.display = 'none'; popup.setAttribute('aria-hidden', 'true'); }
        _selInsProcPending = [];
        _selInsProcCallback = null;
    }

'''

# Insert before the costo promedio function
anchor_costo = "    // === Costo promedio autom\u00e1tico para insumos ==="
do_replace(anchor_costo, js_proc_insumos + "\n" + anchor_costo, "Insert proceso insumos JS functions")

# ======================================================================
# 4. Add event listeners for popup
# ======================================================================
print("\n--- PART 4: Event listeners ---")

old_procesos_listener = """    // Procesos popup button
    const procesosBtn = document.getElementById('prodFormProcesosBtn');
    if (procesosBtn) procesosBtn.addEventListener('click', () => openProcesosPopup());"""

new_all_listeners = """    // Procesos popup button
    const procesosBtn = document.getElementById('prodFormProcesosBtn');
    if (procesosBtn) procesosBtn.addEventListener('click', () => openProcesosPopup());

    // Proceso-Insumos popup button
    const procInsBtn = document.getElementById('prodFormProcesoInsumosBtn');
    if (procInsBtn) procInsBtn.addEventListener('click', () => openProcesoInsumosPopup());
    const procInsumoClose = document.getElementById('procInsumoPopupClose');
    const procInsumoCancelar = document.getElementById('procInsumoCancelar');
    const procInsumoAceptar = document.getElementById('procInsumoAceptar');
    if (procInsumoClose) procInsumoClose.addEventListener('click', () => closeProcesoInsumosPopup(false));
    if (procInsumoCancelar) procInsumoCancelar.addEventListener('click', () => closeProcesoInsumosPopup(false));
    if (procInsumoAceptar) procInsumoAceptar.addEventListener('click', () => closeProcesoInsumosPopup(true));
    const procInsumoSearch = document.getElementById('procInsumoSearchInput');
    if (procInsumoSearch) procInsumoSearch.addEventListener('input', () => renderProcInsumoAvailable());
    const popupProcIns = document.getElementById('popupProcesoInsumos');
    if (popupProcIns) popupProcIns.addEventListener('click', (e) => { if (e.target === popupProcIns) closeProcesoInsumosPopup(false); });

    // Cotizador insumo selection popup
    const selInsProcClose = document.getElementById('selInsProcClose');
    const selInsProcCancelar = document.getElementById('selInsProcCancelar');
    if (selInsProcClose) selInsProcClose.addEventListener('click', () => cancelSeleccionInsumoProc());
    if (selInsProcCancelar) selInsProcCancelar.addEventListener('click', () => cancelSeleccionInsumoProc());
    const popupSelIns = document.getElementById('popupSeleccionInsumoProc');
    if (popupSelIns) popupSelIns.addEventListener('click', (e) => { if (e.target === popupSelIns) cancelSeleccionInsumoProc(); });"""

do_replace(old_procesos_listener, new_all_listeners, "Add proceso insumos event listeners")

# ======================================================================
# 5. Add insumosEnlazados to payload
# ======================================================================
print("\n--- PART 5: Update payload ---")

do_replace(
    "            desgastePorUso: Math.max(0, Number(document.getElementById('prodFormDesgastePorUso')?.value || 0)),",
    "            desgastePorUso: Math.max(0, Number(document.getElementById('prodFormDesgastePorUso')?.value || 0)),\n            insumosEnlazados: (prodFormNaturaleza?.value === 'proceso') ? [...procesoInsumosDraft] : [],",
    "Add insumosEnlazados to payload"
)

# ======================================================================
# 6. Add procesoInsumosDraft to reset
# ======================================================================
print("\n--- PART 6: Update form reset ---")

do_replace(
    "        recetaDraft = []; procesosDraft = [];",
    "        recetaDraft = []; procesosDraft = []; procesoInsumosDraft = [];",
    "Clear procesoInsumosDraft on reset"
)

# ======================================================================
# 7. Add procesoInsumosDraft to edit load
# ======================================================================
print("\n--- PART 7: Update form edit load ---")

do_replace(
    "        updateRecetaResumen();\n        updateProcesosResumen();",
    "        procesoInsumosDraft = Array.isArray(row.insumosEnlazados) ? row.insumosEnlazados.map(i => ({insumoId: i.insumoId || '', insumoNombre: i.insumoNombre || i.insumoId || '', insumoCode: i.insumoCode || i.insumoId || '', categoria: i.categoria || ''})) : [];\n        updateRecetaResumen();\n        updateProcesosResumen();\n        updateProcesoInsumosResumen();",
    "Load procesoInsumosDraft on edit"
)

# Also update form clear resumen
do_replace(
    "        updateRecetaResumen();\n        updateProcesosResumen();",
    "        updateRecetaResumen();\n        updateProcesosResumen();\n        updateProcesoInsumosResumen();",
    "Update procesoInsumosResumen on clear",
    count=1  # Only the first occurrence (in clear), the edit one was already updated
)

# ======================================================================
# 8. Modify addLineaDesdeStockSeleccion to prompt for proceso insumos
# ======================================================================
print("\n--- PART 8: Add proceso insumo prompt in order flow ---")

old_add_linea = """    const addLineaDesdeStockSeleccion = () => {
        const producto = getProductoStockSeleccionadoOrden();
        if (!producto) {
            alert('Selecciona un producto.');
            return;
        }

        const qty = Math.max(1, Math.floor(Number(ordenStockQty || 1)));
        const available = Math.max(0, Number(producto.existencias || 0));
        if (qty > available) {
            alert(`No hay suficiente stock. Existencias disponibles: ${available}.`);
            return;
        }

        ordenLineas.push({
            producto: producto.producto || 'Producto de stock',
            medida: producto.medida || '-',
            material: producto.material || '-',
            precio: getPrecioProductoStockOrden(producto),
            cantidad: qty,
            productoId: producto.sourceType === 'producto' ? producto.id : '',
            sourceType: producto.sourceType || 'producto',
            linkedInsumoId: producto.linkedInsumoId || ''
        });
        ordenLineaActiva = ordenLineas.length - 1;
        renderTabla();
        closeOrdenStockPopup();
    };"""

new_add_linea = """    const addLineaDesdeStockSeleccion = () => {
        const producto = getProductoStockSeleccionadoOrden();
        if (!producto) {
            alert('Selecciona un producto.');
            return;
        }

        const qty = Math.max(1, Math.floor(Number(ordenStockQty || 1)));
        const available = Math.max(0, Number(producto.existencias || 0));
        if (qty > available) {
            alert(`No hay suficiente stock. Existencias disponibles: ${available}.`);
            return;
        }

        // Check if product has procesos with insumosEnlazados
        const productoModel = productosData.find(p => p.id === producto.id) || producto;
        const tieneProcesoConInsumos = Array.isArray(productoModel.procesosDetalle) &&
            productoModel.procesosDetalle.some(pd => {
                const procModel = productosData.find(p => p.naturaleza === 'proceso' && (p.producto === pd.procesoId || p.id === pd.procesoId));
                return Array.isArray(procModel?.insumosEnlazados) && procModel.insumosEnlazados.length > 0;
            });

        if (tieneProcesoConInsumos) {
            // Prompt user to select insumo for each proceso
            promptSeleccionInsumosProcesos(productoModel, (selecciones) => {
                ordenLineas.push({
                    producto: producto.producto || 'Producto de stock',
                    medida: producto.medida || '-',
                    material: producto.material || '-',
                    precio: getPrecioProductoStockOrden(producto),
                    cantidad: qty,
                    productoId: producto.sourceType === 'producto' ? producto.id : '',
                    sourceType: producto.sourceType || 'producto',
                    linkedInsumoId: producto.linkedInsumoId || '',
                    insumosProcesoSeleccionados: selecciones
                });
                ordenLineaActiva = ordenLineas.length - 1;
                renderTabla();
                closeOrdenStockPopup();
            });
            return;
        }

        ordenLineas.push({
            producto: producto.producto || 'Producto de stock',
            medida: producto.medida || '-',
            material: producto.material || '-',
            precio: getPrecioProductoStockOrden(producto),
            cantidad: qty,
            productoId: producto.sourceType === 'producto' ? producto.id : '',
            sourceType: producto.sourceType || 'producto',
            linkedInsumoId: producto.linkedInsumoId || ''
        });
        ordenLineaActiva = ordenLineas.length - 1;
        renderTabla();
        closeOrdenStockPopup();
    };"""

do_replace(old_add_linea, new_add_linea, "Add proceso insumo prompt in order flow")

# ======================================================================
# 9. Update syncProdFormModeByTipo to show resumen for proceso
# ======================================================================
print("\n--- PART 9: Show resumen in proceso mode ---")

do_replace(
    """        } else if (nat === 'proceso') {
            // PROCESO: pocos campos \u2014 expandir descripci\u00f3n
            if (nombreWrap) nombreWrap.style.gridColumn = 'span 3';""",
    """        } else if (nat === 'proceso') {
            // PROCESO: pocos campos \u2014 expandir descripci\u00f3n
            if (nombreWrap) nombreWrap.style.gridColumn = 'span 3';
            updateProcesoInsumosResumen();""",
    "Update proceso insumos resumen on type switch"
)

# ======================================================================
# WRITE
# ======================================================================
with open('mockup.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n=== Total: {changes} changes applied to disk! ===")
print(f"File size: {original_len} -> {len(content)} bytes")
