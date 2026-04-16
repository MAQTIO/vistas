#!/usr/bin/env python3
"""
Patch 15: Complete workflow overhaul
Flow: Cotizador → Diseño → Producción → Almacenamiento Pedidos → Reparto

Changes:
1. Strip production form (auto-filled from sales), restyle white/orange
2. Add per-area comments to cotizador (producción, diseñador, general)
3. Add DISEÑO module to main menu and abrirModuloPrincipal  
4. Add ALMACENAMIENTO PEDIDOS module
5. Connect flow: sales auto → design → production → storage → delivery
6. Enhance client locations (DOMICILIO, NEGOCIO, PUNTO MEDIO with map)
7. Enhance delivery labels with popup
"""
import re

with open('mockup.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. RESTYLE PRODUCTION CSS → White/Orange theme
# ═══════════════════════════════════════════════════════════

old_prod_css = """                .produccion-overlay {
                    display: none;
                    position: fixed;
                    inset: 0;
                    background: #0a0f1a;
                    z-index: 9100;
                    flex-direction: column;
                    overflow: hidden;
                }
                .produccion-container {
                    display: flex;
                    flex-direction: column;
                    height: 100%;
                }
                .produccion-header {
                    position: relative;
                    display: flex;
                    align-items: center;
                    justify-content: flex-start;
                    padding: 12px 20px 12px 52px;
                    background: #0d1421;
                    border-bottom: 2px solid #0288d1;
                    flex-shrink: 0;
                }
                .produccion-back {
                    position: absolute;
                    top: 10px;
                    left: 12px;
                    width: 30px;
                    height: 30px;
                    border-radius: 999px;
                    border: 1px solid #274665;
                    background: #0f1b2b;
                    color: #ffffff;
                    font-size: 0.95rem;
                    font-weight: 900;
                    line-height: 1;
                    cursor: pointer;
                    display: grid;
                    place-items: center;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
                    z-index: 2;
                }
                .produccion-back:hover {
                    background: #13263d;
                    border-color: #2d5a86;
                }
                .produccion-body {
                    display: flex;
                    flex: 1;
                    overflow: hidden;
                }
                .produccion-left {
                    width: 360px;
                    flex-shrink: 0;
                    background: #0f1724;
                    border-right: 1px solid #1e2e40;
                    overflow-y: auto;
                    padding: 14px;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }
                .produccion-right {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                    padding: 14px;
                    gap: 10px;
                }
                .prod-section-title {
                    font-size: 0.65rem;
                    font-weight: 800;
                    letter-spacing: 1px;
                    color: #7ecff5;
                    padding-bottom: 6px;
                    border-bottom: 1px solid #1e2e40;
                }"""

new_prod_css = """                .produccion-overlay {
                    display: none;
                    position: fixed;
                    inset: 0;
                    background: #f8f9fb;
                    z-index: 9100;
                    flex-direction: column;
                    overflow: hidden;
                }
                .produccion-container {
                    display: flex;
                    flex-direction: column;
                    height: 100%;
                }
                .produccion-header {
                    position: relative;
                    display: flex;
                    align-items: center;
                    justify-content: flex-start;
                    padding: 12px 20px 12px 52px;
                    background: linear-gradient(135deg, #ff9900, #ffb84d);
                    border-bottom: none;
                    flex-shrink: 0;
                }
                .produccion-back {
                    position: absolute;
                    top: 10px;
                    left: 12px;
                    width: 30px;
                    height: 30px;
                    border-radius: 999px;
                    border: none;
                    background: rgba(255,255,255,0.25);
                    color: #fff;
                    font-size: 0.95rem;
                    font-weight: 900;
                    line-height: 1;
                    cursor: pointer;
                    display: grid;
                    place-items: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                    z-index: 2;
                    backdrop-filter: blur(4px);
                }
                .produccion-back:hover {
                    background: rgba(255,255,255,0.4);
                }
                .produccion-body {
                    display: flex;
                    flex: 1;
                    overflow: hidden;
                }
                .produccion-left {
                    width: 340px;
                    flex-shrink: 0;
                    background: #fff;
                    border-right: 1px solid #e5e7eb;
                    overflow-y: auto;
                    padding: 14px;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }
                .produccion-right {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                    padding: 14px;
                    gap: 10px;
                    background: #f8f9fb;
                }
                .prod-section-title {
                    font-size: 0.65rem;
                    font-weight: 800;
                    letter-spacing: 1px;
                    color: #ff9900;
                    padding-bottom: 6px;
                    border-bottom: 1px solid #fde8c8;
                }"""

html = html.replace(old_prod_css, new_prod_css, 1)

# Restyle prod form fields
old_prod_form_css = """                .prod-form { display: flex; flex-direction: column; gap: 8px; }
                .prod-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
                .prod-field { display: flex; flex-direction: column; gap: 3px; }
                .prod-field label { font-size: 0.6rem; font-weight: 700; color: #7a9ab4; letter-spacing: 0.5px; }
                .prod-field input,
                .prod-field select,
                .prod-field textarea {
                    background: #0d1421;
                    border: 1px solid #1e3048;
                    color: #e0eaf4;
                    border-radius: 6px;
                    padding: 6px 8px;
                    font-size: 0.7rem;
                    outline: none;
                    transition: border-color 0.15s;
                    font-family: inherit;
                    resize: vertical;
                }
                .prod-field input:focus,
                .prod-field select:focus,
                .prod-field textarea:focus { border-color: #0288d1; }
                .prod-save-btn {
                    background: linear-gradient(135deg, #0277bd, #0288d1);
                    color: #fff;
                    border: none;
                    padding: 10px;
                    border-radius: 8px;
                    font-size: 0.75rem;
                    font-weight: 700;
                    cursor: pointer;
                    transition: filter 0.15s;
                    margin-top: 4px;
                }
                .prod-save-btn:hover { filter: brightness(1.1); }
                .prod-save-btn:disabled { opacity: 0.5; cursor: not-allowed; filter: none; }"""

new_prod_form_css = """                .prod-form { display: flex; flex-direction: column; gap: 8px; }
                .prod-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
                .prod-field { display: flex; flex-direction: column; gap: 3px; }
                .prod-field label { font-size: 0.6rem; font-weight: 700; color: #92400e; letter-spacing: 0.5px; }
                .prod-field input,
                .prod-field select,
                .prod-field textarea {
                    background: #fffbf5;
                    border: 1px solid #fde8c8;
                    color: #1f2937;
                    border-radius: 6px;
                    padding: 6px 8px;
                    font-size: 0.7rem;
                    outline: none;
                    transition: border-color 0.15s;
                    font-family: inherit;
                    resize: vertical;
                }
                .prod-field input:focus,
                .prod-field select:focus,
                .prod-field textarea:focus { border-color: #ff9900; }
                .prod-save-btn {
                    background: linear-gradient(135deg, #ff9900, #ffb84d);
                    color: #fff;
                    border: none;
                    padding: 10px;
                    border-radius: 8px;
                    font-size: 0.75rem;
                    font-weight: 700;
                    cursor: pointer;
                    transition: filter 0.15s;
                    margin-top: 4px;
                }
                .prod-save-btn:hover { filter: brightness(1.08); }
                .prod-save-btn:disabled { opacity: 0.5; cursor: not-allowed; filter: none; }"""

html = html.replace(old_prod_form_css, new_prod_form_css, 1)

# Restyle prod tabs
old_tab_css = """                .prod-tab {
                    background: rgba(255,255,255,0.05);
                    border: 1px solid #1e3048;
                    color: #7a9ab4;
                    padding: 6px 12px;
                    border-radius: 8px;
                    font-size: 0.62rem;
                    font-weight: 700;
                    cursor: pointer;
                    transition: all 0.15s;
                    white-space: nowrap;
                }
                .prod-tab:hover { background: rgba(255,255,255,0.08); }
                .prod-tab.active { background: #0288d1; border-color: #0288d1; color: #fff; }"""

new_tab_css = """                .prod-tab {
                    background: #fff;
                    border: 1px solid #e5e7eb;
                    color: #6b7280;
                    padding: 6px 12px;
                    border-radius: 8px;
                    font-size: 0.62rem;
                    font-weight: 700;
                    cursor: pointer;
                    transition: all 0.15s;
                    white-space: nowrap;
                }
                .prod-tab:hover { background: #fff7ed; }
                .prod-tab.active { background: #ff9900; border-color: #ff9900; color: #fff; }"""

html = html.replace(old_tab_css, new_tab_css, 1)

# Restyle search bar
old_search_css = """                .prod-search-bar input {
                    flex: 1;
                    background: #0d1421;
                    border: 1px solid #1e3048;
                    color: #e0eaf4;
                    border-radius: 8px;
                    padding: 7px 10px;
                    font-size: 0.7rem;
                    outline: none;
                }
                .prod-search-bar input:focus { border-color: #0288d1; }
                .prod-search-bar button {
                    background: rgba(255,255,255,0.07);
                    border: 1px solid #1e3048;
                    color: #fff;
                    border-radius: 8px;
                    padding: 0 12px;
                    cursor: pointer;
                    font-size: 0.9rem;
                    transition: background 0.15s;
                }
                .prod-search-bar button:hover { background: rgba(255,255,255,0.14); }"""

new_search_css = """                .prod-search-bar input {
                    flex: 1;
                    background: #fff;
                    border: 1px solid #e5e7eb;
                    color: #1f2937;
                    border-radius: 8px;
                    padding: 7px 10px;
                    font-size: 0.7rem;
                    outline: none;
                }
                .prod-search-bar input:focus { border-color: #ff9900; }
                .prod-search-bar button {
                    background: #fff7ed;
                    border: 1px solid #fde8c8;
                    color: #92400e;
                    border-radius: 8px;
                    padding: 0 12px;
                    cursor: pointer;
                    font-size: 0.9rem;
                    transition: background 0.15s;
                }
                .prod-search-bar button:hover { background: #ffedd5; }"""

html = html.replace(old_search_css, new_search_css, 1)

# Restyle order cards and loading
old_card_css = """                .prod-loading, .prod-empty {
                    text-align: center;
                    color: #4a6a84;
                    font-size: 0.72rem;
                    padding: 30px;
                }
                .prod-orden-card {
                    background: #0d1421;
                    border: 1px solid #1e2e40;
                    border-radius: 10px;
                    padding: 12px 14px;
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                    transition: border-color 0.15s;
                }
                .prod-orden-card:hover { border-color: #0288d1; }"""

new_card_css = """                .prod-loading, .prod-empty {
                    text-align: center;
                    color: #9ca3af;
                    font-size: 0.72rem;
                    padding: 30px;
                }
                .prod-orden-card {
                    background: #fff;
                    border: 1px solid #e5e7eb;
                    border-radius: 10px;
                    padding: 12px 14px;
                    display: flex;
                    flex-direction: column;
                    gap: 8px;
                    transition: border-color 0.15s;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
                }
                .prod-orden-card:hover { border-color: #ff9900; }"""

html = html.replace(old_card_css, new_card_css, 1)

# Restyle folio and info
old_info_css = """                .prod-orden-folio {
                    font-size: 0.8rem;
                    font-weight: 800;
                    color: #29b6f6;
                }
                .prod-orden-fecha {
                    font-size: 0.58rem;
                    color: #4a6a84;
                }
                .prod-orden-info {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 3px 12px;
                    font-size: 0.63rem;
                    color: #a0b8cc;
                }
                .prod-orden-info strong { color: #ccdde9; }"""

new_info_css = """                .prod-orden-folio {
                    font-size: 0.8rem;
                    font-weight: 800;
                    color: #ff9900;
                }
                .prod-orden-fecha {
                    font-size: 0.58rem;
                    color: #9ca3af;
                }
                .prod-orden-info {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 3px 12px;
                    font-size: 0.63rem;
                    color: #6b7280;
                }
                .prod-orden-info strong { color: #374151; }"""

html = html.replace(old_info_css, new_info_css, 1)

# Restyle status select
old_status_css = """                .prod-status-select {
                    background: #0a111d;
                    border: 1px solid #1e3048;
                    color: #e0eaf4;
                    border-radius: 6px;
                    padding: 4px 8px;
                    font-size: 0.62rem;
                    font-weight: 700;
                    cursor: pointer;
                    outline: none;
                }"""

new_status_css = """                .prod-status-select {
                    background: #fff;
                    border: 1px solid #e5e7eb;
                    color: #374151;
                    border-radius: 6px;
                    padding: 4px 8px;
                    font-size: 0.62rem;
                    font-weight: 700;
                    cursor: pointer;
                    outline: none;
                }"""

html = html.replace(old_status_css, new_status_css, 1)

# Restyle action buttons
old_btn_css = """                .prod-btn-action {
                    background: rgba(255,255,255,0.07);
                    border: 1px solid rgba(255,255,255,0.1);
                    color: #e0eaf4;
                    padding: 4px 10px;
                    border-radius: 6px;
                    font-size: 0.62rem;
                    font-weight: 700;
                    cursor: pointer;
                    transition: background 0.15s;
                }
                .prod-btn-action:hover { background: rgba(255,255,255,0.15); }
                .prod-btn-action.print { background: rgba(255,153,0,0.12); border-color: rgba(255,153,0,0.3); color: #ffb300; }
                .prod-btn-action.print:hover { background: rgba(255,153,0,0.22); }
                .prod-btn-action.del { background: rgba(244,67,54,0.1); border-color: rgba(244,67,54,0.25); color: #ef5350; }
                .prod-btn-action.del:hover { background: rgba(244,67,54,0.2); }
                .prod-btn-action.entrega { background: rgba(76,175,80,0.12); border-color: rgba(76,175,80,0.3); color: #81c784; }
                .prod-btn-action.entrega:hover { background: rgba(76,175,80,0.22); }"""

new_btn_css = """                .prod-btn-action {
                    background: #f9fafb;
                    border: 1px solid #e5e7eb;
                    color: #374151;
                    padding: 4px 10px;
                    border-radius: 6px;
                    font-size: 0.62rem;
                    font-weight: 700;
                    cursor: pointer;
                    transition: background 0.15s;
                }
                .prod-btn-action:hover { background: #f3f4f6; }
                .prod-btn-action.print { background: #fff7ed; border-color: #fde8c8; color: #92400e; }
                .prod-btn-action.print:hover { background: #ffedd5; }
                .prod-btn-action.del { background: #fef2f2; border-color: #fecaca; color: #dc2626; }
                .prod-btn-action.del:hover { background: #fee2e2; }
                .prod-btn-action.entrega { background: #f0fdf4; border-color: #bbf7d0; color: #166534; }
                .prod-btn-action.entrega:hover { background: #dcfce7; }"""

html = html.replace(old_btn_css, new_btn_css, 1)

# Restyle PDF drop zone
old_pdf_css = """                .pdf-drop-zone {
                    border: 2px dashed #0288d1;
                    border-radius: 10px;
                    padding: 16px 10px;
                    text-align: center;
                    cursor: pointer;
                    transition: border-color 0.15s, background 0.15s;
                    background: rgba(2,136,209,0.05);
                }
                .pdf-drop-zone:hover, .pdf-drop-zone.drag-over {
                    border-color: #29b6f6;
                    background: rgba(41,182,246,0.1);
                }
                .pdf-drop-icon { font-size: 1.8rem; line-height: 1; }
                .pdf-drop-text { font-size: 0.68rem; color: #90bdd4; margin-top: 6px; line-height: 1.4; }
                .pdf-link { color: #29b6f6; cursor: pointer; text-decoration: underline; }"""

new_pdf_css = """                .pdf-drop-zone {
                    border: 2px dashed #fbbf24;
                    border-radius: 10px;
                    padding: 16px 10px;
                    text-align: center;
                    cursor: pointer;
                    transition: border-color 0.15s, background 0.15s;
                    background: rgba(255,153,0,0.04);
                }
                .pdf-drop-zone:hover, .pdf-drop-zone.drag-over {
                    border-color: #ff9900;
                    background: rgba(255,153,0,0.08);
                }
                .pdf-drop-icon { font-size: 1.8rem; line-height: 1; }
                .pdf-drop-text { font-size: 0.68rem; color: #92400e; margin-top: 6px; line-height: 1.4; }
                .pdf-link { color: #ff9900; cursor: pointer; text-decoration: underline; }"""

html = html.replace(old_pdf_css, new_pdf_css, 1)


# ═══════════════════════════════════════════════════════════
# 2. REPLACE PRODUCTION HTML — Remove form, make it read-only list
# ═══════════════════════════════════════════════════════════

old_prod_header = """      <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:1.6rem;line-height:1;">📦</span>
        <div>
          <div style="font-size:1rem;font-weight:800;color:#fff;letter-spacing:0.5px;">MÓDULO DE PRODUCCIÓN</div>
          <div style="font-size:0.6rem;color:#4a8fad;">Gestión de órdenes recibidas y autorizadas</div>
        </div>
      </div>"""

new_prod_header = """      <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:1.6rem;line-height:1;">🏭</span>
        <div>
          <div style="font-size:1rem;font-weight:800;color:#fff;letter-spacing:0.5px;">PRODUCCIÓN</div>
          <div style="font-size:0.6rem;color:rgba(255,255,255,0.7);">Órdenes autorizadas desde diseño — más urgente primero</div>
        </div>
      </div>"""

html = html.replace(old_prod_header, new_prod_header, 1)

# Replace entire production left panel (strip the form)
old_prod_left_start = """      <div class="produccion-left">
        <div class="prod-section-title">📄 NUEVA ORDEN DE PRODUCCIÓN</div>
        <div class="prod-form">"""

# Find the end of prod-form and replace entire left panel
idx_left_start = html.find(old_prod_left_start)
if idx_left_start >= 0:
    # Find closing of produccion-left </div>
    # The left panel ends at </div>\n      <div class="produccion-right">
    idx_right_start = html.find('<div class="produccion-right">', idx_left_start)
    if idx_right_start >= 0:
        # Find the closing tag right before produccion-right
        # Walk back to find the </div> that closes produccion-left
        search_back = html[idx_left_start:idx_right_start]
        # Count opening divs to find proper close
        # Simple approach: replace everything from left start to right start  
        new_left_panel = """      <div class="produccion-left">
        <div class="prod-section-title">📊 RESUMEN DE PRODUCCIÓN</div>
        <div style="display:flex;flex-direction:column;gap:10px;">
          <div style="background:#fff7ed;border:1px solid #fde8c8;border-radius:10px;padding:12px;">
            <div style="font-size:0.6rem;font-weight:700;color:#92400e;margin-bottom:6px;">⏳ PENDIENTES</div>
            <div id="prodResumenPendientes" style="font-size:1.5rem;font-weight:900;color:#ff9900;">0</div>
          </div>
          <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:12px;">
            <div style="font-size:0.6rem;font-weight:700;color:#166534;margin-bottom:6px;">⚙️ EN PROCESO</div>
            <div id="prodResumenEnProceso" style="font-size:1.5rem;font-weight:900;color:#16a34a;">0</div>
          </div>
          <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;padding:12px;">
            <div style="font-size:0.6rem;font-weight:700;color:#1e40af;margin-bottom:6px;">✅ TERMINADAS HOY</div>
            <div id="prodResumenTerminadas" style="font-size:1.5rem;font-weight:900;color:#2563eb;">0</div>
          </div>
        </div>

        <div class="prod-section-title" style="margin-top:8px;">📝 NOTAS DE PRODUCCIÓN</div>
        <div class="prod-field">
          <textarea id="prodNotasGenerales" rows="4" placeholder="Anotaciones del equipo de producción..." style="background:#fffbf5;border:1px solid #fde8c8;color:#1f2937;border-radius:8px;padding:8px;font-size:0.7rem;resize:vertical;font-family:inherit;"></textarea>
          <button id="btnGuardarNotasProd" type="button" style="margin-top:4px;background:#ff9900;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:0.65rem;font-weight:700;cursor:pointer;">💾 Guardar notas</button>
        </div>

        <div class="prod-section-title" style="margin-top:8px;">📦 SOLICITAR INSUMOS</div>
        <div class="prod-field">
          <input type="text" id="prodInsumoNombre" placeholder="Nombre del insumo" style="background:#fffbf5;border:1px solid #fde8c8;color:#1f2937;border-radius:6px;padding:6px 8px;font-size:0.7rem;">
        </div>
        <div class="prod-row">
          <div class="prod-field">
            <input type="number" id="prodInsumoCantidad" placeholder="Cantidad" min="1" style="background:#fffbf5;border:1px solid #fde8c8;color:#1f2937;border-radius:6px;padding:6px 8px;font-size:0.7rem;">
          </div>
          <div class="prod-field">
            <select id="prodInsumoUrgencia" style="background:#fffbf5;border:1px solid #fde8c8;color:#1f2937;border-radius:6px;padding:6px 8px;font-size:0.7rem;">
              <option value="normal">Normal</option>
              <option value="urgente">Urgente</option>
            </select>
          </div>
        </div>
        <button id="btnSolicitarInsumo" type="button" class="prod-save-btn" style="font-size:0.68rem;">📦 Solicitar insumo</button>
        <div id="prodInsumosSolicitados" style="margin-top:6px;font-size:0.62rem;color:#6b7280;max-height:120px;overflow-y:auto;"></div>
      </div>
"""
        html = html[:idx_left_start] + new_left_panel + html[idx_right_start:]


# ═══════════════════════════════════════════════════════════
# 3. ADD COMMENTS FIELDS TO COTIZADOR (per area)
# ═══════════════════════════════════════════════════════════

old_comments = """            <div class="orden-field">
                <label>COMENTARIOS</label>
                <textarea id="ordenComentarios" rows="2" placeholder="Comentarios de la orden"></textarea>
            </div>"""

new_comments = """            <div class="orden-field">
                <label>COMENTARIOS GENERALES</label>
                <textarea id="ordenComentarios" rows="2" placeholder="Comentarios visibles para todos"></textarea>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                <div class="orden-field">
                    <label>📝 NOTAS PARA PRODUCCIÓN</label>
                    <textarea id="ordenNotasProduccion" rows="2" placeholder="Instrucciones para el equipo de producción..." style="border-color:#fde8c8;background:#fffbf5;"></textarea>
                </div>
                <div class="orden-field">
                    <label>🎨 NOTAS PARA DISEÑADOR</label>
                    <textarea id="ordenNotasDisenador" rows="2" placeholder="Indicaciones para el diseñador..." style="border-color:#e0e7ff;background:#f5f7ff;"></textarea>
                </div>
            </div>"""

html = html.replace(old_comments, new_comments, 1)


# ═══════════════════════════════════════════════════════════
# 4. ADD NEW MODULES TO MENU (Diseño, Almacén Pedidos)
# ═══════════════════════════════════════════════════════════

old_menu = """            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('PRODUCCION')"><span class="ico">🏭</span><span>PRODUCCION</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('REPARTO')"><span class="ico">🚚</span><span>REPARTO</span></button>"""

new_menu = """            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('DISENO')"><span class="ico">🎨</span><span>DISEÑO</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('PRODUCCION')"><span class="ico">🏭</span><span>PRODUCCIÓN</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('ALMACEN PEDIDOS')"><span class="ico">📦</span><span>ALMACÉN PEDIDOS</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('REPARTO')"><span class="ico">🚚</span><span>REPARTO</span></button>"""

html = html.replace(old_menu, new_menu, 1)


# ═══════════════════════════════════════════════════════════
# 5. ADD DISEÑO AND ALMACÉN PEDIDOS handlers in abrirModuloPrincipal
# ═══════════════════════════════════════════════════════════

old_prod_handler = """        if (key === 'PRODUCCION') {
            ocultarInicioSistema();
            if (window.openProduccionPopupGlobal) window.openProduccionPopupGlobal();
            return;
        }"""

new_prod_handler = """        if (key === 'DISENO' || key === 'DISEÑO') {
            ocultarInicioSistema();
            if (window.openDisenoPopupGlobal) window.openDisenoPopupGlobal();
            return;
        }

        if (key === 'PRODUCCION') {
            ocultarInicioSistema();
            if (window.openProduccionPopupGlobal) window.openProduccionPopupGlobal();
            return;
        }

        if (key === 'ALMACEN PEDIDOS') {
            ocultarInicioSistema();
            if (window.openAlmacenPedidosPopupGlobal) window.openAlmacenPedidosPopupGlobal();
            return;
        }"""

html = html.replace(old_prod_handler, new_prod_handler, 1)


# ═══════════════════════════════════════════════════════════
# 6. ADD buildPedidoRegistro to include new notes fields
# ═══════════════════════════════════════════════════════════

old_build = """        return {
            id: `MP-${Date.now().toString(36).toUpperCase()}`,
            tipo,
            folio: ordenTrabajoFolio,
            clienteNombre,
            telefono,
            metodoPago,
            disenador,
            vendedor,
            fechaEmitida: todayISO(),
            fechaEntrega,
            estatusProduccion: 'pendiente',
            anticipo,
            adeudoCliente,
            lineas,
            producto: productoResumen,
            subtotal: subtotalVal,
            impuestos: impuestosVal,
            descuento: descuentoVal,
            total: totalVal,
            inversion: inversionVal,
            ganancia: gananciaVal
        };"""

new_build = """        const notasProduccion = (el('ordenNotasProduccion')?.value || '').trim();
        const notasDisenador = (el('ordenNotasDisenador')?.value || '').trim();
        const comentariosGenerales = (el('ordenComentarios')?.value || '').trim();

        return {
            id: `MP-${Date.now().toString(36).toUpperCase()}`,
            tipo,
            folio: ordenTrabajoFolio,
            clienteNombre,
            telefono,
            metodoPago,
            disenador,
            vendedor,
            fechaEmitida: todayISO(),
            fechaEntrega,
            estatusProduccion: 'pendiente',
            anticipo,
            adeudoCliente,
            lineas,
            producto: productoResumen,
            subtotal: subtotalVal,
            impuestos: impuestosVal,
            descuento: descuentoVal,
            total: totalVal,
            inversion: inversionVal,
            ganancia: gananciaVal,
            notasProduccion,
            notasDisenador,
            comentarios: comentariosGenerales
        };"""

html = html.replace(old_build, new_build, 1)


# ═══════════════════════════════════════════════════════════
# 7. UPDATE auto-send to production to include notes & send to DISEÑO first
# ═══════════════════════════════════════════════════════════

old_auto_send = """        // Auto-enviar a producción cuando se registra una venta
        if (typeof window.enviarAutoAProduccion === 'function' && venta.lineas && venta.lineas.length) {
            const linea0 = venta.lineas[0];
            const cantTotal = venta.lineas.reduce((s, l) => s + Number(l.cantidad || 1), 0);
            window.enviarAutoAProduccion({
                folio: venta.folio,
                clienteNombre: venta.clienteNombre,
                telefono: venta.telefono,
                clienteId: '',
                fechaEntrega: venta.fechaEntrega,
                producto: typeof window.mapProductoParaProduccion === 'function' ? window.mapProductoParaProduccion(linea0.producto) : linea0.producto,
                medida: linea0.medida || '',
                cantidad: cantTotal,
                total: venta.total,
                origen: 'venta'
            });
        }"""

new_auto_send = """        // Auto-enviar a DISEÑO cuando se registra una venta (Diseño → Producción → Almacén → Reparto)
        if (typeof window.enviarAutoADiseno === 'function' && venta.lineas && venta.lineas.length) {
            window.enviarAutoADiseno(venta);
        } else if (typeof window.enviarAutoAProduccion === 'function' && venta.lineas && venta.lineas.length) {
            const linea0 = venta.lineas[0];
            const cantTotal = venta.lineas.reduce((s, l) => s + Number(l.cantidad || 1), 0);
            window.enviarAutoAProduccion({
                folio: venta.folio,
                clienteNombre: venta.clienteNombre,
                telefono: venta.telefono,
                clienteId: '',
                fechaEntrega: venta.fechaEntrega,
                producto: typeof window.mapProductoParaProduccion === 'function' ? window.mapProductoParaProduccion(linea0.producto) : linea0.producto,
                medida: linea0.medida || '',
                cantidad: cantTotal,
                total: venta.total,
                origen: 'venta',
                notasProduccion: venta.notasProduccion || '',
                notasDisenador: venta.notasDisenador || ''
            });
        }"""

html = html.replace(old_auto_send, new_auto_send, 1)


# ═══════════════════════════════════════════════════════════
# 8. UPDATE PRODUCTION renderOrdenes — remove phone/prices, sort by urgency
# ═══════════════════════════════════════════════════════════

# Replace the card rendering in renderOrdenes to exclude phone/prices
old_render_card = """            return '<div class="prod-orden-card" data-id="'+esc(o.id)+'">'+
                '<div class="prod-orden-top">'+
                  '<div><div class="prod-orden-folio">'+esc(o.folio||'Sin folio')+'</div><div class="prod-orden-fecha">'+fecha+' · Urgencia '+esc(urg.text)+' ('+esc(String(urg.days))+'d)</div></div>'+
                  '<select class="prod-status-select" data-id="'+esc(o.id)+'">'+opts+'</select>'+
                '</div>'+
                '<div class="prod-orden-info">'+
                  '<span><strong>Cliente:</strong> '+esc(o.cliente||'—')+'</span>'+
                                    '<span><strong>Teléfono:</strong> '+esc(o.telefono||'—')+'</span>'+
                                    '<span><strong>ID Cliente:</strong> '+esc(o.clienteId||'—')+'</span>'+
                  '<span><strong>Producto:</strong> '+esc(o.producto||'—')+'</span>'+
                                      '<span><strong>'+esc(colorLabel)+':</strong> '+esc(o.color||'—')+'</span>'+
                  '<span><strong>Cantidad:</strong> '+esc(o.cantidad||'—')+'</span>'+
                                    '<span><strong>Detalle Producto:</strong> '+esc(o.detalleProducto||'—')+'</span>'+
                                    '<span><strong>Creación:</strong> '+esc(o.fechaCreacion||'—')+'</span>'+
                                    '<span><strong>Entrega:</strong> '+esc(o.fechaEntrega||'—')+'</span>'+
                  (o.notas?'<span style="grid-column:1/-1"><strong>Notas:</strong> '+esc(o.notas)+'</span>':'')+
                '</div>'+"""

new_render_card = """            var urgColor = urg.text === 'ALTA' ? '#dc2626' : urg.text === 'MEDIA' ? '#f59e0b' : '#16a34a';
            var urgBg = urg.text === 'ALTA' ? '#fef2f2' : urg.text === 'MEDIA' ? '#fffbeb' : '#f0fdf4';
            return '<div class="prod-orden-card" data-id="'+esc(o.id)+'" style="border-left:3px solid '+urgColor+';">'+
                '<div class="prod-orden-top">'+
                  '<div><div class="prod-orden-folio">'+esc(o.folio||'Sin folio')+'</div>'+
                  '<div class="prod-orden-fecha"><span style="display:inline-block;padding:1px 6px;border-radius:4px;background:'+urgBg+';color:'+urgColor+';font-weight:700;">'+esc(urg.text)+' ('+esc(String(urg.days))+'d)</span> · Entrega: '+esc(o.fechaEntrega||'—')+'</div></div>'+
                  '<select class="prod-status-select" data-id="'+esc(o.id)+'">'+opts+'</select>'+
                '</div>'+
                '<div class="prod-orden-info">'+
                  '<span><strong>Cliente:</strong> '+esc(o.cliente||'—')+'</span>'+
                  '<span><strong>Producto:</strong> '+esc(o.producto||'—')+'</span>'+
                  '<span><strong>'+esc(colorLabel)+':</strong> '+esc(o.color||'—')+'</span>'+
                  '<span><strong>Cantidad:</strong> '+esc(o.cantidad||'—')+'</span>'+
                  '<span><strong>Detalle:</strong> '+esc(o.detalleProducto||'—')+'</span>'+
                  '<span><strong>Creación:</strong> '+esc(o.fechaCreacion||'—')+'</span>'+
                  (o.notas?'<span style="grid-column:1/-1"><strong>Notas prod:</strong> '+esc(o.notas)+'</span>':'')+
                  (o.disenoUrl?'<span style="grid-column:1/-1"><a href="'+esc(o.disenoUrl)+'" target="_blank" style="color:#ff9900;font-weight:700;">🎨 Ver diseño</a></span>':'')+
                '</div>'+"""

html = html.replace(old_render_card, new_render_card, 1)

# Update action buttons — add "return to pending" button and remove ver-diseno button (now inline)
old_action_btns = """                                    (o.estado === 'pendiente' ? '<button class="prod-btn-action" data-action="iniciar" data-id="'+esc(o.id)+'">🚀 Comenzar</button>' : '')+
                                    (o.estado === 'terminada' ? '<button class="prod-btn-action entrega" data-action="a-entregas" data-id="'+esc(o.id)+'">🚚 A Entregas</button>' : '')+
                                    '<button class="prod-btn-action" data-action="ver-diseno" data-id="'+esc(o.id)+'" '+(o.disenoUrl ? '' : 'style="opacity:0.45;pointer-events:none;"')+'>🎨 Ver diseño</button>'+
                                    '<button class="prod-btn-action" data-action="etiqueta" data-id="'+esc(o.id)+'">🏷 Etiqueta</button>'+
                  '<button class="prod-btn-action print" data-action="imprimir" data-id="'+esc(o.id)+'">🖨 Imprimir</button>'+
                  '<button class="prod-btn-action del" data-action="eliminar" data-id="'+esc(o.id)+'">🗑</button>'+"""

new_action_btns = """                                    (o.estado === 'pendiente' ? '<button class="prod-btn-action" style="background:#fff7ed;border-color:#fde8c8;color:#92400e;" data-action="iniciar" data-id="'+esc(o.id)+'">🚀 Iniciar</button>' : '')+
                                    (o.estado === 'en_proceso' ? '<button class="prod-btn-action" style="background:#fef2f2;border-color:#fecaca;color:#dc2626;" data-action="a-pendiente" data-id="'+esc(o.id)+'">⏸ A Pendiente</button>' : '')+
                                    (o.estado === 'terminada' ? '<button class="prod-btn-action entrega" data-action="a-almacen" data-id="'+esc(o.id)+'">📦 A Almacén</button>' : '')+
                                    '<button class="prod-btn-action" data-action="etiqueta" data-id="'+esc(o.id)+'">🏷 Etiqueta</button>'+
                  '<button class="prod-btn-action print" data-action="imprimir" data-id="'+esc(o.id)+'">🖨</button>'+
                  '<button class="prod-btn-action del" data-action="eliminar" data-id="'+esc(o.id)+'">🗑</button>'+"""

html = html.replace(old_action_btns, new_action_btns, 1)

# Add handler for a-pendiente and a-almacen actions
old_action_handlers = """                if(action==='iniciar') iniciarTrabajoOrden(docId);
                if(action==='ver-diseno') verDisenoOrden(orden);
                if(action==='etiqueta') imprimirEtiquetaOrden(orden);
                if(action==='imprimir') imprimirOrden(orden);
                if(action==='eliminar') eliminarOrden(docId);
                if(action==='a-entregas') enviarAEntregas(orden);"""

new_action_handlers = """                if(action==='iniciar') iniciarTrabajoOrden(docId);
                if(action==='a-pendiente') regresarAPendiente(docId);
                if(action==='etiqueta') imprimirEtiquetaOrden(orden);
                if(action==='imprimir') imprimirOrden(orden);
                if(action==='eliminar') eliminarOrden(docId);
                if(action==='a-almacen') enviarAAlmacenPedidos(orden);"""

html = html.replace(old_action_handlers, new_action_handlers, 1)

# Add regresarAPendiente function and enviarAAlmacenPedidos - insert after iniciarTrabajoOrden
old_iniciar_fn = """    async function iniciarTrabajoOrden(docId) {
        var db = getProdDB(); if (!db) return;
        try {
            await db.collection(PROD_COLLECTION).doc(docId).update({
                estado: 'en_proceso',
                inicioTrabajoEn: window.firebase.firestore.FieldValue.serverTimestamp(),
                actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
            });
            var o = allOrders.find(function(x){ return x.id === docId; });
            if (o) o.estado = 'en_proceso';
            renderOrdenes();
        } catch (err) {
            alert('Error al iniciar orden: ' + err.message);
        }
    }"""

new_iniciar_fn = """    async function iniciarTrabajoOrden(docId) {
        var db = getProdDB(); if (!db) return;
        try {
            await db.collection(PROD_COLLECTION).doc(docId).update({
                estado: 'en_proceso',
                inicioTrabajoEn: window.firebase.firestore.FieldValue.serverTimestamp(),
                actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
            });
            var o = allOrders.find(function(x){ return x.id === docId; });
            if (o) o.estado = 'en_proceso';
            renderOrdenes();
            actualizarResumenProduccion();
        } catch (err) {
            alert('Error al iniciar orden: ' + err.message);
        }
    }

    async function regresarAPendiente(docId) {
        var motivo = prompt('Motivo para regresar a pendiente (ej: falta material, error, etc.):');
        if (motivo === null) return;
        var db = getProdDB(); if (!db) return;
        try {
            await db.collection(PROD_COLLECTION).doc(docId).update({
                estado: 'pendiente',
                motivoPendiente: motivo || 'Sin motivo especificado',
                actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
            });
            var o = allOrders.find(function(x){ return x.id === docId; });
            if (o) { o.estado = 'pendiente'; o.motivoPendiente = motivo; }
            renderOrdenes();
            actualizarResumenProduccion();
        } catch (err) {
            alert('Error: ' + err.message);
        }
    }

    async function enviarAAlmacenPedidos(orden) {
        var db = getProdDB(); if (!db) return;
        try {
            var existing = await db.collection('stored_orders')
                .where('folioProduccion', '==', String(orden.folio || ''))
                .limit(1).get();
            if (!existing.empty) {
                alert('Esta orden ya está en almacén de pedidos (folio ' + orden.folio + ').');
                return;
            }
            await db.collection('stored_orders').add({
                folioProduccion: String(orden.folio || ''),
                produccionDocId: orden.id || '',
                cliente: orden.cliente || '',
                clienteId: orden.clienteId || '',
                producto: orden.producto || '',
                cantidad: orden.cantidad || '',
                detalleProducto: orden.detalleProducto || '',
                color: orden.color || '',
                fechaEntrega: orden.fechaEntrega || '',
                disenoUrl: orden.disenoUrl || '',
                estado: 'almacenado',
                envioDecidido: false,
                creadoEn: window.firebase.firestore.FieldValue.serverTimestamp(),
                actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
            });
            await db.collection(PROD_COLLECTION).doc(orden.id).update({ estado: 'almacenada', actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp() });
            var o = allOrders.find(function(x){ return x.id === orden.id; });
            if (o) o.estado = 'almacenada';
            renderOrdenes();
            actualizarResumenProduccion();
            alert('✅ Pedido enviado a Almacén de Pedidos.');
        } catch (err) {
            alert('Error: ' + err.message);
        }
    }

    function actualizarResumenProduccion() {
        var pend = allOrders.filter(function(o){ return o.estado === 'pendiente'; }).length;
        var proc = allOrders.filter(function(o){ return o.estado === 'en_proceso'; }).length;
        var hoy = new Date().toISOString().slice(0,10);
        var term = allOrders.filter(function(o){ return o.estado === 'terminada' && o.fechaCreacion === hoy; }).length;
        var el1 = document.getElementById('prodResumenPendientes'); if (el1) el1.textContent = pend;
        var el2 = document.getElementById('prodResumenEnProceso'); if (el2) el2.textContent = proc;
        var el3 = document.getElementById('prodResumenTerminadas'); if (el3) el3.textContent = term;
    }"""

html = html.replace(old_iniciar_fn, new_iniciar_fn, 1)

# Update cargarOrdenes to call actualizarResumenProduccion
old_load_orders = """            allOrders = snap.docs.map(function(doc){ return Object.assign({id:doc.id}, doc.data()); });
            renderOrdenes();
        }).catch"""

new_load_orders = """            allOrders = snap.docs.map(function(doc){ return Object.assign({id:doc.id}, doc.data()); });
            renderOrdenes();
            actualizarResumenProduccion();
        }).catch"""

html = html.replace(old_load_orders, new_load_orders, 1)


# ═══════════════════════════════════════════════════════════
# 9. ADD CSS FOR NEW MODULES (Diseño, Almacén Pedidos) before entrega CSS
# ═══════════════════════════════════════════════════════════

# Find entrega CSS section
entrega_css_marker = """                /* ═══════════════════════════════════════════════════════
                   MÓDULO DE ENTREGAS
                ════════════════════════════════════════════════════════ */"""

new_modules_css = """                /* ═══════════════════════════════════════════════════════
                   MÓDULO DE DISEÑO
                ════════════════════════════════════════════════════════ */
                .diseno-overlay {
                    display: none; position: fixed; inset: 0; background: #f5f3ff; z-index: 9100; flex-direction: column; overflow: hidden;
                }
                .diseno-header {
                    position: relative; display: flex; align-items: center; justify-content: flex-start; padding: 12px 20px 12px 52px;
                    background: linear-gradient(135deg, #7c3aed, #a78bfa); border-bottom: none; flex-shrink: 0;
                }
                .diseno-back {
                    position: absolute; top: 10px; left: 12px; width: 30px; height: 30px; border-radius: 999px;
                    border: none; background: rgba(255,255,255,0.25); color: #fff; font-size: 0.95rem; font-weight: 900;
                    cursor: pointer; display: grid; place-items: center; z-index: 2; backdrop-filter: blur(4px);
                }
                .diseno-back:hover { background: rgba(255,255,255,0.4); }
                .diseno-body { display: flex; flex: 1; overflow: hidden; }
                .diseno-list-panel {
                    flex: 1; display: flex; flex-direction: column; overflow: hidden; padding: 14px; gap: 10px; background: #f5f3ff;
                }
                .diseno-card {
                    background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 12px 14px;
                    display: flex; flex-direction: column; gap: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); transition: border-color .15s;
                }
                .diseno-card:hover { border-color: #7c3aed; }

                /* ═══════════════════════════════════════════════════════
                   MÓDULO DE ALMACÉN PEDIDOS
                ════════════════════════════════════════════════════════ */
                .almacenpedidos-overlay {
                    display: none; position: fixed; inset: 0; background: #fafaf9; z-index: 9100; flex-direction: column; overflow: hidden;
                }
                .almacenpedidos-header {
                    position: relative; display: flex; align-items: center; justify-content: flex-start; padding: 12px 20px 12px 52px;
                    background: linear-gradient(135deg, #0d9488, #2dd4bf); border-bottom: none; flex-shrink: 0;
                }
                .almacenpedidos-back {
                    position: absolute; top: 10px; left: 12px; width: 30px; height: 30px; border-radius: 999px;
                    border: none; background: rgba(255,255,255,0.25); color: #fff; font-size: 0.95rem; font-weight: 900;
                    cursor: pointer; display: grid; place-items: center; z-index: 2; backdrop-filter: blur(4px);
                }
                .almacenpedidos-back:hover { background: rgba(255,255,255,0.4); }
                .almacenpedidos-body { flex: 1; overflow-y: auto; padding: 14px; display: flex; flex-direction: column; gap: 10px; }
                .almped-card {
                    background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 12px 14px;
                    display: flex; flex-direction: column; gap: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); transition: border-color .15s;
                }
                .almped-card:hover { border-color: #0d9488; }

""" + entrega_css_marker

html = html.replace(entrega_css_marker, new_modules_css, 1)


# ═══════════════════════════════════════════════════════════
# 10. ADD DISEÑO MODULE HTML + JS + ALMACÉN PEDIDOS HTML + JS
# Insert before the entrega module HTML
# ═══════════════════════════════════════════════════════════

entrega_html_marker = '<div id="panelEntregas" class="entrega-overlay">'

new_modules_html = """
<!-- ═══════════════════════════════════════════════════════════════
     MÓDULO DE DISEÑO — Panel HTML
════════════════════════════════════════════════════════════════ -->
<div id="panelDiseno" class="diseno-overlay">
  <div style="display:flex;flex-direction:column;height:100%;">
    <div class="diseno-header">
      <button id="disenoBack" class="diseno-back" type="button" title="Volver" aria-label="Volver">←</button>
      <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:1.6rem;line-height:1;">🎨</span>
        <div>
          <div style="font-size:1rem;font-weight:800;color:#fff;letter-spacing:0.5px;">MÓDULO DE DISEÑO</div>
          <div style="font-size:0.6rem;color:rgba(255,255,255,0.7);">Todas las órdenes llegan aquí primero — diseña y envía a producción</div>
        </div>
      </div>
    </div>
    <div class="diseno-body">
      <div class="diseno-list-panel">
        <div style="display:flex;gap:6px;flex-shrink:0;">
          <button class="prod-tab active" data-dis-status="pendiente" style="background:#7c3aed;border-color:#7c3aed;color:#fff;">⏳ Pendientes</button>
          <button class="prod-tab" data-dis-status="en_diseno" style="">🎨 En Diseño</button>
          <button class="prod-tab" data-dis-status="listo" style="">✅ Listos</button>
          <button class="prod-tab" data-dis-status="enviado" style="">📦 Enviados a Prod.</button>
        </div>
        <div style="display:flex;gap:6px;flex-shrink:0;">
          <input type="text" id="disenoBuscador" placeholder="🔍 Buscar por folio, cliente o producto..." style="flex:1;background:#fff;border:1px solid #e5e7eb;color:#1f2937;border-radius:8px;padding:7px 10px;font-size:0.7rem;">
          <button id="disenoRecargar" style="background:#f5f3ff;border:1px solid #e5e7eb;color:#7c3aed;border-radius:8px;padding:0 12px;cursor:pointer;font-size:0.9rem;">🔄</button>
        </div>
        <div id="disenoOrdenList" style="flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:8px;">
          <div style="text-align:center;color:#9ca3af;font-size:0.72rem;padding:30px;">Cargando órdenes de diseño...</div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
/* Módulo de Diseño */
document.addEventListener('DOMContentLoaded', function() {
    var DIS_COLLECTION = 'design_orders';
    function getDisDB() {
        if (!window.firebase) return null;
        return window.firebase.firestore();
    }
    var allDisOrders = [];
    var currentDisTab = 'pendiente';
    var esc = window._escHtml;
    var panelDiseno = document.getElementById('panelDiseno');
    var disenoBack = document.getElementById('disenoBack');
    var disenoList = document.getElementById('disenoOrdenList');
    var disenoBuscador = document.getElementById('disenoBuscador');

    function openDisenoPanel() {
        panelDiseno.style.display = 'flex';
        cargarDisOrdenes();
    }
    function closeDisenoPanel() {
        panelDiseno.style.display = 'none';
    }
    window.openDisenoPopupGlobal = openDisenoPanel;
    window.closeDisenoPopupGlobal = closeDisenoPanel;

    if (disenoBack) disenoBack.addEventListener('click', function() {
        closeDisenoPanel();
        if (typeof mostrarInicioSistema === 'function') mostrarInicioSistema();
    });

    // Tab clicks  
    panelDiseno.querySelectorAll('[data-dis-status]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            panelDiseno.querySelectorAll('[data-dis-status]').forEach(function(b) {
                b.classList.remove('active');
                b.style.background = ''; b.style.borderColor = ''; b.style.color = '';
            });
            btn.classList.add('active');
            btn.style.background = '#7c3aed'; btn.style.borderColor = '#7c3aed'; btn.style.color = '#fff';
            currentDisTab = btn.dataset.disStatus;
            renderDisOrdenes();
        });
    });

    if (disenoBuscador) disenoBuscador.addEventListener('input', renderDisOrdenes);
    var disenoRecargar = document.getElementById('disenoRecargar');
    if (disenoRecargar) disenoRecargar.addEventListener('click', cargarDisOrdenes);

    function cargarDisOrdenes() {
        disenoList.innerHTML = '<div style="text-align:center;color:#9ca3af;padding:30px;">Cargando...</div>';
        var db = getDisDB(); if (!db) return;
        db.collection(DIS_COLLECTION).orderBy('creadoEn','desc').get().then(function(snap) {
            allDisOrders = snap.docs.map(function(d){ return Object.assign({id:d.id}, d.data()); });
            renderDisOrdenes();
        }).catch(function(err) {
            disenoList.innerHTML = '<div style="text-align:center;color:#dc2626;padding:30px;">Error: '+esc(err.message)+'</div>';
        });
    }

    function renderDisOrdenes() {
        var q = (disenoBuscador.value||'').toLowerCase().trim();
        var lista = allDisOrders.filter(function(o) {
            if (o.estado !== currentDisTab) return false;
            if (!q) return true;
            return (o.folio||'').toLowerCase().includes(q)||(o.cliente||'').toLowerCase().includes(q)||(o.producto||'').toLowerCase().includes(q);
        });
        // Sort: most urgent first (earliest fechaEntrega)
        lista.sort(function(a,b){ return String(a.fechaEntrega||'9999').localeCompare(String(b.fechaEntrega||'9999')); });
        if (!lista.length) { disenoList.innerHTML = '<div style="text-align:center;color:#9ca3af;padding:30px;">Sin órdenes en esta categoría.</div>'; return; }
        disenoList.innerHTML = lista.map(function(o) {
            var opts = [['pendiente','⏳ Pendiente'],['en_diseno','🎨 En Diseño'],['listo','✅ Listo'],['enviado','📦 Enviado']]
                .map(function(p){ return '<option value="'+p[0]+'"'+(p[0]===o.estado?' selected':'')+'>'+p[1]+'</option>'; }).join('');
            return '<div class="diseno-card" data-id="'+esc(o.id)+'">'+
                '<div style="display:flex;justify-content:space-between;align-items:flex-start;">'+
                  '<div><div style="font-size:0.8rem;font-weight:800;color:#7c3aed;">'+esc(o.folio||'Sin folio')+'</div>'+
                  '<div style="font-size:0.55rem;color:#9ca3af;">Entrega: '+esc(o.fechaEntrega||'—')+' · '+esc(o.producto||'—')+'</div></div>'+
                  '<select class="dis-status-sel" data-id="'+esc(o.id)+'" style="background:#fff;border:1px solid #e5e7eb;color:#374151;border-radius:6px;padding:4px 8px;font-size:0.6rem;font-weight:700;">'+opts+'</select>'+
                '</div>'+
                '<div style="display:grid;grid-template-columns:1fr 1fr;gap:3px 12px;font-size:0.63rem;color:#6b7280;">'+
                  '<span><strong style="color:#374151;">Cliente:</strong> '+esc(o.cliente||'—')+'</span>'+
                  '<span><strong style="color:#374151;">Cantidad:</strong> '+esc(o.cantidad||'—')+'</span>'+
                  '<span><strong style="color:#374151;">Diseñador:</strong> '+esc(o.disenador||'Sin asignar')+'</span>'+
                  '<span><strong style="color:#374151;">Color:</strong> '+esc(o.color||'—')+'</span>'+
                  (o.notasDisenador?'<span style="grid-column:1/-1;color:#7c3aed;"><strong>Notas diseñador:</strong> '+esc(o.notasDisenador)+'</span>':'')+
                  (o.disenoUrl?'<span style="grid-column:1/-1"><a href="'+esc(o.disenoUrl)+'" target="_blank" style="color:#7c3aed;font-weight:700;">🎨 Ver diseño actual</a></span>':'')+
                '</div>'+
                '<div style="display:flex;gap:6px;flex-wrap:wrap;">'+
                  '<label style="font-size:0.6rem;font-weight:700;color:#6b7280;display:flex;align-items:center;gap:4px;cursor:pointer;background:#f5f3ff;padding:4px 10px;border-radius:6px;border:1px solid #e5e7eb;">📎 Subir diseño <input type="file" accept="image/*,.pdf,.ai,.psd,.cdr" data-upload-id="'+esc(o.id)+'" style="display:none;"></label>'+
                  (o.estado==='listo'?'<button class="prod-btn-action entrega" data-action="enviar-prod" data-id="'+esc(o.id)+'" style="background:#f0fdf4;border-color:#bbf7d0;color:#166534;">🏭 Enviar a Producción</button>':'')+
                  '<button class="prod-btn-action del" data-action="dis-eliminar" data-id="'+esc(o.id)+'">🗑</button>'+
                '</div></div>';
        }).join('');

        // Status change
        disenoList.querySelectorAll('.dis-status-sel').forEach(function(sel) {
            sel.addEventListener('change', function() {
                var db = getDisDB(); if (!db) return;
                db.collection(DIS_COLLECTION).doc(sel.dataset.id).update({
                    estado: sel.value, actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
                }).then(function() {
                    var o = allDisOrders.find(function(x){ return x.id === sel.dataset.id; });
                    if (o) o.estado = sel.value;
                    renderDisOrdenes();
                });
            });
        });

        // File upload
        disenoList.querySelectorAll('[data-upload-id]').forEach(function(inp) {
            inp.addEventListener('change', async function() {
                var file = inp.files && inp.files[0]; if (!file) return;
                var docId = inp.dataset.uploadId;
                try {
                    var storage = window.firebase.storage();
                    var path = 'design_files/' + Date.now() + '_' + file.name.replace(/[^a-zA-Z0-9._-]/g,'_');
                    var ref = storage.ref(path);
                    await ref.put(file);
                    var url = await ref.getDownloadURL();
                    var db = getDisDB();
                    await db.collection(DIS_COLLECTION).doc(docId).update({ disenoUrl: url, disenoNombre: file.name, actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp() });
                    var o = allDisOrders.find(function(x){ return x.id === docId; });
                    if (o) o.disenoUrl = url;
                    renderDisOrdenes();
                    alert('✅ Diseño subido correctamente.');
                } catch(err) { alert('Error al subir: '+err.message); }
            });
        });

        // Actions
        disenoList.querySelectorAll('[data-action]').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var action = btn.dataset.action, docId = btn.dataset.id;
                var orden = allDisOrders.find(function(x){ return x.id === docId; }); if (!orden) return;
                if (action === 'enviar-prod') enviarDisenoAProduccion(orden);
                if (action === 'dis-eliminar') eliminarDisOrden(docId);
            });
        });
    }

    async function enviarDisenoAProduccion(orden) {
        var db = getDisDB(); if (!db) return;
        try {
            // Create production order
            await db.collection('production_orders').add({
                folio: orden.folio || '',
                cliente: orden.cliente || '',
                clienteId: orden.clienteId || '',
                telefono: orden.telefono || '',
                fechaCreacion: new Date().toISOString().slice(0,10),
                fechaEntrega: orden.fechaEntrega || '',
                producto: orden.producto || '',
                color: orden.color || '',
                cantidad: orden.cantidad || '',
                detalleProducto: orden.detalleProducto || '',
                notas: orden.notasProduccion || '',
                disenoUrl: orden.disenoUrl || '',
                disenoNombre: orden.disenoNombre || '',
                disenoTipo: '',
                estado: 'pendiente',
                origenDiseno: true,
                disenoDocId: orden.id,
                inicioTrabajoEn: null,
                creadoEn: window.firebase.firestore.FieldValue.serverTimestamp(),
                actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
            });
            // Update design order status
            await db.collection(DIS_COLLECTION).doc(orden.id).update({
                estado: 'enviado', actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
            });
            orden.estado = 'enviado';
            renderDisOrdenes();
            alert('✅ Diseño enviado a producción.');
        } catch(err) { alert('Error: '+err.message); }
    }

    async function eliminarDisOrden(docId) {
        if (!confirm('¿Eliminar esta orden de diseño?')) return;
        var db = getDisDB(); if (!db) return;
        try {
            await db.collection(DIS_COLLECTION).doc(docId).delete();
            allDisOrders = allDisOrders.filter(function(o){ return o.id !== docId; });
            renderDisOrdenes();
        } catch(err) { alert('Error: '+err.message); }
    }

    // Auto-send from cotizador → diseño
    window.enviarAutoADiseno = function(venta) {
        var db = getDisDB(); if (!db) return;
        var linea0 = (venta.lineas && venta.lineas[0]) || {};
        var cantTotal = (venta.lineas || []).reduce(function(s,l){ return s + Number(l.cantidad || 1); }, 0);
        db.collection(DIS_COLLECTION).add({
            folio: venta.folio || '',
            cliente: venta.clienteNombre || '',
            telefono: venta.telefono || '',
            clienteId: '',
            producto: typeof window.mapProductoParaProduccion === 'function' ? window.mapProductoParaProduccion(linea0.producto||'') : (linea0.producto||''),
            color: '',
            cantidad: String(cantTotal),
            detalleProducto: linea0.medida || '',
            fechaEntrega: venta.fechaEntrega || '',
            disenador: venta.disenador || '',
            notasProduccion: venta.notasProduccion || '',
            notasDisenador: venta.notasDisenador || '',
            comentarios: venta.comentarios || '',
            disenoUrl: '',
            disenoNombre: '',
            estado: 'pendiente',
            total: venta.total || 0,
            creadoEn: window.firebase.firestore.FieldValue.serverTimestamp(),
            actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
        }).then(function() {
            if (typeof notifyInfo === 'function') notifyInfo('Orden enviada automáticamente a Diseño.', 'Diseño');
        }).catch(function(err) { console.error('Error auto-diseño:', err); });
    };
});
</script>

<!-- ═══════════════════════════════════════════════════════════════
     MÓDULO ALMACÉN DE PEDIDOS — Panel HTML
════════════════════════════════════════════════════════════════ -->
<div id="panelAlmacenPedidos" class="almacenpedidos-overlay">
  <div style="display:flex;flex-direction:column;height:100%;">
    <div class="almacenpedidos-header">
      <button id="almacenPedidosBack" class="almacenpedidos-back" type="button" title="Volver" aria-label="Volver">←</button>
      <div style="display:flex;align-items:center;gap:12px;">
        <span style="font-size:1.6rem;line-height:1;">📦</span>
        <div>
          <div style="font-size:1rem;font-weight:800;color:#fff;letter-spacing:0.5px;">ALMACÉN DE PEDIDOS</div>
          <div style="font-size:0.6rem;color:rgba(255,255,255,0.7);">Pedidos terminados — decide si se envían o se entregan en local</div>
        </div>
      </div>
    </div>
    <div class="almacenpedidos-body">
      <div style="display:flex;gap:6px;flex-shrink:0;">
        <button class="prod-tab active" data-alm-status="almacenado" style="background:#0d9488;border-color:#0d9488;color:#fff;">📦 Almacenados</button>
        <button class="prod-tab" data-alm-status="para_envio">🚚 Para Envío</button>
        <button class="prod-tab" data-alm-status="entregado_local">🏪 Entregado en Local</button>
      </div>
      <div style="display:flex;gap:6px;flex-shrink:0;">
        <input type="text" id="almPedBuscador" placeholder="🔍 Buscar por folio, cliente..." style="flex:1;background:#fff;border:1px solid #e5e7eb;color:#1f2937;border-radius:8px;padding:7px 10px;font-size:0.7rem;">
        <button id="almPedRecargar" style="background:#f0fdfa;border:1px solid #ccfbf1;color:#0d9488;border-radius:8px;padding:0 12px;cursor:pointer;font-size:0.9rem;">🔄</button>
      </div>
      <div id="almPedList" style="flex:1;overflow-y:auto;display:flex;flex-direction:column;gap:8px;"></div>
    </div>
  </div>
</div>

<script>
/* Módulo Almacén de Pedidos */
document.addEventListener('DOMContentLoaded', function() {
    var ALMP_COLLECTION = 'stored_orders';
    function getAlmpDB() { return window.firebase ? window.firebase.firestore() : null; }
    var allAlmPed = [];
    var currentAlmTab = 'almacenado';
    var esc = window._escHtml;
    var panel = document.getElementById('panelAlmacenPedidos');
    var backBtn = document.getElementById('almacenPedidosBack');
    var listEl = document.getElementById('almPedList');
    var buscador = document.getElementById('almPedBuscador');

    function openAlmPedPanel() { panel.style.display = 'flex'; cargarAlmPed(); }
    function closeAlmPedPanel() { panel.style.display = 'none'; }
    window.openAlmacenPedidosPopupGlobal = openAlmPedPanel;
    window.closeAlmacenPedidosPopupGlobal = closeAlmPedPanel;

    if (backBtn) backBtn.addEventListener('click', function() { closeAlmPedPanel(); if (typeof mostrarInicioSistema==='function') mostrarInicioSistema(); });

    panel.querySelectorAll('[data-alm-status]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            panel.querySelectorAll('[data-alm-status]').forEach(function(b){ b.classList.remove('active'); b.style.background=''; b.style.borderColor=''; b.style.color=''; });
            btn.classList.add('active'); btn.style.background='#0d9488'; btn.style.borderColor='#0d9488'; btn.style.color='#fff';
            currentAlmTab = btn.dataset.almStatus; renderAlmPed();
        });
    });
    if (buscador) buscador.addEventListener('input', renderAlmPed);
    var recargar = document.getElementById('almPedRecargar');
    if (recargar) recargar.addEventListener('click', cargarAlmPed);

    function cargarAlmPed() {
        listEl.innerHTML = '<div style="text-align:center;color:#9ca3af;padding:30px;">Cargando...</div>';
        var db = getAlmpDB(); if (!db) return;
        db.collection(ALMP_COLLECTION).orderBy('creadoEn','desc').get().then(function(snap) {
            allAlmPed = snap.docs.map(function(d){ return Object.assign({id:d.id}, d.data()); });
            renderAlmPed();
        }).catch(function(err) { listEl.innerHTML = '<div style="text-align:center;color:#dc2626;padding:30px;">Error: '+esc(err.message)+'</div>'; });
    }

    function renderAlmPed() {
        var q = (buscador.value||'').toLowerCase().trim();
        var lista = allAlmPed.filter(function(o) {
            if (o.estado !== currentAlmTab) return false;
            if (!q) return true;
            return (o.folioProduccion||'').toLowerCase().includes(q)||(o.cliente||'').toLowerCase().includes(q);
        });
        if (!lista.length) { listEl.innerHTML = '<div style="text-align:center;color:#9ca3af;padding:30px;">Sin pedidos en esta categoría.</div>'; return; }
        listEl.innerHTML = lista.map(function(o) {
            return '<div class="almped-card" data-id="'+esc(o.id)+'">'+
                '<div style="display:flex;justify-content:space-between;align-items:center;">'+
                  '<div><div style="font-size:0.8rem;font-weight:800;color:#0d9488;">'+esc(o.folioProduccion||o.id)+'</div>'+
                  '<div style="font-size:0.55rem;color:#9ca3af;">Entrega: '+esc(o.fechaEntrega||'—')+'</div></div>'+
                  '<div style="font-size:0.58rem;font-weight:700;color:#6b7280;background:#f3f4f6;padding:3px 8px;border-radius:6px;">'+esc(o.estado||'')+'</div>'+
                '</div>'+
                '<div style="display:grid;grid-template-columns:1fr 1fr;gap:3px 12px;font-size:0.63rem;color:#6b7280;">'+
                  '<span><strong style="color:#374151;">Cliente:</strong> '+esc(o.cliente||'—')+'</span>'+
                  '<span><strong style="color:#374151;">Producto:</strong> '+esc(o.producto||'—')+'</span>'+
                  '<span><strong style="color:#374151;">Cantidad:</strong> '+esc(o.cantidad||'—')+'</span>'+
                  '<span><strong style="color:#374151;">Color:</strong> '+esc(o.color||'—')+'</span>'+
                  (o.disenoUrl?'<span style="grid-column:1/-1"><a href="'+esc(o.disenoUrl)+'" target="_blank" style="color:#0d9488;font-weight:700;">📷 Ver imagen</a></span>':'')+
                '</div>'+
                '<div style="display:flex;gap:6px;">'+
                  (o.estado==='almacenado'?'<button class="prod-btn-action entrega" data-action="a-envio" data-id="'+esc(o.id)+'" style="background:#f0fdf4;border-color:#bbf7d0;color:#166534;">🚚 Preparar Envío</button>'+
                  '<button class="prod-btn-action" data-action="entrega-local" data-id="'+esc(o.id)+'" style="background:#fff7ed;border-color:#fde8c8;color:#92400e;">🏪 Entrega en Local</button>':'')+
                  (o.estado==='para_envio'?'<button class="prod-btn-action entrega" data-action="a-reparto" data-id="'+esc(o.id)+'" style="background:#eff6ff;border-color:#bfdbfe;color:#1e40af;">🚚 Enviar a Reparto</button>':'')+
                  '<button class="prod-btn-action" data-action="etiqueta-alm" data-id="'+esc(o.id)+'" style="background:#f9fafb;border-color:#e5e7eb;color:#374151;">🏷 Etiqueta</button>'+
                '</div></div>';
        }).join('');

        listEl.querySelectorAll('[data-action]').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var action=btn.dataset.action, docId=btn.dataset.id;
                var orden = allAlmPed.find(function(x){ return x.id===docId; }); if (!orden) return;
                if (action==='a-envio') cambiarEstadoAlmPed(docId, 'para_envio');
                if (action==='entrega-local') cambiarEstadoAlmPed(docId, 'entregado_local');
                if (action==='a-reparto') enviarAlmPedAReparto(orden);
                if (action==='etiqueta-alm') imprimirEtiquetaAlmacen(orden);
            });
        });
    }

    async function cambiarEstadoAlmPed(docId, nuevoEstado) {
        var db = getAlmpDB(); if (!db) return;
        try {
            await db.collection(ALMP_COLLECTION).doc(docId).update({ estado: nuevoEstado, actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp() });
            var o = allAlmPed.find(function(x){ return x.id===docId; }); if (o) o.estado = nuevoEstado;
            renderAlmPed();
        } catch(err) { alert('Error: '+err.message); }
    }

    async function enviarAlmPedAReparto(orden) {
        var db = getAlmpDB(); if (!db) return;
        try {
            await db.collection('delivery_orders').add({
                folioProduccion: orden.folioProduccion || '',
                produccionDocId: orden.produccionDocId || '',
                cliente: orden.cliente || '',
                clienteId: orden.clienteId || '',
                telefono: '',
                producto: orden.producto || '',
                cantidad: orden.cantidad || '',
                detalleProducto: orden.detalleProducto || '',
                fechaEntrega: orden.fechaEntrega || '',
                disenoUrl: orden.disenoUrl || '',
                correo: '',
                tipoDireccion: 'negocio',
                direccion: '',
                lat: null, lng: null,
                estado: 'pendiente',
                notas: '',
                creadoEn: window.firebase.firestore.FieldValue.serverTimestamp(),
                actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
            });
            await db.collection(ALMP_COLLECTION).doc(orden.id).update({ estado: 'enviado_reparto', actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp() });
            var o = allAlmPed.find(function(x){ return x.id===orden.id; }); if (o) o.estado = 'enviado_reparto';
            renderAlmPed();
            alert('✅ Pedido enviado a Reparto.');
        } catch(err) { alert('Error: '+err.message); }
    }

    function imprimirEtiquetaAlmacen(orden) {
        var uid = 'ALP-' + String(Date.now()).slice(-8);
        var w = window.open('','_blank','width=520,height=500');
        w.document.write('<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Etiqueta '+esc(orden.folioProduccion)+'</title>'+
            '<style>body{font-family:Segoe UI,sans-serif;padding:14px;}.label{width:360px;border:2px solid #0d9488;padding:14px;margin:0 auto;border-radius:8px;}'+
            '.title{font-size:14px;font-weight:800;color:#0d9488;margin-bottom:8px;}.row{font-size:12px;line-height:1.5;}.uid{text-align:center;font-weight:700;margin-top:10px;font-size:11px;color:#6b7280;}</style></head><body>'+
            '<div class="label"><div class="title">📦 ALMACÉN DE PEDIDOS</div>'+
            '<div class="row"><strong>Folio:</strong> '+esc(orden.folioProduccion||'—')+'</div>'+
            '<div class="row"><strong>Cliente:</strong> '+esc(orden.cliente||'—')+'</div>'+
            '<div class="row"><strong>Producto:</strong> '+esc(orden.producto||'—')+' x'+esc(orden.cantidad||'')+'</div>'+
            '<div class="row"><strong>Entrega:</strong> '+esc(orden.fechaEntrega||'—')+'</div>'+
            '<div class="row"><strong>Estado:</strong> '+esc(orden.estado||'—')+'</div>'+
            '<div class="uid">'+uid+'</div></div>'+
            '<scr'+'ipt>window.onload=function(){window.print();}<\/scr'+'ipt></body></html>');
        w.document.close();
    }
});
</script>

""" + entrega_html_marker

html = html.replace(entrega_html_marker, new_modules_html, 1)


# ═══════════════════════════════════════════════════════════
# 11. ADD LOCATION TYPES TO CLIENT FORM
# ═══════════════════════════════════════════════════════════

# Find the client form CP field and add location fields after it
old_client_cp_area = """            <label class="clientesform-field">
                CP
                <input id="cliFormCp" type="text" placeholder="Codigo postal" autocomplete="off">
            </label>"""

new_client_cp_area = """            <label class="clientesform-field">
                CP
                <input id="cliFormCp" type="text" placeholder="Codigo postal" autocomplete="off">
            </label>

            <div style="grid-column:1/-1;border-top:1px solid rgba(255,255,255,0.1);padding-top:10px;margin-top:4px;">
                <div style="font-size:0.65rem;font-weight:800;color:#ff9900;margin-bottom:8px;">📍 UBICACIONES GUARDADAS</div>
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
                    <label class="clientesform-field">
                        🏠 Domicilio
                        <input id="cliFormUbiDomicilio" type="text" placeholder="Dirección de casa" autocomplete="off">
                    </label>
                    <label class="clientesform-field">
                        🏢 Negocio
                        <input id="cliFormUbiNegocio" type="text" placeholder="Dirección del negocio" autocomplete="off">
                    </label>
                    <label class="clientesform-field">
                        📌 Punto Medio
                        <input id="cliFormUbiPuntoMedio" type="text" placeholder="Punto de encuentro" autocomplete="off">
                    </label>
                </div>
            </div>"""

html = html.replace(old_client_cp_area, new_client_cp_area, 1)


# ═══════════════════════════════════════════════════════════
# 11b. ADD CLIENT LOCATION DOM REFS AND SAVE/LOAD LOGIC
# ═══════════════════════════════════════════════════════════

# Add DOM refs after cliFormReferenciaBancaria
old_dom_refs = """    const cliFormReferenciaBancaria = document.getElementById('cliFormReferenciaBancaria');
    const cliFormCancel = document.getElementById('cliFormCancel');"""

new_dom_refs = """    const cliFormReferenciaBancaria = document.getElementById('cliFormReferenciaBancaria');
    const cliFormUbiDomicilio = document.getElementById('cliFormUbiDomicilio');
    const cliFormUbiNegocio = document.getElementById('cliFormUbiNegocio');
    const cliFormUbiPuntoMedio = document.getElementById('cliFormUbiPuntoMedio');
    const cliFormCancel = document.getElementById('cliFormCancel');"""

html = html.replace(old_dom_refs, new_dom_refs, 1)

# Add location fields to save payload
old_save_payload_end = """            referenciaBancaria: String(cliFormReferenciaBancaria?.value || '').trim(),
            tipoCliente: String(cliFormTipo?.value || 'Publico en general').trim() || 'Publico en general'
        };"""

new_save_payload_end = """            referenciaBancaria: String(cliFormReferenciaBancaria?.value || '').trim(),
            tipoCliente: String(cliFormTipo?.value || 'Publico en general').trim() || 'Publico en general',
            ubiDomicilio: String(cliFormUbiDomicilio?.value || '').trim(),
            ubiNegocio: String(cliFormUbiNegocio?.value || '').trim(),
            ubiPuntoMedio: String(cliFormUbiPuntoMedio?.value || '').trim()
        };"""

html = html.replace(old_save_payload_end, new_save_payload_end, 1)

# Add location fields to load/edit form
old_load_rfc = """        if (cliFormRfc) cliFormRfc.value = isEdit ? String(cliente?.rfc || '') : '';
        if (cliFormReferenciaBancaria) cliFormReferenciaBancaria.value = isEdit ? String(cliente?.referenciaBancaria || '') : '';"""

new_load_rfc = """        if (cliFormRfc) cliFormRfc.value = isEdit ? String(cliente?.rfc || '') : '';
        if (cliFormReferenciaBancaria) cliFormReferenciaBancaria.value = isEdit ? String(cliente?.referenciaBancaria || '') : '';
        if (cliFormUbiDomicilio) cliFormUbiDomicilio.value = isEdit ? String(cliente?.ubiDomicilio || '') : '';
        if (cliFormUbiNegocio) cliFormUbiNegocio.value = isEdit ? String(cliente?.ubiNegocio || '') : '';
        if (cliFormUbiPuntoMedio) cliFormUbiPuntoMedio.value = isEdit ? String(cliente?.ubiPuntoMedio || '') : '';"""

html = html.replace(old_load_rfc, new_load_rfc, 1)


# ═══════════════════════════════════════════════════════════
# 11c. FIX PRODUCTION JS — guard against removed form elements
# ═══════════════════════════════════════════════════════════

# Guard the prodProducto reference that will fail since form is removed
old_prod_product_listener = """    document.getElementById('prodProducto').addEventListener('change', actualizarSeccionesProducto);"""
new_prod_product_listener = """    var prodProductoEl = document.getElementById('prodProducto');
    if (prodProductoEl) prodProductoEl.addEventListener('change', actualizarSeccionesProducto);"""
html = html.replace(old_prod_product_listener, new_prod_product_listener, 1)


# ═══════════════════════════════════════════════════════════
# 11d. ADD INSUMOS + NOTES HANDLERS to production module
# ═══════════════════════════════════════════════════════════

# Insert after actualizarResumenProduccion function (already added)
old_resumen_fn_end = """        var el3 = document.getElementById('prodResumenTerminadas'); if (el3) el3.textContent = term;
    }"""

new_resumen_fn_end = """        var el3 = document.getElementById('prodResumenTerminadas'); if (el3) el3.textContent = term;
    }

    // Insumos request
    var btnSolicitarInsumo = document.getElementById('btnSolicitarInsumo');
    if (btnSolicitarInsumo) {
        btnSolicitarInsumo.addEventListener('click', async function() {
            var nombre = (document.getElementById('prodInsumoNombre')?.value || '').trim();
            var cantidad = document.getElementById('prodInsumoCantidad')?.value || '1';
            var urgencia = document.getElementById('prodInsumoUrgencia')?.value || 'normal';
            if (!nombre) { alert('Escribe el nombre del insumo.'); return; }
            var db = getProdDB(); if (!db) return;
            try {
                await db.collection('supply_requests').add({
                    nombre: nombre, cantidad: Number(cantidad), urgencia: urgencia,
                    estado: 'solicitado',
                    creadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
                });
                document.getElementById('prodInsumoNombre').value = '';
                document.getElementById('prodInsumoCantidad').value = '';
                cargarInsumosSolicitados();
                alert('✅ Insumo solicitado: ' + nombre);
            } catch(err) { alert('Error: ' + err.message); }
        });
    }

    function cargarInsumosSolicitados() {
        var cont = document.getElementById('prodInsumosSolicitados'); if (!cont) return;
        var db = getProdDB(); if (!db) return;
        db.collection('supply_requests').orderBy('creadoEn','desc').limit(10).get().then(function(snap) {
            if (snap.empty) { cont.innerHTML = '<em>Sin solicitudes</em>'; return; }
            cont.innerHTML = snap.docs.map(function(d) {
                var r = d.data();
                var urgStyle = r.urgencia === 'urgente' ? 'color:#dc2626;font-weight:700;' : '';
                return '<div style="padding:3px 0;border-bottom:1px solid #fde8c8;'+urgStyle+'">'+
                    (r.urgencia==='urgente'?'🔴 ':'')+r.nombre+' x'+r.cantidad+' — '+r.estado+'</div>';
            }).join('');
        });
    }

    // Production notes save
    var btnGuardarNotasProd = document.getElementById('btnGuardarNotasProd');
    if (btnGuardarNotasProd) {
        btnGuardarNotasProd.addEventListener('click', function() {
            var notas = (document.getElementById('prodNotasGenerales')?.value || '').trim();
            localStorage.setItem('produccion_notas_generales', notas);
            alert('✅ Notas guardadas.');
        });
        // Load saved notes
        var savedNotas = localStorage.getItem('produccion_notas_generales');
        if (savedNotas) { var el = document.getElementById('prodNotasGenerales'); if (el) el.value = savedNotas; }
    }

    // Load insumos on panel open
    var origOpen = openProduccionPanel;
    openProduccionPanel = function() { origOpen(); cargarInsumosSolicitados(); };
    window.openProduccionPopupGlobal = openProduccionPanel;"""

html = html.replace(old_resumen_fn_end, new_resumen_fn_end, 1)


# ═══════════════════════════════════════════════════════════
# 12. ENHANCE DELIVERY LABELS — add label popup button
# ═══════════════════════════════════════════════════════════

old_delivery_actions = """                '<div class="entrega-card-actions">' +
                  '<button class="entrega-btn nav" data-action="navegar" data-id="'+escEnt(e.id)+'" data-url="'+escEnt(mapsUrl)+'">🗺 Navegar</button>' +
                  '<button class="entrega-btn" data-action="editar" data-id="'+escEnt(e.id)+'">✏️ Editar</button>' +
                  '<button class="entrega-btn del" data-action="eliminar" data-id="'+escEnt(e.id)+'">🗑</button>' +
                '</div></div>';"""

new_delivery_actions = """                '<div class="entrega-card-actions">' +
                  '<button class="entrega-btn nav" data-action="navegar" data-id="'+escEnt(e.id)+'" data-url="'+escEnt(mapsUrl)+'">🗺 Navegar</button>' +
                  '<button class="entrega-btn" data-action="etiqueta-ent" data-id="'+escEnt(e.id)+'" style="background:rgba(255,153,0,0.12);border-color:rgba(255,153,0,0.3);color:#ffb300;">🏷 Etiqueta</button>' +
                  '<button class="entrega-btn" data-action="editar" data-id="'+escEnt(e.id)+'">✏️ Editar</button>' +
                  '<button class="entrega-btn del" data-action="eliminar" data-id="'+escEnt(e.id)+'">🗑</button>' +
                '</div></div>';"""

html = html.replace(old_delivery_actions, new_delivery_actions, 1)

# Add handler for etiqueta-ent action
old_delivery_action_handlers = """                if (action === 'navegar') window.open(btn.dataset.url, '_blank');
                if (action === 'editar') cargarEntregaEnForm(entrega);
                if (action === 'eliminar') eliminarEntrega(docId);"""

new_delivery_action_handlers = """                if (action === 'navegar') window.open(btn.dataset.url, '_blank');
                if (action === 'editar') cargarEntregaEnForm(entrega);
                if (action === 'eliminar') eliminarEntrega(docId);
                if (action === 'etiqueta-ent') mostrarEtiquetaEntrega(entrega);"""

html = html.replace(old_delivery_action_handlers, new_delivery_action_handlers, 1)

# Add the label popup function after renderEntregas
old_render_end_section = """        listEl.querySelectorAll('[data-action]').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var action = btn.dataset.action, docId = btn.dataset.id;
                var entrega = allEntregas.find(function(x){ return x.id === docId; }); if (!entrega) return;
                if (action === 'navegar') window.open(btn.dataset.url, '_blank');
                if (action === 'editar') cargarEntregaEnForm(entrega);
                if (action === 'eliminar') eliminarEntrega(docId);
                if (action === 'etiqueta-ent') mostrarEtiquetaEntrega(entrega);
            });
        });
    }"""

new_render_end_section = """        listEl.querySelectorAll('[data-action]').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var action = btn.dataset.action, docId = btn.dataset.id;
                var entrega = allEntregas.find(function(x){ return x.id === docId; }); if (!entrega) return;
                if (action === 'navegar') window.open(btn.dataset.url, '_blank');
                if (action === 'editar') cargarEntregaEnForm(entrega);
                if (action === 'eliminar') eliminarEntrega(docId);
                if (action === 'etiqueta-ent') mostrarEtiquetaEntrega(entrega);
            });
        });
    }

    function mostrarEtiquetaEntrega(e) {
        var mapsUrl = (e.lat && e.lng)
            ? 'https://www.google.com/maps/dir/?api=1&destination='+e.lat+','+e.lng
            : 'https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(e.direccion||e.cliente||'');
        var mapImg = (e.lat && e.lng)
            ? '<div id="entEtiquetaMap" style="width:100%;height:180px;border-radius:8px;margin:8px 0;border:1px solid #e5e7eb;"></div>'
            : '<div style="text-align:center;padding:20px;color:#9ca3af;font-size:0.7rem;">📭 Sin coordenadas para mostrar mapa</div>';
        var imgSection = e.disenoUrl
            ? '<div style="margin-top:8px;"><div style="font-size:0.6rem;font-weight:700;color:#92400e;margin-bottom:4px;">📷 Foto del producto</div><img src="'+escEnt(e.disenoUrl)+'" style="max-width:100%;max-height:160px;border-radius:8px;border:1px solid #e5e7eb;"></div>'
            : '';
        // Build popup
        var popup = document.createElement('div');
        popup.style.cssText = 'position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.5);backdrop-filter:blur(4px);';
        popup.innerHTML = '<div style="background:#fff;border-radius:14px;max-width:420px;width:90%;max-height:90vh;overflow-y:auto;padding:20px;box-shadow:0 20px 40px rgba(0,0,0,0.2);">'+
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">'+
              '<div style="font-size:1rem;font-weight:800;color:#ff9900;">🏷 Etiqueta de Entrega</div>'+
              '<button id="btnCerrarEtiquetaEnt" style="background:none;border:none;font-size:1.2rem;cursor:pointer;color:#9ca3af;">✕</button>'+
            '</div>'+
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:0.72rem;color:#374151;">'+
              '<div><strong style="color:#92400e;">Folio:</strong><br>'+escEnt(e.folioProduccion||e.id)+'</div>'+
              '<div><strong style="color:#92400e;">Estado:</strong><br>'+escEnt(e.estado||'—')+'</div>'+
              '<div><strong style="color:#92400e;">Cliente:</strong><br>'+escEnt(e.cliente||'—')+'</div>'+
              '<div><strong style="color:#92400e;">Teléfono:</strong><br><a href="tel:'+escEnt(e.telefono||'')+'" style="color:#ff9900;">'+escEnt(e.telefono||'—')+'</a></div>'+
              '<div style="grid-column:1/-1"><strong style="color:#92400e;">Dirección:</strong><br>'+escEnt(e.direccion||'—')+'</div>'+
              '<div><strong style="color:#92400e;">Producto:</strong><br>'+escEnt(e.producto||'—')+'</div>'+
              '<div><strong style="color:#92400e;">Cantidad:</strong><br>'+escEnt(e.cantidad||'—')+'</div>'+
              '<div><strong style="color:#92400e;">Entrega:</strong><br>'+escEnt(e.fechaEntrega||'—')+'</div>'+
              '<div><strong style="color:#92400e;">Adeudo:</strong><br><span style="color:#dc2626;font-weight:700;">Consultar en caja</span></div>'+
            '</div>'+
            mapImg+
            imgSection+
            '<div style="display:flex;gap:8px;margin-top:12px;">'+
              '<a href="'+escEnt(mapsUrl)+'" target="_blank" style="flex:1;text-align:center;background:#ff9900;color:#fff;text-decoration:none;padding:10px;border-radius:8px;font-weight:700;font-size:0.72rem;">🗺 Abrir en Mapa</a>'+
              '<button id="btnImprimirEtiquetaEnt" style="flex:1;background:#f3f4f6;border:1px solid #e5e7eb;border-radius:8px;font-weight:700;font-size:0.72rem;cursor:pointer;">🖨 Imprimir</button>'+
            '</div>'+
        '</div>';
        document.body.appendChild(popup);
        popup.querySelector('#btnCerrarEtiquetaEnt').addEventListener('click', function(){ popup.remove(); });
        popup.addEventListener('click', function(ev){ if (ev.target === popup) popup.remove(); });

        // Initialize mini map with Leaflet
        if (e.lat && e.lng && window.L) {
            setTimeout(function() {
                var mapCont = document.getElementById('entEtiquetaMap');
                if (mapCont) {
                    var miniMap = L.map(mapCont).setView([e.lat, e.lng], 15);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:18}).addTo(miniMap);
                    L.marker([e.lat, e.lng]).addTo(miniMap);
                    setTimeout(function(){ miniMap.invalidateSize(); }, 200);
                }
            }, 100);
        }

        // Print button
        popup.querySelector('#btnImprimirEtiquetaEnt').addEventListener('click', function() {
            var w = window.open('','_blank','width=520,height=600');
            w.document.write('<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Entrega '+escEnt(e.folioProduccion||'')+'</title>'+
                '<style>body{font-family:Segoe UI,sans-serif;padding:14px;} .lbl{width:380px;border:2px solid #ff9900;padding:16px;margin:0 auto;border-radius:10px;}'+
                '.title{font-size:15px;font-weight:800;color:#ff9900;margin-bottom:10px;} .r{font-size:12px;line-height:1.6;}</style></head><body>'+
                '<div class="lbl"><div class="title">🚚 ETIQUETA DE ENTREGA</div>'+
                '<div class="r"><strong>Folio:</strong> '+escEnt(e.folioProduccion||'—')+'</div>'+
                '<div class="r"><strong>Cliente:</strong> '+escEnt(e.cliente||'—')+'</div>'+
                '<div class="r"><strong>Teléfono:</strong> '+escEnt(e.telefono||'—')+'</div>'+
                '<div class="r"><strong>Dirección:</strong> '+escEnt(e.direccion||'—')+'</div>'+
                '<div class="r"><strong>Producto:</strong> '+escEnt(e.producto||'—')+' x'+escEnt(e.cantidad||'')+'</div>'+
                '<div class="r"><strong>Entrega:</strong> '+escEnt(e.fechaEntrega||'—')+'</div>'+
                '</div><scr'+'ipt>window.onload=function(){window.print();}<\\/scr'+'ipt></body></html>');
            w.document.close();
        });
    }"""

html = html.replace(old_render_end_section, new_render_end_section, 1)


# ═══════════════════════════════════════════════════════════
# WRITE OUTPUT
# ═══════════════════════════════════════════════════════════

with open('mockup.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Patch 15 applied successfully!")
print("Changes:")
print("  - Production restyled: white/orange theme")
print("  - Production form stripped → summary panel + insumos request")
print("  - Production cards: no phone/prices, urgency colors, return-to-pending")
print("  - Cotizador: added per-area comments (producción, diseñador)")
print("  - New DISEÑO module (purple theme)")
print("  - New ALMACÉN PEDIDOS module (teal theme)")
print("  - Auto-flow: venta → diseño → producción → almacén → reparto")
print("  - Client form: added location types (domicilio, negocio, punto medio)")
print("  - Menu updated with new modules")
