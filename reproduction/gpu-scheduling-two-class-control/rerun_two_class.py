"""Public two-class strict-FCFS re-execution. No private paths or imports.

Same design/generator logic, not independent replication or real GPU validation.
Known population class/service parameters privilege K_EXACT. Never use F-CI for
this mixture. AB's nominal alpha is not a proven error control for dependent batches.
"""
from pathlib import Path
from fractions import Fraction
import argparse,json,math
import numpy as np
from scipy.stats import chi2
from two_class_control import exact_capacity,generate,fcfs
from diagnostics import algorithm_ab,window_elasticity,clopper_pearson

def decide(z,seed,h,arrival,size,departure):
    a,s,d=arrival[:h],size[:h],departure[:h];tau=float(a[-1])
    ci=chi2.ppf([.025,.975],2*h)/(2*tau)
    k='overloaded' if ci[0]>8/11 else ('subcritical' if ci[1]<8/11 else 'UNKNOWN')
    nominal=h/tau*1.25
    ab=algorithm_ab(a,d,tau,10,.05)
    elastic=window_elasticity(a,d,h,2.,.2,.5)
    return dict(load_factor=z,seed=seed,horizon=h,truth='subcritical' if z<1 else 'overloaded',
        labels=dict(O_AB=ab['label'],D_ALPHA=elastic['label'],K_EXACT=k,NOMINAL_WORK='overloaded' if nominal>=1 else 'subcritical'),
        rate=dict(rate_estimate=h/tau,rate_ci_low=float(ci[0]),rate_ci_high=float(ci[1])),
        ab=ab,elasticity=elastic,nominal_estimate=nominal,
        future_work_share=float(np.minimum(s,np.maximum(0,d-tau)).sum()/s.sum()),
        drain_extra_ratio=max(0,float(np.max(d)-tau))/tau)

def rerun(seeds,horizons,factors):
    rows=[]
    for z in factors:
        if z<=0 or z==1: raise ValueError('positive noncritical effective load required')
        for seed in seeds:
            a,s,need=generate(max(horizons),z*8/11,seed);d=fcfs(a,s,need)
            rows.extend(decide(z,seed,h,a,s,d) for h in horizons)
    cells=[];family_count=len(factors)*len(horizons)*4*2
    for z in factors:
        for h in horizons:
            rr=[r for r in rows if (r['load_factor'],r['horizon'])==(z,h)]
            n=len(rr);metrics={}
            for method in rr[0]['labels']:
                e=sum(r['labels'][method] not in ('UNKNOWN',r['truth']) for r in rr)
                u=sum(r['labels'][method]=='UNKNOWN' for r in rr)
                metrics[method]=dict(correct=n-e-u,wrong=e,unknown=u,
                  wrong_ci=clopper_pearson(e,n,.05/family_count),unknown_ci=clopper_pearson(u,n,.05/family_count),
                  loss={str(a):(e+a*u)/n for a in [.1,.5,.9]})
            cells.append(dict(load_factor=z,horizon=h,n=n,metrics=metrics))
    return dict(exact_capacity=exact_capacity(),decisions=rows,cells=cells,
                independent_replication=False,validated_general_detector=False)

def verify_recorded():
    rec=json.loads(Path(__file__).with_name('summary.json').read_text(encoding='utf-8'))
    assert exact_capacity()==rec['exact_capacity']
    assert rec['seal']['sealed_at']<rec['seal']['started_at']<rec['seal']['completed_at']
    assert np.array_equal(fcfs(np.array([0.,.1,.2]),np.array([10.,1.,1.]),np.array([1,2,1])),[10.,11.,12.])
    assert len(rec['decisions'])==1000 and all(f['passed'] for f in rec['fixtures'])
    for cell in rec['cells']:
        rr=[r for r in rec['decisions'] if (r['load_factor'],r['horizon'])==(cell['load_factor'],cell['horizon'])]
        for method,m in cell['metrics'].items():
            e=sum(r['labels'][method] not in ('UNKNOWN',r['truth']) for r in rr)
            u=sum(r['labels'][method]=='UNKNOWN' for r in rr)
            assert (e,u)==(m['wrong'],m['unknown'])
            assert np.allclose(m['wrong_ci'],clopper_pearson(e,100,.05/80))
            assert np.allclose(m['unknown_ci'],clopper_pearson(u,100,.05/80))
            assert all(math.isclose((e+float(a)*u)/100,v) for a,v in m['loss'].items())
    def cell(z,h):return next(c for c in rec['cells'] if (c['load_factor'],c['horizon'])==(z,h))
    grades={
      'M0':all(cell(z,80000)['metrics'][m]['wrong']<=10 for z in (.8,1.2) for m in ('O_AB','D_ALPHA')),
      'M1':all(cell(1.05,h)['metrics']['NOMINAL_WORK']['wrong']>=95 for h in rec['horizons']) and cell(1.01,80000)['metrics']['NOMINAL_WORK']['wrong']>=90,
      'M2':all(c['metrics']['K_EXACT']['wrong']<=10 for c in rec['cells']),
      'M3':all(cell(z,20000)['metrics']['K_EXACT']['unknown']>=40 for z in (.99,1.01)),
      'M4':cell(.99,20000)['metrics']['D_ALPHA']['wrong']>=15}
    assert grades==rec['prediction_grading']
    # Regenerate ten small runs, compare every diagnostic against the recorded
    # same-model results. This is executable parity, not external replication.
    out=rerun([8001,8002],[20000],rec['load_factors'])
    for row in out['decisions']:
        old=next(r for r in rec['decisions'] if (r['load_factor'],r['seed'],r['horizon'])==(row['load_factor'],row['seed'],row['horizon']))
        assert row['labels']==old['labels']
        for key in ['rate_estimate','rate_ci_low','rate_ci_high']: assert math.isclose(row['rate'][key],old['rate'][key],rel_tol=1e-12)
        assert math.isclose(row['elasticity']['alpha'],old['elasticity']['alpha'],abs_tol=1e-12)
    print('Exact capacity, recorded 4000-decision arithmetic and ten regenerated runs verified; independent replication=false')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--verify-recorded',action='store_true')
    parser.add_argument('--seeds',type=int,default=10)
    parser.add_argument('--seed-start',type=int,default=8001)
    parser.add_argument('--horizons',type=int,nargs='+',default=[20000])
    parser.add_argument('--load-factors',type=float,nargs='+',default=[.8,.99,1.01,1.05,1.2])
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.verify_recorded:verify_recorded();return
    if args.seeds<1 or min(args.horizons)<10 or len(set(args.horizons))!=len(args.horizons): raise ValueError('positive seeds and distinct horizons >=10 required')
    out=rerun(range(args.seed_start,args.seed_start+args.seeds),sorted(args.horizons),args.load_factors)
    if args.output:args.output.write_text(json.dumps(out,indent=1,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'capacity':out['exact_capacity']['throughput'],'cells':out['cells']},indent=1))
if __name__=='__main__':main()
