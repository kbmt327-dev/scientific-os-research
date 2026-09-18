"""Past-only inference for the stated two-block strict-FCFS exponential model.

Uses existing likelihood-mixture/Ville methods, not a new inference theorem.
The capacity formula is a specialization of known two-class stability theory.
No diagnostic accepts true work, future departures or population parameters.
"""
from fractions import Fraction as F
import heapq,math
import numpy as np
from scipy.optimize import brentq

NUMERIC_SLACK=1e-6

def capacity(p,small,big):
    """1/X = (1-p)/big + p(2-p)/(2 small)."""
    return 1/((1-p)/big+p*(2-p)/(2*small))

def capacity_interval(p_bounds,small_bounds,big_bounds):
    pl,ph=map(F,p_bounds);rl,rh=small_bounds;ul,uh=big_bounds
    if rl<=0 or ul<=0: lower=0.
    else:
        r,u=F(rl),F(ul);points=[pl,ph];vertex=1-r/u
        if pl<vertex<ph:points.append(vertex)
        vals=[1/((1-p)/u+p*(2-p)/(2*r)) for p in points]
        lower=math.nextafter(float(min(vals)),0.)
    if rh is None or uh is None:upper=None
    else:
        r,u=F(rh),F(uh)
        vals=[1/((1-p)/u+p*(2-p)/(2*r)) for p in [pl,ph]]
        upper=math.nextafter(float(max(vals)),math.inf)
    return [lower,upper]

def log_rate_e(theta,count,exposure):
    if theta<=0:return -math.log1p(exposure) if count==0 and theta==0 else math.inf
    return theta*exposure-count*math.log(theta)+math.lgamma(count+1)-(count+1)*math.log1p(exposure)

def rate_cs(count,exposure,error):
    """Gamma(1,rate=1) likelihood mixture; count intensity = theta * risk."""
    if count<0 or exposure<0 or not math.isfinite(exposure):raise ValueError('invalid count/exposure')
    if exposure==0:
        if count:raise ValueError('count without positive exposure')
        return [0.,None]
    cut=math.log(1/error)+NUMERIC_SLACK
    if count==0:return [0.,math.nextafter((cut+math.log1p(exposure))/exposure,math.inf)]
    mle=count/exposure
    if log_rate_e(mle,count,exposure)>=cut:raise RuntimeError('nonfinite/inconsistent rate mixture')
    lo=mle/2;hi=mle*2
    while log_rate_e(lo,count,exposure)<cut:lo/=2
    while log_rate_e(hi,count,exposure)<cut:hi*=2
    low=brentq(lambda t:log_rate_e(t,count,exposure)-cut,lo,mle,xtol=1e-13)
    high=brentq(lambda t:log_rate_e(t,count,exposure)-cut,mle,hi,xtol=1e-13)
    # Enlarge roots additionally; the declared slack makes exclusions stricter.
    return [math.nextafter(low*(1-1e-10),0.),math.nextafter(high*(1+1e-10),math.inf)]

def log_mark_e(p,small,big):
    if p<=0:return -math.log(big+1) if small==0 and p==0 else math.inf
    if p>=1:return -math.log(small+1) if big==0 and p==1 else math.inf
    return math.lgamma(small+1)+math.lgamma(big+1)-math.lgamma(small+big+2)-small*math.log(p)-big*math.log1p(-p)

def mark_cs(small,big,error):
    n=small+big
    if not n:return [0.,1.]
    cut=math.log(1/error)+NUMERIC_SLACK;mle=small/n
    lo=0. if small==0 else brentq(lambda p:log_mark_e(p,small,big)-cut,1e-15,mle,xtol=1e-13)
    hi=1. if big==0 else brentq(lambda p:log_mark_e(p,small,big)-cut,mle,1-1e-15,xtol=1e-13)
    return [max(0.,lo*(1-1e-10)),min(1.,hi+(1-hi)*1e-10)]

