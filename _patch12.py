#!/usr/bin/env python3
"""Patch 12: Duplicate BOLSAS KRAFT module as BOLSAS KRAFT BLANCAS with white bag image."""
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
    if count == -1:
        content = content.replace(old, new)
    else:
        content = content.replace(old, new, count)
    changes += 1
    print(f"  [{changes}] {desc} (found {n}, replaced {min(n, count) if count != -1 else n})")

# ======================================================================
# 1. Landing card — add after BOLSAS KRAFT card
# ======================================================================
print("\n--- PART 1: Landing card ---")
do_replace(
    """            <div class="landing-card" onclick="seleccionarProducto('BOLSAS KRAFT')">
                <img class="landing-icon-img" src="https://img.icons8.com/ios-filled/50/FFFFFF/leaf.png" alt="Bolsas Kraft">
                <span>Bolsas Kraft</span>
            </div>""",
    """            <div class="landing-card" onclick="seleccionarProducto('BOLSAS KRAFT')">
                <img class="landing-icon-img" src="https://img.icons8.com/ios-filled/50/FFFFFF/leaf.png" alt="Bolsas Kraft">
                <span>Bolsas Kraft</span>
            </div>
            <div class="landing-card" onclick="seleccionarProducto('BOLSAS KRAFT BLANCAS')">
                <img class="landing-icon-img" src="https://i.postimg.cc/nrNDjDJS/bolsa-blanca.png" alt="Bolsas Kraft Blancas" style="object-fit:contain;">
                <span>Bolsas Kraft Blancas</span>
            </div>""",
    "Add landing card for Bolsas Kraft Blancas"
)

# ======================================================================
# 2. esProductoKraft — include new module
# ======================================================================
print("\n--- PART 2: esProductoKraft ---")
do_replace(
    "const esProductoKraft = (p = productoActual) => p === 'BOLSAS KRAFT' || p === 'DELIVERY KRAFT';",
    "const esProductoKraft = (p = productoActual) => p === 'BOLSAS KRAFT' || p === 'DELIVERY KRAFT' || p === 'BOLSAS KRAFT BLANCAS';",
    "Extend esProductoKraft to include BOLSAS KRAFT BLANCAS"
)

# ======================================================================
# 3. getMedidasKraftActivas — include new module (same medidas as BOLSAS KRAFT)
# ======================================================================
print("\n--- PART 3: getMedidasKraftActivas ---")
do_replace(
    "const getMedidasKraftActivas = (p = productoActual) => (p === 'DELIVERY KRAFT' ? MEDIDAS_DELIVERY_KRAFT : MEDIDAS_KRAFT);",
    "const getMedidasKraftActivas = (p = productoActual) => (p === 'DELIVERY KRAFT' ? MEDIDAS_DELIVERY_KRAFT : MEDIDAS_KRAFT);  // BOLSAS KRAFT BLANCAS uses same MEDIDAS_KRAFT",
    "Comment getMedidasKraft (BLANCAS uses same medidas)"
)

# ======================================================================
# 4. White bag image URL + Image object (after kraft image)
# ======================================================================
print("\n--- PART 4: White bag image ---")
do_replace(
    "    const URL_BOLSA_KRAFT_BASE = 'https://i.postimg.cc/7YTdkNtf/BOLSACAFE.png';",
    "    const URL_BOLSA_KRAFT_BASE = 'https://i.postimg.cc/7YTdkNtf/BOLSACAFE.png';\n    const URL_BOLSA_KRAFT_BLANCA = 'https://i.postimg.cc/nrNDjDJS/bolsa-blanca.png';",
    "Add URL for white kraft bag"
)

do_replace(
    """    const imgBolsaKraftBase = new Image();
    imgBolsaKraftBase.crossOrigin = 'anonymous';
    imgBolsaKraftBase.src = URL_BOLSA_KRAFT_BASE;
    imgBolsaKraftBase.onload = actualizar;""",
    """    const imgBolsaKraftBase = new Image();
    imgBolsaKraftBase.crossOrigin = 'anonymous';
    imgBolsaKraftBase.src = URL_BOLSA_KRAFT_BASE;
    imgBolsaKraftBase.onload = actualizar;

    const imgBolsaKraftBlanca = new Image();
    imgBolsaKraftBlanca.crossOrigin = 'anonymous';
    imgBolsaKraftBlanca.src = URL_BOLSA_KRAFT_BLANCA;
    imgBolsaKraftBlanca.onload = actualizar;""",
    "Add Image object for white kraft bag"
)

# ======================================================================
# 5. getBolsaImageForIndex — return white bag for BLANCAS
# ======================================================================
print("\n--- PART 5: getBolsaImageForIndex ---")
do_replace(
    "        if (esProductoKraft(productoActual)) return imgBolsaKraftBase;",
    "        if (productoActual === 'BOLSAS KRAFT BLANCAS') return imgBolsaKraftBlanca;\n        if (esProductoKraft(productoActual)) return imgBolsaKraftBase;",
    "Return white bag image for BLANCAS"
)

# ======================================================================
# 6. Module config entry — add after BOLSAS KRAFT entry
# ======================================================================
print("\n--- PART 6: Module config ---")
do_replace(
    """        {
            nombre: 'Bolsas Kraft',
            modulo: 'BOLSAS KRAFT',
            colores: ['Kraft Natural', 'Kraft Claro', 'Kraft Oscuro', 'Blanco', 'Negro'],
            medidas: ['MINI', 'CHICA', 'MEDIANA', 'GRANDE'],
            extras: []
        },""",
    """        {
            nombre: 'Bolsas Kraft',
            modulo: 'BOLSAS KRAFT',
            colores: ['Kraft Natural', 'Kraft Claro', 'Kraft Oscuro', 'Blanco', 'Negro'],
            medidas: ['MINI', 'CHICA', 'MEDIANA', 'GRANDE'],
            extras: []
        },
        {
            nombre: 'Bolsas Kraft Blancas',
            modulo: 'BOLSAS KRAFT BLANCAS',
            colores: ['Kraft Natural', 'Kraft Claro', 'Kraft Oscuro', 'Blanco', 'Negro'],
            medidas: ['MINI', 'CHICA', 'MEDIANA', 'GRANDE'],
            extras: []
        },""",
    "Add module config for Bolsas Kraft Blancas"
)

