"""Verify the recorded transition audit and regenerate a two-seed subset."""
from pathlib import Path
import argparse,json,math
from benchmark_transition import execute
ROOT=Path(__file__).parent
def close(a,b):
    if isinstance(a,dict):return set(a)==set(b) and all(close(a[k],b[k]) for k in a)
    if isinstance(a,(list,tuple)):return len(a)==len(b) and all(close(x,y) for x,y in zip(a,b))
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):return math.isclose(float(a),float(b),rel_tol=1e-9,abs_tol=1e-10)
    return a==b
def verify_recorded(data):
    assert data['executed_workloads']==120 and data['executed_looks']==360 and data['executed_method_decisions']==1080
    assert len(data['decisions'])==360 and len(data['cells'])==36 and all(data['prediction_grading'].values())
    for cell in data['cells']:
        rows=[x for x in data['decisions'] if (x['model'],x['scenario'],x['horizon'])==(cell['model'],cell['scenario'],cell['horizon'])]
        assert len(rows)==10
        for method,key in [('checkpoint','checkpoint_label'),('anytime','anytime_label')]:
            labels=[x['false_stationary_declaration'][key] for x in rows];truth=cell['truth']
            got=dict(wrong=sum(x not in ('UNKNOWN',truth) for x in labels),unknown=sum(x=='UNKNOWN' for x in labels),correct=sum(x==truth for x in labels))
            assert got==cell[method]
    drift=[x for x in data['decisions'] if not x['scenario'].startswith('stationary')]
    stationary=[x for x in data['decisions'] if x['scenario'].startswith('stationary')]
    assert len(drift)==240 and all(not x['truthful']['inference_performed'] and x['truthful']['label']=='UNKNOWN' for x in drift)
    assert len(stationary)==120 and all(x['truthful']['inference_performed'] and x['truthful']['label']==x['eventual_tail_truth'] for x in stationary)
def regenerate(data,seeds):
    c=dict(data['contract']);c['seeds']=c['seeds'][:seeds];fresh=execute(c)
    old={(x['model'],x['scenario'],x['seed'],x['horizon']):x for x in data['decisions']}
    for x in fresh['decisions']:
        y=old[(x['model'],x['scenario'],x['seed'],x['horizon'])]
        for key in ['eventual_tail_truth','truthful','false_stationary_declaration','observed','selected_checkpoints']:assert close(x[key],y[key]),key
    return len(fresh['decisions'])
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify-recorded',action='store_true');ap.add_argument('--seeds',type=int,default=2);ap.add_argument('--output',type=Path);a=ap.parse_args();data=json.loads((ROOT/'summary.json').read_text())
    if a.verify_recorded:
        verify_recorded(data);n=regenerate(data,a.seeds);print(f'transition-refusal: PASS; 360 recorded looks and {n} regenerated looks; not independent replication');return
    c=dict(data['contract']);c['seeds']=c['seeds'][:a.seeds];result=execute(c);assert a.output;a.output.write_text(json.dumps(result,indent=1)+'\n')
if __name__=='__main__':main()
