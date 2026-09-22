from __future__ import annotations
import argparse, json, sys
from dataclasses import asdict
from .core import build_index, find_symbols, search_text, context

VERSION = "1.0.0"

def parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser(prog="codebase-nav", description="Local-first codebase navigation and structural search")
    p.add_argument("--version", action="version", version=f"%(prog)s {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    p.add_argument("--root", default=".")
    p.add_argument("--json", action="store_true")
    sub=p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("summary")
    s=sub.add_parser("symbols"); s.add_argument("query", nargs="?", default=""); s.add_argument("--kind")
    t=sub.add_parser("search"); t.add_argument("query"); t.add_argument("--regex", action="store_true"); t.add_argument("--glob", default="*")
    c=sub.add_parser("context"); c.add_argument("path"); c.add_argument("line", type=int); c.add_argument("--radius", type=int, default=3)
    return p

def main(argv=None) -> int:
    args=parser().parse_args(argv)
    try:
        idx=build_index(args.root)
        if args.cmd=="summary": result=idx.summary()
        elif args.cmd=="symbols": result=[asdict(x) for x in find_symbols(idx,args.query,kind=args.kind)]
        elif args.cmd=="search": result=[asdict(x) for x in search_text(idx,args.query,regex=args.regex,glob=args.glob)]
        else: result=[{"line":n,"text":text} for n,text in context(idx,args.path,args.line,args.radius)]
        if args.json: print(json.dumps(result, ensure_ascii=False, indent=2))
        elif isinstance(result,dict):
            for k,v in result.items(): print(f"{k}: {v}")
        else:
            for item in result:
                if "kind" in item: print(f"{item['path']}:{item['line']}  {item['kind']} {item['signature']}")
                elif "path" in item: print(f"{item['path']}:{item['line']}  {item['text']}")
                else: print(f"{item['line']:>5} | {item['text']}")
        return 0
    except (ValueError,RuntimeError,re.error) as exc:
        print(f"error: {exc}",file=sys.stderr); return 2

if __name__=="__main__": raise SystemExit(main())
