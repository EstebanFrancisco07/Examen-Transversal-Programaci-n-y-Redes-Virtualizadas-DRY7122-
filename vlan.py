# vlan.py
vlan = int(input("Ingresa el número de VLAN: "))
if 1 <= vlan <= 1005:
    print("VLAN NORMAL")
elif 1006 <= vlan <= 4094:
    print("VLAN EXTENDIDA")
else:
    print("VLAN FUERA DE RANGO")
