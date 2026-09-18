"""Portability checks only; labels/counts exact, continuous values rel1e-9/abs1e-10."""
import math
MAX_RELATIVE_NUMERIC_DIFFERENCE=0.
MAX_ABSOLUTE_NUMERIC_DIFFERENCE=0.
def assert_equivalent(a,b,path='root'):
    global MAX_RELATIVE_NUMERIC_DIFFERENCE,MAX_ABSOLUTE_NUMERIC_DIFFERENCE
    if isinstance(a,dict):
        assert isinstance(b,dict) and set(a)==set(b),path
        for key in a:assert_equivalent(a[key],b[key],path+'.'+key)
    elif isinstance(a,(list,tuple)):
        assert isinstance(b,(list,tuple)) and len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)):assert_equivalent(x,y,path+'.'+str(i))
    elif isinstance(a,float):
        assert isinstance(b,(int,float)) and math.isfinite(a) and math.isfinite(b),path
        delta=abs(a-b);relative=delta/max(abs(a),abs(b),1e-300)
        MAX_RELATIVE_NUMERIC_DIFFERENCE=max(MAX_RELATIVE_NUMERIC_DIFFERENCE,relative)
        MAX_ABSOLUTE_NUMERIC_DIFFERENCE=max(MAX_ABSOLUTE_NUMERIC_DIFFERENCE,delta)
        assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-10),(path,a,b,delta)
    else:
        # labels, integer counts, booleans and null remain exact.
        assert a==b,(path,a,b)
