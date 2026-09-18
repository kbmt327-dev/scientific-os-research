"""Sealed scheduled-checkpoint comparison; existing time-change/Gamma theory."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import sys,json,math,argparse,hashlib,subprocess,time
import numpy as np
import scipy
from two_class_control import exact_capacity,generate,fcfs
from observation_capacity import diagnose
from checkpoint_capacity import checkpoint_tape,scheduled_diagnose,gamma_interval,ATTESTATION,HORIZONS,MILESTONES

MODELS=[dict(id='baseline',p=.5,mu_small=1.,mu_big=.5),dict(id='transfer',p=.25,mu_small=.5,mu_big=2.)]
FACTORS=[.8,.99,1.01,1.2];SEEDS=list(range(9201,9221))
METHODS=['ANYTIME_RECT','CHECKPOINT_RECT','KNOWN_SCHEDULED','ALLOC_SCHEDULED','PLUGIN_MLE']
def now():return datetime.now(timezone.utc).isoformat()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def side(ci,x):return 'overloaded' if ci[0]>x else ('subcritical' if ci[1]<x else 'UNKNOWN')
def execute(c,cp,native=None,progress=None):
    r=dict(protocol_id=c['protocol_id'],started_at=now(),contract=c,fixtures=[],decisions=[],cells=[],anylook=[],verdict='RUNNING',validated_general_detector=False,
      independent_replication=False,numpy_version=np.__version__,scipy_version=scipy.__version__)
    if native:
        for m in c['models']:
            x=float(F(exact_capacity(F(m['p']),F(m['mu_small']),F(m['mu_big']))['throughput']))
            for seed in [8901,8902]:
                a,s,k=generate(4096,1.2*x,seed,m['p'],m['mu_small'],m['mu_big']);d=fcfs(a,s,k);mask=d<=a[-1]
                tape=checkpoint_tape(a,k,np.where(mask)[0],d[mask],float(a[-1]),c['milestones'])
                f=native(a,s,k,d,tape);f['name']=m['id']+'-'+str(seed);r['fixtures'].append(f)
                if progress:progress(r)
                if not f['passed']:raise RuntimeError('R3 native checkpoint exposure alignment')
    for m in c['models']:
        x=float(F(exact_capacity(F(m['p']),F(m['mu_small']),F(m['mu_big']))['throughput']))
        for z in c['load_factors']:
            for seed in c['seeds']:
                a,s,k=generate(max(c['horizons']),z*x,seed,m['p'],m['mu_small'],m['mu_big']);d=fcfs(a,s,k)
                for h in c['horizons']:
                    aa,kk,dd=a[:h],k[:h],d[:h];tau=float(aa[-1]);mask=dd<=tau
                    tape=checkpoint_tape(aa,kk,np.where(mask)[0],dd[mask],tau,c['milestones']);obs=tape['observed']
                    anytime=diagnose(obs,c['alpha']);checkpoint=scheduled_diagnose(tape,c['attestation'],c['horizons'],c['milestones'],c['alpha'])
                    if not checkpoint['inference_performed']:raise RuntimeError('R3 scheduled applicability/configuration')
                    known=gamma_interval(h,tau,c['alpha']/len(c['horizons']))
                    allocated=checkpoint['intervals']['arrival']
                    labels=dict(ANYTIME_RECT=anytime['label'],CHECKPOINT_RECT=checkpoint['label'],KNOWN_SCHEDULED=side(known,x),ALLOC_SCHEDULED=side(allocated,x),PLUGIN_MLE=anytime['plugin_label'])
                    values=dict(arrival=z*x,p_small=m['p'],mu_small=m['mu_small'],mu_big=m['mu_big'])
                    coverage={method:{key:ci[0]<=values[key] and (ci[1] is None or values[key]<=ci[1]) for key,ci in report['intervals'].items()} for method,report in [('ANYTIME_RECT',anytime),('CHECKPOINT_RECT',checkpoint)]}
                    for method,report in [('ANYTIME_RECT',anytime),('CHECKPOINT_RECT',checkpoint)]:
                        if all(coverage[method][key] for key in ['p_small','mu_small','mu_big']):
                            lo,hi=report['capacity_interval']
                            if not lo<=x<=hi:raise RuntimeError('R3 capacity enclosure')
                    r['decisions'].append(dict(model=m['id'],load_factor=z,seed=seed,horizon=h,truth='subcritical' if z<1 else 'overloaded',tape=tape,anytime=anytime,checkpoint=checkpoint,known_arrival_ci=known,labels=labels,parameter_coverage=coverage))
                if progress:progress(r)
            print(m['id'],z,'finished',flush=True)
    n=len(c['seeds']);family=len(c['models'])*len(c['load_factors'])*len(c['horizons'])*len(METHODS)*2;anyfamily=len(c['models'])*len(c['load_factors'])*len(METHODS)*2
    for m in c['models']:
        for z in c['load_factors']:
            rr=[v for v in r['decisions'] if (v['model'],v['load_factor'])==(m['id'],z)]
            for h in c['horizons']:
                rows=[v for v in rr if v['horizon']==h];metrics={}
                for method in METHODS:
                    e=sum(v['labels'][method] not in ('UNKNOWN',v['truth']) for v in rows);u=sum(v['labels'][method]=='UNKNOWN' for v in rows)
                    metrics[method]=dict(wrong=e,unknown=u,correct=n-e-u,wrong_ci=cp(e,n,.05/family),unknown_ci=cp(u,n,.05/family),loss={str(a):(e+a*u)/n for a in [.1,.5,.9]})
                r['cells'].append(dict(model=m['id'],load_factor=z,horizon=h,n=n,metrics=metrics,joint_noncoverage={method:sum(not all(v['parameter_coverage'][method].values()) for v in rows) for method in ['ANYTIME_RECT','CHECKPOINT_RECT']}))
            metrics={}
            for method in METHODS:
                e=sum(any(v['labels'][method] not in ('UNKNOWN',v['truth']) for v in rr if v['seed']==seed) for seed in c['seeds'])
                u=sum(all(v['labels'][method]=='UNKNOWN' for v in rr if v['seed']==seed) for seed in c['seeds'])
                metrics[method]=dict(wrong_anylook=e,unknown_alllooks=u,wrong_anylook_ci=cp(e,n,.05/anyfamily),unknown_alllooks_ci=cp(u,n,.05/anyfamily))
            r['anylook'].append(dict(model=m['id'],load_factor=z,n=n,metrics=metrics,joint_noncoverage_anylook={method:sum(any(not all(v['parameter_coverage'][method].values()) for v in rr if v['seed']==seed) for seed in c['seeds']) for method in ['ANYTIME_RECT','CHECKPOINT_RECT']}))
    def cell(mid,z,h):return next(v for v in r['cells'] if (v['model'],v['load_factor'],v['horizon'])==(mid,z,h))
    if c['horizons']==HORIZONS and c['seeds']==SEEDS:
        r['prediction_grading']=dict(S1=all(v['metrics']['CHECKPOINT_RECT']['wrong_anylook']<=2 for v in r['anylook']),
           S2=all(cell(m['id'],z,1280000)['metrics']['CHECKPOINT_RECT']['unknown']==0 for m in c['models'] for z in [.8,1.2]),
           S3=all(cell(m['id'],z,1280000)['metrics']['CHECKPOINT_RECT']['correct']>=1 for m in c['models'] for z in [.99,1.01]),
           S4=sum(cell(m['id'],z,1280000)['metrics']['CHECKPOINT_RECT']['unknown'] for m in c['models'] for z in [.99,1.01])<sum(cell(m['id'],z,1280000)['metrics']['ANYTIME_RECT']['unknown'] for m in c['models'] for z in [.99,1.01]))
    else:r['prediction_grading']='NOT_PERFORMED changed grid'
    r.update(verdict='MEASURED bounded-checkpoint-schedule',completed_at=now(),executed_workloads=len(c['models'])*len(c['load_factors'])*n,executed_decisions=len(r['decisions'])*len(METHODS))
    return r
