"""EP-0025 public runner. Reporting looks retain the original error allocation.

Same-design/code re-execution, not independent replication or novel theory.
Public CLI needs no private paths or native-engine imports.
"""
from pathlib import Path
from fractions import Fraction as F
import json,math,argparse,copy
import numpy as np
from two_class_control import generate,fcfs,exact_capacity
from observation_capacity import diagnose
from checkpoint_capacity import checkpoint_tape,scheduled_diagnose,gamma_interval,ATTESTATION
from benchmark_checkpoint import execute
from diagnostics import clopper_pearson
from numeric_verification import assert_equivalent

def side(ci,x):return 'overloaded' if ci[0]>x else ('subcritical' if ci[1]<x else 'UNKNOWN')
def partial_rerun(c,seeds,looks):
    rows=[]
    for m in c['models']:
        x=float(F(exact_capacity(F(m['p']),F(m['mu_small']),F(m['mu_big']))['throughput']))
        for z in c['load_factors']:
            for seed in seeds:
                a,s,k=generate(max(looks),z*x,seed,m['p'],m['mu_small'],m['mu_big']);d=fcfs(a,s,k)
                for h in looks:
                    aa,kk,dd=a[:h],k[:h],d[:h];tau=float(aa[-1]);mask=dd<=tau
                    tape=checkpoint_tape(aa,kk,np.where(mask)[0],dd[mask],tau,c['milestones'])
                    anytime=diagnose(tape['observed'],c['alpha']);checkpoint=scheduled_diagnose(tape,c['attestation'],c['horizons'],c['milestones'],c['alpha'])
                    # c['horizons'] keeps all three original planned looks.
                    # Selecting fewer outputs does not spend their error budget again.
                    known=gamma_interval(h,tau,c['alpha']/len(c['horizons']))
                    labels=dict(ANYTIME_RECT=anytime['label'],CHECKPOINT_RECT=checkpoint['label'],KNOWN_SCHEDULED=side(known,x),ALLOC_SCHEDULED=side(checkpoint['intervals']['arrival'],x),PLUGIN_MLE=anytime['plugin_label'])
                    rows.append(dict(model=m['id'],load_factor=z,seed=seed,horizon=h,truth='subcritical' if z<1 else 'overloaded',tape=tape,anytime=anytime,checkpoint=checkpoint,known_arrival_ci=known,labels=labels))
    return dict(decisions=rows,executed_workloads=len(c['models'])*len(c['load_factors'])*len(seeds),executed_decisions=len(rows)*5,original_reporting_schedule=c['horizons'],requested_looks=looks,prediction_grading='NOT_PERFORMED partial grid',independent_replication=False,validated_general_detector=False)

