#!/usr/bin/env python3
"""Connect, observe, submit one initial hold action, finish; no solving or models."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source/agentbench_sdk'))
from agentbench_sdk import Client


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('session',type=Path,help='Private session JSON created by the environment owner')
    args=parser.parse_args()
    session=json.loads(args.session.read_text())
    client=Client(session['socket_path'],session['native_token'])
    try:
        description=client.describe()
        observation=client.observe()
        if observation['step_index']!=0:
            raise ValueError('This example requires a newly initialized episode')
        action=description['action_spec']['neutral_action']
        observation=client.step(action)['observation']
        print(json.dumps(dict(task=description['task']['id'],step=observation['step_index'],
                              simulation_time_s=observation['simulation_time_s'])))
        client.finish()
    finally:
        try:
            client.finish()
        finally:
            client.close()


if __name__=='__main__':main()
