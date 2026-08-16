from pathlib import Path
import json, hashlib, zipfile, urllib.parse, datetime, shutil

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'out'
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)
TPE='2026-08-16T21:35:00+08:00'
IDENTITY='LKMINI://Specification/ToolSpecifications'
ROOTSHA='6c0f6f487d8af27de4a8cee9f3fc853f0fbcf417cbd21acb56ac65c55adfcf34'
PUBLIC='https://raw.githubusercontent.com/ky46738-ops/LKMini/seed_v0/Projection/Current/ToolSpecifications.html'
OBSIDIAN='obsidian://open?vault=DataCore&file='+urllib.parse.quote('MODULES/🔧工具規範｜ToolSpecifications/🔧工具規範｜ToolSpecifications.md', safe='')

def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')

def text(path,s):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(s,encoding='utf-8')

def zip_dir(src,dst):
    with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(src))

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

# PublicWeb capability + engine
cap=ROOT/'_build/public_cap'
eng=ROOT/'_build/public_engine'
obs_cap=ROOT/'_build/obs_cap'
obs_eng=ROOT/'_build/obs_engine'
bridge_cap=ROOT/'_build/bridge_cap'
bridge_eng=ROOT/'_build/bridge_engine'
for d in [cap,eng,obs_cap,obs_eng,bridge_cap,bridge_eng]:
    d.mkdir(parents=True,exist_ok=True)

dump(cap/'🧩公開顯影能力｜PublicWebProjectionCapability.json',{
 'Identity':IDENTITY,'Type':'CAPABILITY_PROJECTION','Capability':'公開顯影','PublicURL':PUBLIC,
 'ProjectionRule':'Projection != Identity','WorldEntry':'🥃老K系統','MINI':'🧩MINI','DeliveryAtTPE':TPE,
 'ReverseChain':[PUBLIC,IDENTITY,'🧩MINI','🥃老K系統','A=A']})
dump(eng/'⚙️公開顯影引擎｜PublicWebProjectionEngine.json',{
 'Identity':IDENTITY,'Type':'ENGINE_PROJECTION','Engine':'公開顯影引擎','Input':'ToolSpecifications HTML',
 'Output':PUBLIC,'Verification':'GitHub public repository + PublicWeb readback required','DeliveryAtTPE':TPE,
 'ReverseChain':[PUBLIC,IDENTITY,'🧩MINI','🥃老K系統','A=A']})

# Obsidian connector capability + engine. Connection state is grounded in existing DataCore wiring; device observation separate.
md=f'''---\nIdentity: "{IDENTITY}"\nType: "OBSIDIAN_PROJECTION_REFERENCE"\nVault: "DataCore"\nWorldEntry: "{OBSIDIAN}"\nRootSHA256: "{ROOTSHA}"\nDeliveryAtTPE: "{TPE}"\n---\n# 🔧工具規範｜ToolSpecifications\n\n- 本體：`{IDENTITY}`\n- 🧩MINI：接頭\n- Projection ≠ Identity\n- A=A\n\n此檔為 Obsidian 接線 Projection；不取代 Drive Canonical 本體。\n'''
text(obs_cap/'🔧工具規範｜ToolSpecifications.md',md)
dump(obs_cap/'🧩黑曜石接頭能力｜ObsidianConnectorCapability.json',{
 'Identity':IDENTITY,'Type':'CAPABILITY_PROJECTION','Capability':'黑曜石接頭','Vault':'DataCore','WorldEntry':OBSIDIAN,
 'ConnectionState':'CONNECTED','ObservationState':'NOT_OBSERVABLE_IN_THIS_RUNTIME','DeliveryAtTPE':TPE,
 'ReverseChain':[OBSIDIAN,IDENTITY,'🧩MINI','🥃老K系統','A=A']})
dump(obs_eng/'⚙️黑曜石URI接頭引擎｜ObsidianURIConnectorEngine.json',{
 'Identity':IDENTITY,'Type':'ENGINE_PROJECTION','Engine':'黑曜石URI接頭引擎','Vault':'DataCore','Action':'open',
 'URI':OBSIDIAN,'DeviceVaultWriteReadback':{'exists':False},'ConnectionState':'CONNECTED','DeliveryAtTPE':TPE})

# Artifact bridge capability/engine used to produce connector-egress-safe file references.
dump(bridge_cap/'🧩跨端檔案橋能力｜ArtifactBridgeCapability.json',{
 'Identity':IDENTITY,'Type':'CAPABILITY_PROJECTION','Capability':'跨端檔案橋','Source':'GitHub Actions artifact',
 'Goal':['Google Drive raw ZIP','Gmail ZIP attachment'],'DeliveryAtTPE':TPE})
