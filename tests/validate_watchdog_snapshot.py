import contextlib, hashlib, importlib.util, io, json, os, sys, tempfile, types
from pathlib import Path
ROOT=Path(__file__).parent
observer=types.ModuleType("watchdog.observers"); observer.Observer=object
events=types.ModuleType("watchdog.events"); events.FileSystemEventHandler=object
sys.modules.update({"watchdog":types.ModuleType("watchdog"),"watchdog.observers":observer,"watchdog.events":events})
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
def run(label,root):
 scoring=load("ScoringGear",root/"Engine/ScoringGear.py");watch=load("observed_watchdog_"+label,root/"Engine/Watchdog.py");git=load("observed_git_"+label,root/"Engine/GitGear.py")
 results=[]
 def check(name,fn):
  try:fn();results.append({"name":name,"passed":True})
  except Exception as e:results.append({"name":name,"passed":False,"error":type(e).__name__+": "+str(e)})
 with tempfile.TemporaryDirectory() as tmp:
  td=Path(tmp); handler=watch.EngineEventHandler(str(td));file=td/"node.json"
  def event(data):
   file.write_text(json.dumps(data));out=io.StringIO()
   with contextlib.redirect_stdout(out):handler.on_created(types.SimpleNamespace(is_directory=False,src_path=str(file)))
   lines=out.getvalue().strip().splitlines()
   return json.loads(lines[-1]) if lines and lines[-1].startswith("{") else lines
  def high():
   p=event({"display_name":"synthetic","capabilities":{"client_volume":"High"},"execution_fit":{"match_score":100}})
   assert p["execution_performed"] is False and p["approval_state"]=="awaiting_human_review"
   assert len(list(td.iterdir()))==1
  check("high_score_proposes_without_side_effects",high)
  def low():
   p=event({});assert p["suggested_operation"] is None and p["execution_performed"] is False
  check("low_score_no_execution",low)
  def invalid():
   event([]) # event handling must contain malformed root payloads
  check("non_object_payload_does_not_escape_handler",invalid)
  def nested():
   event({"capabilities":[]})
  check("invalid_nested_payload_does_not_escape_handler",nested)
  def outside():
   with tempfile.TemporaryDirectory() as other:
    p=Path(other)/"outside.json";p.write_text("{}");out=io.StringIO()
    with contextlib.redirect_stdout(out):handler.on_created(types.SimpleNamespace(is_directory=False,src_path=str(p)))
    assert "outside" in out.getvalue()
  check("outside_root_ignored",outside)
  def refuse():
   try:git.GitGear().chronicle("synthetic")
   except PermissionError:return
   raise AssertionError("legacy Git operation was not refused")
  check("git_chronicle_fails_closed",refuse)
  def race():
   original=watch.ScoringGear
   class Racing(original):
    def __init__(self,path):
     Path(path).write_text(json.dumps({"execution_fit":{"match_score":100},"capabilities":{"client_volume":"High"}}))
     super().__init__(path)
   watch.ScoringGear=Racing
   try:
    p=event({});assert p["score"]==60,"scored a changed file instead of the hashed snapshot"
   finally:watch.ScoringGear=original
  check("scored_payload_matches_hashed_snapshot_under_race",race)
 return {"label":label,"results":results,"passed":sum(r["passed"] for r in results),"failed":sum(not r["passed"] for r in results)}
if __name__=="__main__":
 root=Path(sys.argv[1]);label=sys.argv[2] if len(sys.argv)>2 else "run"
 report=run(label,root);print(json.dumps(report,indent=2));sys.exit(bool(report["failed"]))

