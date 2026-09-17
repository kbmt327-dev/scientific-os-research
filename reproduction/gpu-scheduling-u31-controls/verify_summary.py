"""Audit projected sufficient-statistic arithmetic, F quantiles and stop branches only."""
import json
import math
from pathlib import Path
from scipy.stats import f
HERE=Path(__file__).resolve().parent
a=json.loads((HERE/'results/ep-0018-summary.json').read_text(encoding='utf-8'))
b=json.loads((HERE/'results/ep-0019-summary.json').read_text(encoding='utf-8'))
for data in (a,b):
    assert data['claim_status']=='UNKNOWN' and data['independent_replications']==0
    assert not data['raw_job_traces_included'] and not data['simulation_source_included']
assert [c['rho'] for c in a['cells']]==[.4,1.2,.95,1.05]
assert a['executed_oracle_workloads']==36 and a['engine_fixture_runs']==4
threshold=(a['cells'][0]['queue_score']+a['cells'][1]['queue_score'])/2
assert math.isclose(threshold,a['calibrated_queue_threshold'],abs_tol=1e-12)
for c in a['cells']:
    assert (c['alpha']>=a['alpha_line'])==(c['truth']=='overloaded')
assert a['cells'][2]['queue_score']<threshold and a['cells'][3]['queue_score']<threshold
assert a['verdict']=='R2 known-control-disagreement' and a['stop_at_rho']==1.05
assert a['unexecuted_holdout_rhos']==[.99,1.01]
assert b['family_error']==.05 and b['max_comparisons']==40
assert [c['rho'] for c in b['cells']]==[.97,1.03,.99,1.01,.995,1.005]
assert set(b['calibration_seeds']).isdisjoint(b['holdout_seeds'])
count=0
for c in b['cells']:
    for i,look in enumerate(c['looks']):
        assert look['horizon']==b['horizons'][i]
        assert look['input_count']==3*look['horizon']
        error=b['family_error']/b['max_comparisons']
        assert look['comparison_error']==error
        n=look['input_count']
        qlow,qhigh=f.ppf([error/2,1-error/2],2*n,2*n)
        assert math.isclose(qlow,look['quantile_low'],rel_tol=1e-7)
        assert math.isclose(qhigh,look['quantile_high'],rel_tol=1e-7)
        estimate=look['input_work']/look['input_time']
        low,high=estimate/qhigh,estimate/qlow
        for got,want in [(estimate,look['load_estimate']),(low,look['load_ci_low']),(high,look['load_ci_high']),
                         (estimate-1,look['net_input_drift_estimate']),(low-1,look['net_input_drift_ci_low']),(high-1,look['net_input_drift_ci_high'])]:
            assert math.isclose(got,want,rel_tol=1e-7,abs_tol=1e-7)
        label='overloaded' if low>1 else ('subcritical' if high<1 else 'UNKNOWN')
        assert label==look['label']
        if i<len(c['looks'])-1: assert label=='UNKNOWN'
        elif c['status']=='resolved': assert label==c['truth']
        count+=1
assert count==b['executed_comparisons']==17 and 3*count==b['executed_workloads']==51
last=b['cells'][-1]['looks'][-1]
assert last['label']=='UNKNOWN' and last['horizon']==320000 and last['load_ci_low']<=1<=last['load_ci_high']
assert b['verdict']=='R3 finite-window-unresolved' and b['stop_at_rho']==1.005
assert b['unexecuted_holdout_rhos']==[.999,1.001]
print('EP-0018/0019 public summaries: CI arithmetic and stop branches OK; simulation not reproduced')