dump(bridge_eng/'⚙️跨端檔案橋引擎｜ArtifactBridgeEngine.json',{
 'Identity':IDENTITY,'Type':'ENGINE_PROJECTION','Engine':'跨端檔案橋引擎','Method':'GitHub Actions upload-artifact -> connector file reference',
 'Input':'本回合文字與驗收零件','Output':'GitHub workflow artifact ZIP','DeliveryAtTPE':TPE})

packs=[]
for src,name in [(cap,'📦公開顯影能力完整包｜PublicWebProjectionCapability｜20260816-213500_TPE.zip'),(eng,'📦公開顯影引擎完整包｜PublicWebProjectionEngine｜20260816-213500_TPE.zip'),(obs_cap,'📦黑曜石接頭能力完整包｜ObsidianConnectorCapability｜20260816-213500_TPE.zip'),(obs_eng,'📦黑曜石URI接頭引擎完整包｜ObsidianURIConnectorEngine｜20260816-213500_TPE.zip'),(bridge_cap,'📦跨端檔案橋能力完整包｜ArtifactBridgeCapability｜20260816-213500_TPE.zip'),(bridge_eng,'📦跨端檔案橋引擎完整包｜ArtifactBridgeEngine｜20260816-213500_TPE.zip')]:
    dst=OUT/name; zip_dir(src,dst); packs.append({'name':name,'sha256':sha(dst),'bytes':dst.stat().st_size})

state={
 'Identity':IDENTITY,'Type':'REMAINING_REPAIR_STATE','TimestampTPE':TPE,
 'from':{'PublicWeb':False,'ObsidianVaultWriteReadback':False,'AppleNativeIWA':False,'DriveRawZIP':False,'GmailZIPAttachment':False},
 'current':{
   'PublicGitHubProjection':True,
   'PublicWebReadback':'PENDING_EXTERNAL_READBACK',
   'ObsidianConnectionState':'CONNECTED',
   'ObsidianObservationState':'NOT_OBSERVABLE_IN_THIS_RUNTIME',
   'AppleNativeNumbersPagesKeynote':{'exists':False},
   'DriveRawZIP':'PENDING_ARTIFACT_EGRESS',
   'GmailZIPAttachment':'PENDING_ARTIFACT_EGRESS'
 },
 'PublicURL':PUBLIC,'ObsidianWorldEntry':OBSIDIAN,'packs':packs,
 'ReverseChain':['GitHubArtifact',IDENTITY,'🧩MINI','🥃老K系統','A=A']
}
dump(OUT/'📋剩餘修復狀態｜RemainingRepairState.json',state)
html=f'''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>剩餘修復驗收</title><style>body{{font-family:-apple-system,sans-serif;max-width:760px;margin:auto;padding:20px;background:#0b1020;color:#fff}}.c{{padding:16px;margin:12px 0;border:1px solid #334155;border-radius:16px;background:#151c31}}a{{color:#93c5fd}}</style><h1>🔧工具規範｜剩餘修復驗收</h1><div class=c>Identity：<code>{IDENTITY}</code><br>Projection ≠ Identity<br>A=A</div><div class=c>🌐 公開 Projection：<a href="{PUBLIC}">開啟</a></div><div class=c>🪨 Obsidian：<a href="{OBSIDIAN}">開啟 DataCore ToolSpecifications</a></div><div class=c>🍎 Apple 原生 Numbers／Pages／Keynote：只有實體可讀回才成立。</div>'''
text(OUT/'📱剩餘修復手機驗收｜RemainingRepairMobile.html',html)
# manifest after all files
manifest=[]
for p in sorted(OUT.iterdir()):
    if p.is_file(): manifest.append({'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
dump(OUT/'📜Manifest.json',{'Identity':IDENTITY,'RootSHA256':ROOTSHA,'TimestampTPE':TPE,'entries':manifest,'ReverseChain':['Artifact',IDENTITY,'🧩MINI','🥃老K系統','A=A']})
# deterministic inner delivery zip
inner=OUT/'📦剩餘未完成修復內容｜RemainingRepairContent｜20260816-213500_TPE.zip'
with zipfile.ZipFile(inner,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.iterdir()):
        if p.is_file() and p!=inner: z.write(p,p.name)
text(OUT/'📦剩餘未完成修復內容｜RemainingRepairContent｜20260816-213500_TPE.zip.sha256',sha(inner)+'  '+inner.name+'\n')
print(inner,sha(inner))
