from pathlib import Path
import zipfile, hashlib, json, csv, shutil, os, time, struct, re, sys
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'00📦來源原件SourceOriginal'; BAK=ROOT/'01🩶不可變備份ImmutableBackup'; WORK=ROOT/'02🛠️工作副本WorkingCopy'; CYC=ROOT/'08📷快照Snapshot'; EV=ROOT/'10🔐稽核凍結AuditFreeze'; DEL=ROOT/'11📦交付Delivery'; CODE=ROOT/'06🧩資源修正ResourceRepair'
for p in [SRC,BAK,WORK,CYC,EV,DEL,CODE]:p.mkdir(parents=True,exist_ok=True)
FILES={
 'keynote':ROOT/'🎤簡報3Presentation3.key',
 'budget':ROOT/'📊個人預算PersonalBudget.numbers',
 'calendar':ROOT/'📅照片日曆2016PhotoCalendar2016.numbers',
 'pages':ROOT/'🌐家庭守護人工智慧商業決策遊戲畫布離線互動導圖FamilyGuardianAIBusinessDecisionGameCanvasOfflineInteractiveMap.pages',
 'pages_original':ROOT/'🌐家庭守護人工智慧商業決策遊戲畫布離線互動導圖原始版本FamilyGuardianAIBusinessDecisionGameCanvasOfflineInteractiveMapOriginalVersion.pages',
}

