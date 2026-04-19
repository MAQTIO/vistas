#!/usr/bin/env python3
"""Fix ubicaciones popup to eliminate vertical scrolling — everything fits in viewport."""
import re

with open('/workspaces/vistas/mockup.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find and replace the entire popup
old_start = '<!-- ═══ POPUP GESTIONAR UBICACIONES DEL CLIENTE ═══ -->'
old_end = '\n<!-- ═══ POPUP PAQUETERÍA INDEPENDIENTE ═══ -->'

idx_start = html.index(old_start)
idx_end = html.index(old_end)

new_popup = r'''<!-- ═══ POPUP GESTIONAR UBICACIONES DEL CLIENTE ═══ -->
<div id="popupUbicaciones" class="popup-overlay" aria-hidden="true" style="z-index:100025;display:none;">
    <div id="ubiPopupInner" style="background:#fff;border-radius:16px;width:97vw;max-width:1300px;height:97vh;
        box-shadow:0 24px 80px rgba(0,0,0,0.4),0 0 0 1px rgba(255,153,0,0.15);display:flex;flex-direction:column;overflow:hidden;">

        <!-- ── Header (compact) ── -->
        <div style="display:flex;align-items:center;justify-content:space-between;padding:10px 22px;
            background:linear-gradient(135deg,#ff9900 0%,#e68a00 100%);flex-shrink:0;">
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:36px;height:36px;background:rgba(255,255,255,0.2);border-radius:10px;display:flex;
                    align-items:center;justify-content:center;font-size:1.1rem;">📍</div>
                <div>
                    <div style="font-size:0.75rem;font-weight:900;color:#fff;letter-spacing:0.03em;">UBICACIONES DEL CLIENTE</div>
                    <div style="font-size:0.42rem;color:rgba(255,255,255,0.8);" id="ubiHeaderClientName">Gestiona domicilio, negocio y puntos de entrega</div>
                </div>
            </div>
            <button id="ubicacionesCerrar" type="button" style="background:rgba(255,255,255,0.2);border:none;width:32px;height:32px;
                border-radius:8px;font-size:1rem;cursor:pointer;color:#fff;display:flex;align-items:center;justify-content:center;">✕</button>
        </div>

        <!-- ── Body: Split layout (fills remaining space) ── -->
        <div style="display:flex;flex:1;overflow:hidden;min-height:0;">

            <!-- LEFT PANEL -->
            <div id="ubiLeftPanel" style="width:400px;min-width:340px;display:flex;flex-direction:column;
                border-right:1px solid #e5e7eb;background:#fafbfc;overflow:hidden;">

                <!-- 3 Location cards — always visible, compact row -->
                <div style="padding:10px 14px 6px;flex-shrink:0;">
                    <div style="font-size:0.44rem;font-weight:800;color:#6b7280;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">
                        Ubicaciones registradas</div>
                    <div style="display:flex;gap:6px;">

                        <!-- Card: Domicilio -->
                        <div class="ubi-card" data-ubi-tipo="domicilio" style="flex:1;display:flex;flex-direction:column;align-items:center;
                            gap:4px;padding:8px 6px;background:#fff;border:2px solid #e5e7eb;border-radius:10px;cursor:pointer;
                            transition:all 0.2s;min-width:0;">
                            <div style="width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,#fef3c7,#fde68a);
                                display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;">🏠</div>
                            <div style="font-size:0.44rem;font-weight:800;color:#1f2937;text-align:center;">Domicilio</div>
                            <div class="ubi-card-addr" style="font-size:0.36rem;color:#6b7280;text-align:center;white-space:nowrap;
                                overflow:hidden;text-overflow:ellipsis;width:100%;">Sin registrar</div>
                            <div class="ubi-card-status" style="width:8px;height:8px;border-radius:50%;background:#d1d5db;"></div>
                        </div>

                        <!-- Card: Negocio -->
                        <div class="ubi-card" data-ubi-tipo="negocio" style="flex:1;display:flex;flex-direction:column;align-items:center;
                            gap:4px;padding:8px 6px;background:#fff;border:2px solid #e5e7eb;border-radius:10px;cursor:pointer;
                            transition:all 0.2s;min-width:0;">
                            <div style="width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,#dbeafe,#93c5fd);
                                display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;">🏢</div>
                            <div style="font-size:0.44rem;font-weight:800;color:#1f2937;text-align:center;">Negocio</div>
                            <div class="ubi-card-addr" style="font-size:0.36rem;color:#6b7280;text-align:center;white-space:nowrap;
                                overflow:hidden;text-overflow:ellipsis;width:100%;">Sin registrar</div>
                            <div class="ubi-card-status" style="width:8px;height:8px;border-radius:50%;background:#d1d5db;"></div>
                        </div>

                        <!-- Card: Punto medio -->
                        <div class="ubi-card" data-ubi-tipo="puntoMedio" style="flex:1;display:flex;flex-direction:column;align-items:center;
                            gap:4px;padding:8px 6px;background:#fff;border:2px solid #e5e7eb;border-radius:10px;cursor:pointer;
                            transition:all 0.2s;min-width:0;">
                            <div style="width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,#fce7f3,#f9a8d4);
                                display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;">📌</div>
                            <div style="font-size:0.44rem;font-weight:800;color:#1f2937;text-align:center;">Punto medio</div>
                            <div class="ubi-card-addr" style="font-size:0.36rem;color:#6b7280;text-align:center;white-space:nowrap;
                                overflow:hidden;text-overflow:ellipsis;width:100%;">Sin registrar</div>
                            <div class="ubi-card-status" style="width:8px;height:8px;border-radius:50%;background:#d1d5db;"></div>
                        </div>
                    </div>
                </div>

                <!-- Editor form — fills remaining left panel space -->
                <div id="ubiEditorPanel" style="display:none;padding:6px 14px 10px;flex:1;overflow-y:auto;min-height:0;">
                    <div style="background:#fff;border:2px solid #ff9900;border-radius:10px;padding:12px;
                        box-shadow:0 4px 16px rgba(255,153,0,0.1);">
                        <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;">
                            <span id="ubiEditorIcon" style="font-size:0.9rem;">🏠</span>
                            <span id="ubiEditorTitle" style="font-size:0.54rem;font-weight:900;color:#ff9900;">EDITAR DOMICILIO</span>
                        </div>

                        <!-- Smart search -->
                        <div style="margin-bottom:8px;">
                            <div style="font-size:0.4rem;font-weight:700;color:#374151;margin-bottom:3px;">
                                Buscar dirección <span style="color:#9ca3af;font-weight:500;">(dirección, coordenadas o link)</span></div>
                            <div style="position:relative;">
                                <input id="ubiBuscadorInput" type="text"
                                    placeholder="🔍 Av. Juárez 100 / 17.065,-96.72 / maps.google.com/..."
                                    style="width:100%;padding:8px 10px;border:2px solid #e5e7eb;border-radius:8px;font-size:0.46rem;
                                    background:#fff;color:#1f2937;font-weight:600;transition:border-color 0.2s;box-sizing:border-box;"
                                    autocomplete="off">
                                <div id="ubiBuscadorResults" style="display:none;position:absolute;top:100%;left:0;right:0;background:#fff;
                                    border:1px solid #e5e7eb;border-radius:8px;max-height:140px;overflow-y:auto;z-index:20;
                                    box-shadow:0 8px 20px rgba(0,0,0,0.15);"></div>
                                <div id="ubiBuscadorDetected" style="font-size:0.36rem;color:#9ca3af;margin-top:1px;min-height:10px;"></div>
                            </div>
                        </div>

                        <!-- Address fields (3-col grid, compact) -->
                        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;margin-bottom:8px;">
                            <div><label style="font-size:0.36rem;font-weight:700;color:#374151;">Calle</label>
                                <input id="ubiCalle" type="text" style="width:100%;padding:5px 6px;border:1px solid #d1d5db;border-radius:6px;
                                    font-size:0.42rem;color:#1f2937;box-sizing:border-box;background:#fafbfc;"></div>
                            <div><label style="font-size:0.36rem;font-weight:700;color:#374151;">Colonia</label>
                                <input id="ubiColonia" type="text" style="width:100%;padding:5px 6px;border:1px solid #d1d5db;border-radius:6px;
                                    font-size:0.42rem;color:#1f2937;box-sizing:border-box;background:#fafbfc;"></div>
                            <div><label style="font-size:0.36rem;font-weight:700;color:#374151;">Ciudad</label>
                                <input id="ubiCiudad" type="text" style="width:100%;padding:5px 6px;border:1px solid #d1d5db;border-radius:6px;
                                    font-size:0.42rem;color:#1f2937;box-sizing:border-box;background:#fafbfc;"></div>
                            <div><label style="font-size:0.36rem;font-weight:700;color:#374151;">Estado</label>
                                <input id="ubiEstado" type="text" style="width:100%;padding:5px 6px;border:1px solid #d1d5db;border-radius:6px;
                                    font-size:0.42rem;color:#1f2937;box-sizing:border-box;background:#fafbfc;"></div>
                            <div><label style="font-size:0.36rem;font-weight:700;color:#374151;">CP</label>
                                <input id="ubiCp" type="text" style="width:100%;padding:5px 6px;border:1px solid #d1d5db;border-radius:6px;
                                    font-size:0.42rem;color:#1f2937;box-sizing:border-box;background:#fafbfc;"></div>
                            <div><label style="font-size:0.36rem;font-weight:700;color:#374151;">Coordenadas</label>
                                <input id="ubiCoords" type="text" readonly style="width:100%;padding:5px 6px;border:1px solid #d1d5db;
                                    border-radius:6px;font-size:0.42rem;color:#6b7280;box-sizing:border-box;background:#f3f4f6;"></div>
                        </div>

                        <!-- Editor actions -->
                        <div style="display:flex;gap:6px;justify-content:flex-end;">
                            <button id="ubiEditorCancel" type="button" style="padding:6px 14px;background:#f3f4f6;color:#6b7280;
                                border:1px solid #d1d5db;border-radius:7px;font-weight:700;font-size:0.42rem;cursor:pointer;">Cancelar</button>
                            <button id="ubiEditorSave" type="button" style="padding:6px 16px;background:linear-gradient(135deg,#ff9900,#e68a00);
                                color:#fff;border:none;border-radius:7px;font-weight:800;font-size:0.42rem;cursor:pointer;
                                box-shadow:0 2px 8px rgba(255,153,0,0.3);">💾 Guardar</button>
                            <button id="ubiEditorDelete" type="button" style="padding:6px 12px;background:#fef2f2;color:#ef4444;
                                border:1px solid #fecaca;border-radius:7px;font-weight:700;font-size:0.42rem;cursor:pointer;">🗑️</button>
                        </div>
                    </div>
                </div>

                <!-- Instruction placeholder (visible when editor is hidden) -->
                <div id="ubiInstructionPlaceholder" style="flex:1;display:flex;flex-direction:column;align-items:center;
                    justify-content:center;padding:20px;text-align:center;">
                    <div style="font-size:2rem;opacity:0.2;">👆</div>
                    <div style="font-size:0.46rem;font-weight:700;color:#9ca3af;margin-top:4px;">Selecciona una ubicación para editarla</div>
                </div>

                <!-- Puntos medios — compact at bottom -->
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
                </div>
            </div>

            <!-- RIGHT PANEL: Leaflet Map (fills all remaining space) -->
            <div style="flex:1;display:flex;flex-direction:column;background:#f0f4f8;min-width:0;overflow:hidden;">
                <div style="padding:8px 14px 4px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;">
                    <div style="font-size:0.46rem;font-weight:800;color:#374151;">🗺️ Vista del mapa</div>
                    <div style="display:flex;gap:8px;">
                        <span style="display:inline-flex;align-items:center;gap:3px;font-size:0.34rem;color:#6b7280;">
                            <span style="width:7px;height:7px;border-radius:50%;background:#f59e0b;display:inline-block;"></span> Domicilio</span>
                        <span style="display:inline-flex;align-items:center;gap:3px;font-size:0.34rem;color:#6b7280;">
                            <span style="width:7px;height:7px;border-radius:50%;background:#3b82f6;display:inline-block;"></span> Negocio</span>
                        <span style="display:inline-flex;align-items:center;gap:3px;font-size:0.34rem;color:#6b7280;">
                            <span style="width:7px;height:7px;border-radius:50%;background:#ec4899;display:inline-block;"></span> Punto medio</span>
                    </div>
                </div>
                <div id="ubiMapaContainer" style="flex:1;margin:0 14px 14px;border-radius:12px;overflow:hidden;
                    border:2px solid #e5e7eb;position:relative;background:#e5e7eb;">
                    <div id="ubiLeafletMap" style="width:100%;height:100%;"></div>
                    <div id="ubiMapPlaceholder" style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
                        justify-content:center;background:#f8fafc;pointer-events:none;">
                        <div style="font-size:3rem;opacity:0.3;">🗺️</div>
                        <div style="font-size:0.48rem;font-weight:700;color:#9ca3af;margin-top:4px;">Agrega una ubicación para ver el mapa</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ── Footer (compact) ── -->
        <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 22px;
            border-top:1px solid #e5e7eb;background:#fafbfc;flex-shrink:0;">
            <div style="font-size:0.38rem;color:#9ca3af;" id="ubiFooterInfo">Haz clic en una ubicación para editarla</div>
            <button id="ubicacionesCancelar" type="button" style="padding:6px 20px;background:#6b7280;color:#fff;border:none;
                border-radius:7px;font-weight:700;font-size:0.44rem;cursor:pointer;">CERRAR</button>
        </div>
    </div>
</div>

'''

html = html[:idx_start] + new_popup + html[idx_end:]

# Also update JS: toggle ubiInstructionPlaceholder when editor opens/closes
# Find ubiOpenEditor function and add placeholder hide
old_open_editor = "panel.style.display = 'block';"
# We need the one inside ubiOpenEditor specifically
open_idx = html.index("const ubiOpenEditor = (tipo) => {")
block_after = html[open_idx:open_idx+600]
target_idx = open_idx + block_after.index("panel.style.display = 'block';")
html = html[:target_idx] + "panel.style.display = 'block';\n        const _ph = document.getElementById('ubiInstructionPlaceholder'); if(_ph) _ph.style.display='none';" + html[target_idx + len("panel.style.display = 'block';"):]

# Find ubiCloseEditor and add placeholder show
old_close = "if (panel) panel.style.display = 'none';\n        ubiRefreshCards();"
close_idx = html.index("const ubiCloseEditor = () => {")
block_after2 = html[close_idx:close_idx+300]
target_idx2 = close_idx + block_after2.index("if (panel) panel.style.display = 'none';")
old_line = "if (panel) panel.style.display = 'none';"
html = html[:target_idx2] + "if (panel) panel.style.display = 'none';\n        const _ph2 = document.getElementById('ubiInstructionPlaceholder'); if(_ph2) _ph2.style.display='flex';" + html[target_idx2 + len(old_line):]

with open('/workspaces/vistas/mockup.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Popup ajustado — sin scroll vertical, todo dentro del viewport.")
print(f"   Tamaño: {len(html)} chars")
