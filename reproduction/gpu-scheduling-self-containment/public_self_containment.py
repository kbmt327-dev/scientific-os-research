"""Score public claim self-containment against a predeclared lexical rubric.

This is a document-content audit, not a human comprehension study.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,re,shutil

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def score(contract,root):
    results={}; total=0; passed=0
    for lang,rel in contract["articles"].items():
        text=(root/rel).read_text(encoding="utf-8")
        rows=[]
        for item in contract["criteria"]:
            patterns=item["patterns"][lang]
            matches=[bool(re.search(p,text,re.I|re.S)) for p in patterns]
            ok=all(matches);passed+=int(ok);total+=1
            rows.append(dict(id=item["id"],name=item["name"],passed=ok,pattern_matches=matches))
        results[lang]=dict(passed=sum(x["passed"] for x in rows),total=len(rows),criteria=rows,sha256=sha(root/rel))
    return dict(scored_at=datetime.now(timezone.utc).isoformat(),languages=results,passed=passed,total=total,all_passed=passed==total,
                human_comprehension_tested=False,independent_reader_count=0)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--protocol",type=Path,required=True);ap.add_argument("--seal",type=Path,required=True);ap.add_argument("--root",type=Path,required=True);ap.add_argument("--output",type=Path,required=True);ap.add_argument("--stage",choices=["baseline","remediation"],required=True);a=ap.parse_args()
    c=json.loads(a.protocol.read_text(encoding="utf-8-sig"));s=json.loads(a.seal.read_text(encoding="utf-8-sig"))
    if sha(a.protocol)!=s["protocol_sha256"] or sha(__file__)!=s["runner_sha256"]:raise RuntimeError("sealed bytes differ")
    for lang,rel in c["articles"].items():
        if a.stage=="baseline" and sha(a.root/rel)!=c["baseline_sha256"][lang]:raise RuntimeError("baseline article changed before audit")
    a.output.mkdir(parents=True,exist_ok=True);result=score(c,a.root);result.update(protocol_id=c["protocol_id"],stage=a.stage,seal=s)
    target=a.output/(a.stage+".json");
    if target.exists():raise FileExistsError(target)
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    if a.stage=="baseline":
        snap=a.output/"baseline-snapshot";snap.mkdir()
        for lang,rel in c["articles"].items():shutil.copyfile(a.root/rel,snap/(lang+".md"))
    print(json.dumps({"stage":a.stage,"passed":result["passed"],"total":result["total"],"by_language":{k:v["passed"] for k,v in result["languages"].items()},"human_comprehension_tested":False}))
if __name__=="__main__":main()
