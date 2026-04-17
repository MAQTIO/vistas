#!/usr/bin/env python3
"""
Patch: Unify CSS (orange/white, no gradients, no heavy transitions),
fix performance, fix client addresses (multiple midpoints), integrate in delivery.
"""
import re

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# ============================================================
# 1. FLATTEN CSS GRADIENTS → Solid colors
# ============================================================

# Map gradient patterns to flat solid colors
gradient_replacements = [
    # Sidebar background: remove radial+linear gradient
    (r'background:\s*radial-gradient\(circle at 18% 20%, rgba\(255,153,0,0\.08\), transparent 42%\),\s*linear-gradient\(135deg, var\(--panel\) 0%, #0b1220 100%\);',
     'background: var(--panel);'),

    # h3::before accent bar
    (r'background:\s*linear-gradient\(180deg, var\(--accent\), var\(--accent-light\)\);',
     'background: var(--accent);'),

    # .btn-mode default
    (r'background:\s*linear-gradient\(180deg, rgba\(255,255,255,0\.06\), rgba\(0,0,0,0\.35\)\);',
     'background: rgba(255,255,255,0.04);'),

    # .btn-mode.active, .btn-tipo.active, .btn-tab.active — accent gradients
    (r'background:\s*linear-gradient\(135deg, var\(--accent\) 0%, var\(--accent-light\) 100%\);',
     'background: var(--accent);'),

    # .btn-exp default
    (r'background:\s*linear-gradient\(180deg, rgba\(255,255,255,0\.05\), rgba\(0,0,0,0\.35\)\);',
     'background: rgba(255,255,255,0.04);'),

    # .popup-chip default
    (r'background:\s*linear-gradient\(180deg, rgba\(255,255,255,0\.06\) 0%, rgba\(255,255,255,0\.02\) 100%\);',
     'background: rgba(255,255,255,0.04);'),

    # .popup-chip.active — BLUE gradient → orange
    (r'\.popup-chip\.active \{ border-color: #64b5f6; background: linear-gradient\(135deg, #1e88e5 0%, #64b5f6 100%\); color: #0a1220; box-shadow: 0 6px 16px rgba\(22,119,255,0\.28\); \}',
     '.popup-chip.active { border-color: var(--accent); background: var(--accent); color: #000; box-shadow: none; }'),

    # .popup-chip:hover — BLUE → orange
    (r'\.popup-chip:hover \{ border-color: #64b5f6; color: #bfe0ff; box-shadow: 0 4px 12px rgba\(0,0,0,0\.18\); \}',
     '.popup-chip:hover { border-color: var(--accent); color: var(--accent-light); box-shadow: none; }'),

    # .popup-card backgrounds
    (r'background:\s*linear-gradient\(135deg, #0e1726 0%, #111b2c 100%\);',
     'background: #0e1726;'),

    # Config buttons gradient
    (r'background:\s*linear-gradient\(135deg, #ff9900, #e68a00\);',
     'background: #ff9900;'),

    # .popup-actions background
    (r'background:\s*linear-gradient\(180deg, rgba\(14,23,38,0\.4\) 0%, rgba\(14,23,38,0\.9\) 100%\);',
     'background: rgba(14,23,38,0.85);'),

    # WhatsApp button
    (r'background:\s*linear-gradient\(135deg, #1eb35a 0%, #2ddf75 100%\);',
     'background: #25d366;'),

    # Chat button
    (r'background:\s*linear-gradient\(135deg, #ff9800 0%, #ffca28 100%\);',
     'background: #ff9800;'),

    # orden-popup background
    (r'background:\s*linear-gradient\(180deg, #f7f8fa 0%, #f2f4f7 100%\);',
     'background: #f2f4f7;'),

    # Progress bar gradient
    (r'background:\s*linear-gradient\(90deg, #f97316 0%, #f59e0b 100%\);',
     'background: #ff9900;'),

    # Blue/white card
    (r'background:\s*linear-gradient\(160deg, #ffffff 0%, #eef4ff 100%\);',
     'background: #ffffff;'),

    # Orange button variant
    (r'background:\s*linear-gradient\(160deg, #f07a00 0%, #d76700 100%\);',
     'background: #ff9900;'),

    # Dark overlay panels
    (r'background:\s*linear-gradient\(135deg, rgba\(20,30,45,0\.92\) 0%, rgba\(10,14,24,0\.95\) 100%\);',
     'background: rgba(14,20,32,0.94);'),

    # Various green buttons → orange
    (r'background:\s*linear-gradient\(135deg, #25d366 0%, #1aaa55 100%\);',
     'background: #25d366;'),

    # Orange tones
    (r'background:\s*linear-gradient\(135deg, #ffb300 0%, #ff8f00 100%\);',
     'background: #ff9900;'),
    (r'background:\s*linear-gradient\(135deg, #ff9800 0%, #fb8c00 100%\);',
     'background: #ff9900;'),
    (r'background:\s*linear-gradient\(135deg, #ff9800 0%, #ffb300 100%\);',
     'background: #ff9900;'),
    (r'background:\s*linear-gradient\(135deg, #ffa500 0%, #ff8c00 100%\);',
     'background: #ff9900;'),
    (r'background:\s*linear-gradient\(135deg, #ff9900, #ffb84d\)',
     'background: #ff9900'),
    (r'background:\s*linear-gradient\(135deg, #ff9900, #ffb347\)',
     'background: #ff9900'),

    # Dark themed panels
    (r'background:\s*linear-gradient\(150deg, #1a1208 0%, #130f0c 100%\);',
     'background: #141010;'),
    (r'background:\s*linear-gradient\(150deg, #06121d 0%, #081a2c 100%\);',
     'background: #071520;'),

    # Blue themed buttons → orange
    (r'background:\s*linear-gradient\(135deg, #0ea5e9 0%, #0284c7 100%\);',
     'background: #ff9900;'),

    # Green buttons → orange
    (r'background:\s*linear-gradient\(135deg, #4CAF50 0%, #6fd36f 100%\);',
     'background: #ff9900;'),
    (r'background:\s*linear-gradient\(135deg, #2e7d32 0%, #43a047 100%\);',
     'background: #ff9900;'),
    (r'background:\s*linear-gradient\(135deg, #2e7d32, #43a047\)',
     'background: #ff9900'),

    # Cyan/light blue → orange
    (r'background:\s*linear-gradient\(135deg, #4fc3f7 0%, #7de3ff 100%\);',
     'background: #ff9900;'),

    # Purple → orange
    (r'background:\s*linear-gradient\(135deg, #7c4dff 0%, #b388ff 100%\);',
     'background: #ff9900;'),
    (r'background:\s*linear-gradient\(135deg, #8e24aa 0%, #ab47bc 100%\);',
     'background: #ff9900;'),
    (r'background:\s*linear-gradient\(135deg, #8e24aa, #ab47bc\)',
     'background: #ff9900'),
    (r'background:\s*linear-gradient\(135deg, #ab2dff 0%, #8a2be2 100%\);',
     'background: #ff9900;'),
    (r'background:\s*linear-gradient\(135deg, #7c3aed 0%, #6d28d9 100%\);',
     'background: #ff9900;'),

    # Deep blue → orange
    (r'background:\s*linear-gradient\(135deg, #0277bd 0%, #29b6f6 100%\);',
     'background: #ff9900;'),
    (r"background:\s*linear-gradient\(135deg,#1d4ed8 0%,#2563eb 100%\)",
     "background: #ff9900"),

    # Dark purples → dark orange panels
    (r'background:\s*linear-gradient\(145deg, #1b0f24 0%, #130b1b 100%\);',
     'background: #1a1008;'),
    (r'background:\s*linear-gradient\(135deg, #0d1b2a 0%, #1a2332 100%\);',
     'background: #0d1520;'),
    (r'background:\s*linear-gradient\(135deg, #2d0d47 0%, #1a0a2e 100%\);',
     'background: #1a0d08;'),

    # Teal almacén → orange
    (r'background:\s*linear-gradient\(135deg, #0d9488, #2dd4bf\)',
     'background: #ff9900'),

    # Modal box
    (r'background:\s*linear-gradient\(135deg, #0f1626 0%, #121c2f 100%\);',
     'background: #0f1626;'),

    # Landing background card gradient
    (r'background:\s*linear-gradient\(135deg, #0a0f1a 0%, #141b2a 50%, #1a2332 100%\);',
     'background: #0a0f1a;'),

    # Gold/yellow gradient 
    (r'background:\s*linear-gradient\(135deg, #ffd166 0%, #ffb347 100%\);',
     'background: #ff9900;'),
    (r'background:\s*linear-gradient\(135deg, #ffd166 0%, #ff9900 100%\)',
     'background: #ff9900'),

    # Accent gradient
    (r"background:\s*linear-gradient\(135deg, var\(--accent\), #e68a00\);",
     "background: var(--accent);"),

    # Config users primary
    (r"background:\s*linear-gradient\(135deg, #ff9900, #e68a00\);\s*color:\s*#fff;",
     "background: #ff9900; color: #fff;"),

    # Green accept
    (r'background:\s*linear-gradient\(135deg, #4caf50 0%, #6ad66a 100%\);',
     'background: #ff9900;'),

    # Rainbow surtido — unique, keep functional but simplify
    (r'background:linear-gradient\(90deg, #f00, #ff0, #0f0, #0ff, #00f, #f0f\)',
     'background: #ff9900'),

    # Upload dual label
    (r'background:\s*linear-gradient\(135deg, #ffd166 0%, #4fc3f7 100%\)',
     'background: #ff9900'),

    # Warm background panels
    (r"background:linear-gradient\(180deg,#fff9f0 0%,#fff7ed 100%\)",
     "background:#fff7ed"),
]