# ======================================================================
# 7. PRODUCTOS_DISPONIBLES — add to list
# ======================================================================
print("\n--- PART 7: PRODUCTOS_DISPONIBLES ---")
do_replace(
    "        'BOLSAS KRAFT',\n        'TARJETAS DE PRESENTACIÓN',",
    "        'BOLSAS KRAFT',\n        'BOLSAS KRAFT BLANCAS',\n        'TARJETAS DE PRESENTACIÓN',",
    "Add BOLSAS KRAFT BLANCAS to PRODUCTOS_DISPONIBLES"
)

# ======================================================================
# 8. moduloFromTipoProducto — add BLANCAS detection
# ======================================================================
print("\n--- PART 8: moduloFromTipoProducto ---")
do_replace(
    "        if (t.indexOf('KRAFT') >= 0) return 'BOLSAS KRAFT';",
    "        if (t.indexOf('KRAFT') >= 0 && t.indexOf('BLANCA') >= 0) return 'BOLSAS KRAFT BLANCAS';\n        if (t.indexOf('KRAFT') >= 0) return 'BOLSAS KRAFT';",
    "Add BLANCAS to moduloFromTipoProducto"
)

# ======================================================================
# 9. mapProductoParaProduccion — add BLANCAS
# ======================================================================
print("\n--- PART 9: mapProductoParaProduccion ---")
do_replace(
    "    if (t.indexOf('KRAFT') >= 0) return 'Bolsas Kraft';",
    "    if (t.indexOf('KRAFT') >= 0 && t.indexOf('BLANCA') >= 0) return 'Bolsas Kraft Blancas';\n    if (t.indexOf('KRAFT') >= 0) return 'Bolsas Kraft';",
    "Add BLANCAS to mapProductoParaProduccion"
)

# ======================================================================
# 10. Chat module fallback — add BLANCAS
# ======================================================================
print("\n--- PART 10: Chat fallback ---")
do_replace(
    "        if (tipo.indexOf('KRAFT') >= 0) modulo = 'BOLSAS KRAFT';",
    "        if (tipo.indexOf('KRAFT') >= 0 && tipo.indexOf('BLANCA') >= 0) modulo = 'BOLSAS KRAFT BLANCAS';\n        else if (tipo.indexOf('KRAFT') >= 0) modulo = 'BOLSAS KRAFT';",
    "Add BLANCAS to chat module fallback"
)

# ======================================================================
# 11. Producción form: add option + product section handling
# ======================================================================
print("\n--- PART 11: Producción form ---")
do_replace(
    "                            <option>Bolsas Kraft</option>",
    "                            <option>Bolsas Kraft</option>\n                            <option>Bolsas Kraft Blancas</option>",
    "Add option to producción select"
)

# actualizarSeccionesProducto — BLANCAS uses same kraft section
do_replace(
    "        else if (producto === 'Bolsas Kraft') target = 'secProductoKraft';",
    "        else if (producto === 'Bolsas Kraft' || producto === 'Bolsas Kraft Blancas') target = 'secProductoKraft';",
    "BLANCAS uses same kraft section in producción"
)

# getProductoDetalle — BLANCAS uses same kraft detail
do_replace(
    "        } else if (producto === 'Bolsas Kraft') {",
    "        } else if (producto === 'Bolsas Kraft' || producto === 'Bolsas Kraft Blancas') {",
    "BLANCAS uses same kraft detail logic",
    count=1
)

# validarDetallePorProducto — BLANCAS uses same kraft validation
do_replace(
    "        } else if (producto === 'Bolsas Kraft') {\n            if (!document.getElementById('prodTamanoKraft').value.trim()) faltantes.push('tamaño bolsa kraft');\n            if (!document.getElementById('prodMaterialKraft').value.trim()) faltantes.push('material kraft');",
    "        } else if (producto === 'Bolsas Kraft' || producto === 'Bolsas Kraft Blancas') {\n            if (!document.getElementById('prodTamanoKraft').value.trim()) faltantes.push('tamaño bolsa kraft');\n            if (!document.getElementById('prodMaterialKraft').value.trim()) faltantes.push('material kraft');",
    "BLANCAS uses same kraft validation"
)

# prodColorLabel — BLANCAS uses same TINTA label
do_replace(
    "            prodColorLabel.textContent = (producto === 'Bolsas Kraft') ? 'TINTA' : 'COLOR';",
    "            prodColorLabel.textContent = (producto === 'Bolsas Kraft' || producto === 'Bolsas Kraft Blancas') ? 'TINTA' : 'COLOR';",
    "BLANCAS same TINTA label"
)

# prodColorInput placeholder
do_replace(
    "            prodColorInput.placeholder = (producto === 'Bolsas Kraft') ? 'Ej: DORADO / NEGRO' : 'Ej: Rosa pastel';",
    "            prodColorInput.placeholder = (producto === 'Bolsas Kraft' || producto === 'Bolsas Kraft Blancas') ? 'Ej: DORADO / NEGRO' : 'Ej: Rosa pastel';",
    "BLANCAS same TINTA placeholder"
)

# ======================================================================
# WRITE
# ======================================================================
with open('mockup.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n=== DONE: {changes} changes. Size: {original} -> {len(content)} ===")
