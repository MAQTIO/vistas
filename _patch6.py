#!/usr/bin/env python3
"""Patch 6: Improve photo pane — bigger preview, remove note, add useful fields below."""
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
# 1. CSS: Make photo pane wider, taller preview, better scrolling
# ======================================================================
print("\n--- PART 1: CSS adjustments ---")

# Increase photo pane width from 150px to 180px
do_replace(
    "grid-template-columns: 150px minmax(0, 1fr);",
    "grid-template-columns: 180px minmax(0, 1fr);",
    "Widen photo pane from 150px to 180px"
)

# Make preview taller
do_replace(
    """.prod-photo-pane .prod-foto-preview {
            border-color: rgba(255,255,255,0.5);
            background: rgba(255,255,255,0.16);
            color: #fff;
            height: 80px;
        }""",
    """.prod-photo-pane .prod-foto-preview {
            border-color: rgba(255,255,255,0.5);
            background: rgba(255,255,255,0.16);
            color: #fff;
            height: 120px;
        }""",
    "Increase photo preview height from 80px to 120px"
)

# Add overflow-y auto to photo pane for extra fields 
do_replace(
    """.prod-photo-pane {
            background: linear-gradient(160deg, #f07a00 0%, #d76700 100%);
            border-radius: 10px;
            padding: 6px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            color: #fff;
            overflow: hidden;
            min-height: 0;
        }""",
    """.prod-photo-pane {
            background: linear-gradient(160deg, #f07a00 0%, #d76700 100%);
            border-radius: 10px;
            padding: 8px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            color: #fff;
            overflow-y: auto;
            min-height: 0;
        }

        .prod-photo-pane-extras {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-top: 2px;
        }

        .prod-photo-pane-extras label {
            font-size: 0.52rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.2px;
            color: rgba(255,255,255,0.85);
            margin-bottom: 1px;
        }

        .prod-photo-pane-extras input,
        .prod-photo-pane-extras select,
        .prod-photo-pane-extras textarea {
            width: 100%;
            padding: 4px 6px;
            border: 1px solid rgba(255,255,255,0.35);
            border-radius: 5px;
            font-size: 0.58rem;
            background: rgba(255,255,255,0.15);
            color: #fff;
            outline: none;
        }

        .prod-photo-pane-extras input::placeholder,
        .prod-photo-pane-extras textarea::placeholder {
            color: rgba(255,255,255,0.5);
        }

        .prod-photo-pane-extras select option {
            color: #1f2937;
            background: #fff;
        }

        .prod-photo-pane-extras .photo-pane-toggle {
            display: flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
        }

        .prod-photo-pane-extras .photo-pane-toggle input[type="checkbox"] {
            width: 14px;
            height: 14px;
            accent-color: #fff;
            cursor: pointer;
        }

        .prod-photo-pane-extras .photo-pane-toggle span {
            font-size: 0.56rem;
            font-weight: 700;
            color: #fff;
        }

        .prod-photo-pane-extras .photo-pane-separator {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.2);
            margin: 2px 0;
        }""",
    "Update photo pane CSS + add extras styles"
)

# ======================================================================
# 2. HTML: Replace photo pane content — remove note, add fields
# ======================================================================
print("\n--- PART 2: HTML photo pane ---")

old_photo_pane = """            <aside class="prod-photo-pane">
                <h4>Foto del producto</h4>
                <div class="prod-foto-principal-box">
                    <div id="prodFormFotoPreview" class="prod-foto-preview">Sin foto principal</div>
                    <input id="prodFormFotoPrincipal" type="file" accept="image/*">
                </div>
                <div class="prod-photo-pane-note">Esta foto se conserva al pasar al segundo paso para configurar tabulador y precios.</div>
            </aside>"""

new_photo_pane = """            <aside class="prod-photo-pane">
                <h4>\U0001f4f7 Foto del producto</h4>
                <div class="prod-foto-principal-box">
                    <div id="prodFormFotoPreview" class="prod-foto-preview">Sin foto principal</div>
                    <input id="prodFormFotoPrincipal" type="file" accept="image/*">
                </div>
                <div class="prod-photo-pane-extras">
                    <hr class="photo-pane-separator">
                    <div>
                        <label>Etiqueta / Color</label>
                        <select id="prodFormEtiqueta">
                            <option value="">Sin etiqueta</option>
                            <option value="rojo" style="color:#ef4444;">\U0001f534 Rojo — Urgente</option>
                            <option value="amarillo" style="color:#eab308;">\U0001f7e1 Amarillo — Revisar</option>
                            <option value="verde" style="color:#22c55e;">\U0001f7e2 Verde — Listo</option>
                            <option value="azul" style="color:#3b82f6;">\U0001f535 Azul — Destacado</option>
                            <option value="morado" style="color:#a855f7;">\U0001f7e3 Morado — Especial</option>
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
                </div>
            </aside>"""