for pattern, replacement in gradient_replacements:
    content = re.sub(pattern, replacement, content)

# Catch remaining inline JS gradients with single quotes
content = re.sub(
    r"'linear-gradient\(135deg, #ffd166 0%, #ffb347 100%\)'",
    "'#ff9900'",
    content
)

# ============================================================
# 2. REMOVE BACKDROP-FILTER (performance killer)
# ============================================================
content = re.sub(r'\s*backdrop-filter:\s*blur\(\d+px\);', '', content)

# ============================================================
# 3. SIMPLIFY TRANSITIONS — remove 'all' transitions, keep specific ones
# ============================================================
# Replace "transition: all X ease" with "transition: none"
content = re.sub(
    r'transition:\s*all\s+[\d.]+s\s*(?:ease(?:-in|-out|-in-out)?)?\s*;',
    'transition: none;',
    content
)
# Remove transform hover effects that cause repaints
content = re.sub(
    r'\s*transform:\s*translateY\(-[123]px\);',
    '',
    content
)

# ============================================================
# 4. SIMPLIFY BOX-SHADOWS — remove very heavy ones (>16px blur)
# ============================================================
def simplify_shadow(m):
    full = m.group(0)
    # Extract blur radius
    nums = re.findall(r'(\d+)px', full)
    if len(nums) >= 3:
        blur = int(nums[2]) if len(nums) > 2 else int(nums[1])
        if blur > 20:
            # Reduce to lighter shadow
            return re.sub(r'(\d{2,})px', lambda n: str(min(int(n.group(1)), 12)) + 'px', full)
    return full

