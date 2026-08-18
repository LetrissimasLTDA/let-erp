from pathlib import Path
import base64, hashlib

source=Path('overrides/developer-badge-original.b64')
expected='d4f28988b6b0b9dd2de5084a7f75e8afc77bd109802e49e7b0216b418a8c5223'
if not source.exists():
    raise SystemExit('Badge Developer base64 não encontrada.')
try:
    data=base64.b64decode(source.read_text(encoding='utf-8').strip(),validate=True)
except Exception as exc:
    raise SystemExit('Badge Developer base64 inválida: '+str(exc))
if hashlib.sha256(data).hexdigest()!=expected:
    raise SystemExit('Hash da badge Developer não confere.')
Path('overrides/developer-badge.png').write_bytes(data)
print('Badge Developer reconstruída e validada:',len(data),'bytes')
