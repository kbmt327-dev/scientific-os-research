"""Predeclared reporting looks and completion checkpoints, known structure only.

Uses the existing random-time-change theorem, gamma/chi-square pivots and
Bonferroni. This is neither new inference theory nor an anytime confidence set.
Applicability declarations are checked, not empirically proved by this module.
"""
import math
import numpy as np
from scipy.stats import chi2,beta
from observation_capacity import past_summary,FIELDS,capacity_interval

ATTESTATION=dict(resources=64,needs=[32,64],policy='strict_nonpreemptive_fcfs',resources_fungible=True,
 arrivals='iid_marked_poisson',service='independent_class_iid_exponential',size_lookahead=False,
 locality=False,overhead=False,initial_state='empty',arrival_log='complete_through_cutoff',
 completion_log='complete_through_cutoff',provenance='sealed_synthetic_generator_contract')
MILESTONES=[2**j for j in range(8,21)]
HORIZONS=[20000,320000,1280000]

def applicability(attestation):
    if not isinstance(attestation,dict) or set(attestation)!=set(ATTESTATION):
        return dict(applicable=False,reason='model_or_log_declarations_missing_or_extra')
    if any(type(attestation[k]) is not type(v) or attestation[k]!=v for k,v in ATTESTATION.items()):
        return dict(applicable=False,reason='model_or_log_declarations_unconfirmed_or_outside_scope')
    return dict(applicable=True,reason='synthetic_contract_matches; declarations_are_not_a_model_fit_test')

def checkpoint_tape(arrival,need,completed_ids,completed_times,cutoff,milestones=MILESTONES):
    obs,starts=past_summary(arrival,need,completed_ids,completed_times,cutoff,True)
    a=np.asarray(arrival,dtype=float);k=np.asarray(need,dtype=int)
    ids=np.asarray(completed_ids,dtype=int);times=np.asarray(completed_times,dtype=float)
    ends=np.full(len(a),math.inf);ends[ids]=times
    checkpoints={}
    if not milestones or len(set(milestones))!=len(milestones) or any(not isinstance(x,int) or x<1 for x in milestones):raise ValueError('positive distinct fixed milestones required')
    for cls,name in [(1,'small'),(2,'big')]:
        events=np.sort(times[k[ids]==cls])
        if np.any(np.diff(events)<=0):raise ValueError('simultaneous same-class completions outside simple-process contract')
        class_starts=starts[k==cls];class_ends=ends[k==cls];records=[]
        for count in sorted(milestones):
            if count>len(events):continue
            at=float(events[count-1]);n_started=int(np.searchsorted(class_starts,at,side='right'))
            # Direct differences avoid subtracting O(n * absolute-clock) sums.
            exposure=float(np.maximum(0,np.minimum(class_ends[:n_started],at)-class_starts[:n_started]).sum())
            if not math.isfinite(exposure) or exposure<=0:raise RuntimeError('nonfinite checkpoint exposure')
            records.append(dict(count=count,at=at,exposure=exposure,started=n_started))
        checkpoints[name]=records
    return dict(observed=obs,checkpoints=checkpoints,cutoff_is_arrival_index=bool(len(a) and cutoff==float(a[-1])))

def gamma_interval(count,exposure,error):
    if not isinstance(count,int) or count<=0 or exposure<=0 or not math.isfinite(exposure) or not 0<error<1:raise ValueError('positive fixed count/exposure and valid error required')
    values=chi2.ppf([error/2,1-error/2],2*count)/(2*exposure)
    return [math.nextafter(float(values[0]),0.),math.nextafter(float(values[1]),math.inf)]

def binomial_interval(small,big,error):
    n=small+big
    return [0. if small==0 else math.nextafter(float(beta.ppf(error/2,small,big+1)),0.),
      1. if big==0 else min(1.,math.nextafter(float(beta.ppf(1-error/2,small+1,big)),math.inf))]

def scheduled_diagnose(tape,attestation,horizons=HORIZONS,milestones=MILESTONES,error=.05):
    gate=applicability(attestation)
    if not gate['applicable']:return dict(label='UNKNOWN',gate=gate,reason='applicability_unconfirmed',inference_performed=False)
    if set(tape)!= {'observed','checkpoints','cutoff_is_arrival_index'} or set(tape['observed'])!=FIELDS or set(tape['checkpoints'])!={'small','big'}:raise ValueError('past-only tape schema required')
    obs=tape['observed'];h=obs['arrivals']
    if h not in horizons or not tape['cutoff_is_arrival_index']:
        return dict(label='UNKNOWN',gate=gate,reason='not_a_predeclared_arrival_look',inference_performed=False)
    if obs['offered_small']+obs['offered_big']!=h:raise ValueError('inconsistent offered counts')
    for name in ['small','big']:
        records=tape['checkpoints'][name];counts=[r['count'] for r in records]
        if counts!=sorted(set(counts)):raise ValueError('checkpoint counts must increase')
        if counts!=[v for v in sorted(milestones) if v<=obs['completed_'+name]]:raise ValueError('attained fixed checkpoints required')
        for record in records:
            if set(record)!= {'count','at','exposure','started'} or not 0<record['at']<=obs['elapsed'] or record['exposure']<=0:raise ValueError('future/invalid checkpoint rejected')
    arrival_error=error/(4*len(horizons));service_error=error/(4*len(milestones))
    intervals=dict(arrival=gamma_interval(h,obs['elapsed'],arrival_error),p_small=binomial_interval(obs['offered_small'],obs['offered_big'],arrival_error))
    chosen={}
    for name in ['small','big']:
        records=tape['checkpoints'][name];record=records[-1] if records else None;chosen[name]=record
        intervals['mu_'+name]=gamma_interval(record['count'],record['exposure'],service_error) if record else [0.,None]
    cap=capacity_interval(intervals['p_small'],intervals['mu_small'],intervals['mu_big']);lo,hi=intervals['arrival']
    label='overloaded' if cap[1] is not None and lo>cap[1] else ('subcritical' if hi<cap[0] else 'UNKNOWN')
    return dict(label=label,intervals=intervals,capacity_interval=cap,selected_checkpoints=chosen,gate=gate,
       inference_performed=True,joint_scheduled_error=error,arrival_mark_error_per_look=arrival_error,service_error_per_checkpoint=service_error,anytime=False)