content = re.sub(r'box-shadow:\s*[^;]+;', simplify_shadow, content)

# ============================================================
# 5. REMOVE FADEANIMATION
# ============================================================
content = re.sub(
    r'\s*animation:\s*fadeIn\s+[\d.]+s\s+ease;',
    '',
    content
)

# ============================================================
# 6. FIX GREEN DELIVERY MODULE → ORANGE THEME
# ============================================================
# Delivery overlay background
content = content.replace(
    'background: #071410; z-index: 9200;',
    'background: #0a0f1a; z-index: 9200;'
)
content = content.replace(
    'background: #0a1c12;',
    'background: var(--panel);'
)
content = content.replace(
    'border-bottom: 2px solid #2e7d32;',
    'border-bottom: 2px solid var(--accent);'
)
content = content.replace(
    'border: 1px solid #2f5b3f;',
    'border: 1px solid var(--border);'
)
content = content.replace(
    'background: #102116;',
    'background: var(--panel);'
)
content = content.replace(
    'background: #163120;',
    'background: var(--hover);'
)
content = content.replace(
    'border-color: #418355;',
    'border-color: var(--accent);'
)
content = content.replace(
    'width: 370px; flex-shrink: 0; background: #0b1a10;',
    'width: 370px; flex-shrink: 0; background: var(--panel);'
)
content = content.replace(
    'border-right: 1px solid #1a3020;',
    'border-right: 1px solid var(--border);'
)
content = content.replace(
    'color: #81c784;',
    'color: var(--accent-light);'
)
# Multiple delivery element replacements
content = content.replace(
    'border-bottom: 1px solid #1a3020;',
    'border-bottom: 1px solid var(--border);'
)
content = content.replace(
    'color: #6a9e74;',
    'color: #9ca3af;'
)
content = content.replace(
    'background: #0d1a13; border: 1px solid #1a3a22;',
    'background: rgba(255,255,255,0.04); border: 1px solid var(--border);'
)
content = content.replace(
    'border-color: #4caf50;',
    'border-color: var(--accent);'
)  
content = content.replace(
    'background: #0b1a12; border: 1px solid #1a3020;',
    'background: var(--panel); border: 1px solid var(--border);'
)
content = content.replace(
    '.entrega-card:hover { border-color: #4caf50; }',
    '.entrega-card:hover { border-color: var(--accent); }'
)
content = content.replace(
    '.entrega-card-folio { font-size: 0.8rem; font-weight: 800; color: #66bb6a; }',
    '.entrega-card-folio { font-size: 0.8rem; font-weight: 800; color: var(--accent); }'
)
content = content.replace(
    'color: #4a6a54;',
    'color: #6b7280;'
)
content = content.replace(
    'color: #a0c8a8;',
    'color: #9ca3af;'
)
content = content.replace(
    'color: #c8e6c9;',
    'color: #e5e7eb;'
)
content = content.replace(
    'background: rgba(76,175,80,0.15); border: 1px solid #388e3c;',
    'background: rgba(255,153,0,0.15); border: 1px solid var(--accent);'
)
content = content.replace(
    'background: rgba(76,175,80,0.28);',
    'background: rgba(255,153,0,0.28);'
)
content = content.replace(
    'background: rgba(76,175,80,0.08); border: 1px solid #2e7d32;',
    'background: rgba(255,153,0,0.08); border: 1px solid var(--accent);'
)
content = content.replace(
    'color: #a5d6a7;',
    'color: var(--accent-light);'
)
content = content.replace(
    'background: #0d1a13;',
    'background: var(--bg);'
)
content = content.replace(
    'border: 1px solid #1a3a22;',
    'border: 1px solid var(--border);'
)
content = content.replace(
    'background: #071410; border: 1px dashed #2e7d32;',
    'background: var(--bg); border: 1px dashed var(--accent);'
)
content = content.replace(
    'border: 1px solid #1a3020;',
    'border: 1px solid var(--border);'
)
content = content.replace(
    'background: rgba(255,255,255,0.05); border: 1px solid var(--border);',
    'background: rgba(255,255,255,0.05); border: 1px solid var(--border);'
)
content = content.replace(
    '.entrega-tab.active { background: #2e7d32; border-color: #2e7d32; color: #fff; }',
    '.entrega-tab.active { background: var(--accent); border-color: var(--accent); color: #000; }'
)

