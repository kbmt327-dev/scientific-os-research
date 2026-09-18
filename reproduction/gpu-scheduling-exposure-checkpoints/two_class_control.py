"""Exact five-state saturated control and causal two-class gang FCFS oracle.

Known two-class stability theorem supplies the label; this module's matrix is a
small-instance construction, not a new theorem or an empirical saturation fit.
"""
from fractions import Fraction as F
import heapq
import numpy as np

STATES = [(0,1,1),(0,1,2),(1,0,2),(2,0,1),(2,0,2)]

def solve_stationary(matrix, generator=True):
    n=len(matrix)
    a=[[matrix[j][i]-(F(int(i==j)) if not generator else 0) for j in range(n)]+[F(0)] for i in range(n-1)]
    a.append([F(1)]*n+[F(1)])
    for col in range(n):
        pivot=next(i for i in range(col,n) if a[i][col])
        a[col],a[pivot]=a[pivot],a[col]
        v=a[col][col];a[col]=[x/v for x in a[col]]
        for i in range(n):
            if i!=col:
                v=a[i][col];a[i]=[x-v*y for x,y in zip(a[i],a[col])]
    return [row[-1] for row in a]

def exact_capacity(p_small=F(1,2),mu_small=F(1),mu_big=F(1,2)):
    if not 0<p_small<1 or min(mu_small,mu_big)<=0:
        raise ValueError('require two positive class probabilities/rates')
    p_small,mu_small,mu_big=map(F,(p_small,mu_small,mu_big))
    def refill(a,b,head,weight,out):
        if a+2*b+head>2:
            state=(a,b,head);out[state]=out.get(state,F(0))+weight;return
        if head==1: a+=1
        else: b+=1
        refill(a,b,1,weight*p_small,out)
        refill(a,b,2,weight*(1-p_small),out)
    q=[[F(0) for _ in STATES] for _ in STATES]
    embedded=[[F(0) for _ in STATES] for _ in STATES]
    rates=[a*mu_small+b*mu_big for a,b,_ in STATES]
    for i,(a,b,head) in enumerate(STATES):
        for aa,bb,rate in [(a-1,b,a*mu_small),(a,b-1,b*mu_big)]:
            if not rate: continue
            out={};refill(aa,bb,head,F(1),out)
            assert sum(out.values())==1
            for state,prob in out.items():
                j=STATES.index(state);q[i][j]+=rate*prob
                embedded[i][j]+=rate*prob/rates[i]
        q[i][i]-=rates[i]
    pi=solve_stationary(q)
    eta=solve_stationary(embedded,generator=False)
    time_weights=[eta[i]/rates[i] for i in range(len(STATES))]
    time_pi=[x/sum(time_weights) for x in time_weights]
    assert pi==time_pi and min(pi)>=0 and sum(pi)==1
    assert all(sum(pi[i]*q[i][j] for i in range(len(STATES)))==0 for j in range(len(STATES)))
    x=sum(pi[i]*rates[i] for i in range(len(STATES)))
    expected_work=p_small/mu_small+2*(1-p_small)/mu_big
    wastage=sum(pi[i]*(2-STATES[i][0]-2*STATES[i][1]) for i in range(len(STATES)))
    assert x*expected_work==2-wastage
    return dict(states=[list(state) for state in STATES],generator=[[str(x) for x in row] for row in q],
                embedded=[[str(x) for x in row] for row in embedded],
                stationary=[str(x) for x in pi],embedded_stationary=[str(x) for x in eta],
                departure_rates=[str(x) for x in rates],throughput=str(x),
                mean_server_work=str(expected_work),wastage=str(wastage),nominal_load_at_boundary=str(x*expected_work/2))

def fcfs(arrival,size,need,capacity=2):
    """Start in arrival order, wait for enough free resources, then draw no data."""
    running=[];busy=0;t=0.;dep=np.empty(len(arrival))
    for i,(a,s,k) in enumerate(zip(arrival,size,need)):
        if k<1 or k>capacity: raise ValueError('infeasible need')
        t=max(t,float(a))
        while running and running[0][0]<=t:
            _,freed=heapq.heappop(running);busy-=freed
        while busy+int(k)>capacity:
            t=running[0][0]
            while running and running[0][0]<=t:
                _,freed=heapq.heappop(running);busy-=freed
        dep[i]=t+float(s);busy+=int(k)
        heapq.heappush(running,(dep[i],int(k)))
    return dep

def generate(n,lam,seed,p_small=.5,mu_small=1.,mu_big=.5):
    # Distinct streams isolate arrivals, class marks and service draws.
    streams=[np.random.default_rng(x) for x in np.random.SeedSequence(seed).spawn(3)]
    a=np.cumsum(streams[0].exponential(1/lam,n))
    need=np.where(streams[1].random(n)<p_small,1,2)
    size=streams[2].exponential(1.,n)/np.where(need==1,mu_small,mu_big)
    return a,size,need
