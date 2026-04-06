#!/usr/bin/env python3
"""Patch 13: Update Bolsas Kraft Blancas — new image + custom medidas."""
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
# 1. Change image URL everywhere
# ======================================================================
print("\n--- PART 1: Change image URL ---")
do_replace(
    "https://i.postimg.cc/nrNDjDJS/bolsa-blanca.png",
    "https://i.postimg.cc/tJD980rY/bolsa-blanca-2.png",
    "Change bolsa-blanca image URL",
    count=-1
)

# ======================================================================
# 2. Add MEDIDAS_KRAFT_BLANCAS array after MEDIDAS_DELIVERY_KRAFT
# ======================================================================
print("\n--- PART 2: Add MEDIDAS_KRAFT_BLANCAS ---")
do_replace(
    """    const MEDIDAS_DELIVERY_KRAFT = [
        { value: '30,41,DELIVERY', label: '30x41+17.5' }
    ];""",
    """    const MEDIDAS_DELIVERY_KRAFT = [
        { value: '30,41,DELIVERY', label: '30x41+17.5' }
    ];
    const MEDIDAS_KRAFT_BLANCAS = [
        { value: '4.3,7.7,000', label: '000 4.3x7.7' },
        { value: '5.2,11,15grs', label: '15grs 5.2x11' },
        { value: '6,11,20grs', label: '20grs 6x11' },
        { value: '6,15.5,1/4', label: '1/4 6x15.5+3.5' },
        { value: '7.5,17,1/2', label: '1/2 7.5x17+3.5' },
        { value: '8.5,20.5,1', label: '1 8.5x20.5+5.5' },
        { value: '10,24.5,2', label: '2 10x24.5+6' },
        { value: '13,30,4', label: '4 13x30+7' },
        { value: '14.5,34,6', label: '6 14.5x34+9' },
        { value: '15,37,8', label: '8 15x37+9' },
        { value: '17.5,41,12', label: '12 17.5x41+10' },
        { value: '17.5,41,14', label: '14 17.5x41+11' },
        { value: '17.5,41,16', label: '16 17.5x41+12' },
        { value: '17.5,41,20', label: '20 17.5x41+13' },
        { value: '17.5,41,25', label: '25 17.5x41+14' },
        { value: '17.5,41,30', label: '30 17.5x41+15' },
        { value: '20.5,61,35', label: '35 20.5x61+12' },
        { value: '69,10.5,1BG', label: '1BG 69x10.5+6' },
        { value: '69,12.5,2BG', label: '2BG 69x12.5+7' }
    ];""",
    "Add MEDIDAS_KRAFT_BLANCAS array"
)

# ======================================================================
# 3. Add fuelle entries for BLANCAS sizes to FUELLE_KRAFT
# ======================================================================
print("\n--- PART 3: Add fuelle entries ---")
do_replace(
    """    const FUELLE_KRAFT = {
        '1/4': '3.5',
        '1/2': '3.5',
        '1': '5.5',
        '2': '6',
        '3': '6.5',
        '4': '7',
        '5': '7.5',
        '6': '9',
        '8': '9',
        '10': '10',
        '12': '10',
        '14': '11',
        '16': '3.5',
        '20': '3.5',
        '25': '5.5',
        '30': '6',
        '35': '6.5',
        'DELIVERY': '17.5'
    };""",
    """    const FUELLE_KRAFT = {
        '000': '0',
        '15grs': '0',
        '20grs': '0',
        '1/4': '3.5',
        '1/2': '3.5',
        '1': '5.5',
        '2': '6',
        '3': '6.5',
        '4': '7',
        '5': '7.5',
        '6': '9',
        '8': '9',
        '10': '10',
        '12': '10',
        '14': '11',
        '16': '12',
        '20': '13',
        '25': '14',
        '30': '15',
        '35': '12',
        '1BG': '6',
        '2BG': '7',
        'DELIVERY': '17.5'
    };""",
    "Update FUELLE_KRAFT with blancas sizes"
)

# ======================================================================
# 4. Update getMedidasKraftActivas to use MEDIDAS_KRAFT_BLANCAS
# ======================================================================
print("\n--- PART 4: getMedidasKraftActivas ---")
do_replace(
    "const getMedidasKraftActivas = (p = productoActual) => (p === 'DELIVERY KRAFT' ? MEDIDAS_DELIVERY_KRAFT : MEDIDAS_KRAFT);  // BOLSAS KRAFT BLANCAS uses same MEDIDAS_KRAFT",
    "const getMedidasKraftActivas = (p = productoActual) => (p === 'DELIVERY KRAFT' ? MEDIDAS_DELIVERY_KRAFT : p === 'BOLSAS KRAFT BLANCAS' ? MEDIDAS_KRAFT_BLANCAS : MEDIDAS_KRAFT);",
    "getMedidasKraftActivas returns BLANCAS medidas"
)

# ======================================================================
# 5. Update module config medidas
# ======================================================================
print("\n--- PART 5: Module config medidas ---")
do_replace(
    """        {
            nombre: 'Bolsas Kraft Blancas',
            modulo: 'BOLSAS KRAFT BLANCAS',
            colores: ['Kraft Natural', 'Kraft Claro', 'Kraft Oscuro', 'Blanco', 'Negro'],
            medidas: ['MINI', 'CHICA', 'MEDIANA', 'GRANDE'],
            extras: []
        },""",
    """        {
            nombre: 'Bolsas Kraft Blancas',
            modulo: 'BOLSAS KRAFT BLANCAS',
            colores: ['Kraft Natural', 'Kraft Claro', 'Kraft Oscuro', 'Blanco', 'Negro'],
            medidas: ['000', '15grs', '20grs', '1/4', '1/2', '1', '2', '4', '6', '8', '12', '14', '16', '20', '25', '30', '35', '1BG', '2BG'],
            extras: []
        },""",
    "Update BLANCAS module config medidas"
)

# ======================================================================
# WRITE
# ======================================================================
with open('mockup.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n=== DONE: {changes} changes. Size: {original} -> {len(content)} ===")