# Corner button entregas
content = content.replace(
    'box-shadow: 0 4px 10px rgba(46,125,50,0.3);',
    'box-shadow: 0 4px 10px rgba(255,153,0,0.3);'
)

# ============================================================
# 7. FIX ALMACEN MODULE — TEAL → ORANGE
# ============================================================
content = content.replace(
    '.almped-card:hover { border-color: #0d9488; }',
    '.almped-card:hover { border-color: #ff9900; }'
)

# ============================================================
# 8. FIX BLUE/PURPLE highlighted colors → ORANGE
# ============================================================
# popup-result-item active state
content = content.replace(
    '.popup-result-item.active { color: #8fc5ff; background: rgba(100,181,246,0.08); }',
    '.popup-result-item.active { color: var(--accent); background: rgba(255,153,0,0.08); }'
)
# popup-color selected
content = content.replace(
    '.popup-color.selected { border-color: #64b5f6; box-shadow: 0 0 0 2px rgba(100,181,246,0.45) inset; }',
    '.popup-color.selected { border-color: var(--accent); box-shadow: 0 0 0 2px rgba(255,153,0,0.45) inset; }'
)
# popup-icon-btn hover
content = content.replace(
    'color: #64b5f6;',
    'color: var(--accent);'
)

# ============================================================
# 9. FIX CLIENT ADDRESSES — Add support for multiple addresses (puntos medios)
# ============================================================
# In loadClientesModulo, add the missing ubi* fields
content = content.replace(
    """                    deshabilitado: !!c.deshabilitado
                }));
                return;""",
    """                    deshabilitado: !!c.deshabilitado,
                    ubiDomicilio: String(c.ubiDomicilio || '').trim(),
                    ubiNegocio: String(c.ubiNegocio || '').trim(),
                    ubiPuntoMedio: String(c.ubiPuntoMedio || '').trim(),
                    puntosMedios: Array.isArray(c.puntosMedios) ? c.puntosMedios : (c.ubiPuntoMedio ? [c.ubiPuntoMedio] : [])
                }));
                return;"""
)

# In saveClienteFromForm, add puntosMedios
content = content.replace(
    """            ubiDomicilio: String(cliFormUbiDomicilio?.value || '').trim(),
            ubiNegocio: String(cliFormUbiNegocio?.value || '').trim(),
            ubiPuntoMedio: String(cliFormUbiPuntoMedio?.value || '').trim()""",
    """            ubiDomicilio: String(cliFormUbiDomicilio?.value || '').trim(),
            ubiNegocio: String(cliFormUbiNegocio?.value || '').trim(),
            ubiPuntoMedio: String(cliFormUbiPuntoMedio?.value || '').trim(),
            puntosMedios: (function(){
                var arr = [];
                document.querySelectorAll('.cli-punto-medio-input').forEach(function(inp){
                    var v = inp.value.trim(); if(v) arr.push(v);
                });
                var mainPM = String(cliFormUbiPuntoMedio?.value || '').trim();
                if(mainPM && arr.indexOf(mainPM)===-1) arr.unshift(mainPM);
                return arr;
            })()"""
)

