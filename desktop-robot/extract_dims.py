import ezdxf

doc = ezdxf.readfile(r'C:\Users\xurui01\AppData\Local\Temp\ESP32-S3-DualEye-LCD-1.28-struct\ESP32-S3-DualEye-LCD-1.28.dxf')
msp = doc.modelspace()

# Extract all DIMENSION entities
dims = []
for entity in msp:
    if entity.dxftype() == 'DIMENSION':
        try:
            text = entity.dxf.text if hasattr(entity.dxf, 'text') else ''
            actual = entity.dxf.actual_measurement if hasattr(entity.dxf, 'actual_measurement') else 'N/A'
            dims.append((text, actual))
        except:
            pass

print(f'Found {len(dims)} DIMENSION entities:')
for t, a in dims:
    print(f'  text="{t}" actual={a}')

# Also check MTEXT and TEXT entities for dimension labels
print('\nTEXT entities:')
for entity in msp:
    if entity.dxftype() in ('TEXT', 'MTEXT'):
        try:
            if entity.dxftype() == 'TEXT':
                t = entity.dxf.text
            else:
                t = entity.text
            print(f'  {entity.dxftype()}: "{t}"')
        except:
            pass
