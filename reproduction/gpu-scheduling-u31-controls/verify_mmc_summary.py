"""Verify public M/M/4 sufficient-statistic arithmetic; no simulator execution."""
import json
import math
from pathlib import Path
from scipy.stats import f
d=json.loads((Path(__file__).resolve().parent/'results/ep-0020-summary.json').read_text(encoding='utf-8'))
assert d['n_servers']==64 and d['need']==16 and d['slots']==4
assert d['claim_status']=='UNKNOWN' and not d['validated_general_detector']
assert d['independent_replications']==0 and not d['simulation_source_included'] and not d['raw_job_traces_included']
assert d['family_error']==.05 and d['max_comparisons']==24
assert d['horizons']==[20000,40000,80000,160000]
assert [c['rho'] for c in d['cells']]==[.8,1.2,.95,1.05,.99,1.01]
assert set(d['calibration_seeds']).isdisjoint(d['holdout_seeds'])
assert len(d['engine_fixtures'])==4 and all(v['passed'] and v['departure_max_abs_error']<=1e-7 and v['mean_jct_abs_error']<=1e-7 for v in d['engine_fixtures'])
count=0
for c in d['cells']:
    assert c['role']==('calibration' if c['rho'] in d['calibration_rhos'] else 'holdout')
    assert c['truth']==('subcritical' if c['rho']<1 else 'overloaded')
    assert c['status']=='resolved' and c['label']==c['truth']
    assert [v['horizon'] for v in c['looks']]==d['horizons'][:len(c['looks'])]
    for i,v in enumerate(c['looks']):
        n=v['input_count']; error=.05/24
        assert n==3*v['horizon'] and v['comparison_error']==error
        ql,qh=f.ppf([error/2,1-error/2],2*n,2*n)
        estimate=v['input_work']/(4*v['input_time']); lo=estimate/qh; hi=estimate/ql
        for k,value in [('load_estimate',estimate),('ci_low',lo),('ci_high',hi),('quantile_low',ql),('quantile_high',qh)]:
            assert math.isclose(v[k],value,rel_tol=1e-7,abs_tol=1e-7)
        label='overloaded' if lo>1 else ('subcritical' if hi<1 else 'UNKNOWN')
        assert v['label']==label
        if i<len(c['looks'])-1: assert label=='UNKNOWN'
        else: assert label==c['truth'] and c['resolved_horizon']==v['horizon']
        count+=1
assert count==d['executed_comparisons']==10 and 3*count==d['executed_workloads']==30
assert d['verdict']=='PASS bounded-transfer' and d['bounded_transfer_status']=='PASS'
assert d['recovery']['controls_previously_observed'] and not d['recovery']['initial_holdouts_executed']
assert d['recovery']['grid_and_error_budget_unchanged']
print('EP-0020: M/M/4 CI arithmetic and stopping OK; simulation not reproduced')