# Replace the single punto medio input section with the multi-address system
old_ubicaciones_html = """            <div style="grid-column:1/-1;border-top:1px solid rgba(255,255,255,0.1);padding-top:10px;margin-top:4px;">
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

new_ubicaciones_html = """            <div style="grid-column:1/-1;border-top:1px solid rgba(255,255,255,0.1);padding-top:10px;margin-top:4px;">
                <div style="font-size:0.65rem;font-weight:800;color:#ff9900;margin-bottom:8px;">📍 UBICACIONES GUARDADAS</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                    <label class="clientesform-field">
                        🏠 Domicilio (casa)
                        <input id="cliFormUbiDomicilio" type="text" placeholder="Dirección de casa o link de Maps" autocomplete="off">
                    </label>
                    <label class="clientesform-field">
                        🏢 Negocio (trabajo)
                        <input id="cliFormUbiNegocio" type="text" placeholder="Dirección del negocio o link de Maps" autocomplete="off">
                    </label>
                </div>
                <div style="margin-top:8px;">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
                        <span style="font-size:0.6rem;font-weight:800;color:#ff9900;">📌 PUNTOS MEDIOS</span>
                        <button type="button" id="btnAddPuntoMedio" style="background:#ff9900;color:#fff;border:none;border-radius:6px;padding:3px 10px;font-size:0.6rem;font-weight:700;cursor:pointer;">＋ Agregar punto medio</button>
                    </div>
                    <div id="puntosMediosContainer" style="display:flex;flex-direction:column;gap:6px;">
                        <label class="clientesform-field">
                            📌 Punto Medio principal
                            <input id="cliFormUbiPuntoMedio" type="text" placeholder="Dirección, coordenadas o link de Google Maps" autocomplete="off">
                        </label>
                    </div>
                    <div id="puntosMediosBuscador" style="margin-top:6px;position:relative;">
                        <input id="buscarPuntoMedioInput" type="text" placeholder="🔍 Buscar entre puntos medios registrados..." style="width:100%;padding:5px 8px;border:1px solid rgba(255,255,255,0.12);border-radius:6px;background:rgba(255,255,255,0.04);color:#e5eaf1;font-size:0.65rem;" autocomplete="off">
                        <div id="buscarPuntoMedioResults" style="display:none;position:absolute;top:100%;left:0;right:0;background:#0f1726;border:1px solid rgba(255,255,255,0.12);border-radius:6px;max-height:150px;overflow-y:auto;z-index:10;"></div>
                    </div>
                </div>
            </div>"""

content = content.replace(old_ubicaciones_html, new_ubicaciones_html)

# ============================================================
# 10. ADD JS FOR MULTI-ADDRESS SYSTEM + DELIVERY INTEGRATION
# ============================================================

# Find the end of saveClienteFromForm to inject new functions after
inject_after = "    window.openClientesPopupGlobal = openClientesModuloPopup;"

new_address_js = """    window.openClientesPopupGlobal = openClientesModuloPopup;

    /* ═══ MULTI-ADDRESS: PUNTOS MEDIOS SYSTEM ═══ */
    const PUNTOS_MEDIOS_GLOBAL_KEY = 'mock_puntos_medios_global_v1';

    function getAllPuntosMedios() {
        try {
            return JSON.parse(localStorage.getItem(PUNTOS_MEDIOS_GLOBAL_KEY) || '[]');
        } catch(e) { return []; }
    }
    function savePuntoMedioGlobal(direccion) {
        if (!direccion) return;
        var arr = getAllPuntosMedios();
        var norm = direccion.trim().toUpperCase();
        if (!arr.some(function(p){ return p.trim().toUpperCase() === norm; })) {
            arr.push(direccion.trim());
            localStorage.setItem(PUNTOS_MEDIOS_GLOBAL_KEY, JSON.stringify(arr));
        }
    }
    function syncAllPuntosMediosFromClientes() {
        var arr = getAllPuntosMedios();
        clientesModuloData.forEach(function(c) {
            (c.puntosMedios || []).forEach(function(pm) {
                var norm = pm.trim().toUpperCase();
                if (pm.trim() && !arr.some(function(p){ return p.trim().toUpperCase() === norm; })) {
                    arr.push(pm.trim());
                }
            });
            if (c.ubiPuntoMedio) {
                var norm2 = c.ubiPuntoMedio.trim().toUpperCase();
                if (!arr.some(function(p){ return p.trim().toUpperCase() === norm2; })) {
                    arr.push(c.ubiPuntoMedio.trim());
                }
            }
        });
        localStorage.setItem(PUNTOS_MEDIOS_GLOBAL_KEY, JSON.stringify(arr));
    }

    // Parse Google Maps link to extract coordinates
    function parseMapsLink(input) {
        if (!input) return null;
        var str = input.trim();
        // Try coords: "17.0669,-96.7232"
        var coordMatch = str.match(/^(-?\\d+\\.\\d+)\\s*,\\s*(-?\\d+\\.\\d+)$/);
        if (coordMatch) return { lat: parseFloat(coordMatch[1]), lng: parseFloat(coordMatch[2]), text: str };
        // Try Google Maps link with @lat,lng
        var mapsMatch = str.match(/@(-?\\d+\\.\\d+),(-?\\d+\\.\\d+)/);
        if (mapsMatch) return { lat: parseFloat(mapsMatch[1]), lng: parseFloat(mapsMatch[2]), text: str };
        // Try Google Maps link with ?q=lat,lng
        var qMatch = str.match(/[?&]q=(-?\\d+\\.\\d+),(-?\\d+\\.\\d+)/);
        if (qMatch) return { lat: parseFloat(qMatch[1]), lng: parseFloat(qMatch[2]), text: str };
        // Try place/lat,lng
        var placeMatch = str.match(/place\\/[^/]*\\/(-?\\d+\\.\\d+),(-?\\d+\\.\\d+)/);
        if (placeMatch) return { lat: parseFloat(placeMatch[1]), lng: parseFloat(placeMatch[2]), text: str };
        return null;
    }

    // Add punto medio input row
    function addPuntoMedioRow(value) {
        var container = document.getElementById('puntosMediosContainer');
        if (!container) return;
        var rowDiv = document.createElement('div');
        rowDiv.style.cssText = 'display:flex;gap:6px;align-items:center;';
        var inp = document.createElement('input');
        inp.type = 'text';
        inp.className = 'cli-punto-medio-input';
        inp.placeholder = 'Dirección, coordenadas o link de Google Maps';
        inp.value = value || '';
        inp.style.cssText = 'flex:1;padding:5px 8px;border:1px solid rgba(255,255,255,0.12);border-radius:6px;background:rgba(255,255,255,0.04);color:#e5eaf1;font-size:0.65rem;';
        var btnRemove = document.createElement('button');
        btnRemove.type = 'button';
        btnRemove.textContent = '✕';
        btnRemove.style.cssText = 'background:#525252;color:#fff;border:none;border-radius:6px;padding:4px 8px;cursor:pointer;font-size:0.7rem;';
        btnRemove.addEventListener('click', function(){ rowDiv.remove(); });
        rowDiv.appendChild(inp);
        rowDiv.appendChild(btnRemove);
        container.appendChild(rowDiv);
    }

    // Render existing puntos medios in form
    function renderPuntosMediosInForm(puntosMedios) {
        var container = document.getElementById('puntosMediosContainer');
        if (!container) return;
        // Remove old dynamic rows (keep the first label with cliFormUbiPuntoMedio)
        container.querySelectorAll('div[style*="display:flex"]').forEach(function(r){ r.remove(); });
        if (Array.isArray(puntosMedios)) {
            puntosMedios.forEach(function(pm, idx) {
                if (idx === 0 && cliFormUbiPuntoMedio) {
                    cliFormUbiPuntoMedio.value = pm;
                } else {
                    addPuntoMedioRow(pm);
                }
            });
        }
    }

    // Buscador de puntos medios
    (function(){
        document.addEventListener('input', function(e){
            if (e.target.id !== 'buscarPuntoMedioInput') return;
            var term = e.target.value.trim().toUpperCase();
            var resultsDiv = document.getElementById('buscarPuntoMedioResults');
            if (!resultsDiv) return;
            if (!term) { resultsDiv.style.display = 'none'; return; }
            var all = getAllPuntosMedios();
            var matches = all.filter(function(p){ return p.toUpperCase().indexOf(term) !== -1; });
            if (!matches.length) { resultsDiv.style.display = 'none'; return; }
            resultsDiv.innerHTML = matches.map(function(m){
                return '<div class="pm-search-result" style="padding:6px 8px;cursor:pointer;font-size:0.65rem;color:#e5eaf1;border-bottom:1px solid rgba(255,255,255,0.06);" data-pm="'+m.replace(/"/g,'&quot;')+'">📌 '+m+'</div>';
            }).join('');
            resultsDiv.style.display = 'block';
            resultsDiv.querySelectorAll('.pm-search-result').forEach(function(item){
                item.addEventListener('click', function(){
                    addPuntoMedioRow(item.dataset.pm);
                    resultsDiv.style.display = 'none';
                    document.getElementById('buscarPuntoMedioInput').value = '';
                });
            });
        });

        document.addEventListener('click', function(e){
            if (e.target.id === 'btnAddPuntoMedio') {
                addPuntoMedioRow('');
            }
        });
    })();

    // Override openClientesFormPopup to load puntosMedios
    var _origOpenClientesForm = openClientesFormPopup;
    // Monkey-patch not needed — we handle in event after form opens
    var observeFormOpen = new MutationObserver(function(mutations){
        mutations.forEach(function(m){
            if (m.target === popupClientesForm && popupClientesForm.style.display === 'flex') {
                var editingCliente = clientesModuloData.find(function(c){ return c.id === clientesModuloEditingId; });
                if (editingCliente && editingCliente.puntosMedios) {
                    renderPuntosMediosInForm(editingCliente.puntosMedios);
                }
            }
        });
    });
    if (popupClientesForm) observeFormOpen.observe(popupClientesForm, { attributes: true, attributeFilter: ['style'] });

    // On save, also update global puntos medios
    var _origSaveCliente = saveClienteFromForm;"""

content = content.replace(inject_after, new_address_js)

# ============================================================
# 11. ADD DELIVERY ADDRESS PICKER INTEGRATION
# ============================================================
# Find enviarAEntregas function and enhance it to include address selection

old_enviar_marker = "    async function enviarAEntregas(orden) {"
enviar_line_idx = content.find(old_enviar_marker)

if enviar_line_idx >= 0:
    # Read current function to see what it does
    pass

# Add address picker function before the delivery module render
inject_delivery_before = "    var tipoDirLabel = { negocio: '🏢 Negocio', casa: '🏠 Casa', ubicacion: '📌 Ubicación Específica' };"

new_delivery_address_picker = """    var tipoDirLabel = { negocio: '🏢 Negocio', casa: '🏠 Casa', punto_medio: '📌 Punto Medio', ubicacion: '📌 Ubicación Específica' };

    /* ═══ DELIVERY ADDRESS PICKER ═══ */
    function mostrarSelectorDireccionEntrega(clienteNombre, callback) {
        var cliente = null;
        if (typeof clientesModuloData !== 'undefined') {
            cliente = clientesModuloData.find(function(c){
                return c.nombre && c.nombre.toUpperCase() === String(clienteNombre||'').toUpperCase();
            });
        }
        if (!cliente) { callback({ tipo: 'ubicacion', direccion: '' }); return; }

        var opciones = [];
        if (cliente.ubiDomicilio) opciones.push({ tipo: 'casa', label: '🏠 Casa', direccion: cliente.ubiDomicilio });
        if (cliente.ubiNegocio) opciones.push({ tipo: 'negocio', label: '🏢 Trabajo', direccion: cliente.ubiNegocio });
        var pms = cliente.puntosMedios || [];
        if (pms.length === 0 && cliente.ubiPuntoMedio) pms = [cliente.ubiPuntoMedio];
        // Default punto medio: last delivered or first in list
        var lastPM = '';
        try { lastPM = localStorage.getItem('ultimo_pm_' + cliente.id) || ''; } catch(e){}
        pms.forEach(function(pm, idx) {
            opciones.push({ tipo: 'punto_medio', label: '📌 Punto Medio' + (pms.length > 1 ? ' #'+(idx+1) : ''), direccion: pm, isDefault: pm === lastPM });
        });

        if (opciones.length === 0) {
            // No addresses, allow manual input
            callback({ tipo: 'ubicacion', direccion: '' });
            return;
        }

        // Mark last PM as default
        var defaultIdx = opciones.findIndex(function(o){ return o.isDefault; });
        if (defaultIdx < 0 && opciones.length > 0) defaultIdx = 0;

        var popup = document.createElement('div');
        popup.style.cssText = 'position:fixed;inset:0;z-index:200005;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;padding:16px;';
        var html = '<div style="background:#fff;border-radius:14px;max-width:440px;width:92%;padding:20px;max-height:80vh;overflow-y:auto;">';
        html += '<div style="font-size:0.9rem;font-weight:800;color:#ff9900;margin-bottom:12px;">📍 Seleccionar dirección de entrega</div>';
        html += '<div style="font-size:0.7rem;color:#6b7280;margin-bottom:12px;">Cliente: <strong>'+escEnt(clienteNombre)+'</strong></div>';
        html += '<div style="display:flex;flex-direction:column;gap:6px;">';
        opciones.forEach(function(op, idx) {
            var sel = idx === defaultIdx ? 'border:2px solid #ff9900;background:#fff7ed;' : 'border:1px solid #e5e7eb;background:#fff;';
            html += '<button class="addr-option-btn" data-idx="'+idx+'" style="'+sel+'border-radius:10px;padding:10px 12px;text-align:left;cursor:pointer;font-size:0.72rem;">';
            html += '<div style="font-weight:700;color:#111;">'+escEnt(op.label)+'</div>';
            html += '<div style="font-size:0.65rem;color:#6b7280;margin-top:2px;">'+escEnt(op.direccion)+'</div>';
            html += '</button>';
        });
        html += '<button class="addr-option-btn" data-idx="-1" style="border:1px solid #e5e7eb;background:#f9fafb;border-radius:10px;padding:10px 12px;text-align:left;cursor:pointer;font-size:0.72rem;">';
        html += '<div style="font-weight:700;color:#111;">➕ Agregar nueva dirección</div>';
        html += '<div style="font-size:0.65rem;color:#6b7280;margin-top:2px;">Ingresar dirección manualmente</div>';
        html += '</button>';
        html += '</div>';
        html += '<div style="margin-top:12px;display:none;" id="addrManualWrap">';
        html += '<input id="addrManualInput" type="text" placeholder="Dirección, coordenadas o link de Maps" style="width:100%;padding:8px;border:1px solid #d1d5db;border-radius:8px;font-size:0.72rem;">';
        html += '<div style="display:flex;gap:6px;margin-top:6px;">';
        html += '<label style="font-size:0.6rem;display:flex;align-items:center;gap:4px;"><input type="checkbox" id="addrSaveAsPM"> Guardar como punto medio del cliente</label>';
        html += '</div>';
        html += '</div>';
        html += '<div style="display:flex;gap:8px;margin-top:14px;justify-content:flex-end;">';
        html += '<button id="addrCancelBtn" style="padding:8px 16px;border:1px solid #d1d5db;border-radius:8px;background:#fff;cursor:pointer;font-size:0.72rem;">Cancelar</button>';
        html += '<button id="addrConfirmBtn" style="padding:8px 16px;border:none;border-radius:8px;background:#ff9900;color:#fff;cursor:pointer;font-weight:700;font-size:0.72rem;">Confirmar</button>';
        html += '</div></div>';
        popup.innerHTML = html;
        document.body.appendChild(popup);

        var selectedIdx = defaultIdx;
        var manualMode = false;

        function updateSelection() {
            popup.querySelectorAll('.addr-option-btn').forEach(function(btn){
                var bIdx = parseInt(btn.dataset.idx);
                if (bIdx === selectedIdx) {
                    btn.style.border = '2px solid #ff9900';
                    btn.style.background = '#fff7ed';
                } else {
                    btn.style.border = '1px solid #e5e7eb';
                    btn.style.background = bIdx === -1 ? '#f9fafb' : '#fff';
                }
            });
            var manualWrap = popup.querySelector('#addrManualWrap');
            if (manualWrap) manualWrap.style.display = selectedIdx === -1 ? 'block' : 'none';
        }

        popup.querySelectorAll('.addr-option-btn').forEach(function(btn){
            btn.addEventListener('click', function(){
                selectedIdx = parseInt(btn.dataset.idx);
                updateSelection();
            });
        });

        popup.querySelector('#addrCancelBtn').addEventListener('click', function(){ popup.remove(); });
        popup.addEventListener('click', function(e){ if(e.target === popup) popup.remove(); });

        popup.querySelector('#addrConfirmBtn').addEventListener('click', function(){
            var result;
            if (selectedIdx === -1) {
                var manualVal = (popup.querySelector('#addrManualInput')||{}).value || '';
                var saveAsPM = (popup.querySelector('#addrSaveAsPM')||{}).checked;
                if (saveAsPM && manualVal.trim() && cliente) {
                    if (!cliente.puntosMedios) cliente.puntosMedios = [];
                    cliente.puntosMedios.push(manualVal.trim());
                    savePuntoMedioGlobal(manualVal.trim());
                    if (typeof saveClientesModulo === 'function') saveClientesModulo();
                }
                result = { tipo: 'ubicacion', direccion: manualVal.trim() };
            } else {
                result = opciones[selectedIdx];
                if (result.tipo === 'punto_medio' && cliente) {
                    try { localStorage.setItem('ultimo_pm_' + cliente.id, result.direccion); } catch(e){}
                }
            }
            popup.remove();
            callback(result);
        });
    }"""

content = content.replace(inject_delivery_before, new_delivery_address_picker)

# ============================================================
# 12. FIX: Export CSV should include ubicaciones
# ============================================================
content = content.replace(
    "const headers = ['ID','NOMBRE','NEGOCIO','TELEFONO','CORREO','TIPO_CLIENTE','CALLE','COLONIA','NUMERO','PAIS','CIUDAD','ESTADO','CP','RAZON_SOCIAL','RFC','REFERENCIA_BANCARIA'];",
    "const headers = ['ID','NOMBRE','NEGOCIO','TELEFONO','CORREO','TIPO_CLIENTE','CALLE','COLONIA','NUMERO','PAIS','CIUDAD','ESTADO','CP','RAZON_SOCIAL','RFC','REFERENCIA_BANCARIA','UBI_DOMICILIO','UBI_NEGOCIO','UBI_PUNTO_MEDIO','PUNTOS_MEDIOS'];"
)
content = content.replace(
    """            c.razonSocial,
            c.rfc,
            c.referenciaBancaria
        ].map(esc).join(',')));""",
    """            c.razonSocial,
            c.rfc,
            c.referenciaBancaria,
            c.ubiDomicilio || '',
            c.ubiNegocio || '',
            c.ubiPuntoMedio || '',
            (c.puntosMedios || []).join(' | ')
        ].map(esc).join(',')));"""
)

# ============================================================
# 13. PERFORMANCE: Remove heavy inset shadows
# ============================================================
content = content.replace(
    'box-shadow: 0 0 60px rgba(0,0,0,0.8), inset 0 0 12px rgba(255,153,0,0.1);',
    'box-shadow: 0 4px 12px rgba(0,0,0,0.3);'
)

# ============================================================
# 14. Fix remaining non-orange colored module headers
# ============================================================
content = content.replace(
    "background: #071410;",
    "background: #0a0f1a;"
)

# ============================================================
# WRITE OUTPUT
# ============================================================
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

# Report changes
lines_orig = original.count('\n')
lines_new = content.count('\n')
changes = sum(1 for a, b in zip(original, content) if a != b)
print(f"✅ Patch applied successfully!")
print(f"   Lines: {lines_orig} → {lines_new}")
print(f"   Characters changed: {changes}")

# Count remaining gradients
remaining_grads = len(re.findall(r'linear-gradient|radial-gradient', content))
remaining_backdrop = len(re.findall(r'backdrop-filter', content))
remaining_trans_all = len(re.findall(r'transition:\s*all', content))
print(f"   Remaining gradients: {remaining_grads}")
print(f"   Remaining backdrop-filter: {remaining_backdrop}")
print(f"   Remaining transition:all: {remaining_trans_all}")
