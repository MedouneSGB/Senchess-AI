import openvino as ov

core = ov.Core()
devices = core.available_devices

print("=" * 60)
print("DEVICES OpenVINO DISPONIBLES")
print("=" * 60)
print()
print(f"Devices détectés : {devices}")
print()

for device in devices:
    print(f"📱 {device}:")
    try:
        name = core.get_property(device, "FULL_DEVICE_NAME")
        print(f"   Nom: {name}")
    except Exception as e:
        print(f"   Erreur: {e}")
    print()