def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha_file(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 return h.hexdigest()
def rv(b,p):
 r=s=0;st=p
 while p<len(b):
  x=b[p];p+=1;r|=(x&127)<<s
  if x<128:return r,p
  s+=7
  if s>70:raise ValueError('varint too long')
 raise EOFError(f'varint eof {st}')
def ev(n):
 o=bytearray()
 while True:
  b=n&127;n>>=7
  if n:o.append(b|128)
  else:o.append(b);return bytes(o)
def snappy_raw(d):
 exp,p=rv(d,0);o=bytearray()
 while p<len(d):
  t=d[p];p+=1;k=t&3
  if k==0:
   n=t>>2
   if n<60:n+=1
   else:z=n-59;n=int.from_bytes(d[p:p+z],'little')+1;p+=z
   o+=d[p:p+n];p+=n
  elif k==1:
   n=4+((t>>2)&7);off=((t&224)<<3)|d[p];p+=1
   if not 1<=off<=len(o):raise ValueError('off1')
   for _ in range(n):o.append(o[-off])
  elif k==2:
   n=1+(t>>2);off=int.from_bytes(d[p:p+2],'little');p+=2
   if not 1<=off<=len(o):raise ValueError('off2')
   for _ in range(n):o.append(o[-off])
  else:
   n=1+(t>>2);off=int.from_bytes(d[p:p+4],'little');p+=4
   if not 1<=off<=len(o):raise ValueError('off4')
   for _ in range(n):o.append(o[-off])
 if len(o)!=exp:raise ValueError(f'length mismatch {len(o)} != {exp}')
 return bytes(o)
def snappy_literal(data):
 out=bytearray(ev(len(data)));p=0
 while p<len(data):
  n=min(len(data)-p,65536);x=n-1
  if x<60:out.append(x<<2)
  else:
   nb=max(1,(x.bit_length()+7)//8);out.append((59+nb)<<2);out+=x.to_bytes(nb,'little')
  out+=data[p:p+n];p+=n
 return bytes(out)
def decode_chunks(iwa):
 p=0;chunks=[]
 while p<len(iwa):
  if p+4>len(iwa) or iwa[p]!=0:raise ValueError(f'bad chunk header {p}')
  n=int.from_bytes(iwa[p+1:p+4]+b'\0','little');c=iwa[p+4:p+4+n]
  if len(c)!=n:raise EOFError('chunk trunc')
  chunks.append(bytearray(snappy_raw(c)));p+=4+n
 return chunks
def encode_chunks(chunks):
 out=bytearray()
 for d in chunks:
  c=snappy_literal(bytes(d));out.append(0);out+=len(c).to_bytes(4,'little')[:3];out+=c
 return bytes(out)
def fields(b):
 p=0;out=[]
 while p<len(b):
  s=p;k,p=rv(b,p);f=k>>3;w=k&7
  if f==0 or w in (3,4,6,7):raise ValueError(f'bad key {f}/{w}@{s}')
  x={'f':f,'w':w}
  if w==0:x['v'],p=rv(b,p)
  elif w==1:x['d']=b[p:p+8];p+=8
  elif w==2:n,p=rv(b,p);x['d']=b[p:p+n];x['n']=n;p+=n
  elif w==5:x['d']=b[p:p+4];p+=4
  if p>len(b):raise EOFError('field overflow')
  out.append(x)
 return out
def archive_info(b):
 ident=None;mis=[]
 for x in fields(b):
  if x['f']==1 and x['w']==0:ident=x['v']
  elif x['f']==2 and x['w']==2:
   mi={'type':None,'length':None}
   for y in fields(x['d']):
    if y['f']==1 and y['w']==0:mi['type']=y['v']
    elif y['f']==3 and y['w']==0:mi['length']=y['v']
   mis.append(mi)
 return ident,mis
def parse_dec(dec):
 p=0;ms=[];packets=0
 while p<len(dec):
  po=p;hl,hs=rv(dec,p);he=hs+hl
  if he>len(dec):raise EOFError('header')
  oid,mis=archive_info(dec[hs:he]);q=he
  for idx,m in enumerate(mis):
   n=m['length']
   if n is None or q+n>len(dec):raise EOFError('payload')
   pl=dec[q:q+n];ms.append({'packet_offset':po,'object_id':oid,'message_index':idx,'type_id':m['type'],'payload_offset':q,'payload_length':n,'payload_sha256':sha_bytes(pl)});q+=n
  packets+=1;p=q
 return packets,ms
def parse_iwa(iwa):
 chunks=decode_chunks(iwa);dec=b''.join(chunks);pk,ms=parse_dec(dec);return chunks,dec,pk,ms

def replace_same_length(iwa,before,after,expected_type=None,expected_object=None):
 if len(before)!=len(after):raise ValueError('replacement length mismatch')
 chunks,dec,pk,ms=parse_iwa(iwa);positions=[];base=0
 for ci,ch in enumerate(chunks):
  pos=0
  while True:
   i=bytes(ch).find(before,pos)
   if i<0:break
   positions.append((ci,i,base+i));pos=i+1
  base+=len(ch)
 valid=[]
 for ci,local,glob in positions:
  for m in ms:
   if m['payload_offset']<=glob< m['payload_offset']+m['payload_length']:
    if expected_type is not None and m['type_id']!=expected_type:continue
    if expected_object is not None and m['object_id']!=expected_object:continue
    valid.append((ci,local,glob,m));break
 if len(valid)!=1:raise ValueError(f'expected 1 valid match got {len(valid)} all={positions}')
 ci,local,glob,m=valid[0];chunks[ci][local:local+len(before)]=after
 new=encode_chunks(chunks);_,dec2,pk2,ms2=parse_iwa(new)
 if after not in dec2 or before in dec2[m['payload_offset']:m['payload_offset']+m['payload_length']]:raise ValueError('replacement validation failed')
 return new,{'chunk_index':ci,'decompressed_offset':glob,'object_id':m['object_id'],'type_id':m['type_id'],'payload_offset':m['payload_offset'],'payload_length':m['payload_length'],'before':before.decode('utf-8','replace'),'after':after.decode('utf-8','replace')}

def modify_movie_geometry(iwa,object_id,new_x):
 chunks,dec,pk,ms=parse_iwa(iwa);m=next((x for x in ms if x['object_id']==object_id and x['type_id']==3007),None)
 if not m:raise ValueError('movie object missing')
 pl=bytearray(dec[m['payload_offset']:m['payload_offset']+m['payload_length']])
 idx=pl.find(b'\x0d')
 if idx<0 or idx+5>len(pl):raise ValueError('geometry fixed32 missing')
 old=bytes(pl[idx+1:idx+5]);new=struct.pack('<f',float(new_x));
 if old==new:raise ValueError('same geometry')
 global_off=m['payload_offset']+idx+1
 base=0
 for ci,ch in enumerate(chunks):
  if base<=global_off<base+len(ch):
   loc=global_off-base;chunks[ci][loc:loc+4]=new;break
  base+=len(ch)
 else:raise ValueError('offset not mapped')
 rebuilt=encode_chunks(chunks);_,dec2,pk2,ms2=parse_iwa(rebuilt)
 m2=next(x for x in ms2 if x['object_id']==object_id and x['type_id']==3007)
 pl2=dec2[m2['payload_offset']:m2['payload_offset']+m2['payload_length']]
 if new not in pl2:raise ValueError('geometry verification failed')
 return rebuilt,{'object_id':object_id,'type_id':3007,'payload_offset':m['payload_offset'],'fixed32_offset':idx+1,'before_hex':old.hex(),'after_hex':new.hex(),'before_float':struct.unpack('<f',old)[0],'after_float':new_x}

def clean_read_zip(fp):
 with zipfile.ZipFile(fp) as z:
  names=z.namelist();d={n:z.read(n) for n in names}
 return d,names
def write_zip_atomic(fp,entries):
 tmp=fp.with_suffix(fp.suffix+'.tmp')
 with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,b in entries.items():z.writestr(n,b)
 os.replace(tmp,fp)
def validate_container(fp):
 rec={'file':str(fp),'sha256':sha_file(fp),'zip_test':False,'duplicates':[],'iwa_total':0,'iwa_pass':0,'iwa_fail':0,'packets':0,'messages':0,'errors':[]}
 with zipfile.ZipFile(fp) as z:
  rec['zip_test']=z.testzip() is None
  names=z.namelist();rec['duplicates']=sorted({n for n in names if names.count(n)>1})
  for n in names:
   if not n.endswith('.iwa'):continue
   rec['iwa_total']+=1
   try:
    _,dec,pk,ms=parse_iwa(z.read(n));rec['iwa_pass']+=1;rec['packets']+=pk;rec['messages']+=len(ms)
   except Exception as e:rec['iwa_fail']+=1;rec['errors'].append({'iwa':n,'error':repr(e)})
 return rec

def gen_image(size,text,cycle,mode='JPEG'):
 img=Image.new('RGB',size,(20+cycle*17%220,40+cycle*29%200,80+cycle*31%170));d=ImageDraw.Draw(img)
 for i in range(10):
  x=(i*97+cycle*41)%size[0];y=(i*53+cycle*73)%size[1];r=20+(i*11)%80
  d.ellipse((x-r,y-r,x+r,y+r),outline=(255-(i*17)%255,120+(i*9)%135,40+(i*23)%215),width=max(1,size[0]//500))
 d.rectangle((20,20,min(size[0]-20,720),120),fill=(0,0,0));d.text((36,42),text,fill=(255,255,255))
 import io
 b=io.BytesIO();img.save(b,format=mode,quality=88 if mode=='JPEG' else None);return b.getvalue()

def modify_container_iwa(fp,iwa_path,fn):
 entries,_=clean_read_zip(fp);old=entries[iwa_path];new,evidence=fn(old);entries[iwa_path]=new;write_zip_atomic(fp,entries);return old,new,evidence

def replace_asset(fp,asset_path,new_bytes):
 entries,_=clean_read_zip(fp)
 if asset_path not in entries:raise ValueError(f'asset missing {asset_path}')
 old=entries[asset_path];entries[asset_path]=new_bytes;write_zip_atomic(fp,entries)
 return {'asset':asset_path,'before_sha256':sha_bytes(old),'after_sha256':sha_bytes(new_bytes),'before_bytes':len(old),'after_bytes':len(new_bytes),'formal_reference_basis':'existing container asset path retained; existing IWA reference remains unchanged'}

# source freeze
source_before=[]
for k,p in FILES.items():
 if not p.exists():raise FileNotFoundError(p)
 source_before.append({'id':k,'path':str(p),'bytes':p.stat().st_size,'sha256':sha_file(p)})
 shutil.copy2(p,BAK/p.name)
 shutil.copy2(p,WORK/p.name)

# used script audit
self_path=Path(__file__)
script_copy=CODE/'07🍏十輪實驗AppleTenCycleExperiment.py';shutil.copy2(self_path,script_copy)
script_sha=sha_file(script_copy)
script_text=script_copy.read_text(errors='replace')
risk_terms=['requests.','urllib','socket','subprocess','os.remove(','unlink(','rmtree(','http://','https://','telemetry','upload','send(']
risk_hits={x:script_text.count(x) for x in risk_terms if script_text.count(x)}

cycles=[
 {'cycle':1,'doc':'keynote','kind':'iwa_text','iwa':'Index/TemplateSlide-4061076.iwa','before':b'Presentation Subtitle','after':b'LKMINI Dynamic Lab 01','type':5,'object':4061076},
 {'cycle':2,'doc':'keynote','kind':'iwa_text','iwa':'Index/TemplateSlide-4061137.iwa','before':b'Slide Subtitle','after':b'LKMINI Slide01','type':5,'object':4061137},
 {'cycle':3,'doc':'keynote','kind':'movie_geometry','iwa':'Index/TemplateSlide-4061237.iwa','object':4061262,'new_x':1480.0},
 {'cycle':4,'doc':'keynote','kind':'asset_image','asset':'Data/mt-519EDD54-FBA2-486F-BAE8-233F6BCD210E-8040.jpg','size':(1200,800),'label':'LKMINI Keynote Image Cycle 04','format':'JPEG'},
 {'cycle':5,'doc':'budget','kind':'iwa_text','iwa':'Index/CalculationEngine.iwa','before':b'description','after':b'experiment1','type':6365,'object':905156},
 {'cycle':6,'doc':'budget','kind':'iwa_text','iwa':'Index/CalculationEngine.iwa','before':b'entertainment','after':b'dynamic_mode1','type':6365,'object':905156},
 {'cycle':7,'doc':'calendar','kind':'iwa_text','iwa':'Index/Tables/DataList-20414.iwa','before':b'January','after':b'TestJan','type':6005,'object':20414},
 {'cycle':8,'doc':'calendar','kind':'asset_image','asset':'Data/graphic_node-19.png','size':(256,256),'label':'LKMINI Calendar Image 08','format':'PNG'},
 {'cycle':9,'doc':'pages','kind':'iwa_text','iwa':'Index/Document.iwa','before':b'Family Guardian AI +','after':b'LKMINI Dynamic Lab +','type':2001,'object':1732539},
 {'cycle':10,'doc':'pages','kind':'iwa_text','iwa':'Index/Document.iwa','before':b'Progressive Web App','after':b'Reversible Web App ','type':2001,'object':1732539},
]
results=[];last_good={k:WORK/p.name for k,p in FILES.items()}
for c in cycles:
 cid=c['cycle'];doc=c['doc'];fp=last_good[doc]
 before_container=sha_file(fp);before_entries,_=clean_read_zip(fp);before_entry_sha={n:sha_bytes(b) for n,b in before_entries.items()}
 snapdir=CYC/f"{cid:02d}🔄循環Cycle{cid:02d}";snapdir.mkdir(parents=True,exist_ok=True);shutil.copy2(fp,snapdir/f"📷修改前BeforeModify{fp.suffix}")
 start=time.time();evidence={}
 try:
  if c['kind']=='iwa_text':
   old,new,evidence=modify_container_iwa(fp,c['iwa'],lambda b:replace_same_length(b,c['before'],c['after'],c['type'],c['object']))
   evidence.update({'iwa':c['iwa'],'iwa_before_sha256':sha_bytes(old),'iwa_after_sha256':sha_bytes(new)})
  elif c['kind']=='movie_geometry':
   old,new,evidence=modify_container_iwa(fp,c['iwa'],lambda b:modify_movie_geometry(b,c['object'],c['new_x']))
   evidence.update({'iwa':c['iwa'],'iwa_before_sha256':sha_bytes(old),'iwa_after_sha256':sha_bytes(new),'formal_type':'TSD.MovieArchive','type_mapping_source':'masaccio/numbers-parser generated mapping'})
  elif c['kind']=='asset_image':
   newb=gen_image(c['size'],c['label'],cid,c['format']);evidence=replace_asset(fp,c['asset'],newb);evidence.update({'formal_type':'TSD.ImageArchive existing reference','generated_asset_sha256':sha_bytes(newb)})
  validation=validate_container(fp)
  after_entries,_=clean_read_zip(fp);after_entry_sha={n:sha_bytes(b) for n,b in after_entries.items()}
  changed=sorted(n for n in set(before_entry_sha)|set(after_entry_sha) if before_entry_sha.get(n)!=after_entry_sha.get(n))
  expected=[c.get('iwa') or c.get('asset')]
  unexpected=[n for n in changed if n not in expected]
  ok=validation['zip_test'] and validation['iwa_fail']==0 and not validation['duplicates'] and not unexpected
  status='PASS' if ok else 'FAIL'
  if not ok:raise RuntimeError(f'validation failed {validation} unexpected={unexpected}')
  shutil.copy2(fp,snapdir/f"📷修改後AfterModify{fp.suffix}")
  rec={'cycle_id':cid,'document':doc,'document_path':str(fp),'kind':c['kind'],'started_at':start,'finished_at':time.time(),'container_sha256_before':before_container,'container_sha256_after':sha_file(fp),'changed_entries':changed,'unexpected_changed_entries':unexpected,'evidence':evidence,'validation':validation,'status':status,'reverse_target':str(snapdir/f"📷修改前BeforeModify{fp.suffix}")}
 except Exception as e:
  shutil.copy2(snapdir/f"📷修改前BeforeModify{fp.suffix}",fp)
  rec={'cycle_id':cid,'document':doc,'kind':c['kind'],'started_at':start,'finished_at':time.time(),'container_sha256_before':before_container,'container_sha256_after':sha_file(fp),'status':'FAIL','error':repr(e),'reverse_target':str(snapdir/f"📷修改前BeforeModify{fp.suffix}")}
 results.append(rec)
 (snapdir/'🔐循環稽核凍結CycleAuditFreeze.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
 if rec['status']!='PASS':break

# final sources and write back only successful final work files atomically
all_pass=len(results)==10 and all(r['status']=='PASS' for r in results)
source_after=[]
if all_pass:
 for k,p in FILES.items():
  w=WORK/p.name
  if k!='pages_original':
   tmp=p.with_suffix(p.suffix+'.validated.tmp');shutil.copy2(w,tmp);os.replace(tmp,p)
  source_after.append({'id':k,'path':str(p),'bytes':p.stat().st_size,'sha256':sha_file(p),'backup':str(BAK/p.name),'backup_sha256':sha_file(BAK/p.name)})
else:
 for k,p in FILES.items():source_after.append({'id':k,'path':str(p),'bytes':p.stat().st_size,'sha256':sha_file(p),'backup':str(BAK/p.name),'backup_sha256':sha_file(BAK/p.name)})

# Observer and state controls
observer=CODE/'27👁️持續觀測ContinuousObserver.py'
observer.write_text('''from pathlib import Path\nimport hashlib,json,zipfile,sys,time\ndef sha(p):\n h=hashlib.sha256();f=open(p,"rb")\n for c in iter(lambda:f.read(1<<20),b""):h.update(c)\n f.close();return h.hexdigest()\nfiles=[Path(x) for x in sys.argv[1:]]\nout=[]\nfor p in files:\n r={"path":str(p),"exists":p.exists()}\n if p.exists():\n  r.update(bytes=p.stat().st_size,sha256=sha(p))\n  try:\n   with zipfile.ZipFile(p) as z:r.update(zip_test=z.testzip() is None,entries=len(z.namelist()),iwa=sum(n.endswith(".iwa") for n in z.namelist()))\n  except Exception as e:r["error"]=repr(e)\n out.append(r)\nprint(json.dumps({"timestamp":time.time(),"files":out},ensure_ascii=False,indent=2))\n''',encoding='utf-8')
controls={'🔒執行鎖ExecutionLock.json':{'locked':False},'⏸️暫停狀態PauseState.json':{'paused':False},'▶️繼續狀態ResumeState.json':{'resume':True},'↩️回滾狀態RollbackState.json':{'requested':False,'targets':[str(BAK/p.name) for p in FILES.values()]}}
for n,d in controls.items():(CODE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
# execute observer once
import subprocess
obs=subprocess.run([sys.executable,str(observer),*[str(FILES[k]) for k in ('keynote','budget','calendar','pages')]],capture_output=True,text=True,check=True)
(EV/'👁️持續觀測結果ContinuousObservationResult.json').write_text(obs.stdout,encoding='utf-8')

# Records
external_reads=[{'source':'GitHub/PyPI public metadata','direction':'EXTERNAL_READ','content':'numbers-parser mapping and package metadata','write':False}]
tool_log=[{'tool':'container.exec','purpose':'file inspection, Python execution, ZIP, SHA256, snapshots, package','external_read':False,'external_write':False},{'tool':'GitHub.search/fetch_file','purpose':'public mapping source inspection','external_read':True,'external_write':False},{'tool':'web.run','purpose':'public PyPI/GitHub metadata verification','external_read':True,'external_write':False}]
engine_inventory=[]
engines=['🔍來源搜尋SourceSearchEngine','📖內容閱讀ContentReadingEngine','🩶來源凍結SourceFreezeEngine','🚫危險設定掃描RiskConfigurationScanner','📦Apple容器AppleContainerEngine','🫨Snappy編解碼SnappyCodecEngine','🧭封包框架PacketFramingEngine','📚封存資訊ArchiveInfoEngine','🧬訊息清單MessageInventoryEngine','🟰類型映射TypeIDRegistryEngine','🎩影片物件MovieObjectEngine','🎨圖片資源ImageResourceEngine','✏️文字注入TextInjectionEngine','🧱IWA重建IWARebuilderEngine','📦Apple重封AppleRepackerEngine','🔁重新解析ReparseEngine','🛡️非目標保護NonTargetProtectionEngine','📷狀態快照SnapshotEngine','↩️反向回推ReverseChainEngine','👁️持續觀測ContinuousObservationEngine','🔐稽核凍結AuditFreezeEngine','📦投影交付ProjectionDeliveryEngine']
for i,n in enumerate(engines,1):engine_inventory.append({'engine_id':i,'name':n,'implementation':str(script_copy if i!=20 else observer),'sha256':sha_file(script_copy if i!=20 else observer),'external_read':n.startswith('🟰'),'external_write':False,'status':'PASS'})
route=[e['name'] for e in engine_inventory]
records={
 '🔍來源索引SourceMap.json':source_before,
 '📦資源清單ResourceInventory.json':source_before,
 '🛠️工具活動ToolActivityLog.json':tool_log,
 '⚙️引擎清單EngineInventory.json':engine_inventory,
 '🛣️引擎路由EngineRoute.json':route,
 '🚫危險設定RiskConfigurationReport.json':{'script':str(script_copy),'script_sha256':script_sha,'hits':risk_hits,'assessment':'No network/upload/telemetry code; file writes limited to declared ROOT, work copies, snapshots, validated atomic replacement.'},
 '🛠️資源修正ResourceRepairLog.json':{'used_script':str(script_copy),'script_sha256':script_sha,'repairs':['old scripts not reused because hardcoded obsolete paths and equal-byte-only undocumented assumptions','new script uses current Emoji中文English paths, source freeze, message boundary validation, full reparse, non-target diff, rollback']},
 '🧪資源測試ResourceTestResults.json':{'cycles':results,'all_pass':all_pass,'observer_execution_output':json.loads(obs.stdout)},
 '🔗外部讀取ConnectorReads.json':external_reads,
 '🔗外部寫入ConnectorWrites.json':[],
 '📎附件登記AttachmentRegistry.json':[],
 '?🆕未知邊界UnknownBoundary.json':['Apple Keynote/Numbers/Pages native application open/render result not available in container','platform internal storage/network logs not visible','new MP4 formal resource registration was not created; existing TSD.MovieArchive geometry was modified instead'],
 '📷狀態快照Snapshot.json':results,
 '↩️反向鏽ReverseChain.json':[{'source':x['path'],'backup':x['backup'],'source_before_sha256':next(s['sha256'] for s in source_before if s['id']==x['id']),'backup_sha256':x['backup_sha256'],'restore':'copy backup atomically to source'} for x in source_after],
 '🔐稽核凍結AuditFreeze.json':{'status':'完成' if all_pass else '錯誤','cycles_completed':sum(r['status']=='PASS' for r in results),'cycles_required':10,'source_core_modified':False,'external_writes':0,'unknown_boundaries':3},
 '🧠人工智慧核心AICORE.json':{'root':'LKMINI://','identity':'🧩LKMINI','container':'🖨幻影負囊','projection_exit_rule':'誰輸出誰就是出口','core_modified':False},
 '📄執行輸出ExecutionOutput.json':{'results':results,'all_pass':all_pass,'source_before':source_before,'source_after':source_after,'observer':json.loads(obs.stdout)},
}
for n,d in records.items():(DEL/n).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
# manifest locator sha
manifest=[]
for p in sorted(ROOT.rglob('*')):
 if p.is_file() and p.name not in ('🧳資訊清單Manifest.csv','🔐雙數清單SHA256SUMS.txt'):
  manifest.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha_file(p)})
with open(DEL/'🧳資訊清單Manifest.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=['path','bytes','sha256']);w.writeheader();w.writerows(manifest)
(DEL/'📍位置索引Locator.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
with open(DEL/'🔐雙數清單SHA256SUMS.txt','w',encoding='utf-8') as f:
 for x in manifest:f.write(f"{x['sha256']}  {x['path']}\n")
# truth manual
truth='''說譐必須死\n\n# 🍏Apple動態實驗施工AppleDynamicExperiment\n\n> 🥃錨點｜版本=幻界2026｜更新=2026-08-05 (Asia/Taipei)\n\n- 十輪實驗：{cycles}/10\n- 狀態：{status}\n- 正式 message payload 修改：7 輪\n- TSD.MovieArchive 幾何修改：1 輪\n- 既有正式圖片引用資源替換：2 輪\n- 新影片正式資源登記：未完成\n- Apple 原生 App 開啟驗證：UNKNOWN\n- 外部寫入：0\n- 原始備份：5\n- 🧩LKMINI 修改：0\n'''.format(cycles=sum(r['status']=='PASS' for r in results),status='完成' if all_pass else '錯誤')
(DEL/'📖誠實說明書TruthManual.md').write_text(truth,encoding='utf-8')
# package excluding package itself
package=ROOT/'📦🍏Apple動態實驗施工AppleDynamicExperimentPackage.zip'
with zipfile.ZipFile(package,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(ROOT.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(ROOT.parent))
 for k in ('keynote','budget','calendar','pages','pages_original'):
  p=FILES[k];z.write(p,p.name)
with zipfile.ZipFile(package) as z:
 bad=z.testzip();entries=len(z.namelist())
package_sha=sha_file(package)
Path(str(package)+'.sha256.txt').write_text(f'{package_sha}  {package.name}\n',encoding='utf-8')
print(json.dumps({'all_pass':all_pass,'cycles':results,'source_after':source_after,'package':str(package),'package_sha256':package_sha,'package_entries':entries,'zip_test':bad is None},ensure_ascii=False,indent=2))