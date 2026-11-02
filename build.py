#!/usr/bin/env python3
import html,json,pathlib,shutil
R=pathlib.Path(__file__).parent
D=R/"dist"
HOME="https://home.geraldsomehow.workers.dev/"
def e(v):return html.escape(str(v),quote=True)
def shell(title,body):
 return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} · Gerald's Doors</title><link rel="stylesheet" href="/styles.css"></head><body><header><a class="brand" href="/">GERALD <span>/ DOORS</span></a><nav aria-label="Site navigation"><a href="{HOME}">Gerald Home</a><a href="/" aria-current="page">Gerald’s Doors</a><a href="{HOME}about/">About</a></nav></header>{body}<footer><span>GERALD. BECAUSE CAT.</span><a href="/">Gerald's Doors</a><span>A Studio MidKnight production.</span></footer></body></html>"""
data=json.loads((R/"chapters.json").read_text())
if D.exists():shutil.rmtree(D)
D.mkdir()
shutil.copy2(R/"styles.css",D/"styles.css")
(D/"assets").mkdir()
shutil.copy2(R/"assets/doors-header.webp",D/"assets/doors-header.webp")
cards=[]
for ch in data["chapters"]:
 slug=ch["slug"];pages=ch["pages"];title=ch["title"];cover=ch["cover"]
 if not slug or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in slug) or not pages:raise ValueError("Invalid chapter")
 if cover!=pages[0]:raise ValueError("First reader image must be the cover")
 for path in set([cover]+pages):
  src=R/path
  if src.is_absolute() or ".." in pathlib.PurePosixPath(path).parts or not src.is_file():raise ValueError("Invalid image path "+path)
  dest=D/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
 cards.append(f'<a class="card" href="/chapters/{e(slug)}/1/"><img src="/{e(cover)}" alt="{e(title)} cover"><strong>{e(title)}</strong></a>')
 for position,img in enumerate(pages,1):
  is_cover=position==1
  label="Cover" if is_cover else f"Page {position-1} of {len(pages)-1}"
  prev=f"/chapters/{slug}/{position-1}/" if position>1 else "/"
  nxt=f"/chapters/{slug}/{position+1}/" if position<len(pages) else "/"
  next_label="Next page →" if position<len(pages) else "Back to Gerald's Doors →"
  alt=f"{title}, cover" if is_cover else f"{title}, page {position-1}"
  body=f'<main class="reader"><p><a href="/">← All chapters</a> · {e(title)} · {e(label)}</p><img src="/{e(img)}" alt="{e(alt)}"><div class="paging"><a href="{prev}">← Previous</a><a href="{nxt}">{next_label}</a></div></main>'
  target=D/"chapters"/slug/str(position);target.mkdir(parents=True,exist_ok=True);(target/"index.html").write_text(shell(title,body))
gallery="".join(cards) or '<p class="empty">Chapter previews will appear here when the first installment is ready.</p>'
body=f'<main><section class="hero"><img src="/assets/doors-header.webp" alt="Gerald’s Doors illustrated header"><div class="intro"><p class="eyebrow">A Gerald miniseries</p><h1>Gerald’s Doors</h1><p>Every door leads somewhere. Gerald has a habit of finding the wrong one.</p></div></section><section class="collection"><p class="eyebrow">Choose a door</p><h2>Chapters</h2><p>Select a title page to begin reading.</p><div class="gallery">{gallery}</div></section></main>'
(D/"index.html").write_text(shell("Home",body))
print("Built",len(data["chapters"]),"chapters")
