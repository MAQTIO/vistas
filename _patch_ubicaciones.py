#!/usr/bin/env python3
"""Replace the popupUbicaciones HTML and JS with a completely redesigned version."""
import re

with open('/workspaces/vistas/mockup.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════════════
# 1. REPLACE THE POPUP HTML (lines ~11437-11500)
# ═══════════════════════════════════════════════════════════════════
old_popup_start = '<!-- ═══ POPUP GESTIONAR UBICACIONES DEL CLIENTE ═══ -->'
old_popup_end = '<!-- ═══ POPUP PAQUETERÍA INDEPENDIENTE ═══ -->'

idx_start = html.index(old_popup_start)
idx_end = html.index(old_popup_end)

new_popup_html = r'''<!-- ═══ POPUP GESTIONAR UBICACIONES DEL CLIENTE ═══ -->
<div id="popupUbicaciones" class="popup-overlay" aria-hidden="true" style="z-index:100025;display:none;">
    <div id="ubiPopupInner" style="background:#fff;border-radius:16px;max-width:1200px;width:97vw;max-height:94vh;
        box-shadow:0 24px 80px rgba(0,0,0,0.4),0 0 0 1px rgba(255,153,0,0.15);display:flex;flex-direction:column;overflow:hidden;">

        <!-- ── Header ── -->
        <div style="display:flex;align-items:center;justify-content:space-between;padding:18px 26px 14px;
            background:linear-gradient(135deg,#ff9900 0%,#e68a00 100%);flex-shrink:0;">
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:42px;height:42px;background:rgba(255,255,255,0.2);border-radius:12px;display:flex;
                    align-items:center;justify-content:center;font-size:1.3rem;">📍</div>
                <div>
                    <div style="font-size:0.85rem;font-weight:900;color:#fff;letter-spacing:0.03em;">UBICACIONES DEL CLIENTE</div>
                    <div style="font-size:0.46rem;color:rgba(255,255,255,0.8);margin-top:1px;" id="ubiHeaderClientName">Gestiona domicilio, negocio y puntos de entrega</div>
                </div>
            </div>
            <button id="ubicacionesCerrar" type="button" style="background:rgba(255,255,255,0.2);border:none;width:36px;height:36px;
                border-radius:10px;font-size:1.1rem;cursor:pointer;color:#fff;display:flex;align-items:center;justify-content:center;
                transition:background 0.2s;">✕</button>
        </div>

        <!-- ── Body: Split layout ── -->
        <div style="display:flex;flex:1;overflow:hidden;min-height:0;">

            <!-- LEFT PANEL: Location cards + editor -->
            <div id="ubiLeftPanel" style="width:420px;min-width:360px;display:flex;flex-direction:column;
                border-right:1px solid #e5e7eb;overflow-y:auto;background:#fafbfc;">

                <!-- Location cards -->
                <div style="padding:16px 18px 8px;">
                    <div style="font-size:0.5rem;font-weight:800;color:#6b7280;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;">
                        Ubicaciones registradas</div>

                    <!-- Card: Domicilio -->
                    <div class="ubi-card" data-ubi-tipo="domicilio" style="display:flex;align-items:center;gap:12px;padding:12px 14px;
                        background:#fff;border:2px solid #e5e7eb;border-radius:12px;margin-bottom:8px;cursor:pointer;
                        transition:all 0.2s;">
                        <div style="width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,#fef3c7,#fde68a);
                            display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">🏠</div>
                        <div style="flex:1;min-width:0;">
                            <div style="font-size:0.56rem;font-weight:800;color:#1f2937;">Domicilio</div>
                            <div class="ubi-card-addr" style="font-size:0.44rem;color:#6b7280;white-space:nowrap;overflow:hidden;
                                text-overflow:ellipsis;">Sin registrar</div>
                        </div>
                        <div class="ubi-card-status" style="width:10px;height:10px;border-radius:50%;background:#d1d5db;flex-shrink:0;"></div>
                    </div>

                    <!-- Card: Negocio -->
                    <div class="ubi-card" data-ubi-tipo="negocio" style="display:flex;align-items:center;gap:12px;padding:12px 14px;
                        background:#fff;border:2px solid #e5e7eb;border-radius:12px;margin-bottom:8px;cursor:pointer;
                        transition:all 0.2s;">
                        <div style="width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,#dbeafe,#93c5fd);
                            display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">🏢</div>
                        <div style="flex:1;min-width:0;">
                            <div style="font-size:0.56rem;font-weight:800;color:#1f2937;">Negocio</div>
                            <div class="ubi-card-addr" style="font-size:0.44rem;color:#6b7280;white-space:nowrap;overflow:hidden;
                                text-overflow:ellipsis;">Sin registrar</div>
                        </div>
                        <div class="ubi-card-status" style="width:10px;height:10px;border-radius:50%;background:#d1d5db;flex-shrink:0;"></div>
                    </div>

                    <!-- Card: Punto medio -->
                    <div class="ubi-card" data-ubi-tipo="puntoMedio" style="display:flex;align-items:center;gap:12px;padding:12px 14px;
                        background:#fff;border:2px solid #e5e7eb;border-radius:12px;margin-bottom:8px;cursor:pointer;
                        transition:all 0.2s;">
                        <div style="width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,#fce7f3,#f9a8d4);
                            display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">📌</div>
                        <div style="flex:1;min-width:0;">
                            <div style="font-size:0.56rem;font-weight:800;color:#1f2937;">Punto medio</div>
                            <div class="ubi-card-addr" style="font-size:0.44rem;color:#6b7280;white-space:nowrap;overflow:hidden;
                                text-overflow:ellipsis;">Sin registrar</div>
                        </div>
                        <div class="ubi-card-status" style="width:10px;height:10px;border-radius:50%;background:#d1d5db;flex-shrink:0;"></div>
                    </div>
                </div>

                <!-- Editor form (shown when a card is clicked) -->
                <div id="ubiEditorPanel" style="display:none;padding:0 18px 16px;flex:1;">
                    <div style="background:#fff;border:2px solid #ff9900;border-radius:12px;padding:16px;box-shadow:0 4px 16px rgba(255,153,0,0.1);">
                        <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
                            <span id="ubiEditorIcon" style="font-size:1rem;">🏠</span>
                            <span id="ubiEditorTitle" style="font-size:0.6rem;font-weight:900;color:#ff9900;">EDITAR DOMICILIO</span>
                        </div>

                        <!-- Smart search -->
                        <div style="margin-bottom:10px;">
                            <div style="font-size:0.46rem;font-weight:700;color:#374151;margin-bottom:4px;">
                                Buscar dirección <span style="color:#9ca3af;font-weight:500;">(dirección, coordenadas o link Google Maps)</span></div>
                            <div style="position:relative;">
                                <input id="ubiBuscadorInput" type="text"
                                    placeholder="🔍 Av. Juárez 100, Oaxaca / 17.065,-96.72 / maps.google.com/..."
                                    style="width:100%;padding:10px 12px;border:2px solid #e5e7eb;border-radius:10px;font-size:0.52rem;
                                    background:#fff;color:#1f2937;font-weight:600;transition:border-color 0.2s;box-sizing:border-box;"
                                    autocomplete="off">
                                <div id="ubiBuscadorResults" style="display:none;position:absolute;top:100%;left:0;right:0;background:#fff;
                                    border:1px solid #e5e7eb;border-radius:8px;max-height:160px;overflow-y:auto;z-index:20;
                                    box-shadow:0 8px 20px rgba(0,0,0,0.15);"></div>
                                <div id="ubiBuscadorDetected" style="font-size:0.4rem;color:#9ca3af;margin-top:2px;min-height:12px;"></div>
                            </div>
                        </div>

                        <!-- Address fields -->
                        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:10px;">
                            <div><label style="font-size:0.42rem;font-weight:700;color:#374151;">Calle</label>
                                <input id="ubiCalle" type="text" style="width:100%;padding:7px 8px;border:1px solid #d1d5db;border-radius:7px;
                                    font-size:0.48rem;color:#1f2937;box-sizing:border-box;background:#fafbfc;"></div>
                            <div><label style="font-size:0.42rem;font-weight:700;color:#374151;">Colonia</label>
                                <input id="ubiColonia" type="text" style="width:100%;padding:7px 8px;border:1px solid #d1d5db;border-radius:7px;
                                    font-size:0.48rem;color:#1f2937;box-sizing:border-box;background:#fafbfc;"></div>
                            <div><label style="font-size:0.42rem;font-weight:700;color:#374151;">Ciudad</label>
                                <input id="ubiCiudad" type="text" style="width:100%;padding:7px 8px;border:1px solid #d1d5db;border-radius:7px;
                                    font-size:0.48rem;color:#1f2937;box-sizing:border-box;background:#fafbfc;"></div>
                            <div><label style="font-size:0.42rem;font-weight:700;color:#374151;">Estado</label>
                                <input id="ubiEstado" type="text" style="width:100%;padding:7px 8px;border:1px solid #d1d5db;border-radius:7px;
                                    font-size:0.48rem;color:#1f2937;box-sizing:border-box;background:#fafbfc;"></div>
                            <div><label style="font-size:0.42rem;font-weight:700;color:#374151;">CP</label>
                                <input id="ubiCp" type="text" style="width:100%;padding:7px 8px;border:1px solid #d1d5db;border-radius:7px;
                                    font-size:0.48rem;color:#1f2937;box-sizing:border-box;background:#fafbfc;"></div>
                            <div><label style="font-size:0.42rem;font-weight:700;color:#374151;">Coordenadas</label>
                                <input id="ubiCoords" type="text" readonly style="width:100%;padding:7px 8px;border:1px solid #d1d5db;
                                    border-radius:7px;font-size:0.48rem;color:#6b7280;box-sizing:border-box;background:#f3f4f6;"></div>
                        </div>

                        <!-- Editor actions -->
                        <div style="display:flex;gap:8px;justify-content:flex-end;">
                            <button id="ubiEditorCancel" type="button" style="padding:7px 16px;background:#f3f4f6;color:#6b7280;
                                border:1px solid #d1d5db;border-radius:8px;font-weight:700;font-size:0.48rem;cursor:pointer;">Cancelar</button>
                            <button id="ubiEditorSave" type="button" style="padding:7px 20px;background:linear-gradient(135deg,#ff9900,#e68a00);
                                color:#fff;border:none;border-radius:8px;font-weight:800;font-size:0.48rem;cursor:pointer;
                                box-shadow:0 2px 8px rgba(255,153,0,0.3);">💾 Guardar</button>
                            <button id="ubiEditorDelete" type="button" style="padding:7px 14px;background:#fef2f2;color:#ef4444;
                                border:1px solid #fecaca;border-radius:8px;font-weight:700;font-size:0.48rem;cursor:pointer;">🗑️</button>
                        </div>
                    </div>
                </div>

                <!-- Puntos medios list -->
                <div id="ubiPuntosMediosSection" style="padding:0 18px 14px;margin-top:auto;">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
                        <div style="font-size:0.48rem;font-weight:800;color:#6b7280;text-transform:uppercase;letter-spacing:0.06em;">
                            Puntos medios guardados</div>
                        <button id="ubiAddPuntoMedio" type="button" style="background:#ff9900;color:#fff;border:none;
                            border-radius:6px;padding:4px 10px;font-size:0.42rem;font-weight:800;cursor:pointer;">+ Nuevo</button>
                    </div>
                    <div id="ubiPuntosMediosLista" style="max-height:100px;overflow-y:auto;display:flex;flex-direction:column;gap:4px;">
                        <div style="font-size:0.44rem;color:#9ca3af;text-align:center;padding:8px;">No hay puntos medios</div>
                    </div>
                </div>
            </div>

            <!-- RIGHT PANEL: Leaflet Map -->
            <div style="flex:1;display:flex;flex-direction:column;background:#f0f4f8;min-width:0;">
                <div style="padding:12px 16px 8px;display:flex;align-items:center;justify-content:space-between;">
                    <div style="font-size:0.5rem;font-weight:800;color:#374151;">🗺️ Vista del mapa</div>
                    <div style="display:flex;gap:6px;">
                        <span style="display:inline-flex;align-items:center;gap:3px;font-size:0.38rem;color:#6b7280;">
                            <span style="width:8px;height:8px;border-radius:50%;background:#f59e0b;display:inline-block;"></span> Domicilio</span>
                        <span style="display:inline-flex;align-items:center;gap:3px;font-size:0.38rem;color:#6b7280;">
                            <span style="width:8px;height:8px;border-radius:50%;background:#3b82f6;display:inline-block;"></span> Negocio</span>
                        <span style="display:inline-flex;align-items:center;gap:3px;font-size:0.38rem;color:#6b7280;">
                            <span style="width:8px;height:8px;border-radius:50%;background:#ec4899;display:inline-block;"></span> Punto medio</span>
                    </div>
                </div>
                <div id="ubiMapaContainer" style="flex:1;margin:0 16px 16px;border-radius:14px;overflow:hidden;
                    border:2px solid #e5e7eb;position:relative;min-height:300px;background:#e5e7eb;">
                    <div id="ubiLeafletMap" style="width:100%;height:100%;"></div>
                    <!-- Placeholder when no map -->
                    <div id="ubiMapPlaceholder" style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
                        justify-content:center;background:#f8fafc;pointer-events:none;">
                        <div style="font-size:3rem;opacity:0.3;">🗺️</div>
                        <div style="font-size:0.52rem;font-weight:700;color:#9ca3af;margin-top:4px;">Agrega una ubicación para ver el mapa</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ── Footer ── -->
        <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 22px;
            border-top:1px solid #e5e7eb;background:#fafbfc;flex-shrink:0;">
            <div style="font-size:0.42rem;color:#9ca3af;" id="ubiFooterInfo">Haz clic en una ubicación para editarla</div>
            <button id="ubicacionesCancelar" type="button" style="padding:8px 22px;background:#6b7280;color:#fff;border:none;
                border-radius:8px;font-weight:700;font-size:0.5rem;cursor:pointer;">CERRAR</button>
        </div>
    </div>
</div>

'''

html = html[:idx_start] + new_popup_html + html[idx_end:]

# ═══════════════════════════════════════════════════════════════════
# 2. REPLACE THE JS HANDLERS (lines ~31164-31370)
# ═══════════════════════════════════════════════════════════════════
# Find the block that starts with detectInputType and ends before PAQUETERÍA INDEPENDIENTE
old_js_start = "// Detección inteligente de tipo de entrada (dirección, coordenadas, link de Google Maps)"
old_js_end = "    // ===== PAQUETERÍA INDEPENDIENTE ====="

js_start = html.index(old_js_start)
js_end = html.index(old_js_end)

new_js = r'''// ═══ UBICACIONES DEL CLIENTE — REDESIGNED ═══
    // State
    let _ubiLeafletMap = null;
    let _ubiMarkers = {};   // { domicilio: L.marker, negocio: L.marker, puntoMedio: L.marker }
    let _ubiData = {};      // { domicilio: {addr,coords}, negocio: {...}, puntoMedio: {...} }
    let _ubiEditingTipo = null;

    const UBI_COLORS = { domicilio: '#f59e0b', negocio: '#3b82f6', puntoMedio: '#ec4899' };
    const UBI_ICONS  = { domicilio: '🏠', negocio: '🏢', puntoMedio: '📌' };
    const UBI_LABELS = { domicilio: 'Domicilio', negocio: 'Negocio', puntoMedio: 'Punto medio' };

    const detectInputType = (val) => {
        val = (val || '').trim();
        if (!val) return { type: null };
        if (/google\.\w+\/maps|maps\.google|maps\.app\.goo\.gl|goo\.gl\/maps/i.test(val))
            return { type: 'googleMaps', value: val };
        const coordMatch = val.match(/^(-?\d{1,3}\.\d+)[,\s]+(-?\d{1,3}\.\d+)$/);
        if (coordMatch) return { type: 'coords', lat: parseFloat(coordMatch[1]), lng: parseFloat(coordMatch[2]) };
        return { type: 'address', value: val };
    };

    // Create Leaflet colored marker
    const ubiCreateIcon = (color) => {
        return L.divIcon({
            className: '',
            html: `<div style="width:28px;height:28px;border-radius:50%;background:${color};border:3px solid #fff;
                box-shadow:0 2px 8px rgba(0,0,0,0.3);display:flex;align-items:center;justify-content:center;"></div>`,
            iconSize: [28, 28], iconAnchor: [14, 14]
        });
    };

    // Initialize Leaflet map
    const ubiInitMap = () => {
        const el = document.getElementById('ubiLeafletMap');
        if (!el || _ubiLeafletMap) return;
        _ubiLeafletMap = L.map(el, { zoomControl: true, attributionControl: false }).setView([17.0654, -96.7236], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19, attribution: '© OpenStreetMap'
        }).addTo(_ubiLeafletMap);
        setTimeout(() => _ubiLeafletMap.invalidateSize(), 200);
    };

    // Update markers on map
    const ubiRefreshMarkers = () => {
        if (!_ubiLeafletMap) return;
        const placeholder = document.getElementById('ubiMapPlaceholder');
        let hasAny = false;
        const bounds = [];
        ['domicilio','negocio','puntoMedio'].forEach(tipo => {
            if (_ubiMarkers[tipo]) { _ubiLeafletMap.removeLayer(_ubiMarkers[tipo]); delete _ubiMarkers[tipo]; }
            const d = _ubiData[tipo];
            if (d && d.coords) {
                const parts = d.coords.split(',').map(Number);
                if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
                    const latlng = [parts[0], parts[1]];
                    _ubiMarkers[tipo] = L.marker(latlng, { icon: ubiCreateIcon(UBI_COLORS[tipo]) })
                        .addTo(_ubiLeafletMap)
                        .bindPopup(`<strong>${UBI_ICONS[tipo]} ${UBI_LABELS[tipo]}</strong><br>${d.addr || d.coords}`);
                    bounds.push(latlng);
                    hasAny = true;
                }
            }
        });
        if (placeholder) placeholder.style.display = hasAny ? 'none' : 'flex';
        if (bounds.length > 1) _ubiLeafletMap.fitBounds(bounds, { padding: [40, 40], maxZoom: 16 });
        else if (bounds.length === 1) _ubiLeafletMap.setView(bounds[0], 16);
    };

    // Refresh cards UI
    const ubiRefreshCards = () => {
        document.querySelectorAll('.ubi-card').forEach(card => {
            const tipo = card.dataset.ubiTipo;
            const d = _ubiData[tipo];
            const addrEl = card.querySelector('.ubi-card-addr');
            const statusEl = card.querySelector('.ubi-card-status');
            if (addrEl) addrEl.textContent = (d && d.addr) ? d.addr : 'Sin registrar';
            if (statusEl) statusEl.style.background = (d && d.addr) ? '#22c55e' : '#d1d5db';
            // Highlight if editing
            card.style.borderColor = (_ubiEditingTipo === tipo) ? '#ff9900' : '#e5e7eb';
            card.style.background = (_ubiEditingTipo === tipo) ? '#fff7ed' : '#fff';
        });
        // Update summary in client form
        ['domicilio','negocio','puntoMedio'].forEach(tipo => {
            const d = _ubiData[tipo];
            const resId = tipo === 'domicilio' ? 'cliResUbiDomicilio' : tipo === 'negocio' ? 'cliResUbiNegocio' : 'cliResUbiPuntoMedio';
            const res = document.getElementById(resId);
            if (res) res.textContent = (d && d.addr) ? d.addr : 'Sin registrar';
            const hidId = tipo === 'domicilio' ? 'cliFormUbiDomicilio' : tipo === 'negocio' ? 'cliFormUbiNegocio' : 'cliFormUbiPuntoMedio';
            const hid = document.getElementById(hidId);
            if (hid) hid.value = (d && d.addr) || '';
        });
        const coordsHid = document.getElementById('cliFormUbiCoords');
        if (coordsHid) {
            const allCoords = ['domicilio','negocio','puntoMedio'].map(t => (_ubiData[t]||{}).coords).filter(Boolean).join(';');
            coordsHid.value = allCoords;
        }
    };

    // Load _ubiData from hidden fields
    const ubiLoadFromFields = () => {
        _ubiData = {};
        const dom = document.getElementById('cliFormUbiDomicilio')?.value;
        if (dom) _ubiData.domicilio = { addr: dom, coords: '' };
        const neg = document.getElementById('cliFormUbiNegocio')?.value;
        if (neg) _ubiData.negocio = { addr: neg, coords: '' };
        const pm = document.getElementById('cliFormUbiPuntoMedio')?.value;
        if (pm) _ubiData.puntoMedio = { addr: pm, coords: '' };
        // Try to extract coords from addr or from coords field
        const allCoords = (document.getElementById('cliFormUbiCoords')?.value || '').split(';');
        allCoords.forEach(c => {
            const parts = c.split(',').map(Number);
            if (parts.length === 2 && !isNaN(parts[0])) {
                // assign to first empty coords
                ['domicilio','negocio','puntoMedio'].forEach(t => {
                    if (_ubiData[t] && !_ubiData[t].coords) _ubiData[t].coords = c;
                });
            }
        });
    };

    // Open editor for a location type
    const ubiOpenEditor = (tipo) => {
        _ubiEditingTipo = tipo;
        const panel = document.getElementById('ubiEditorPanel');
        if (!panel) return;
        panel.style.display = 'block';
        document.getElementById('ubiEditorIcon').textContent = UBI_ICONS[tipo];
        document.getElementById('ubiEditorTitle').textContent = 'EDITAR ' + UBI_LABELS[tipo].toUpperCase();
        // Populate fields
        const d = _ubiData[tipo] || {};
        document.getElementById('ubiBuscadorInput').value = d.addr || '';
        document.getElementById('ubiCalle').value = d.calle || '';
        document.getElementById('ubiColonia').value = d.colonia || '';
        document.getElementById('ubiCiudad').value = d.ciudad || '';
        document.getElementById('ubiEstado').value = d.estado || '';
        document.getElementById('ubiCp').value = d.cp || '';
        document.getElementById('ubiCoords').value = d.coords || '';
        document.getElementById('ubiBuscadorDetected').textContent = '';
        const resultsEl = document.getElementById('ubiBuscadorResults');
        if (resultsEl) resultsEl.style.display = 'none';
        // Focus on search
        document.getElementById('ubiBuscadorInput').focus();
        ubiRefreshCards();
        // Show delete only if has data
        const delBtn = document.getElementById('ubiEditorDelete');
        if (delBtn) delBtn.style.display = (d.addr) ? 'inline-block' : 'none';
    };

    const ubiCloseEditor = () => {
        _ubiEditingTipo = null;
        const panel = document.getElementById('ubiEditorPanel');
        if (panel) panel.style.display = 'none';
        ubiRefreshCards();
    };

    // Fly map to coords
    const ubiMapFlyTo = (lat, lng) => {
        if (!_ubiLeafletMap) return;
        _ubiLeafletMap.flyTo([lat, lng], 17, { duration: 0.8 });
        const placeholder = document.getElementById('ubiMapPlaceholder');
        if (placeholder) placeholder.style.display = 'none';
    };

    const updateMapPreview = (lat, lng) => {
        if (!_ubiLeafletMap) ubiInitMap();
        ubiMapFlyTo(lat, lng);
        // Update current editing marker preview
        if (_ubiEditingTipo) {
            if (_ubiMarkers['_preview']) { _ubiLeafletMap.removeLayer(_ubiMarkers['_preview']); }
            _ubiMarkers['_preview'] = L.marker([lat, lng], { icon: ubiCreateIcon(UBI_COLORS[_ubiEditingTipo]) })
                .addTo(_ubiLeafletMap)
                .bindPopup('📍 Posición seleccionada').openPopup();
        }
    };

    // ── Event handlers ──

    // Open popup
    document.addEventListener('click', (e) => {
        if (e.target.id === 'btnAbrirUbicaciones' || e.target.closest('#btnAbrirUbicaciones')) {
            const popup = document.getElementById('popupUbicaciones');
            if (popup) {
                popup.style.display = 'flex';
                ubiLoadFromFields();
                ubiRefreshCards();
                ubiCloseEditor();
                // Show client name in header
                const nombre = document.getElementById('cliFormNombre')?.value;
                const headerName = document.getElementById('ubiHeaderClientName');
                if (headerName && nombre) headerName.textContent = nombre;
                // Init map
                setTimeout(() => {
                    ubiInitMap();
                    ubiRefreshMarkers();
                }, 100);
                renderPuntosMediosPopup();
            }
        }
    });

    // Close popup 
    document.addEventListener('click', (e) => {
        if (e.target.id === 'ubicacionesCerrar' || e.target.id === 'ubicacionesCancelar') {
            const popup = document.getElementById('popupUbicaciones');
            if (popup) popup.style.display = 'none';
            if (_ubiMarkers['_preview'] && _ubiLeafletMap) {
                _ubiLeafletMap.removeLayer(_ubiMarkers['_preview']);
                delete _ubiMarkers['_preview'];
            }
        }
    });

    // Card click — open editor
    document.addEventListener('click', (e) => {
        const card = e.target.closest('.ubi-card');
        if (card && card.dataset.ubiTipo) {
            ubiOpenEditor(card.dataset.ubiTipo);
            // Fly to marker if exists
            const d = _ubiData[card.dataset.ubiTipo];
            if (d && d.coords) {
                const parts = d.coords.split(',').map(Number);
                if (parts.length === 2 && !isNaN(parts[0])) ubiMapFlyTo(parts[0], parts[1]);
            }
        }
    });

    // Editor cancel
    document.addEventListener('click', (e) => {
        if (e.target.id === 'ubiEditorCancel') ubiCloseEditor();
    });

    // Editor save
    document.addEventListener('click', (e) => {
        if (e.target.id === 'ubiEditorSave' && _ubiEditingTipo) {
            const raw = document.getElementById('ubiBuscadorInput')?.value || '';
            const coords = document.getElementById('ubiCoords')?.value || '';
            const calle = document.getElementById('ubiCalle')?.value || '';
            const colonia = document.getElementById('ubiColonia')?.value || '';
            const ciudad = document.getElementById('ubiCiudad')?.value || '';
            const estado = document.getElementById('ubiEstado')?.value || '';
            const cp = document.getElementById('ubiCp')?.value || '';
            const addrText = raw || [calle, colonia, ciudad, estado, cp].filter(Boolean).join(', ') || coords;
            _ubiData[_ubiEditingTipo] = { addr: addrText, coords, calle, colonia, ciudad, estado, cp };
            // Remove preview marker
            if (_ubiMarkers['_preview'] && _ubiLeafletMap) {
                _ubiLeafletMap.removeLayer(_ubiMarkers['_preview']);
                delete _ubiMarkers['_preview'];
            }
            // If punto medio, also save to collection
            if (_ubiEditingTipo === 'puntoMedio' && (raw || coords)) {
                const pms = getPuntosMedios();
                pms.push({ nombre: calle || raw, direccion: raw, coords: coords, ciudad: ciudad, fecha: new Date().toISOString() });
                savePuntosMedios(pms);
                renderPuntosMediosPopup();
            }
            ubiRefreshCards();
            ubiRefreshMarkers();
            ubiCloseEditor();
        }
    });

    // Editor delete
    document.addEventListener('click', (e) => {
        if (e.target.id === 'ubiEditorDelete' && _ubiEditingTipo) {
            delete _ubiData[_ubiEditingTipo];
            if (_ubiMarkers['_preview'] && _ubiLeafletMap) {
                _ubiLeafletMap.removeLayer(_ubiMarkers['_preview']);
                delete _ubiMarkers['_preview'];
            }
            ubiRefreshCards();
            ubiRefreshMarkers();
            ubiCloseEditor();
        }
    });

    // Smart search input
    const ubiBuscadorInput = document.getElementById('ubiBuscadorInput');
    if (ubiBuscadorInput) {
        ubiBuscadorInput.addEventListener('focus', function() { this.style.borderColor = '#ff9900'; });
        ubiBuscadorInput.addEventListener('blur', function() { this.style.borderColor = '#e5e7eb'; });
        ubiBuscadorInput.addEventListener('input', () => {
            const val = ubiBuscadorInput.value;
            const det = detectInputType(val);
            const detEl = document.getElementById('ubiBuscadorDetected');
            if (detEl) {
                if (det.type === 'googleMaps') detEl.textContent = '🔗 Detectado: Link de Google Maps';
                else if (det.type === 'coords') detEl.textContent = '📍 Detectado: Coordenadas (' + det.lat + ', ' + det.lng + ')';
                else if (det.type === 'address' && val.length > 3) detEl.textContent = '🏠 Detectado: Búsqueda por dirección';
                else detEl.textContent = '';
            }
            // Autocomplete suggestions
            const resultsEl = document.getElementById('ubiBuscadorResults');
            if (resultsEl) {
                if (det.type === 'address' && val.length > 2) {
                    const q = val.toLowerCase();
                    const sugs = [];
                    getPuntosMedios().forEach((pm) => {
                        const haystack = ((pm.nombre || '') + ' ' + (pm.direccion || '') + ' ' + (pm.ciudad || '')).toLowerCase();
                        if (haystack.includes(q)) sugs.push({ label: '📌 ' + (pm.nombre || pm.direccion), sub: pm.direccion + (pm.ciudad ? ' (' + pm.ciudad + ')' : ''), value: pm.direccion, coords: pm.coords, src: 'pm' });
                    });
                    try {
                        const cliRaw = localStorage.getItem('mock_clientes_quick_v1');
                        if (cliRaw) {
                            JSON.parse(cliRaw).forEach(c => {
                                [c.direccion, c.domicilio, c.negocio, c.puntoMedio].filter(Boolean).forEach(f => {
                                    if (f.toLowerCase().includes(q)) sugs.push({ label: '👤 ' + (c.nombre || 'Cliente'), sub: f, value: f, coords: '', src: 'cli' });
                                });
                            });
                        }
                    } catch(_){}
                    if (sugs.length) {
                        resultsEl.innerHTML = sugs.slice(0, 8).map((s, i) => `<div data-sug-idx="${i}" style="padding:8px 12px;cursor:pointer;border-bottom:1px solid #f3f4f6;transition:background 0.15s;" onmouseenter="this.style.background='#fff7ed'" onmouseleave="this.style.background='#fff'">
                            <div style="font-weight:600;color:#374151;font-size:0.48rem;">${s.label}</div>
                            <div style="font-size:0.42rem;color:#9ca3af;">${s.sub}</div>
                        </div>`).join('');
                        resultsEl.style.display = 'block';
                        resultsEl.querySelectorAll('[data-sug-idx]').forEach((el, idx) => {
                            el.addEventListener('click', () => {
                                const s = sugs[idx];
                                ubiBuscadorInput.value = s.value;
                                resultsEl.style.display = 'none';
                                if (s.coords) {
                                    const coordsField = document.getElementById('ubiCoords');
                                    if (coordsField) coordsField.value = s.coords;
                                    const parts = s.coords.split(',').map(Number);
                                    if (parts.length === 2 && !isNaN(parts[0])) updateMapPreview(parts[0], parts[1]);
                                }
                                ubiBuscadorInput.dispatchEvent(new Event('input'));
                            });
                        });
                    } else {
                        resultsEl.innerHTML = '<div style="padding:10px;color:#9ca3af;font-size:0.44rem;text-align:center;">Sin coincidencias</div>';
                        resultsEl.style.display = 'block';
                    }
                } else {
                    resultsEl.style.display = 'none';
                }
            }
            if (det.type === 'coords') {
                const coordsField = document.getElementById('ubiCoords');
                if (coordsField) coordsField.value = det.lat + ', ' + det.lng;
                updateMapPreview(det.lat, det.lng);
            }
            if (det.type === 'googleMaps') {
                const m = val.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/);
                if (m) {
                    const coordsField = document.getElementById('ubiCoords');
                    if (coordsField) coordsField.value = m[1] + ', ' + m[2];
                    updateMapPreview(parseFloat(m[1]), parseFloat(m[2]));
                }
            }
        });
        document.addEventListener('click', (ev) => {
            const resultsEl = document.getElementById('ubiBuscadorResults');
            if (resultsEl && !ubiBuscadorInput.contains(ev.target) && !resultsEl.contains(ev.target))
                resultsEl.style.display = 'none';
        });
    }

    // Render puntos medios list
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

'''

html = html[:js_start] + new_js + html[js_end:]

with open('/workspaces/vistas/mockup.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Popup de ubicaciones rediseñado exitosamente.")
print(f"   Tamaño final: {len(html)} caracteres")
