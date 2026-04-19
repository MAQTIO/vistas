#!/usr/bin/env python3
"""
1. Remove 'Puntos medios' section from ubicaciones popup
2. Add a first-step location type selector when 'Requiere envío' is checked
   before showing the cotizador
"""

with open('/workspaces/vistas/mockup.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════════
# 1. REMOVE "Puntos medios" section from ubicaciones popup
# ═══════════════════════════════════════════════════════════════
pm_section_start = '<!-- Puntos medios — compact at bottom -->'
pm_section_end = '</div>\n                </div>\n            </div>\n\n            <!-- RIGHT PANEL'

# More reliable: find the exact div
old_pm = '''                <!-- Puntos medios — compact at bottom -->
                <div id="ubiPuntosMediosSection" style="padding:6px 14px 10px;border-top:1px solid #e5e7eb;flex-shrink:0;">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;">
                        <div style="font-size:0.4rem;font-weight:800;color:#6b7280;text-transform:uppercase;letter-spacing:0.06em;">
                            Puntos medios</div>
                        <button id="ubiAddPuntoMedio" type="button" style="background:#ff9900;color:#fff;border:none;
                            border-radius:5px;padding:3px 8px;font-size:0.38rem;font-weight:800;cursor:pointer;">+ Nuevo</button>
                    </div>
                    <div id="ubiPuntosMediosLista" style="max-height:60px;overflow-y:auto;display:flex;flex-direction:column;gap:3px;">
                        <div style="font-size:0.38rem;color:#9ca3af;text-align:center;padding:4px;">No hay puntos medios</div>
                    </div>
                </div>'''

if old_pm in html:
    html = html.replace(old_pm, '')
    print("✅ Removed puntos medios section from popup")
else:
    print("⚠️ Could not find puntos medios section to remove")

# ═══════════════════════════════════════════════════════════════
# 2. MODIFY the chkEnvio handler to show location selector FIRST
# ═══════════════════════════════════════════════════════════════

# Replace the chkEnvio change handler
old_handler = '''        if (chkEnvio) {
            chkEnvio.addEventListener('change', () => {
                if (chkEnvio.checked) {
                    showEnvioPopup((val) => {
                        if (val === null || val === 0) { chkEnvio.checked = false; window.costoEnvio = 0; removeEnvioFromOrdenLineas(); }
                        // costoEnvio stays 0 because addEnvioToOrdenLineas handles the cost via the table row
                        updateExtraCosts();
                    });
                } else {
                    window.costoEnvio = 0;
                    window._envioSeleccionado = null;
                    removeEnvioFromOrdenLineas();
                    updateExtraCosts();
                }
            });
        }'''

new_handler = '''        if (chkEnvio) {
            chkEnvio.addEventListener('change', () => {
                if (chkEnvio.checked) {
                    showEnvioDirSelector((tipoDir) => {
                        if (!tipoDir) { chkEnvio.checked = false; return; }
                        window._envioTipoDirSeleccionado = tipoDir;
                        showEnvioPopup((val) => {
                            if (val === null || val === 0) { chkEnvio.checked = false; window.costoEnvio = 0; removeEnvioFromOrdenLineas(); }
                            updateExtraCosts();
                        });
                    });
                } else {
                    window.costoEnvio = 0;
                    window._envioSeleccionado = null;
                    window._envioTipoDirSeleccionado = null;
                    removeEnvioFromOrdenLineas();
                    updateExtraCosts();
                }
            });
        }'''

if old_handler in html:
    html = html.replace(old_handler, new_handler)
    print("✅ Replaced chkEnvio handler with location selector step")
else:
    print("⚠️ Could not find chkEnvio handler")

# ═══════════════════════════════════════════════════════════════
# 3. ADD showEnvioDirSelector function before showEnvioPopup
# ═══════════════════════════════════════════════════════════════

insert_before = "    const showEnvioPopup = (cb) => {"
insert_idx = html.index(insert_before)

new_selector_fn = r'''    // ═══ STEP 1: Location type selector before cotizador ═══
    const showEnvioDirSelector = (cb) => {
        const existing = document.getElementById('envioDirSelectorOverlay');
        if (existing) existing.remove();

        // Get client data
        const clienteIdEl = document.getElementById('ordenClienteId');
        const clienteId = clienteIdEl ? clienteIdEl.value : '';
        let allClientes = [];
        try { allClientes = JSON.parse(localStorage.getItem('mock_clientes_modulo_v1') || '[]'); } catch(_) {}
        const cliente = allClientes.find(c => String(c.id || '').trim() === clienteId) || {};
        const clienteNombre = document.getElementById('ordenClienteNombre')?.value || cliente.nombre || 'Cliente';

        const tieneUbiDomicilio = !!(cliente.ubiDomicilio || '').trim();
        const tieneUbiNegocio = !!(cliente.ubiNegocio || '').trim();
        const tieneUbiPuntoMedio = !!(cliente.ubiPuntoMedio || '').trim();

        const overlay = document.createElement('div');
        overlay.id = 'envioDirSelectorOverlay';
        overlay.style.cssText = 'position:fixed;inset:0;z-index:200010;background:rgba(0,0,0,0.55);display:flex;align-items:center;justify-content:center;padding:16px;animation:fadeIn 0.15s ease;';

        const buildCard = (tipo, icon, label, sublabel, color, hasData) => {
            const addr = hasData ? (tipo === 'domicilio' ? cliente.ubiDomicilio : tipo === 'negocio' ? cliente.ubiNegocio : cliente.ubiPuntoMedio) : '';
            const statusDot = hasData
                ? '<span style="width:8px;height:8px;border-radius:50%;background:#22c55e;display:inline-block;"></span>'
                : '<span style="width:8px;height:8px;border-radius:50%;background:#d1d5db;display:inline-block;"></span>';
            const addrText = hasData && addr
                ? '<div style="font-size:0.52rem;color:#6b7280;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:260px;">' + addr.replace(/</g,'&lt;') + '</div>'
                : '<div style="font-size:0.48rem;color:#d1d5db;margin-top:4px;font-style:italic;">Sin dirección registrada</div>';
            return `<button class="envio-dir-step1-btn" data-dir-tipo="${tipo}" style="display:flex;align-items:center;gap:14px;
                padding:16px 18px;background:#fff;border:2px solid ${hasData ? color : '#e5e7eb'};border-radius:14px;cursor:pointer;
                text-align:left;width:100%;transition:all 0.2s;${!hasData ? 'opacity:0.5;' : ''}"
                ${!hasData ? 'disabled' : ''}>
                <div style="width:52px;height:52px;border-radius:14px;background:linear-gradient(135deg,${color}22,${color}44);
                    display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0;">${icon}</div>
                <div style="flex:1;min-width:0;">
                    <div style="display:flex;align-items:center;gap:6px;">
                        <span style="font-size:0.65rem;font-weight:800;color:#1f2937;">${label}</span>
                        ${statusDot}
                    </div>
                    <div style="font-size:0.44rem;color:#9ca3af;">${sublabel}</div>
                    ${addrText}
                </div>
                <div style="color:${hasData ? color : '#d1d5db'};font-size:1rem;">&rsaquo;</div>
            </button>`;
        };

        overlay.innerHTML = `<div style="background:#fff;border-radius:18px;max-width:480px;width:94%;
            box-shadow:0 24px 80px rgba(0,0,0,0.35);overflow:hidden;">
            <div style="background:linear-gradient(135deg,#ff9900,#e68a00);padding:18px 24px 14px;">
                <div style="font-size:0.82rem;font-weight:900;color:#fff;">📦 ¿A DÓNDE SE ENVÍA?</div>
                <div style="font-size:0.46rem;color:rgba(255,255,255,0.85);margin-top:2px;">
                    Cliente: <strong>${clienteNombre.replace(/</g,'&lt;')}</strong> — Selecciona el tipo de dirección</div>
            </div>
            <div style="padding:16px 20px;display:flex;flex-direction:column;gap:8px;">
                ${buildCard('domicilio', '🏠', 'DOMICILIO', 'Dirección de casa del cliente', '#f59e0b', tieneUbiDomicilio)}
                ${buildCard('negocio', '🏢', 'NEGOCIO', 'Dirección del negocio o trabajo', '#3b82f6', tieneUbiNegocio)}
                ${buildCard('puntoMedio', '📌', 'PUNTO MEDIO', 'Punto de entrega acordado', '#ec4899', tieneUbiPuntoMedio)}
                <button class="envio-dir-step1-btn" data-dir-tipo="nueva" style="display:flex;align-items:center;gap:14px;
                    padding:14px 18px;background:#f9fafb;border:2px dashed #d1d5db;border-radius:14px;cursor:pointer;
                    text-align:left;width:100%;transition:all 0.2s;">
                    <div style="width:52px;height:52px;border-radius:14px;background:#f3f4f6;
                        display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0;">➕</div>
                    <div style="flex:1;">
                        <div style="font-size:0.65rem;font-weight:800;color:#374151;">NUEVA DIRECCIÓN</div>
                        <div style="font-size:0.44rem;color:#9ca3af;">Ingresar dirección manualmente</div>
                    </div>
                    <div style="color:#9ca3af;font-size:1rem;">&rsaquo;</div>
                </button>
            </div>
            <div style="padding:8px 20px 16px;display:flex;justify-content:flex-end;">
                <button id="envioDirSelectorCancel" type="button" style="padding:8px 20px;background:#6b7280;color:#fff;
                    border:none;border-radius:8px;font-weight:700;font-size:0.5rem;cursor:pointer;">CANCELAR</button>
            </div>
        </div>`;

        document.body.appendChild(overlay);

        // Hover effects
        overlay.querySelectorAll('.envio-dir-step1-btn:not([disabled])').forEach(btn => {
            btn.addEventListener('mouseenter', () => { btn.style.transform = 'scale(1.01)'; btn.style.boxShadow = '0 4px 16px rgba(0,0,0,0.08)'; });
            btn.addEventListener('mouseleave', () => { btn.style.transform = ''; btn.style.boxShadow = ''; });
        });

        // Click handlers
        overlay.querySelectorAll('.envio-dir-step1-btn:not([disabled])').forEach(btn => {
            btn.addEventListener('click', () => {
                const tipo = btn.dataset.dirTipo;
                overlay.remove();
                cb(tipo);
            });
        });

        document.getElementById('envioDirSelectorCancel').addEventListener('click', () => {
            overlay.remove();
            cb(null);
        });

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) { overlay.remove(); cb(null); }
        });
    };

'''

html = html[:insert_idx] + new_selector_fn + html[insert_idx:]
print("✅ Added showEnvioDirSelector function")

# ═══════════════════════════════════════════════════════════════
# 4. MODIFY showEnvioPopup to auto-select the pre-chosen direction
# ═══════════════════════════════════════════════════════════════
# After the envio popup is appended to body and direction buttons are wired,
# add auto-click for the pre-selected direction type.
# Find where the dir selector buttons are handled and add auto-trigger.

# The dir selector inline section in showEnvioPopup starts with opcionesDirHtml
# We need to find where the overlay is appended and direction buttons are set up.
# Look for the line after overlay.querySelectorAll('.envio-dir-btn').forEach(btn => { block ends

# Instead, let's add a simple auto-trigger right after "renderPresets();" which is after the overlay setup
auto_trigger_marker = "        renderPresets();\n\n        // ===== AUTOGUARDADO"
auto_trigger_code = """        renderPresets();

        // Auto-select direction type if pre-chosen from step 1
        if (window._envioTipoDirSeleccionado) {
            const preDir = window._envioTipoDirSeleccionado;
            setTimeout(() => {
                const targetBtn = overlay.querySelector('.envio-dir-btn[data-dir="' + preDir + '"]');
                if (targetBtn) { targetBtn.click(); }
                else if (preDir === 'nueva') {
                    const nuevaBtn = overlay.querySelector('.envio-dir-btn[data-dir="nueva"]');
                    if (nuevaBtn) nuevaBtn.click();
                }
            }, 50);
        }

        // ===== AUTOGUARDADO"""

if auto_trigger_marker in html:
    html = html.replace(auto_trigger_marker, auto_trigger_code)
    print("✅ Added auto-trigger for pre-selected direction")
else:
    print("⚠️ Could not find auto-trigger insertion point")

# ═══════════════════════════════════════════════════════════════
# 5. ALSO REMOVE JS references to puntos medios in ubi popup
# ═══════════════════════════════════════════════════════════════

# Remove renderPuntosMediosPopup calls from ubicaciones open
old_render_pm = "                renderPuntosMediosPopup();\n"
# Only remove the one in ubicaciones open handler
old_open_call = """                setTimeout(() => {
                    ubiInitMap();
                    ubiRefreshMarkers();
                }, 100);
                renderPuntosMediosPopup();"""
new_open_call = """                setTimeout(() => {
                    ubiInitMap();
                    ubiRefreshMarkers();
                }, 100);"""

if old_open_call in html:
    html = html.replace(old_open_call, new_open_call)
    print("✅ Removed renderPuntosMediosPopup from open handler")

# Remove renderPuntosMediosPopup from editor save (punto medio)
old_pm_save_render = """                renderPuntosMediosPopup();
            }
            ubiRefreshCards();"""
new_pm_save_render = """            }
            ubiRefreshCards();"""

if old_pm_save_render in html:
    html = html.replace(old_pm_save_render, new_pm_save_render)
    print("✅ Removed renderPuntosMediosPopup from save handler")

# Remove the standalone renderPuntosMediosPopup function and ubiAddPuntoMedio handler
old_render_fn = """    // Render puntos medios list
    const renderPuntosMediosPopup = () => {
        const lista = document.getElementById('ubiPuntosMediosLista');
        if (!lista) return;
        const pms = getPuntosMedios();
        if (!pms.length) {
            lista.innerHTML = '<div style="font-size:0.44rem;color:#9ca3af;text-align:center;padding:8px;">No hay puntos medios</div>';
            return;
        }
        lista.innerHTML = pms.map((pm, i) => `<div style="display:flex;align-items:center;gap:6px;padding:5px 8px;background:#fff;
            border:1px solid #e5e7eb;border-radius:6px;font-size:0.44rem;cursor:pointer;transition:background 0.15s;"
            onmouseenter="this.style.background='#fff7ed'" onmouseleave="this.style.background='#fff'" data-pm-idx="${i}">
            <span style="color:#ec4899;font-weight:800;">📌</span>
            <span style="flex:1;color:#374151;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${pm.nombre || pm.direccion}</span>
            <button type="button" data-pm-del="${i}" style="background:none;border:none;color:#ef4444;cursor:pointer;font-size:0.5rem;">✕</button>
        </div>`).join('');
    };

    // Add new punto medio
    document.addEventListener('click', (e) => {
        if (e.target.id === 'ubiAddPuntoMedio') {
            const nombre = prompt('Nombre del punto medio:');
            const dir = prompt('Dirección, coordenadas o link de Google Maps:');
            if (nombre && dir) {
                const pms = getPuntosMedios();
                const det = detectInputType(dir);
                pms.push({ nombre, direccion: dir, coords: det.type === 'coords' ? det.lat + ',' + det.lng : '', fecha: new Date().toISOString() });
                savePuntosMedios(pms);
                renderPuntosMediosPopup();
            }
        }
    });

"""

if old_render_fn in html:
    html = html.replace(old_render_fn, '\n')
    print("✅ Removed renderPuntosMediosPopup function and ubiAddPuntoMedio handler")
else:
    print("⚠️ Could not find renderPuntosMediosPopup function to remove")

with open('/workspaces/vistas/mockup.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ All changes applied. File size: {len(html)} chars")
