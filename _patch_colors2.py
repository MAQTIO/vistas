#!/usr/bin/env python3
"""
Patch 2: Fix remaining blue/purple inline colors → orange/neutral
"""
import re

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Blue UI elements → orange (keep actual color swatches like in the color picker)
# These are BUTTON/UI colors, not product colors

# Mis Pedidos footer blue → orange
content = content.replace(
    ".mispedidos-foot-item:nth-child(4) span { color: #1d4ed8; }",
    ".mispedidos-foot-item:nth-child(4) span { color: #ff9900; }"
)

# Blue buttons in popups
content = content.replace(
    """            background: #2563eb;
            border-color: #1d4ed8;""",
    """            background: #ff9900;
            border-color: #e68a00;""",
)

# Clientes quick form focus purple → orange
content = content.replace(
    ".clientes-quick-form input:focus { border-color: #ab47bc; }",
    ".clientes-quick-form input:focus { border-color: #ff9900; }"
)
content = content.replace(
    ".clientes-quick-form select:focus { border-color: #ab47bc; }",
    ".clientes-quick-form select:focus { border-color: #ff9900; }"
)
content = content.replace(
    ".clientes-buscar:focus { border-color: #ab47bc; }",
    ".clientes-buscar:focus { border-color: #ff9900; }"
)

# Reportes KPI blue → orange
content = content.replace(
    'border-left:3px solid #2563eb;"><b>📈 GANANCIA</b><span id="repKpiGanancia" style="color:#2563eb;">',
    'border-left:3px solid #ff9900;"><b>📈 GANANCIA</b><span id="repKpiGanancia" style="color:#ff9900;">'
)

# Produccion resume blue → orange
content = content.replace(
    'style="font-size:1.5rem;font-weight:900;color:#2563eb;"',
    'style="font-size:1.5rem;font-weight:900;color:#ff9900;"'
)

# Print view blue → orange
content = content.replace(
    "'.hdr h1{font-size:1.3rem;color:#0277bd;}.folio{font-size:1rem;font-weight:800;}'+",
    "'.hdr h1{font-size:1.3rem;color:#ff9900;}.folio{font-size:1rem;font-weight:800;}'+"
)
content = content.replace(
    "'.badge{display:inline-block;padding:3px 10px;border-radius:999px;font-size:0.75rem;font-weight:700;background:#e3f2fd;color:#0277bd;}'+",
    "'.badge{display:inline-block;padding:3px 10px;border-radius:999px;font-size:0.75rem;font-weight:700;background:#fff7ed;color:#ff9900;}'+"
)

# Client picker blue → orange
content = content.replace(
    "'<div style=\"font-weight:800;font-size:0.85rem;color:#0277bd;\">👥 SELECCIONAR CLIENTE</div>'",
    "'<div style=\"font-weight:800;font-size:0.85rem;color:#ff9900;\">👥 SELECCIONAR CLIENTE</div>'"
)
content = content.replace(
    "'<div style=\"font-size:0.6rem;color:#0277bd;font-weight:700;\">Seleccionar</div></div>'",
    "'<div style=\"font-size:0.6rem;color:#ff9900;font-weight:700;\">Seleccionar</div></div>'"
)

# Purple buttons → orange
content = content.replace(
    'style="background:#7c3aed;border-color:#7c3aed;color:#fff;margin-left:auto;">📷 Recolectar</button>',
    'style="background:#ff9900;border-color:#e68a00;color:#fff;margin-left:auto;">📷 Recolectar</button>'
)
content = content.replace(
    'style="background:#7c3aed;border-color:#7c3aed;color:#fff;">📊 Estadísticas</button>',
    'style="background:#ff9900;border-color:#e68a00;color:#fff;">📊 Estadísticas</button>'
)
content = content.replace(
    "'<div style=\"font-size:1rem;font-weight:900;color:#7c3aed;\">ESTADÍSTICAS DE TRÁNSITO</div>'+",
    "'<div style=\"font-size:1rem;font-weight:900;color:#ff9900;\">ESTADÍSTICAS DE TRÁNSITO</div>'+"
)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

# Count remaining non-standard colors
remaining_blue = len(re.findall(r'#1d4ed8|#2563eb|#0277bd', content))
remaining_purple = len(re.findall(r'#7c3aed|#8e24aa|#ab47bc|#6d28d9|#7c4dff', content))
print(f"✅ Patch 2 applied!")
print(f"   Remaining blue UI elements: {remaining_blue}")
print(f"   Remaining purple UI elements: {remaining_purple}")
