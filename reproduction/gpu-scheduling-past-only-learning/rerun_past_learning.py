"""Public EP-0024 re-execution, with no private paths, imports or future labels.

Model structure remains known. Same-design execution is not independent
replication. Likelihood mixtures and the capacity theorem are prior work.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,math
import numpy as np
from two_class_control import exact_capacity,generate,fcfs
from observation_capacity import past_summary,diagnose,rate_cs,capacity,capacity_interval
from diagnostics import algorithm_ab,clopper_pearson

METHODS=['PAST_AB','KNOWN_CS','ALLOCATED_CS','LEARNED_CS','PLUGIN_MLE']
def side(ci,x):return 'overloaded' if ci[0]>x else ('subcritical' if ci[1] is not None and ci[1]<x else 'UNKNOWN')
def rerun(contract,seeds,horizons):
    rows=[]
    for model in contract['models']:
        x=float(F(exact_capacity(F(model['p']),F(model['mu_small']),F(model['mu_big']))['throughput']))
        for z in contract['load_factors']:
            for seed in seeds:
                a,s,k=generate(max(horizons),z*x,seed,model['p'],model['mu_small'],model['mu_big']);d=fcfs(a,s,k)
                for h in horizons:
                    aa,kk,dd=a[:h],k[:h],d[:h];tau=float(aa[-1]);mask=dd<=tau
                    obs=past_summary(aa,kk,np.where(mask)[0],dd[mask],tau)
                    learned=diagnose(obs,contract['alpha']);known=rate_cs(h,tau,contract['alpha']);allocated=rate_cs(h,tau,contract['alpha']/4)
                    observed_d=np.full(h,math.inf);observed_d[mask]=dd[mask]
                    ab=algorithm_ab(aa,observed_d,tau,10,contract['alpha'])
                    labels=dict(PAST_AB=ab['label'],KNOWN_CS=side(known,x),ALLOCATED_CS=side(allocated,x),LEARNED_CS=learned['label'],PLUGIN_MLE=learned['plugin_label'])
                    rows.append(dict(model=model['id'],load_factor=z,seed=seed,horizon=h,truth='subcritical' if z<1 else 'overloaded',
                         observed=obs,learned=learned,known_arrival_cs=known,allocated_arrival_cs=allocated,labels=labels,ab=ab))
    cells=[];anylook=[];n=len(seeds);family=len(contract['models'])*len(contract['load_factors'])*len(horizons)*len(METHODS)*2
    anyfamily=len(contract['models'])*len(contract['load_factors'])*len(METHODS)*2
    for model in contract['models']:
        for z in contract['load_factors']:
            rr=[r for r in rows if (r['model'],r['load_factor'])==(model['id'],z)]
            for h in horizons:
                rrr=[r for r in rr if r['horizon']==h];metrics={}
                for method in METHODS:
                    e=sum(r['labels'][method] not in ('UNKNOWN',r['truth']) for r in rrr);u=sum(r['labels'][method]=='UNKNOWN' for r in rrr)
                    metrics[method]=dict(wrong=e,unknown=u,correct=n-e-u,wrong_ci=clopper_pearson(e,n,.05/family),unknown_ci=clopper_pearson(u,n,.05/family),loss={str(a):(e+a*u)/n for a in [.1,.5,.9]})
                cells.append(dict(model=model['id'],load_factor=z,horizon=h,n=n,metrics=metrics))
            metrics={}
            for method in METHODS:
                e=sum(any(r['labels'][method] not in ('UNKNOWN',r['truth']) for r in rr if r['seed']==seed) for seed in seeds)
                u=sum(all(r['labels'][method]=='UNKNOWN' for r in rr if r['seed']==seed) for seed in seeds)
                metrics[method]=dict(wrong_anylook=e,unknown_alllooks=u,wrong_anylook_ci=clopper_pearson(e,n,.05/anyfamily),unknown_alllooks_ci=clopper_pearson(u,n,.05/anyfamily))
            anylook.append(dict(model=model['id'],load_factor=z,n=n,metrics=metrics))
    return dict(decisions=rows,cells=cells,anylook=anylook,workloads=len(contract['models'])*len(contract['load_factors'])*n,executed_decisions=len(rows)*len(METHODS),
      prediction_grading='NOT_PERFORMED for a changed grid; sealed predictions are in summary.json',independent_replication=False,validated_general_detector=False)

def verify_recorded():
    rec=json.loads(Path(__file__).with_name('summary.json').read_text(encoding='utf-8-sig'));c=rec['contract'];n=50
    assert rec['seal']['sealed_at']<rec['started_at']<rec['completed_at']
    assert len(rec['decisions'])==1200 and rec['executed_decisions']==6000 and all(f['passed'] for f in rec['fixtures'])
    for p in [F(1,8),F(1,4),F(1,2),F(3,4),F(7,8)]:
        for r,u in [(F(1),F(1,2)),(F(1,2),F(2)),(F(3,2),F(3,4)),(F(2),F(3))]:
            assert F(exact_capacity(p,r,u)['throughput'])==1/((1-p)/u+p*(2-p)/(2*r))
    ci=capacity_interval([.5,.9],[.5,.5],[2.,2.]);assert ci[0]<=16/17<=ci[1] and ci[0]<.95 and ci[1]>=1.
    hand=past_summary([0.,.1,.2],[1,2,1],[0],[10.],10.5);assert hand['exposure_small']==10 and hand['exposure_big']==.5
    try:past_summary([0.],[1],[0],[12.],10.)
    except ValueError:pass
    else:raise AssertionError('future completion accepted')
    for row in rec['decisions']:
        assert diagnose(row['observed'],c['alpha'])==row['learned']
        assert row['learned']['label']==row['labels']['LEARNED_CS'] and row['learned']['plugin_label']==row['labels']['PLUGIN_MLE']
    for cell in rec['cells']:
        rows=[r for r in rec['decisions'] if (r['model'],r['load_factor'],r['horizon'])==(cell['model'],cell['load_factor'],cell['horizon'])]
        assert len(rows)==n and len({r['seed'] for r in rows})==n
        for name,m in cell['metrics'].items():
            e=sum(r['labels'][name] not in ('UNKNOWN',r['truth']) for r in rows);u=sum(r['labels'][name]=='UNKNOWN' for r in rows)
            assert (e,u,n-e-u)==(m['wrong'],m['unknown'],m['correct'])
            assert np.allclose(m['wrong_ci'],clopper_pearson(e,n,.05/240)) and np.allclose(m['unknown_ci'],clopper_pearson(u,n,.05/240))
            assert all(math.isclose((e+float(a)*u)/n,v) for a,v in m['loss'].items())
    for cell in rec['anylook']:
        rows=[r for r in rec['decisions'] if (r['model'],r['load_factor'])==(cell['model'],cell['load_factor'])]
        for name,m in cell['metrics'].items():
            e=sum(any(r['labels'][name] not in ('UNKNOWN',r['truth']) for r in rows if r['seed']==seed) for seed in c['seeds'])
            u=sum(all(r['labels'][name]=='UNKNOWN' for r in rows if r['seed']==seed) for seed in c['seeds'])
            assert (e,u)==(m['wrong_anylook'],m['unknown_alllooks'])
            assert np.allclose(m['wrong_anylook_ci'],clopper_pearson(e,n,.05/80)) and np.allclose(m['unknown_alllooks_ci'],clopper_pearson(u,n,.05/80))
    def cell(mid,z,h):return next(v for v in rec['cells'] if (v['model'],v['load_factor'],v['horizon'])==(mid,z,h))
    grading=dict(S1=all(v['metrics']['LEARNED_CS']['wrong_anylook']<=5 for v in rec['anylook']),
      S2=all(cell(m['id'],z,320000)['metrics']['LEARNED_CS']['unknown']<=5 for m in c['models'] for z in [.8,1.2]),
      S3=all(cell(m['id'],z,20000)['metrics']['LEARNED_CS']['unknown']>=35 for m in c['models'] for z in [.99,1.01]),
      S4=any(cell(m['id'],z,20000)['metrics']['PLUGIN_MLE']['wrong']>=5 for m in c['models'] for z in [.99,1.01]))
    assert grading==rec['prediction_grading']
    out=rerun(c,[9101,9102],[20000])
    for row in out['decisions']:
        old=next(r for r in rec['decisions'] if (r['model'],r['load_factor'],r['seed'],r['horizon'])==(row['model'],row['load_factor'],row['seed'],row['horizon']))
        assert row['labels']==old['labels'] and row['learned']==old['learned'] and row['observed']==old['observed']
    print('Verified 6000 recorded decisions, capacity extrema, past telemetry, CP/anylook arithmetic and 16 regenerated runs; independent replication=false')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--verify-recorded',action='store_true');ap.add_argument('--seeds',type=int,default=2)
    ap.add_argument('--seed-start',type=int,default=9101);ap.add_argument('--horizons',nargs='+',type=int,default=[20000]);ap.add_argument('--output',type=Path)
    a=ap.parse_args()
    if a.verify_recorded:verify_recorded();return
    if a.seeds<1 or min(a.horizons)<10 or len(set(a.horizons))!=len(a.horizons):raise ValueError('positive seed count and distinct horizons>=10 required')
    c=json.loads(Path(__file__).with_name('summary.json').read_text(encoding='utf-8-sig'))['contract']
    out=rerun(c,list(range(a.seed_start,a.seed_start+a.seeds)),sorted(a.horizons))
    if a.output:a.output.write_text(json.dumps(out,indent=1,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(dict(workloads=out['workloads'],decisions=out['executed_decisions'],independent_replication=False)))
if __name__=='__main__':main()
