#!/usr/bin/env python3
"""Regenerate manifest versions from VERSION; --check is read only."""
import argparse
import json
from project_version import ROOT, read_version

def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    version=read_version(); mismatch=[]
    for name in ('plugin.json','.codex-plugin/plugin.json'):
        path=ROOT/name; data=json.loads(path.read_text(encoding='utf-8'))
        if data.get('version') != version:
            mismatch.append(name)
            if not a.check:
                data['version']=version
                path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Version:',version,'|', 'mismatch: '+', '.join(mismatch) if a.check and mismatch else 'synchronized')
    return 1 if a.check and mismatch else 0
if __name__=='__main__': raise SystemExit(main())
