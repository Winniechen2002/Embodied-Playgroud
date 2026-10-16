#!/usr/bin/env python3
"""Check vendored source bytes against their fixed snapshot manifest, offline."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/agentbench_platform'))


def main():
    from agentbench_platform.embedded_sources import verify_embedded_sources
    result=verify_embedded_sources(ROOT)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return int(result['status']!='passed')


if __name__=='__main__':raise SystemExit(main())