do_replace(old_photo_pane, new_photo_pane, "Replace photo pane HTML with extras")

# ======================================================================
# 3. JS: Add new fields to payload
# ======================================================================
print("\n--- PART 3: Update payload ---")

do_replace(
    "            precioVenta: Math.max(0, Number(prodFormVenta?.value || 0))\n        };",
    """            precioVenta: Math.max(0, Number(prodFormVenta?.value || 0)),
            etiqueta: String(document.getElementById('prodFormEtiqueta')?.value || ''),
            ubicacion: String(document.getElementById('prodFormUbicacion')?.value || '').trim(),
            notasInternas: String(document.getElementById('prodFormNotasInternas')?.value || '').trim(),
            activo: document.getElementById('prodFormActivo')?.checked !== false,
            visibleCotizador: document.getElementById('prodFormVisibleCotizador')?.checked !== false
        };""",
    "Add new fields to payload"
)

# ======================================================================
# 4. JS: Clear new fields in reset
# ======================================================================
print("\n--- PART 4: Clear fields in reset ---")

do_replace(
    "        recetaDraft = []; procesosDraft = []; procesoInsumosDraft = [];\n        // receta cleared via recetaDraft = []",
    """        recetaDraft = []; procesosDraft = []; procesoInsumosDraft = [];
        // receta cleared via recetaDraft = []
        const etiquetaClear = document.getElementById('prodFormEtiqueta');
        const ubicacionClear = document.getElementById('prodFormUbicacion');
        const notasInternasClear = document.getElementById('prodFormNotasInternas');
        const activoClear = document.getElementById('prodFormActivo');
        const visibleCotClear = document.getElementById('prodFormVisibleCotizador');
        if (etiquetaClear) etiquetaClear.value = '';
        if (ubicacionClear) ubicacionClear.value = '';
        if (notasInternasClear) notasInternasClear.value = '';
        if (activoClear) activoClear.checked = true;
        if (visibleCotClear) visibleCotClear.checked = true;""",
    "Clear new fields on reset"
)

# ======================================================================
# 5. JS: Load new fields in edit
# ======================================================================
print("\n--- PART 5: Load fields in edit ---")

do_replace(
    "        if (prodFormProveedor) prodFormProveedor.value = row.proveedor || '';\n        if (prodFormDescripcion) prodFormDescripcion.value = row.descripcion || '';",
    """        if (prodFormProveedor) prodFormProveedor.value = row.proveedor || '';
        if (prodFormDescripcion) prodFormDescripcion.value = row.descripcion || '';
        const etiquetaEdit = document.getElementById('prodFormEtiqueta');
        const ubicacionEdit = document.getElementById('prodFormUbicacion');
        const notasInternasEdit = document.getElementById('prodFormNotasInternas');
        const activoEdit = document.getElementById('prodFormActivo');
        const visibleCotEdit = document.getElementById('prodFormVisibleCotizador');
        if (etiquetaEdit) etiquetaEdit.value = row.etiqueta || '';
        if (ubicacionEdit) ubicacionEdit.value = row.ubicacion || '';
        if (notasInternasEdit) notasInternasEdit.value = row.notasInternas || '';
        if (activoEdit) activoEdit.checked = row.activo !== false;
        if (visibleCotEdit) visibleCotEdit.checked = row.visibleCotizador !== false;""",
    "Load new fields on edit"
)

# ======================================================================
# 6. Also update the step-2 photo pane (tabulador) — just remove note
# ======================================================================
print("\n--- PART 6: Fix step-2 photo pane note ---")

do_replace(
    '<div class="prod-photo-pane-note">Vista previa bloqueada para mantener la foto cargada en el paso anterior.</div>',
    '',
    "Remove note from step-2 photo pane"
)

# ======================================================================
# 7. Include new fields in the display/listado rendering if etiqueta exists
# ======================================================================
print("\n--- PART 7: Show etiqueta badge in product list ---")

# Find where the product list renders each row — look for the product name cell
# Let's find the renderProductosTablaCuerpo or similar
# We'll search for where producto row items are rendered in the table

# WRITE
with open('mockup.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n=== {changes} changes applied. Size: {original} -> {len(content)} ===")
