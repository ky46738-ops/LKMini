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