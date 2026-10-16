import json
import sys

from agentbench_platform.environment_supervisor import supervise


def test_supervisor_reaps_timed_out_child_and_records_invalid_outcome(tmp_path):
    status=supervise([sys.executable,'-c','import time; time.sleep(30)'],seconds=.05,output=tmp_path)
    result=json.loads((tmp_path/'supervisor-result.private.json').read_text())
    assert status==124 and result['outcome']=='invalid' and result['reason']=='wall_timeout'
    assert result['configured_wall_seconds']==.05 and result['child_returncode'] is not None


def test_supervisor_preserves_normal_child_exit(tmp_path):
    assert supervise([sys.executable,'-c','raise SystemExit(3)'],seconds=5,output=tmp_path)==3
    assert not (tmp_path/'supervisor-result.private.json').exists()
