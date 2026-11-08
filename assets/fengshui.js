/* Sapiopedia: Feng Shui Room Planner (EN/FR via fengshui-fr.js) */
(function(){
"use strict";
/* i18n: English strings are the keys; window.FS_FR (fengshui-fr.js) supplies French. */
const FR=document.documentElement.lang==="fr"&&window.FS_FR?window.FS_FR:null;
function T(s,v){let r=FR&&FR[s]!=null?FR[s]:s;if(v)for(const k in v)r=r.split("{"+k+"}").join(v[k]);return r;}
const THE={bed:"the bed",desk:"the desk",sofa:"the sofa",armchair:"the armchair",chair:"the chair",table:"the table",countertop:"the countertop",appliance:"the appliance",tv:"the TV",wardrobe:"the wardrobe",shelf:"the bookshelf",screen:"the folding screen",plant:"the plant",door:"the door",window:"the window",mirror:"the mirror"};
const A1={door:"a door",window:"a window",mirror:"a mirror"};
const the=k=>T(THE[k]),a1=k=>T(A1[k]),dirT=d=>T(d);
const num=(n,d)=>Number(n).toLocaleString(document.documentElement.lang||"en",{minimumFractionDigits:d,maximumFractionDigits:d});
const POINT8=["north","north-east","east","south-east","south","south-west","west","north-west"];
/* w = width along the wall, h = depth into the room. wall:true pieces back onto the nearest wall. */
const FURN=[
 {k:"bed",name:T("Bed"),w:112,h:160,wall:true},
 {k:"desk",name:T("Desk"),w:96,h:48,wall:true},
 {k:"sofa",name:T("Sofa"),w:144,h:64,wall:true},
 {k:"armchair",name:T("Armchair"),w:68,h:68,wall:true},
 {k:"chair",name:T("Chair"),w:36,h:40,wall:false},
 {k:"table",name:T("Table"),w:96,h:64,wall:false},
 {k:"tv",name:T("TV"),w:96,h:14,wall:true},
 {k:"wardrobe",name:T("Wardrobe"),w:96,h:48,wall:true},
 {k:"countertop",name:T("Countertop"),w:160,h:48,wall:true},
 {k:"appliance",name:T("Appliance"),w:48,h:48,wall:true},
 {k:"shelf",name:T("Bookshelf"),w:76,h:28,wall:true},
 {k:"screen",name:T("Folding screen"),w:116,h:12,wall:false},
 {k:"plant",name:T("Plant"),w:36,h:36,wall:false,round:true}
];
const PXM=80; /* pixels per metre */
const FBY=Object.fromEntries(FURN.map(f=>[f.k,f]));
const OPEN={door:{name:T("Door"),len:72},window:{name:T("Window"),len:96},mirror:{name:T("Mirror"),len:52}};
const VL={good:T("Good"),caution:T("Caution"),bad:T("Avoid"),neutral:T("No rule")};
const ACTIVE=["desk","tv","sofa","armchair","appliance","countertop"],DIVIDERS=["screen","shelf","plant"];

/* ---------- Geometry ---------- */
const SHAPES={
 square:{name:T("Square"),pts:[[160,160],[480,160],[480,480],[160,480]]},
 wide:{name:T("Wide"),pts:[[40,180],[600,180],[600,460],[40,460]]},
 tall:{name:T("Tall"),pts:[[180,40],[460,40],[460,600],[180,600]]},
 lshape:{name:T("L-shape"),pts:[[100,100],[540,100],[540,320],[340,320],[340,540],[100,540]]}
};
function centroid(p){let a=0,cx=0,cy=0;for(let i=0;i<p.length;i++){const[x1,y1]=p[i],[x2,y2]=p[(i+1)%p.length];const f=x1*y2-x2*y1;a+=f;cx+=(x1+x2)*f;cy+=(y1+y2)*f;}a/=2;return[cx/(6*a),cy/(6*a)];}
function inside(x,y,p){let c=false;for(let i=0,j=p.length-1;i<p.length;j=i++){const[xi,yi]=p[i],[xj,yj]=p[j];if(((yi>y)!==(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi))c=!c;}return c;}
let EDGES=[];
function buildEdges(){const P=pts();EDGES=P.map((a,i)=>{const b=P[(i+1)%P.length],dx=b[0]-a[0],dy=b[1]-a[1],L=Math.hypot(dx,dy);let nx=-dy/L,ny=dx/L;const mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2;if(!inside(mx+nx*4,my+ny*4,P)){nx=-nx;ny=-ny;}return{a,b,dx,dy,L,tx:dx/L,ty:dy/L,nx,ny};});}
function onEdge(px,py,i,lo,hi){const e=EDGES[i];let t=((px-e.a[0])*e.dx+(py-e.a[1])*e.dy)/(e.L*e.L);t=Math.max(lo==null?0:lo,Math.min(hi==null?1:hi,t));const x=e.a[0]+t*e.dx,y=e.a[1]+t*e.dy;return{x,y,t,d:Math.hypot(px-x,py-y)};}
function nearestEdge(px,py,skip){let best=null;EDGES.forEach((e,i)=>{if(i===skip)return;const q=onEdge(px,py,i);if(!best||q.d<best.d)best=Object.assign(q,{i});});return best;}
function segDist(px,py,ax,ay,bx,by){const dx=bx-ax,dy=by-ay,L=dx*dx+dy*dy||1;let t=((px-ax)*dx+(py-ay)*dy)/L;t=Math.max(0,Math.min(1,t));return Math.hypot(px-(ax+t*dx),py-(ay+t*dy));}
const dot=(ax,ay,bx,by)=>ax*bx+ay*by;
function bearingOf(vx,vy){const s=Math.atan2(vx,-vy)*180/Math.PI;return((s-S.north)%360+720)%360;}
const dir8=b=>POINT8[Math.round(b/45)%8];
function halfOf(x,y){const[cx,cy]=centroid(pts());const b=bearingOf(x-cx,y-cy);return{north:b<90||b>270,east:b>0&&b<180,south:b>90&&b<270,west:b>180};}
function rayDist(px,py,dx,dy){let best=1e9;EDGES.forEach(e=>{const rx=e.dx,ry=e.dy,den=dx*ry-dy*rx;if(Math.abs(den)<1e-9)return;const qx=e.a[0]-px,qy=e.a[1]-py,t=(qx*ry-qy*rx)/den,u=(qx*dy-qy*dx)/den;if(t>.5&&u>=0&&u<=1)best=Math.min(best,t);});return best;}
function contains(it,x,y){const f=FBY[it.k],o=oi(it);if(f.round)return Math.hypot(x-o.x,y-o.y)<f.w/2;const u=dot(x-o.x,y-o.y,o.tx,o.ty),v=dot(x-o.x,y-o.y,o.bx,o.by);return Math.abs(u)<f.w/2&&Math.abs(v)<f.h/2;}
function blockers(A,B,skipIds){const out=[];S.items.forEach(it=>{if(skipIds.includes(it.id))return;for(let k=1;k<30;k++){const x=A[0]+(B[0]-A[0])*k/30,y=A[1]+(B[1]-A[1])*k/30;if(contains(it,x,y)){out.push(it);break;}}});return out;}
function containsAt(f,o,x,y){if(f.round)return Math.hypot(x-o.x,y-o.y)<f.w/2;const u=dot(x-o.x,y-o.y,o.tx,o.ty),v=dot(x-o.x,y-o.y,o.bx,o.by);return Math.abs(u)<f.w/2&&Math.abs(v)<f.h/2;}
function bedPaths(bo,bedId){ /* circulation from the bed to each door and window */
  if(!bo){const bed=S.items.find(i=>i.k==="bed");if(!bed)return[];bo=oi(bed);bedId=bed.id;}
  return S.opens.filter(o=>o.k==="door"||o.k==="window").map(op=>{const p=openPos(op),T=[p.x+p.nx*12,p.y+p.ny*12];
    const by=blockers([bo.x,bo.y],T,[bedId]);let walls=false;for(let k=1;k<30;k++){const x=bo.x+(T[0]-bo.x)*k/30,y=bo.y+(T[1]-bo.y)*k/30;if(!inside(x,y,pts())){walls=true;break;}}
    return{op,A:[bo.x,bo.y],B:T,by,walls};});
}
function zoneOf(x,y){const[cx,cy]=centroid(pts());if(Math.hypot(x-cx,y-cy)<18)return"centre";return dir8(bearingOf(x-cx,y-cy));}

/* Orientation: back toward the nearest wall. Returns centre (snapped if close), back vector, tangent. */
function orient(k,px,py,rot){
  const f=FBY[k];
  if(rot!=null&&isFinite(rot)){
    const a=rot*Math.PI/180,bx=Math.sin(a),by=-Math.cos(a);let x=px,y=py,edge=-1,best=null;
    EDGES.forEach((e,i)=>{if(dot(-e.nx,-e.ny,bx,by)<.97)return;const q=onEdge(px,py,i,.02,.98);if(!best||q.d<best.d)best=Object.assign(q,{i});});
    if(best&&best.d<f.h/2+48){edge=best.i;if(f.wall){const e=EDGES[edge];x=best.x+e.nx*(f.h/2+5);y=best.y+e.ny*(f.h/2+5);}}
    const gap=edge>=0?onEdge(x,y,edge).d-f.h/2:rayDist(x,y,bx,by)-f.h/2;
    return{x,y,bx,by,tx:-by,ty:bx,edge,gap,manual:true};
  }
  const ne=nearestEdge(px,py);if(!ne)return{x:px,y:py,bx:0,by:-1,tx:1,ty:0,edge:-1,gap:999};
  const e=EDGES[ne.i];let x=px,y=py;
  if(f.wall&&ne.d<f.h/2+48){const q=onEdge(px,py,ne.i);x=q.x+e.nx*(f.h/2+5);y=q.y+e.ny*(f.h/2+5);}
  const bx=-e.nx,by=-e.ny;
  const gap=onEdge(x,y,ne.i).d-f.h/2;
  return{x,y,bx,by,tx:-by,ty:bx,edge:ne.i,gap};
}
const oi=(it,x,y)=>orient(it.k,x==null?it.x:x,y==null?it.y:y,it.rot);
function corners(f,o){const hw=f.w/2,hh=f.h/2;return[[-1,-1],[1,-1],[1,1],[-1,1]].map(([a,b])=>[o.x+o.tx*hw*a+o.bx*hh*-b,o.y+o.ty*hw*a+o.by*hh*-b]);}
function fits(f,o){const P=pts();return inside(o.x,o.y,P)&&corners(f,o).every(([x,y])=>inside(x+(o.x-x)*.04,y+(o.y-y)*.04,P));}
function aabb(f,o){const c=corners(f,o),xs=c.map(p=>p[0]),ys=c.map(p=>p[1]);return[Math.min(...xs),Math.min(...ys),Math.max(...xs),Math.max(...ys)];}
function overlaps(f,o,skip){const A=aabb(f,o);return S.items.some(it=>{if(it.id===skip)return false;const g=FBY[it.k],B=aabb(g,oi(it));return A[0]<B[2]-4&&A[2]>B[0]+4&&A[1]<B[3]-4&&A[3]>B[1]+4;});}
function openPos(o){const e=EDGES[o.edge];if(!e)return null;const t=Math.max(.06,Math.min(.94,o.t));return{x:e.a[0]+t*e.dx,y:e.a[1]+t*e.dy,nx:e.nx,ny:e.ny,tx:e.tx,ty:e.ty,edge:o.edge,len:OPEN[o.k].len};}

/* ---------- State ---------- */
let S={shape:"wide",room:SHAPES.wide.pts.map(p=>p.slice()),north:0,armed:null,drawing:null,sel:null,items:[],opens:[],next:1,v:7};
const pts=()=>S.room;
function example(){
  Object.assign(S,{shape:"wide",room:SHAPES.wide.pts.map(p=>p.slice()),north:0,items:[],opens:[],next:1,sel:null,armed:null,drawing:null,v:7});
  buildEdges(); /* start with an empty room */
}
function valid(){
  if(S.v!==7)return false;
  if(!Array.isArray(S.room)||S.room.length<3||!S.room.every(p=>Array.isArray(p)&&isFinite(p[0])&&isFinite(p[1])))return false;
  if(!Array.isArray(S.items)||!Array.isArray(S.opens))return false;
  buildEdges();
  S.items=S.items.filter(i=>FBY[i.k]&&isFinite(i.x)&&isFinite(i.y));
  S.opens=S.opens.filter(o=>OPEN[o.k]&&EDGES[o.edge]&&isFinite(o.t));
  if(!isFinite(S.north))S.north=0;
  return true;
}
let loaded=false;
try{const s=JSON.parse(localStorage.getItem("sapiopedia-fengshui-1")||"null");if(s){Object.assign(S,s,{armed:null,drawing:null});loaded=true;}}catch(e){}
const hot=window.claude&&window.claude.hot;
if(hot&&hot.data&&hot.data.v===7){Object.assign(S,hot.data,{armed:null,drawing:null});loaded=true;}
if(!loaded||!valid())example();
buildEdges();
if(hot&&hot.snapshot)hot.snapshot(()=>S);
function save(){try{localStorage.setItem("sapiopedia-fengshui-1",JSON.stringify(S));}catch(e){}}

/* ---------- Rules ---------- */
function lines(){ /* door↔window and window↔window on opposite walls */
  const out=[],ops=S.opens.map(o=>Object.assign({op:o},openPos(o))).filter(p=>isFinite(p.x));
  for(let i=0;i<ops.length;i++)for(let j=i+1;j<ops.length;j++){
    const a=ops[i],b=ops[j],ka=a.op.k,kb=b.op.k;
    if(a.edge===b.edge)continue;
    const pair=[ka,kb].sort().join("-");
    if(pair!=="door-window"&&pair!=="window-window")continue;
    if(dot(a.nx,a.ny,b.nx,b.ny)>-.7)continue;
    if(Math.abs(dot(b.x-a.x,b.y-a.y,a.tx,a.ty))>(a.len+b.len)/2+PXM*.6)continue;
    out.push({a,b,kind:pair});
  }
  return out;
}
function between(A,B,skipIds){ /* is a divider standing between points A and B? */
  return S.items.some(it=>{if(!DIVIDERS.includes(it.k)||skipIds.includes(it.id))return false;const o=oi(it),f=FBY[it.k];
    const d=segDist(o.x,o.y,A[0],A[1],B[0],B[1]);return d<Math.max(f.w,f.h)/2+6&&Math.hypot(o.x-A[0],o.y-A[1])>40&&Math.hypot(o.x-B[0],o.y-B[1])>40;});
}
function evaluate(k,o,selfId){
  const f=FBY[k],C=[],add=(v,t,x)=>C.push({v,t:T(t,x)});
  const fx=-o.bx,fy=-o.by;
  const against=f.wall&&o.gap<14;
  const opens=S.opens.map(op=>Object.assign({op},openPos(op))).filter(p=>p.op&&isFinite(p.x));
  const behind=opens.filter(p=>p.edge===o.edge&&Math.abs(dot(p.x-o.x,p.y-o.y,o.tx,o.ty))<f.w/2+p.len/2-6);
  const doors=opens.filter(p=>p.op.k==="door"),windows=opens.filter(p=>p.op.k==="window");
  const L=lines(),inLine=L.filter(l=>{const half=Math.min(l.a.len,l.b.len)/2;for(let s=0;s<=40;s++){const x=l.a.x+(l.b.x-l.a.x)*s/40,y=l.a.y+(l.b.y-l.a.y)*s/40;if(f.round?Math.hypot(x-o.x,y-o.y)<f.w/2+half:Math.abs(dot(x-o.x,y-o.y,o.tx,o.ty))<f.w/2+half&&Math.abs(dot(x-o.x,y-o.y,o.bx,o.by))<f.h/2+half)return true;}return false;});
  const zone=zoneOf(o.x,o.y),others=S.items.filter(i=>i.id!==selfId);
  const facing=dir8(bearingOf(fx,fy)),headDir=dir8(bearingOf(o.bx,o.by));

  if(k==="bed"){
    if(behind.some(p=>p.op.k==="window"))add("bad","Headboard under a window: it feels insecure. If you can't move it, use a tall solid headboard and close the curtains at night.");
    else if(behind.some(p=>p.op.k==="door"))add("bad","Headboard against a door: it needs a solid wall behind it.");
    else if(against)add("good","Headboard against a solid wall.");
    else add("caution","Headboard isn't against a wall: it needs solid support behind it.");
    if(!doors.length)add("neutral","Add your door to check the command position.");
    doors.forEach(d=>{const v=[d.x-o.x,d.y-o.y],ahead=dot(v[0],v[1],fx,fy),lat=Math.abs(dot(v[0],v[1],o.tx,o.ty));
      if(ahead>10&&lat<f.w/2+12&&d.edge!==o.edge)add("bad","Feet point straight at the door: the “coffin position”. Move the bed, or put a footboard, bench or screen at its foot.");
      else if(ahead<=10)add("caution","You can't see the door from the bed.");
      else add("good","Diagonal from the door: you see it without being in line with it (command position).");});
    if(inLine.some(l=>l.kind==="door-window"))add("bad","In the straight line between the door and a window: energy rushes through here.");
    else if(inLine.length)add("caution","Between two facing windows: a fast draught of energy.");
    const side=[1,-1].some(s=>{const sx=o.x+o.tx*s*(f.w/2),sy=o.y+o.ty*s*(f.w/2),n=nearestEdge(sx,sy,o.edge);return n&&n.d<PXM*.45;});
    if(side)add("caution","Pushed against a side wall: leave space on both sides of the bed.");
    if(headDir==="north"||headDir==="east"||headDir==="north-east")add("good",headDir==="north"?"Head points north: deep sleep and calm.":headDir==="east"?"Head points east: energy and new beginnings.":"Head points north-east: calm sleep and fresh energy.");
    else if(headDir==="south")add("bad","Head points south: too active for sleep.");
    const H=halfOf(o.x,o.y);
    if(H.north||H.east)add("good",H.north?"In the north half of the room: calm, restorative sleep.":"In the east half of the room: calm, restorative sleep.");
    else add("caution","In the south-west of the room: the north or east half is calmer for sleep.");
    if(doors.length){const dd=doors[0],dists=EDGES.map((e,i)=>segDist(dd.x,dd.y,e.a[0],e.a[1],e.b[0],e.b[1])),mx=Math.max(...dists);
      if(dists[o.edge]>=mx*.85)add("good","Headboard on the wall farthest from the door.");
      else add("caution","Put the headboard on the wall farthest from the door, so you see the door diagonally from bed.");}
    const BP=bedPaths(o,selfId);
    BP.forEach(pth=>{if(pth.by.length)add("caution","The way to {op} is blocked by {by}: keep paths straight and clear.",{op:the(pth.op.k),by:pth.by.map(b=>the(b.k)).join(T(" and "))});});
    if(BP.length&&BP.every(pth=>!pth.by.length))add("good","Straight, clear paths from the bed to the door and windows.");
    others.filter(i=>i.k==="desk"||i.k==="tv"||i.k==="appliance").forEach(i=>{const oo=oi(i),v=[oo.x-o.x,oo.y-o.y];
      if(dot(v[0],v[1],fx,fy)>0&&Math.abs(dot(v[0],v[1],o.tx,o.ty))<170&&!between([o.x,o.y],[oo.x,oo.y],[]))add("caution","You can see {x} from your pillow: hide it with a screen, bookshelf or large plant.",{x:the(i.k)});});
  }
  else if(k==="desk"){
    if(behind.some(p=>p.op.k==="window"))add("caution","Your back is to a window: no support behind you.");
    else if(behind.some(p=>p.op.k==="door"))add("bad","Your back is to the door.");
    else if(against)add("good","Back against a solid wall.");
    else add("caution","No wall behind you: a solid wall gives support.");
    if(!doors.length)add("neutral","Add your door to check the command position.");
    doors.forEach(d=>{const ahead=dot(d.x-o.x,d.y-o.y,fx,fy);
      if(behind.some(p=>p.op===d.op))return;
      if(d.edge===o.edge){add("caution","The door is on the wall behind you, off to one side: you can't see it without turning.");return;}
      if(ahead>10)add("good","You face the room and can see the door (command position).");
      else if(ahead>-40)add("good","The door is in clear view to your side.");
      else add("bad","The door is behind you: it creates unconscious stress.");});
    const room=rayDist(o.x+fx*(f.h/2),o.y+fy*(f.h/2),fx,fy);
    if(room<90)add("bad","You stare at a wall close up: it blocks your opportunities. Leave open space in front of the desk.");
    else add("good","Open space in front of you.");
    if(windows.some(w=>Math.abs(dot(w.nx,w.ny,o.bx,o.by))<.5))add("good","Window light from the side: bright without distraction.");
    if(inLine.some(l=>l.kind==="door-window"))add("bad","In the straight line between the door and a window.");
    if(zone==="north")add("good","North zone: governs career.");
    else if(zone==="south-east")add("good","South-east zone: governs wealth.");
  }
  else if(k==="sofa"||k==="armchair"){
    if(!doors.length)add("neutral","Add your door to check the command position.");
    else if(!behind.some(p=>p.op.k==="door")){const d=doors[0],ahead=dot(d.x-o.x,d.y-o.y,fx,fy);
      if(ahead>-20)add("good","Seated here, you can see the door.");
      else add("caution","Seated here, your back is to the door: turn it so you can see who comes in.");}
    if(behind.some(p=>p.op.k==="window"))add("caution","Backed onto a window: a solid wall feels more protective.");
    else if(against)add("good","Backed by a solid wall: protective for you and your guests.");
    else add("caution","Floating sofa: ground it against a wall.");
    {const H=halfOf(o.x,o.y);if(H.south)add("good","South half: the active, social side of the room.");else add("caution","The north half suits sleep: keep seating for friends in the south half.");}
    const bed=others.find(i=>i.k==="bed");
    if(bed){const bo=oi(bed);if(dot(bo.bx,bo.by,o.bx,o.by)<-.5)add("good","Opposite the bed: keeps the living area separate from sleep.");}
    if(inLine.some(l=>l.kind==="door-window"))add("caution","In the door-to-window line: a restless spot to sit.");
  }
  else if(k==="chair"){
    if(!doors.length)add("neutral","Add your door to check the command position.");
    else if(!behind.some(p=>p.op.k==="door")){const d=doors[0],ahead=dot(d.x-o.x,d.y-o.y,fx,fy);
      if(ahead>-20)add("good","Seated here, you can see the door.");
      else add("caution","Seated here, your back is to the door: turn it so you can see who comes in.");}
    if(inLine.some(l=>l.kind==="door-window"))add("caution","In the door-to-window line: a restless spot to sit.");
  }
  else if(k==="table"){
    if(inLine.some(l=>l.kind==="door-window"))add("caution","In the door-to-window line: energy rushes past the table.");
    const[cx,cy]=centroid(pts());if(Math.hypot(o.x-cx,o.y-cy)<PXM*.9)add("good","Near the centre of the room: a natural gathering point.");
    const clear=Math.min(...corners(f,o).map(([x,y])=>{const n=nearestEdge(x,y);return n?n.d:999;}));
    if(clear<PXM*.6)add("caution","Less than 60 cm between the table and a wall: leave room to pull out the chairs.");
    else add("good","Room to move all around the table.");
  }
  else if(k==="countertop"){
    if(behind.some(p=>p.op.k==="window"))add("good","A window above the counter: daylight where you work.");
    else if(against)add("good","Against a solid wall.");
    else add("caution","Stand it against a wall.");
    if(!doors.length)add("neutral","Add your door to check the command position.");
    else if(doors.some(d=>d.edge!==o.edge&&dot(d.x-o.x,d.y-o.y,fx,fy)>10))add("caution","While you work here your back is to the door: a mirror or shiny backsplash lets you see who comes in.");
    else add("good","You can see the door while you work.");
    if(inLine.some(l=>l.kind==="door-window"))add("caution","In the straight line between the door and a window.");
  }
  else if(k==="appliance"){
    if(against)add("good","Against a wall, out of the way.");
    else add("caution","Stand it against a wall.");
    const bed=others.find(i=>i.k==="bed");
    if(bed){const bo=oi(bed);if(Math.hypot(bo.x-o.x,bo.y-o.y)<FBY.bed.h/2+f.h/2+PXM)add("bad","Too close to the bed: its hum and heat disturb sleep. Keep appliances at least a metre away.");}
    if(inLine.some(l=>l.kind==="door-window"))add("caution","In the straight line between the door and a window.");
  }
  else if(k==="tv"){
    if(against)add("good","Against a wall.");
    {const H=halfOf(o.x,o.y);if(H.south)add("good","South half: the active, social side of the room.");else add("caution","The north half suits sleep: the TV belongs in the south half.");}
    const bed=others.find(i=>i.k==="bed");
    if(bed){const bo=oi(bed),v=[o.x-bo.x,o.y-bo.y];
      if(dot(v[0],v[1],-bo.bx,-bo.by)>0&&Math.abs(dot(v[0],v[1],bo.tx,bo.ty))<170&&!between([bo.x,bo.y],[o.x,o.y],[]))add("caution","Visible from the bed: it keeps your mind active. Screen it off.");}
  }
  else if(k==="wardrobe"){
    add("good","Closed storage hides clutter and keeps a single room calm.");
    if(f.wall&&!against)add("caution","Stand it against a wall.");
  }
  else if(DIVIDERS.includes(k)){
    const bed=others.find(i=>i.k==="bed");let divides=false;
    if(bed){const bo=oi(bed);divides=others.filter(i=>ACTIVE.includes(i.k)).some(i=>{const ao=oi(i);return segDist(o.x,o.y,bo.x,bo.y,ao.x,ao.y)<Math.max(f.w,f.h)/2+6&&Math.hypot(o.x-bo.x,o.y-bo.y)>40&&Math.hypot(o.x-ao.x,o.y-ao.y)>40;});}
    if(divides)add("good","Shields the bed from the active part of the room.");
    else if(k==="shelf")add("caution","Open shelving looks busy in one room: use it as a divider, or prefer closed storage.");
    else add("neutral",bed?"Place it between the bed and the desk, sofa or TV to shield your sleep.":"Add a bed first: this piece works best as a divider.");
  }
  if(k!=="bed"){const seen=new Set();bedPaths().forEach(pth=>{for(let s=1;s<30;s++){const x=pth.A[0]+(pth.B[0]-pth.A[0])*s/30,y=pth.A[1]+(pth.B[1]-pth.A[1])*s/30;if(containsAt(f,o,x,y)){if(!seen.has(pth.op.k)){seen.add(pth.op.k);add("caution","Blocks the path between the bed and {op}: energy should flow like water.",{op:the(pth.op.k)});}break;}}});}
  return C;
}
function evaluateOpen(op){
  const p=openPos(op),C=[],add=(v,t,x)=>C.push({v,t:T(t,x)});if(!p)return C;
  const L=lines().filter(l=>l.a.op===op||l.b.op===op);
  if(op.k==="door"||op.k==="window"){
    if(L.some(l=>l.kind==="door-window"))add("caution",op.k==="door"?"Faces a window across the room: energy enters and leaves in a straight line. Keep the bed and desk out of that line.":"Faces the door across the room: keep the bed and desk out of the line between them.");
    else if(L.length)add("caution","Faces another window: a fast draught of energy.");
    else add("good",op.k==="door"?"No window directly opposite: energy can settle in the room.":"Not lined up with the door.");
  } else {
    const bed=S.items.find(i=>i.k==="bed");
    if(bed){const bo=oi(bed),v=[bo.x-p.x,bo.y-p.y];if(dot(v[0],v[1],p.nx,p.ny)>20&&Math.abs(dot(v[0],v[1],p.tx,p.ty))<FBY.bed.w/2+40)add("bad","Reflects the bed: it causes restlessness.");}
    const win=S.opens.map(o=>Object.assign({o},openPos(o))).filter(w=>w.o.k==="window"&&w.edge!==p.edge&&dot(w.nx,w.ny,p.nx,p.ny)<-.5&&Math.abs(dot(w.x-p.x,w.y-p.y,p.tx,p.ty))<90);
    if(win.length)add("good","Reflects window light: it opens up the room.");
    if(!C.length)add("neutral","Hang it where it reflects a window or an open path, never the bed.");
  }
  return C;
}
function overall(C){if(C.some(c=>c.v==="bad"))return"bad";if(C.some(c=>c.v==="caution"))return"caution";if(C.some(c=>c.v==="good"))return"good";return"neutral";}
function SCORE(C){return C.reduce((s,c)=>s+(c.v==="good"?1:c.v==="caution"?-1.5:c.v==="bad"?-4:0),0);}

/* Best spot and heat map for a piece */
function bestSpot(k,skip){
  const f=FBY[k],P=pts(),xs=P.map(p=>p[0]),ys=P.map(p=>p[1]);let best=null;
  for(let x=Math.min(...xs);x<=Math.max(...xs);x+=10)for(let y=Math.min(...ys);y<=Math.max(...ys);y+=10){
    if(!inside(x,y,P))continue;const o=orient(k,x,y);if(!fits(f,o)||overlaps(f,o,skip))continue;
    const sc=SCORE(evaluate(k,o,skip))*100+(f.wall?-o.gap:0);
    if(!best||sc>best.sc)best={x:o.x,y:o.y,sc};
  }
  return best;
}
let HEAT=null;
function computeHeat(){
  HEAT=null;const it=S.sel&&S.sel.t==="item"?S.items.find(i=>i.id===S.sel.id):null;if(!it)return;
  const P=pts(),xs=P.map(p=>p[0]),ys=P.map(p=>p[1]),cells=[],step=20;
  for(let x=Math.min(...xs);x<Math.max(...xs);x+=step)for(let y=Math.min(...ys);y<Math.max(...ys);y+=step){
    const cx=x+step/2,cy=y+step/2;if(!inside(cx,cy,P))continue;
    const o=orient(it.k,cx,cy);cells.push([x,y,overall(evaluate(it.k,o,it.id))]);
  }
  HEAT={k:it.k,cells,step};
}

/* ---------- Drawing ---------- */
const NS="http://www.w3.org/2000/svg",svg=document.getElementById("plan");
function el(tag,a,p,t){const e=document.createElementNS(NS,tag);for(const k in a)e.setAttribute(k,a[k]);if(t!=null)e.textContent=t;(p||svg).appendChild(e);return e;}
const css=v=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const VCOL=v=>v==="good"?css("--good"):v==="bad"?css("--bad"):v==="caution"?css("--warn"):css("--muted");
const VBG=v=>v==="good"?css("--good-bg"):v==="bad"?css("--bad-bg"):v==="caution"?css("--warn-bg"):"transparent";
let VB=[0,0,640,640],VB0=[0,0,640,640];
function draw(){
  svg.innerHTML="";
  if(S.drawing){VB=[0,0,640,640];svg.setAttribute("viewBox",VB.join(" "));drawDrawing();return;}
  const P=pts(),[cx,cy]=centroid(P),poly=P.map(p=>p.join(",")).join(" ");
  const xs=P.map(q=>q[0]),ys=P.map(q=>q[1]),bx0=Math.min(...xs)-46,bx1=Math.max(...xs)+46,by0=Math.min(...ys)-46,by1=Math.max(...ys)+46,PAD=18;
  if(!(drag&&drag.t==="vertex")){VB=[bx0-PAD,by0-PAD,bx1-bx0+PAD*2,by1-by0+PAD*2+34];}
  else VB=VB0.slice();
  svg.setAttribute("viewBox",VB.join(" "));
  const edgeAt=b=>{const a=b*Math.PI/180,dx=Math.sin(a),dy=-Math.cos(a);let t=1e9;if(dx>1e-6)t=Math.min(t,(bx1-cx)/dx);if(dx<-1e-6)t=Math.min(t,(bx0-cx)/dx);if(dy>1e-6)t=Math.min(t,(by1-cy)/dy);if(dy<-1e-6)t=Math.min(t,(by0-cy)/dy);return[cx+dx*t,cy+dy*t];};
  const defs=el("defs",{}),cp=el("clipPath",{id:"room"},defs);el("polygon",{points:poly},cp);
  el("polygon",{points:poly,fill:css("--floor")});
  const g=el("g",{"clip-path":"url(#room)"});
  if(HEAT)HEAT.cells.forEach(([x,y,v])=>{if(v!=="neutral")el("rect",{x,y,width:HEAT.step+.5,height:HEAT.step+.5,fill:VBG(v)},g);});
  bedPaths().forEach(pth=>el("line",{x1:pth.A[0],y1:pth.A[1],x2:pth.B[0],y2:pth.B[1],stroke:pth.by.length?css("--warn"):css("--good"),"stroke-width":1.6,"stroke-dasharray":"2 5","stroke-linecap":"round",opacity:.9},g));
  lines().forEach(l=>el("line",{x1:l.a.x,y1:l.a.y,x2:l.b.x,y2:l.b.y,stroke:l.kind==="door-window"?css("--bad"):css("--warn"),"stroke-width":2,"stroke-dasharray":"7 6",opacity:.8},g));
  el("polygon",{points:poly,fill:"none",stroke:css("--ink"),"stroke-width":7,"stroke-linejoin":"miter"});
  EDGES.forEach(e=>{const L=e.L/PXM;if(L<.9)return;const mx=(e.a[0]+e.b[0])/2-e.nx*17,my=(e.a[1]+e.b[1])/2-e.ny*17;
    el("text",{x:mx,y:my+4,"text-anchor":"middle","font-size":11.5,fill:css("--muted"),"font-family":"'Source Sans 3', Helvetica, Arial, sans-serif",stroke:css("--sheet"),"stroke-width":3,"paint-order":"stroke"},null,num(Math.round(L*10)/10,(Math.round(L*10)%10)?1:0)+" m");});
  // openings
  S.opens.forEach(op=>{
    const p=openPos(op);if(!p)return;const v=overall(evaluateOpen(op)),sel=S.sel&&S.sel.t==="open"&&S.sel.id===op.id,h=p.len/2,col=VCOL(v);
    const og=el("g",{"data-open":op.id,style:"cursor:grab"});
    const x1=p.x-p.tx*h,y1=p.y-p.ty*h,x2=p.x+p.tx*h,y2=p.y+p.ty*h;
    el("line",{x1,y1,x2,y2,stroke:"transparent","stroke-width":30},og);
    if(op.k==="door"){
      el("line",{x1,y1,x2,y2,stroke:css("--floor"),"stroke-width":9},og);
      el("line",{x1,y1,x2,y2,stroke:col,"stroke-width":sel?7:5,"stroke-linecap":"round"},og);
      const ex=x1+p.nx*h*2,ey=y1+p.ny*h*2,sweep=(p.tx*p.ny-p.ty*p.nx)>0?1:0;
      el("path",{d:`M${x1} ${y1}L${ex} ${ey}A${h*2} ${h*2} 0 0 ${sweep} ${x2} ${y2}`,fill:"none",stroke:col,"stroke-width":1.3,opacity:.75},og);
    } else if(op.k==="window"){
      el("line",{x1,y1,x2,y2,stroke:col,"stroke-width":sel?10:8},og);
      el("line",{x1,y1,x2,y2,stroke:css("--sheet"),"stroke-width":2.5},og);
    } else {
      const ox=p.nx*7,oy=p.ny*7;
      el("line",{x1:x1+ox,y1:y1+oy,x2:x2+ox,y2:y2+oy,stroke:col,"stroke-width":sel?6:4,"stroke-linecap":"round"},og);
      el("text",{x:p.x+p.nx*20,y:p.y+p.ny*20+4,"text-anchor":"middle","font-size":11,"font-weight":600,fill:css("--muted"),"font-family":"'Source Sans 3', Helvetica, Arial, sans-serif"},og,T("Mirror"));
    }
  });
  // furniture
  S.items.forEach(it=>{
    const f=FBY[it.k],o=oi(it),v=overall(evaluate(it.k,o,it.id)),sel=S.sel&&S.sel.t==="item"&&S.sel.id===it.id,col=VCOL(v);
    const ang=Math.atan2(o.bx,-o.by)*180/Math.PI;
    const ig=el("g",{transform:`translate(${o.x.toFixed(1)} ${o.y.toFixed(1)})`,"data-id":it.id,style:"cursor:grab"});
    const rg=el("g",{transform:`rotate(${f.round?0:ang.toFixed(1)})`},ig);
    const sw=sel?3.5:2;
    if(f.round){el("circle",{r:f.w/2,fill:css("--sheet"),stroke:col,"stroke-width":sw},rg);el("circle",{r:f.w/2,fill:VBG(v)},rg);el("circle",{r:6,fill:col,opacity:.5},rg);}
    else{
      el("rect",{x:-f.w/2,y:-f.h/2,width:f.w,height:f.h,rx:4,fill:css("--sheet"),stroke:col,"stroke-width":sw},rg);
      el("rect",{x:-f.w/2,y:-f.h/2,width:f.w,height:f.h,rx:4,fill:VBG(v)},rg);
      if(it.k==="bed"){[-1,1].forEach(s=>el("rect",{x:s*f.w/4-17,y:-f.h/2+8,width:34,height:16,rx:4,fill:css("--sheet"),stroke:col,"stroke-width":1.2},rg));el("line",{x1:-f.w/2,y1:-f.h/2+34,x2:f.w/2,y2:-f.h/2+34,stroke:col,"stroke-width":1,opacity:.6},rg);}
      if(it.k==="desk")el("circle",{cx:0,cy:f.h/2+13,r:10,fill:css("--sheet"),stroke:col,"stroke-width":1.4},rg);
      if(it.k==="sofa")el("rect",{x:-f.w/2,y:-f.h/2,width:f.w,height:12,rx:3,fill:col,opacity:.35},rg);
      if(it.k==="armchair"){el("rect",{x:-f.w/2,y:-f.h/2,width:f.w,height:12,rx:3,fill:col,opacity:.35},rg);[-1,1].forEach(s=>el("rect",{x:s<0?-f.w/2:f.w/2-10,y:-f.h/2,width:10,height:f.h,rx:3,fill:col,opacity:.25},rg));}
      if(it.k==="chair")el("rect",{x:-f.w/2,y:-f.h/2,width:f.w,height:7,rx:2,fill:col,opacity:.4},rg);
      if(it.k==="table")el("rect",{x:-f.w/2+7,y:-f.h/2+7,width:f.w-14,height:f.h-14,rx:3,fill:"none",stroke:col,"stroke-width":1,opacity:.6},rg);
      if(it.k==="countertop"){el("rect",{x:-f.w/2+14,y:-f.h/2+8,width:34,height:24,rx:5,fill:"none",stroke:col,"stroke-width":1.3},rg);[0,1].forEach(s=>el("circle",{cx:f.w/2-34+s*18,cy:-2,r:6,fill:"none",stroke:col,"stroke-width":1.2},rg));}
      if(it.k==="appliance")el("circle",{cx:0,cy:2,r:13,fill:"none",stroke:col,"stroke-width":1.4},rg);
      if(it.k==="tv")el("line",{x1:-f.w/2+6,y1:f.h/2,x2:f.w/2-6,y2:f.h/2,stroke:col,"stroke-width":3},rg);
      if(it.k==="wardrobe")el("line",{x1:0,y1:-f.h/2,x2:0,y2:f.h/2,stroke:col,"stroke-width":1.2},rg);
      if(it.k==="shelf")[-1,0,1].forEach(s=>el("line",{x1:s*f.w/4,y1:-f.h/2,x2:s*f.w/4,y2:f.h/2,stroke:col,"stroke-width":1},rg));
      if(it.k==="screen")el("polyline",{points:`${-f.w/2},0 ${-f.w/4},${-f.h/2} 0,${f.h/2} ${f.w/4},${-f.h/2} ${f.w/2},0`,fill:"none",stroke:col,"stroke-width":1.4},rg);
    }
    const thin=f.h<32,off=thin?f.h/2+13:0;
    const lx=f.round?0:-o.bx*off,ly=f.round?f.w/2+14:-o.by*off+4;
    el("text",{x:lx,y:ly,"text-anchor":"middle","font-size":Math.max(8,Math.min(12,(Math.max(f.w,f.h)-6)/(f.name.length*.58))).toFixed(1),"font-weight":600,fill:css("--ink"),"font-family":"'Source Sans 3', Helvetica, Arial, sans-serif",stroke:css("--floor"),"stroke-width":3,"paint-order":"stroke"},ig,f.name);
    if(sel&&!f.round){
      const hx=o.tx*(f.w/2+16)-o.bx*(f.h/2+4),hy=o.ty*(f.w/2+16)-o.by*(f.h/2+4);
      const hg=el("g",{"data-rot":it.id,style:"cursor:alias",transform:`translate(${(o.x+hx).toFixed(1)} ${(o.y+hy).toFixed(1)})`});
      el("circle",{r:15,fill:css("--ink")},hg);
      el("path",{d:"M-6 -1 A6.5 6.5 0 1 1 -1.5 6",fill:"none",stroke:css("--sheet"),"stroke-width":2,"stroke-linecap":"round"},hg);
      el("path",{d:"M-9.5 -3 L-6 2 L-2.2 -2.6",fill:"none",stroke:css("--sheet"),"stroke-width":2,"stroke-linecap":"round","stroke-linejoin":"round"},hg);
      el("title",{},hg,T("Drag to turn, click to turn 90°"));
    }
  });
  if(S.armed)el("g",{id:"ghost","pointer-events":"none"});
  // corner handles
  P.forEach((q,i)=>{const hg=el("g",{"data-v":i,style:"cursor:move"});el("circle",{cx:q[0],cy:q[1],r:16,fill:"transparent"},hg);el("circle",{cx:q[0],cy:q[1],r:7.5,fill:css("--sheet"),stroke:css("--ink"),"stroke-width":2.2},hg);});
  // north marker
  [["N",0],["E",90],["S",180],["W",270]].forEach(([t,b])=>{const[x,y]=edgeAt(b+S.north);
    if(t==="N"){el("circle",{cx:x,cy:y,r:12,fill:css("--bad")});el("text",{x,y:y+5,"text-anchor":"middle","font-size":13,"font-weight":700,fill:"#fff","font-family":"'Source Sans 3', Helvetica, Arial, sans-serif"},null,T(t));}
    else el("text",{x,y:y+5,"text-anchor":"middle","font-size":13,"font-weight":600,fill:css("--muted"),"font-family":"'Source Sans 3', Helvetica, Arial, sans-serif"},null,T(t));});
  const m=document.getElementById("mode"),sel=selName();
  const dimTxt=T("Room ≈ {w} × {h} m. Drag a corner to resize. ",{w:num((Math.max(...xs)-Math.min(...xs))/PXM,1),h:num((Math.max(...ys)-Math.min(...ys))/PXM,1)});
  if(S.armed)m.textContent=T("Placing {x}: move over a wall and click. Esc to cancel.",{x:a1(S.armed)});
  else if(HEAT)m.textContent=dimTxt+T("Coloured floor: where {x} works.",{x:the(HEAT.k)});
  else m.textContent=dimTxt+(sel?T("{x} selected.",{x:sel}):T("Pick a piece to see where it works."));
}
function selName(){if(S.sel&&S.sel.t==="open"){const o=S.opens.find(i=>i.id===S.sel.id);return o?OPEN[o.k].name:null;}if(S.sel&&S.sel.t==="item"){const i=S.items.find(i=>i.id===S.sel.id);return i?FBY[i.k].name:null;}return null;}
function drawDrawing(){
  for(let x=40;x<=600;x+=40)for(let y=40;y<=600;y+=40)el("circle",{cx:x,cy:y,r:1.6,fill:css("--line")});
  const d=S.drawing;
  if(d.length){el("polyline",{points:d.map(p=>p.join(",")).join(" "),fill:"none",stroke:css("--ink"),"stroke-width":5});d.forEach((p,i)=>el("circle",{cx:p[0],cy:p[1],r:i===0?9:5,fill:i===0?css("--good"):css("--ink")}));}
  document.getElementById("mode").textContent=d.length<3?T("Click corner by corner to draw the walls. Dots are 50 cm apart."):T("Click the green first corner, or Finish, to close the room.");
}

/* ---------- North arrow ---------- */
const dial=document.getElementById("dial");
function drawDial(){
  dial.innerHTML="";
  const e=(t,a,p)=>{const n=document.createElementNS(NS,t);for(const k in a)n.setAttribute(k,a[k]);(p||dial).appendChild(n);return n;};
  e("circle",{r:29,fill:"transparent"});
  const g=e("g",{transform:`rotate(${S.north})`});
  e("path",{d:"M0 -27 L10 -9 L3.5 -9 L3.5 24 L-3.5 24 L-3.5 -9 L-10 -9 Z",fill:css("--ink")},g);
  const t=e("text",{x:0,y:8,"text-anchor":"middle","font-size":10,"font-weight":700,fill:css("--sheet"),"font-family":"'Source Sans 3', Helvetica, Arial, sans-serif",transform:`rotate(${-S.north} 0 4)`},g);t.textContent="N";
  dial.setAttribute("aria-valuenow",S.north);
}
function setNorth(v){S.north=((Math.round(v/5)*5)%360+360)%360;}
let dialDrag=false;
const dialAngle=ev=>{const r=dial.getBoundingClientRect();return Math.atan2(ev.clientX-(r.left+r.width/2),-(ev.clientY-(r.top+r.height/2)))*180/Math.PI;};
dial.addEventListener("pointerdown",ev=>{dialDrag=true;dial.setPointerCapture(ev.pointerId);setNorth(dialAngle(ev));computeHeat();render(true);});
dial.addEventListener("pointermove",ev=>{if(!dialDrag)return;const old=S.north;setNorth(dialAngle(ev));if(S.north!==old){computeHeat();render(true);}});
dial.addEventListener("pointerup",()=>{if(dialDrag){dialDrag=false;save();}});
dial.addEventListener("keydown",ev=>{const d={ArrowLeft:-5,ArrowDown:-5,ArrowRight:5,ArrowUp:5}[ev.key];if(d){ev.preventDefault();setNorth(S.north+d);computeHeat();save();render(true);}});

/* ---------- Plan pointer: place, drag, bin ---------- */
const trash=document.getElementById("trash");
function pt(ev){const p=svg.createSVGPoint();p.x=ev.clientX;p.y=ev.clientY;return p.matrixTransform(svg.getScreenCTM().inverse());}
function overTrash(ev){const r=trash.getBoundingClientRect();return ev.clientX>=r.left-10&&ev.clientX<=r.right+10&&ev.clientY>=r.top-10&&ev.clientY<=r.bottom+10;}
let drag=null;
svg.addEventListener("pointerdown",ev=>{
  const p=pt(ev);
  if(S.drawing){const s=[Math.round(p.x/20)*20,Math.round(p.y/20)*20],d=S.drawing;
    if(d.length>=3&&Math.hypot(s[0]-d[0][0],s[1]-d[0][1])<22){finishDraw();return;}
    if(!d.length||Math.hypot(s[0]-d[d.length-1][0],s[1]-d[d.length-1][1])>10)d.push(s);render();return;}
  if(S.armed){const ne=nearestEdge(p.x,p.y);if(ne&&ne.d<45){const op={id:S.next++,k:S.armed,edge:ne.i,t:ne.t};S.opens.push(op);S.sel={t:"open",id:op.id};S.armed=null;computeHeat();save();render();}return;}
  const rh=ev.target.closest("g[data-rot]");
  if(rh){const it=S.items.find(i=>i.id===+rh.dataset.rot),o=oi(it);const a0=Math.atan2(p.x-o.x,-(p.y-o.y))*180/Math.PI;
    drag={t:"rotate",id:it.id,cx:o.x,cy:o.y,a0,r0:Math.atan2(o.bx,-o.by)*180/Math.PI,moved:false};svg.setPointerCapture(ev.pointerId);return;}
  const vg=ev.target.closest("g[data-v]");
  if(vg){drag={t:"vertex",i:+vg.dataset.v};VB0=VB.slice();HEAT=null;svg.setPointerCapture(ev.pointerId);return;}
  const og=ev.target.closest("g[data-open]");
  if(og){drag={t:"open",id:+og.dataset.open};S.sel={t:"open",id:drag.id};HEAT=null;svg.setPointerCapture(ev.pointerId);trash.classList.add("live");render();return;}
  const ig=ev.target.closest("g[data-id]");
  if(ig){const id=+ig.dataset.id,it=S.items.find(i=>i.id===id),o=oi(it);drag={t:"item",id,dx:p.x-o.x,dy:p.y-o.y};S.sel={t:"item",id};computeHeat();svg.setPointerCapture(ev.pointerId);trash.classList.add("live");render();return;}
  S.sel=null;HEAT=null;render();
});
svg.addEventListener("pointermove",ev=>{
  if(!drag&&S.armed){drawGhost(pt(ev));return;}
  if(drag&&drag.t==="rotate"){const p=pt(ev),a=Math.atan2(p.x-drag.cx,-(p.y-drag.cy))*180/Math.PI;let r=drag.r0+(a-drag.a0);r=((Math.round(r/15)*15)%360+360)%360;
    const it=S.items.find(i=>i.id===drag.id);if(Math.abs(a-drag.a0)>4)drag.moved=true;if(drag.moved&&it.rot!==r){it.rot=r;const o=oi(it);it.x=o.x;it.y=o.y;draw();drawDetail();}return;}
  if(drag&&drag.t==="vertex"){moveVertex(drag.i,pt(ev));return;}
  if(!drag)return;const p=pt(ev),hotBin=overTrash(ev);trash.classList.toggle("hot",hotBin);if(hotBin)return;
  if(drag.t==="item"){const it=S.items.find(i=>i.id===drag.id),nx=p.x-drag.dx,ny=p.y-drag.dy;if(!inside(nx,ny,pts()))return;const o=oi(it,nx,ny);it.x=o.x;it.y=o.y;}
  else{const op=S.opens.find(i=>i.id===drag.id),ne=nearestEdge(p.x,p.y);if(ne&&ne.d<70){op.edge=ne.i;op.t=Math.max(.06,Math.min(.94,ne.t));}}
  draw();drawDetail();
});
svg.addEventListener("pointerup",ev=>{
  if(drag&&drag.t==="rotate"){const it=S.items.find(i=>i.id===drag.id);if(!drag.moved)turn(it,90);drag=null;computeHeat();save();render();return;}
  if(drag&&drag.t==="vertex"){drag=null;refit();computeHeat();save();render();return;}
  if(!drag)return;const d=drag;drag=null;trash.classList.remove("live","hot");
  if(overTrash(ev)){if(d.t==="item")S.items=S.items.filter(i=>i.id!==d.id);else S.opens=S.opens.filter(i=>i.id!==d.id);S.sel=null;HEAT=null;}
  else computeHeat();
  save();render();
});
function turn(it,deg){const o=oi(it);const cur=Math.atan2(o.bx,-o.by)*180/Math.PI;it.rot=((Math.round((cur+deg)/15)*15)%360+360)%360;const n=oi(it);if(inside(n.x,n.y,pts())){it.x=n.x;it.y=n.y;}}
function drawGhost(p){
  const g=document.getElementById("ghost");if(!g)return;g.innerHTML="";const ne=nearestEdge(p.x,p.y);if(!ne)return;
  const e=EDGES[ne.i],t=Math.max(.06,Math.min(.94,ne.t)),x=e.a[0]+t*e.dx,y=e.a[1]+t*e.dy,h=OPEN[S.armed].len/2,near=ne.d<45;
  const col=near?css("--ink"):css("--muted");
  el("line",{x1:x-e.tx*h,y1:y-e.ty*h,x2:x+e.tx*h,y2:y+e.ty*h,stroke:col,"stroke-width":9,opacity:near?.75:.35,"stroke-linecap":"round"},g);
  el("text",{x:p.x+14,y:p.y-12,"font-size":12.5,"font-weight":600,fill:css("--ink"),"font-family":"'Source Sans 3', Helvetica, Arial, sans-serif",stroke:css("--sheet"),"stroke-width":3,"paint-order":"stroke"},g,near?T("Click to place {x}",{x:the(S.armed)}):T("Move to a wall: {x}",{x:the(S.armed)}));
}
function moveVertex(i,p){
  const R=S.room,n=R.length,old=R[i].slice(),x=Math.round(p.x/8)*8,y=Math.round(p.y/8)*8;
  const next=R.map(q=>q.slice()),pi=(i-1+n)%n,ni=(i+1)%n;
  [pi,ni].forEach(j=>{if(Math.abs(next[j][0]-old[0])<1)next[j][0]=x;else if(Math.abs(next[j][1]-old[1])<1)next[j][1]=y;});
  next[i]=[x,y];
  for(let k=0;k<n;k++){const a=next[k],b=next[(k+1)%n];if(Math.hypot(b[0]-a[0],b[1]-a[1])<PXM*1.2)return;}
  let area=0;for(let k=0;k<n;k++){const a=next[k],b=next[(k+1)%n];area+=a[0]*b[1]-b[0]*a[1];}
  let area0=0;for(let k=0;k<n;k++){const a=R[k],b=R[(k+1)%n];area0+=a[0]*b[1]-b[0]*a[1];}
  if(Math.sign(area)!==Math.sign(area0))return;
  if(Math.max(...next.map(q=>q[0]))-Math.min(...next.map(q=>q[0]))>PXM*12||Math.max(...next.map(q=>q[1]))-Math.min(...next.map(q=>q[1]))>PXM*12)return;
  S.room=next;S.shape=S.shape==="custom"?"custom":S.shape;buildEdges();
  S.items.forEach(it=>{const o=oi(it);it.x=o.x;it.y=o.y;});
  draw();
}
function refit(){S.items.forEach(it=>{const o=oi(it),f=FBY[it.k];if(!fits(f,o)){const b=bestSpot(it.k,it.id);if(b){it.x=b.x;it.y=b.y;}}});}
function finishDraw(){const d=S.drawing;if(d.length<3)return;S.room=d.map(p=>p.slice());S.shape="custom";S.drawing=null;buildEdges();S.opens=[];S.items=S.items.filter(i=>inside(i.x,i.y,S.room));S.sel=null;HEAT=null;save();render();}

/* ---------- Panels ---------- */
const MARK={good:"✓",caution:"!",bad:"✕",neutral:"·"};
function checkList(C){return `<ul class="checks">${C.map(c=>`<li class="${c.v}"><span class="m">${MARK[c.v]}</span><span>${c.t}</span></li>`).join("")}</ul>`;}
function drawDetail(){
  const box=document.getElementById("detail");let html,stripe="var(--line)";
  if(S.sel&&S.sel.t==="item"){
    const it=S.items.find(i=>i.id===S.sel.id);if(!it){S.sel=null;return drawDetail();}
    const f=FBY[it.k],o=oi(it),C=evaluate(it.k,o,it.id),v=overall(C);stripe=VCOL(v);
    html=`<h3>${f.name}</h3><p class="muted" style="margin:4px 0 0"><span class="pill ${v}">${VL[v]}</span> &nbsp;${T("{z} of the room",{z:dirT(zoneOf(o.x,o.y))})}${f.wall&&!f.round?T(", facing {d}",{d:dirT(dir8(bearingOf(-o.bx,-o.by)))}):""}</p>${checkList(C)}
      <div class="actions">${f.round?"":`<button type="button" class="chip" id="tl" aria-label="${T("Turn left")}">↺ ${T("Turn")}</button><button type="button" class="chip" id="tr" aria-label="${T("Turn right")}">${T("Turn")} ↻</button>`}${it.rot!=null&&!f.round?`<button type="button" class="chip" id="auto">${T("Back to wall")}</button>`:""}<button type="button" class="chip" id="rm">${T("Remove")}</button></div>
      ${f.round?"":`<p class="muted" style="font-size:13px;margin:8px 0 0">${T("Tip: drag the round handle on the plan to turn it freely, or press R.")}</p>`}`;
    box.style.setProperty("--stripe",stripe);box.innerHTML=html;
    document.getElementById("rm").addEventListener("click",()=>{S.items=S.items.filter(i=>i.id!==it.id);S.sel=null;HEAT=null;save();render();});
    const step=it.k==="screen"?45:90;
    const tl=document.getElementById("tl"),tr=document.getElementById("tr"),au=document.getElementById("auto");
    if(tl)tl.addEventListener("click",()=>{turn(it,-step);computeHeat();save();render();});
    if(tr)tr.addEventListener("click",()=>{turn(it,step);computeHeat();save();render();});
    if(au)au.addEventListener("click",()=>{delete it.rot;const o=oi(it);it.x=o.x;it.y=o.y;computeHeat();save();render();});
    return;
  }
  if(S.sel&&S.sel.t==="open"){
    const op=S.opens.find(i=>i.id===S.sel.id);if(!op){S.sel=null;return drawDetail();}
    const C=evaluateOpen(op),v=overall(C),p=openPos(op);stripe=VCOL(v);
    const[cx,cy]=centroid(pts());
    html=`<h3>${OPEN[op.k].name}</h3><p class="muted" style="margin:4px 0 0"><span class="pill ${v}">${VL[v]}</span> &nbsp;${T("on the {d} wall",{d:dirT(dir8(bearingOf(p.x-cx,p.y-cy)))})}</p>${checkList(C)}
      <p class="muted" style="font-size:13.5px;margin:10px 0 0">${T("Drag it along the walls to move it, or onto the bin to remove it.")}</p>
      <div class="actions"><button type="button" class="chip" id="rm">${T("Remove")}</button></div>`;
    box.style.setProperty("--stripe",stripe);box.innerHTML=html;
    document.getElementById("rm").addEventListener("click",()=>{S.opens=S.opens.filter(i=>i.id!==op.id);S.sel=null;save();render();});
    return;
  }
  if(S.drawing)html=`<h3>${T("Draw your room")}</h3><p class="muted">${T("Click each corner of the room in turn. Points snap to a grid. Close the shape by clicking the first corner.")}</p>`;
  else html=`<h3>${T("How it works")}</h3><p class="muted">${T("Add your door and windows on the walls and point the arrow north. Then pick a piece of furniture: it goes to its best spot, and while it's selected the floor shows how it would do anywhere in the room. Drag anything onto the bin to remove it.")}</p>`;
  box.style.setProperty("--stripe",stripe);box.innerHTML=html;
}
function drawNotes(){
  const N=[],L=lines();
  if(!S.opens.some(o=>o.k==="door"))N.push(["caution","Add your entrance door: most rules depend on it."]);
  L.filter(l=>l.kind==="door-window").forEach(()=>N.push(["bad","Your door lines up with a window (red dashed line): keep the bed and desk out of that path."]));
  L.filter(l=>l.kind==="window-window").forEach(()=>N.push(["caution","Two windows face each other (amber dashed line): avoid resting or working in between."]));
  const bed=S.items.find(i=>i.k==="bed");
  if(bed&&S.items.some(i=>ACTIVE.includes(i.k))&&!S.items.some(i=>DIVIDERS.includes(i.k)))N.push(["neutral","In a single room, a screen, open bookshelf or large plant between the bed and the active area protects your sleep."]);
  if(S.items.some(i=>i.k==="shelf")&&!S.items.some(i=>i.k==="wardrobe"))N.push(["neutral","Prefer closed storage to open shelves: clutter in one corner affects the whole room."]);
  const BP=bedPaths();
  if(BP.some(p=>p.by.length))N.push(["caution","A piece of furniture blocks the way from the bed to a door or window (amber dotted line). Paths should be straight and clear."]);
  else if(BP.length)N.push(["good","Clear, straight paths from the bed to the door and windows (green dotted lines)."]);
  if(!N.length)N.push(["good","No problems with the room's layout."]);
  document.getElementById("notes").innerHTML=N.map(([v,t])=>`<li class="${v}"><span class="m" style="color:${v==="good"?"var(--good)":v==="bad"?"var(--bad)":v==="caution"?"var(--warn)":"var(--muted)"}">${MARK[v]}</span><span>${T(t)}</span></li>`).join("");
}
function drawList(){
  const ul=document.getElementById("list"),c={good:0,caution:0,bad:0,neutral:0};
  const rows=[...S.opens.map(op=>{const v=overall(evaluateOpen(op));c[v]++;return{t:"open",id:op.id,name:OPEN[op.k].name,v,where:T("on a wall")};}),
              ...S.items.map(it=>{const o=oi(it),v=overall(evaluate(it.k,o,it.id));c[v]++;return{t:"item",id:it.id,name:FBY[it.k].name,v,where:T("{z} of the room",{z:dirT(zoneOf(o.x,o.y))})};})];
  ul.innerHTML=rows.map(w=>`<li><span class="nm"><button type="button" data-t="${w.t}" data-id="${w.id}">${w.name}</button><small>${w.where}</small></span><span class="pill ${w.v}">${VL[w.v]}</span><button type="button" class="x" aria-label="${T("Remove")} ${w.name}" data-rmt="${w.t}" data-rm="${w.id}">✕</button></li>`).join("")||`<li class="muted">${T("The room is empty.")}</li>`;
  document.getElementById("tally").innerHTML=rows.length?`<span><b>${c.good}</b> ${T("good")}</span><span><b>${c.caution}</b> ${T("caution")}</span><span><b>${c.bad}</b> ${T("avoid")}</span>`:"";
  ul.querySelectorAll("[data-id]").forEach(b=>b.addEventListener("click",()=>{S.sel={t:b.dataset.t,id:+b.dataset.id};computeHeat();render();}));
  ul.querySelectorAll("[data-rm]").forEach(b=>b.addEventListener("click",()=>{const id=+b.dataset.rm;if(b.dataset.rmt==="item")S.items=S.items.filter(i=>i.id!==id);else S.opens=S.opens.filter(i=>i.id!==id);if(S.sel&&S.sel.id===id){S.sel=null;HEAT=null;}save();render();}));
}
function drawControls(){
  const sh=document.getElementById("shapes");sh.querySelectorAll("button").forEach(b=>b.remove());
  const mk=(cls,html,fn,extra)=>{const b=document.createElement("button");b.type="button";b.className=cls;b.innerHTML=html;b.addEventListener("click",fn);if(extra)extra(b);sh.appendChild(b);return b;};
  if(S.drawing){
    mk("chip solid",T("Finish"),finishDraw,b=>{b.disabled=S.drawing.length<3;});
    mk("chip",T("Undo corner"),()=>{S.drawing.pop();render();});
    mk("chip",T("Cancel"),()=>{S.drawing=null;render();});
  } else {
    Object.entries(SHAPES).forEach(([k,s])=>mk("shape",`<svg viewBox="30 30 580 580" aria-hidden="true"><polygon points="${s.pts.map(p=>p.join(",")).join(" ")}" fill="none" stroke="currentColor" stroke-width="44"/></svg>`,
      ()=>{S.shape=k;S.room=s.pts.map(p=>p.slice());buildEdges();S.opens=[];S.items=S.items.filter(i=>inside(i.x,i.y,s.pts)).map(i=>{const o=oi(i);return Object.assign(i,{x:o.x,y:o.y});});S.items=S.items.filter(i=>{const f=FBY[i.k];if(fits(f,oi(i))&&!overlaps(f,oi(i),i.id))return true;delete i.rot;const b=bestSpot(i.k,i.id);if(!b)return false;i.x=b.x;i.y=b.y;return true;});S.sel=null;HEAT=null;save();render();},
      b=>{b.title=s.name;b.setAttribute("aria-label",T("{x} room",{x:s.name}));b.setAttribute("aria-pressed",S.shape===k);}));
    mk("shape draw","✎ "+T("Draw"),()=>{S.drawing=[];S.armed=null;S.sel=null;HEAT=null;render();},b=>b.setAttribute("aria-pressed",S.shape==="custom"));
  }
  const op=document.getElementById("openings");op.innerHTML="";
  Object.entries(OPEN).forEach(([k,o])=>{const b=document.createElement("button");b.type="button";b.className="chip";b.textContent="+ "+o.name;b.setAttribute("aria-pressed",S.armed===k);b.disabled=!!S.drawing;
    b.addEventListener("click",()=>{S.armed=S.armed===k?null:k;S.sel=null;HEAT=null;render();});op.appendChild(b);});
  const pc=document.getElementById("pieces");pc.innerHTML="";
  FURN.forEach(f=>{const b=document.createElement("button");b.type="button";b.className="chip";b.textContent="+ "+f.name;b.disabled=!!S.drawing;
    b.addEventListener("click",()=>{let s=bestSpot(f.k);if(!s){const[cx,cy]=centroid(pts());const o=orient(f.k,cx,cy);s={x:o.x,y:o.y};}
      const it={id:S.next++,k:f.k,x:s.x,y:s.y};S.items.push(it);S.sel={t:"item",id:it.id};S.armed=null;computeHeat();save();render();});pc.appendChild(b);});
}
function render(light){svg.style.cursor=S.armed?"copy":"";if(!light)drawControls();drawDial();draw();drawDetail();drawNotes();drawList();}

document.getElementById("clear").addEventListener("click",()=>{S.items=[];S.opens=[];S.sel=null;S.armed=null;HEAT=null;save();render();});
document.addEventListener("keydown",e=>{if(e.key==="Escape"){S.drawing=null;S.armed=null;render();}
  if((e.key==="r"||e.key==="R")&&!e.metaKey&&!e.ctrlKey&&S.sel&&S.sel.t==="item"&&!/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName)){const it=S.items.find(i=>i.id===S.sel.id);if(it&&!FBY[it.k].round){turn(it,e.shiftKey?-(it.k==="screen"?45:90):(it.k==="screen"?45:90));computeHeat();save();render();}}});
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>render());
new MutationObserver(()=>render()).observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]});
computeHeat();render();