def verify_recorded():
    rec=json.loads(Path(__file__).with_name('summary.json').read_text(encoding='utf-8-sig'));c=rec['contract']
    assert len(rec['decisions'])==480 and rec['executed_decisions']==2400 and all(f['passed'] for f in rec['fixtures'])
    assert rec['seal']['sealed_at']<rec['started_at']<rec['completed_at']
    hand=checkpoint_tape([0.,.1,11.],[1,1,2],[0],[10.],11.,[1])
    assert hand['checkpoints']['small'][0]['exposure']==19.9 and hand['observed']['exposure_small']==20.9
    bad=copy.deepcopy(ATTESTATION);bad['service']='UNKNOWN';gate=scheduled_diagnose(hand,bad,[3],[1]);assert gate['label']=='UNKNOWN' and not gate['inference_performed']
    for field,value in [('policy','backfill'),('completion_log','UNKNOWN'),('resources_fungible',False),('provenance','real_cluster_unconfirmed')]:
        bad=copy.deepcopy(ATTESTATION);bad[field]=value;assert not scheduled_diagnose(hand,bad,[3],[1])['inference_performed']
    bad=copy.deepcopy(ATTESTATION);del bad['arrival_log'];assert not scheduled_diagnose(hand,bad,[3],[1])['inference_performed']
    bad=copy.deepcopy(ATTESTATION);bad['true_mu_small']=1.;assert not scheduled_diagnose(hand,bad,[3],[1])['inference_performed']
    assert scheduled_diagnose(hand,ATTESTATION)['reason']=='not_a_predeclared_arrival_look'
    bad=copy.deepcopy(hand);bad['cutoff_is_arrival_index']=False;assert not scheduled_diagnose(bad,ATTESTATION,[3],[1])['inference_performed']
    try:checkpoint_tape([0.,.1],[1,1],[0],[12.],11.,[1])
    except ValueError:pass
    else:raise AssertionError('future completion accepted')
    for row in rec['decisions']:
        assert_equivalent(scheduled_diagnose(row['tape'],c['attestation'],c['horizons'],c['milestones'],c['alpha']),row['checkpoint'],'recorded.checkpoint')
        assert_equivalent(diagnose(row['tape']['observed'],c['alpha']),row['anytime'],'recorded.anytime')
        assert row['checkpoint']['label']==row['labels']['CHECKPOINT_RECT'] and not row['checkpoint']['anytime']
    for cell in rec['cells']:
        rows=[r for r in rec['decisions'] if (r['model'],r['load_factor'],r['horizon'])==(cell['model'],cell['load_factor'],cell['horizon'])]
        assert len(rows)==20 and len({r['seed'] for r in rows})==20
        for name,m in cell['metrics'].items():
            e=sum(r['labels'][name] not in ('UNKNOWN',r['truth']) for r in rows);u=sum(r['labels'][name]=='UNKNOWN' for r in rows)
            assert (e,u,20-e-u)==(m['wrong'],m['unknown'],m['correct'])
            assert_equivalent(clopper_pearson(e,20,.05/240),m['wrong_ci'],'wrong_ci');assert_equivalent(clopper_pearson(u,20,.05/240),m['unknown_ci'],'unknown_ci')
            assert all(math.isclose((e+float(a)*u)/20,value,rel_tol=1e-12) for a,value in m['loss'].items())
    for cell in rec['anylook']:
        rows=[r for r in rec['decisions'] if (r['model'],r['load_factor'])==(cell['model'],cell['load_factor'])]
        for name,m in cell['metrics'].items():
            e=sum(any(r['labels'][name] not in ('UNKNOWN',r['truth']) for r in rows if r['seed']==seed) for seed in c['seeds']);u=sum(all(r['labels'][name]=='UNKNOWN' for r in rows if r['seed']==seed) for seed in c['seeds'])
            assert (e,u)==(m['wrong_anylook'],m['unknown_alllooks'])
            assert_equivalent(clopper_pearson(e,20,.05/80),m['wrong_anylook_ci'],'anylook_ci');assert_equivalent(clopper_pearson(u,20,.05/80),m['unknown_alllooks_ci'],'unresolved_ci')
    def cell(mid,z,h):return next(v for v in rec['cells'] if (v['model'],v['load_factor'],v['horizon'])==(mid,z,h))
    grading=dict(S1=all(v['metrics']['CHECKPOINT_RECT']['wrong_anylook']<=2 for v in rec['anylook']),S2=all(cell(m['id'],z,1280000)['metrics']['CHECKPOINT_RECT']['unknown']==0 for m in c['models'] for z in [.8,1.2]),S3=all(cell(m['id'],z,1280000)['metrics']['CHECKPOINT_RECT']['correct']>=1 for m in c['models'] for z in [.99,1.01]),S4=sum(cell(m['id'],z,1280000)['metrics']['CHECKPOINT_RECT']['unknown'] for m in c['models'] for z in [.99,1.01])<sum(cell(m['id'],z,1280000)['metrics']['ANYTIME_RECT']['unknown'] for m in c['models'] for z in [.99,1.01]))
    assert grading==rec['prediction_grading']
    out=partial_rerun(c,[9201,9202],[20000])
    for row in out['decisions']:
        old=next(r for r in rec['decisions'] if (r['model'],r['load_factor'],r['seed'],r['horizon'])==(row['model'],row['load_factor'],row['seed'],row['horizon']))
        assert row['labels']==old['labels']
        for key in ['tape','anytime','checkpoint','known_arrival_ci']:assert_equivalent(row[key],old[key],'rerun.'+key)
    print('Verified 2400 recorded decisions, fixed-count exposures, declaration/unscheduled gates, CP/anylook/predictions and16 regenerated small runs; independent replication=false')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify-recorded',action='store_true');ap.add_argument('--seeds',type=int,default=2);ap.add_argument('--seed-start',type=int,default=9201)
    ap.add_argument('--horizons',type=int,nargs='+',default=[20000]);ap.add_argument('--output',type=Path);args=ap.parse_args()
    if args.verify_recorded:verify_recorded();return
    c=json.loads(Path(__file__).with_name('summary.json').read_text(encoding='utf-8-sig'))['contract'];looks=sorted(args.horizons)
    if args.seeds<1 or len(set(looks))!=len(looks) or any(h not in c['horizons'] for h in looks):raise ValueError('positive seeds and distinct original reporting looks required')
    seeds=list(range(args.seed_start,args.seed_start+args.seeds))
    if looks==c['horizons']:
        c['seeds']=seeds;out=execute(c,clopper_pearson)
    else:out=partial_rerun(c,seeds,looks)
    if args.output:args.output.write_text(json.dumps(out,indent=1,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(dict(workloads=out['executed_workloads'],decisions=out['executed_decisions'],independent_replication=False)))
if __name__=='__main__':main()
