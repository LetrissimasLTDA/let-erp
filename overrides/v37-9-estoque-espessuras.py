from pathlib import Path
import re

site=Path('_site')
estoque=site/'estoque.html'
if not estoque.exists():
    raise SystemExit('estoque.html não encontrado')

text=estoque.read_text(encoding='utf-8')

# Garante 3 mm e 5 mm no select de ESPESSURA do Cadastro de Produto.
pat=re.compile(r'(<select[^>]*name=["\']espessura["\'][^>]*id=["\']espessura["\'][^>]*>)([\s\S]*?)(</select>)',re.I)
m=pat.search(text)
if not m:
    pat=re.compile(r'(<select[^>]*id=["\']espessura["\'][^>]*>)([\s\S]*?)(</select>)',re.I)
    m=pat.search(text)
if not m:
    raise SystemExit('Select de espessura do estoque não encontrado')

body=m.group(2)
# Remove duplicatas eventuais e recompõe a lista na ordem correta.
body=re.sub(r'\s*<option[^>]*>\s*(?:2|3|5|10|15|20)\s*mm\s*</option>\s*','\n',body,flags=re.I)
options='''
              <option>2 mm</option>
              <option>3 mm</option>
              <option>5 mm</option>
              <option>10 mm</option>
              <option>15 mm</option>
              <option>20 mm</option>
'''
# Mantém a opção "Selecione..." se existir e injeta as espessuras logo depois.
select_body=body
sel=re.search(r'(<option[^>]*value=["\']["\'][^>]*>[\s\S]*?</option>)',select_body,re.I)
if sel:
    select_body=select_body[:sel.end()]+options+select_body[sel.end():]
else:
    select_body=options+select_body

text=text[:m.start()]+m.group(1)+select_body+m.group(3)+text[m.end():]
if '3 mm' not in text or '5 mm' not in text:
    raise SystemExit('Falha ao inserir 3 mm e 5 mm no estoque')
if 'v37.9-estoque-espessuras' not in text:
    text+='\n<!-- v37.9-estoque-espessuras -->\n'
estoque.write_text(text,encoding='utf-8')