/* ---------- Export PNG with Sapiopedia branding ---------- */
const LOGO="/assets/logo-horizontal.png";
const expBtn=document.getElementById("export"),expMsg=document.getElementById("exp-msg");
let downloads=null,plainDownload=false;
if(window.claude&&typeof window.claude.use==="function"){
  window.claude.use("downloads").then(d=>{downloads=d;expBtn.hidden=!d;}).catch(()=>{expBtn.hidden=true;});
} else {plainDownload=true;expBtn.hidden=false;}
const loadImg=src=>new Promise((res,rej)=>{const i=new Image();i.onload=()=>res(i);i.onerror=rej;i.src=src;});
async function buildPNG(){
  const root=document.documentElement,prevTheme=root.getAttribute("data-theme");
  const keep={sel:S.sel,armed:S.armed,heat:HEAT};
  S.sel=null;S.armed=null;HEAT=null;root.setAttribute("data-theme","light");draw();
  const clone=svg.cloneNode(true),vb=VB.slice(),xs=pts().map(q=>q[0]),ys=pts().map(q=>q[1]);
  const counts={good:0,caution:0,bad:0};
  S.items.forEach(it=>{const v=overall(evaluate(it.k,oi(it),it.id));if(v in counts)counts[v]++;});
  S.opens.forEach(op=>{const v=overall(evaluateOpen(op));if(v in counts)counts[v]++;});
  if(prevTheme==null)root.removeAttribute("data-theme");else root.setAttribute("data-theme",prevTheme);
  S.sel=keep.sel;S.armed=keep.armed;HEAT=keep.heat;render();
  clone.querySelectorAll("g[data-v],g[data-rot],#ghost").forEach(n=>n.remove());
  const W=1600,PAD=70,planW=W-PAD*2,planH=Math.round(vb[3]*planW/vb[2]),BAND=200,GAP=80,H=PAD+planH+GAP+BAND;
  clone.setAttribute("xmlns","http://www.w3.org/2000/svg");clone.setAttribute("width",planW);clone.setAttribute("height",planH);clone.style.cssText="";
  const svgUrl="data:image/svg+xml;charset=utf-8,"+encodeURIComponent(new XMLSerializer().serializeToString(clone));
  await (document.fonts&&document.fonts.ready);
  const[planImg,logo]=await Promise.all([loadImg(svgUrl),loadImg(LOGO)]);
  const c=document.createElement("canvas");c.width=W;c.height=H;const x=c.getContext("2d");
  x.fillStyle="#ffffff";x.fillRect(0,0,W,H);
  x.drawImage(planImg,PAD,PAD,planW,planH);
  const by=PAD+planH+GAP;
  /* legend */
  x.font="500 26px 'Source Sans 3', Arial, sans-serif";x.textAlign="left";x.textBaseline="middle";
  const LEG=[[T("Good"),"rgba(63,138,104,.18)","#3f8a68"],[T("Caution"),"rgba(181,138,46,.17)","#b58a2e"],[T("Avoid"),"rgba(194,80,59,.16)","#c2503b"]];
  const sw=26,gapL=14,gapI=44,widths=LEG.map(l=>sw+gapL+x.measureText(l[0]).width),total=widths.reduce((a,b)=>a+b,0)+gapI*(LEG.length-1);
  let lx=(W-total)/2;const ly=PAD+planH+GAP/2-4;
  LEG.forEach((l,i)=>{x.fillStyle="#ffffff";x.fillRect(lx,ly-sw/2,sw,sw);x.fillStyle=l[1];x.fillRect(lx,ly-sw/2,sw,sw);x.strokeStyle=l[2];x.lineWidth=3;x.strokeRect(lx+1.5,ly-sw/2+1.5,sw-3,sw-3);
    x.fillStyle="#2A1F26";x.fillText(l[0],lx+sw+gapL,ly+1);lx+=widths[i]+gapI;});
  x.textBaseline="alphabetic";
  x.fillStyle="#F7E9EC";x.fillRect(0,by,W,BAND);x.fillStyle="#DCC9CE";x.fillRect(0,by,W,2);
  const lh=120,lw=logo.width*lh/logo.height;x.drawImage(logo,PAD-10,by+(BAND-lh)/2,lw,lh);
  x.textAlign="right";x.fillStyle="#2A1F26";x.font="600 36px 'Source Sans 3', Arial, sans-serif";x.fillText((FR?"sapiopedia.com/fr/outils/fengshui":"sapiopedia.com/en/tools/fengshui"),W-PAD,by+82);
  x.fillStyle="#6E5A62";x.font="400 24px 'Source Sans 3', Arial, sans-serif";
  const dims=T("Room ≈ {w} × {h} m",{w:num((Math.max(...xs)-Math.min(...xs))/PXM,1),h:num((Math.max(...ys)-Math.min(...ys))/PXM,1)});
  x.fillText(T("Feng Shui Room Planner")+" · "+dims,W-PAD,by+124);
  x.fillText(`${counts.good} ${T("good")} · ${counts.caution} ${T("caution")} · ${counts.bad} ${T("avoid")}`,W-PAD,by+158);
  return await new Promise(res=>c.toBlob(res,"image/png"));
}
/* Preview the PNG in an overlay; download only when asked */
const FN="sapiopedia-feng-shui-room.png";
function preview(blob){
  const url=URL.createObjectURL(blob),ov=document.createElement("div"),touch=matchMedia("(pointer:coarse)").matches;
  ov.className="fs-ov";ov.setAttribute("role","dialog");ov.setAttribute("aria-modal","true");ov.setAttribute("aria-label",T("Your room plan"));
  ov.innerHTML=`<div class="fs-ovbox"><img src="${url}" alt="${T("Your room plan")}">${touch?`<p class="muted fs-ovhint">${T("On a phone, you can also press and hold the image to save it.")}</p>`:""}<div class="fs-ovact"><button type="button" class="chip" data-a="close">${T("Close")}</button><button type="button" class="chip solid" data-a="dl">${T("Download PNG")}</button></div><span class="muted fs-ovmsg" aria-live="polite"></span></div>`;
  const msg=ov.querySelector(".fs-ovmsg"),prevOverflow=document.body.style.overflow;
  const close=()=>{ov.remove();URL.revokeObjectURL(url);document.removeEventListener("keydown",esc,true);document.body.style.overflow=prevOverflow;expBtn.focus();};
  const esc=e=>{if(e.key==="Escape"){e.stopPropagation();close();}};
  ov.addEventListener("click",async e=>{const a=e.target.closest("[data-a]");
    if(e.target===ov||(a&&a.dataset.a==="close"))return close();
    if(a&&a.dataset.a==="dl"){
      if(downloads){try{await downloads.save({filename:FN,data:blob});msg.textContent=T("Saved.");}catch(err){msg.textContent=err&&err.code==="declined"?T("Export cancelled."):T("Export isn't available here.");}}
      else{const l=document.createElement("a");l.href=url;l.download=FN;document.body.appendChild(l);l.click();l.remove();}
    }});
  document.addEventListener("keydown",esc,true);document.body.style.overflow="hidden";
  document.querySelector(".fs").appendChild(ov);ov.querySelector('[data-a="dl"]').focus();
}
expBtn.addEventListener("click",async()=>{
  expBtn.disabled=true;expMsg.textContent=T("Preparing image…");
  try{
    const blob=await buildPNG();
    expMsg.textContent="";preview(blob);
  }catch(e){const code=e&&e.code;expMsg.textContent=code==="declined"?T("Export cancelled."):code==="rate_limited"?T("Another save is open: try again in a moment."):T("Export isn't available here.");if(code&&code!=="declined"&&code!=="rate_limited"&&!plainDownload)expBtn.hidden=true;}
  finally{expBtn.disabled=false;setTimeout(()=>{if(expMsg.textContent===T("Saved."))expMsg.textContent="";},3000);}
});

})();
