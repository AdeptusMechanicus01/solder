import io
import pathlib
import re
import subprocess
import sys
import tempfile

fail = 0
html_files = [p for p in pathlib.Path('.').rglob('*.html') if '.git' not in p.parts]
if not html_files:
    print('No HTML files found')
    sys.exit(0)

for p in html_files:
    print(f'::group::{p}')
    s = p.read_text(encoding='utf-8')
    scripts = re.findall(r'<script type="module">(.*?)</script>', s, re.S)
    if not scripts:
        print('no module scripts, skipping')
    else:
        with tempfile.NamedTemporaryFile('w', suffix='.mjs', delete=False, encoding='utf-8') as tmp:
            tmp.write('\n'.join(scripts))
            tmp_path = tmp.name
        print(f'checking {len(scripts)} module script(s)')
        r = subprocess.run(['node', '--check', tmp_path])
        if r.returncode != 0:
            fail = 1
            print(f'::error file={p}::JS syntax check failed')
    print('::endgroup::')

sys.exit(fail)