def past_summary(arrival,need,completed_ids,completed_times,cutoff,return_starts=False):
    """Reconstruct starts using strict FCFS and *observed* completions only.

    Unobserved completion times are represented internally as infinity, never
    read from an oracle. Jobs still queued contribute no service exposure.
    """
    a=np.asarray(arrival,dtype=float);raw_need=np.asarray(need);k=np.asarray(need,dtype=int)
    ids=np.asarray(completed_ids,dtype=int);times=np.asarray(completed_times,dtype=float)
    if len(a)!=len(k) or len(ids)!=len(times) or cutoff<0 or not math.isfinite(cutoff):raise ValueError('invalid observation shape')
    if np.any(~np.isfinite(a)) or np.any(a<0) or np.any(np.diff(a)<0) or np.any(a>cutoff) or np.any(~np.isin(raw_need,[1,2])):raise ValueError('invalid offered observations')
    if not np.array_equal(ids,np.asarray(completed_ids)):raise ValueError('completion ids must be integers')
    if len(set(ids.tolist()))!=len(ids) or np.any(ids<0) or np.any(ids>=len(a)):raise ValueError('invalid completion ids')
    if np.any(~np.isfinite(times)) or np.any(times>cutoff) or np.any(times<=a[ids]):raise ValueError('future/impossible completion rejected')
    ends=np.full(len(a),math.inf);ends[ids]=times
    starts=np.full(len(a),math.inf);running=[];busy=0;t=0.
    for i,(ai,ki) in enumerate(zip(a,k)):
        t=max(t,float(ai))
        while running and running[0][0]<=t:
            _,freed=heapq.heappop(running);busy-=freed
        while busy+int(ki)>2:
            t=running[0][0]
            if t>cutoff:break
            while running and running[0][0]<=t:
                _,freed=heapq.heappop(running);busy-=freed
        if t>cutoff:break
        if ends[i]<=t:raise ValueError('completion before reconstructed start')
        starts[i]=t;busy+=int(ki);heapq.heappush(running,(ends[i],int(ki)))
    if np.any(~np.isfinite(starts[ids])):raise ValueError('completion for unstarted job')
    exposure=np.maximum(0.,np.minimum(ends,cutoff)-np.minimum(starts,cutoff))
    ns=int(np.sum(k==1));nb=len(k)-ns
    result=dict(arrivals=len(a),elapsed=float(cutoff),offered_small=ns,offered_big=nb,
       completed_small=int(np.sum(k[ids]==1)),completed_big=int(np.sum(k[ids]==2)),
       exposure_small=float(exposure[k==1].sum()),exposure_big=float(exposure[k==2].sum()),
       started=int(np.isfinite(starts).sum()))
    return (result,starts) if return_starts else result

FIELDS={'arrivals','elapsed','offered_small','offered_big','completed_small','completed_big','exposure_small','exposure_big','started'}
def diagnose(observed,error=.05):
    if set(observed)!=FIELDS:raise ValueError('diagnostic accepts past-only sufficient statistics')
    s=observed;delta=error/4
    counts=[s[k] for k in ['arrivals','offered_small','offered_big','completed_small','completed_big','started']]
    if any(not isinstance(x,int) or x<0 for x in counts):raise ValueError('nonnegative integer counts required')
    if s['offered_small']+s['offered_big']!=s['arrivals'] or s['completed_small']>s['offered_small'] or s['completed_big']>s['offered_big'] or not s['completed_small']+s['completed_big']<=s['started']<=s['arrivals']:raise ValueError('inconsistent observation counts')
    if not s['arrivals'] or s['elapsed']<=0:return dict(label='UNKNOWN',reason='no arrival exposure')
    intervals=dict(arrival=rate_cs(s['arrivals'],s['elapsed'],delta),
      p_small=mark_cs(s['offered_small'],s['offered_big'],delta),
      mu_small=rate_cs(s['completed_small'],s['exposure_small'],delta),
      mu_big=rate_cs(s['completed_big'],s['exposure_big'],delta))
    cap=capacity_interval(intervals['p_small'],intervals['mu_small'],intervals['mu_big'])
    low,high=intervals['arrival']
    label='overloaded' if cap[1] is not None and low>cap[1] else ('subcritical' if high is not None and high<cap[0] else 'UNKNOWN')
    point=None;plugin='UNKNOWN'
    if s['completed_small'] and s['completed_big']:
        point=capacity(s['offered_small']/s['arrivals'],s['completed_small']/s['exposure_small'],s['completed_big']/s['exposure_big'])
        plugin='overloaded' if s['arrivals']/s['elapsed']>=point else 'subcritical'
    return dict(label=label,intervals=intervals,capacity_interval=cap,capacity_point=point,plugin_label=plugin,
                joint_anytime_error=error,numeric_log_slack=NUMERIC_SLACK)
