/* 뉴런 반응 연구실 공통 엔진 v2 — 외부 라이브러리 없음, 브라우저 저장소 쓰지 않음 */
(function(){
'use strict';
var L = window.LAB = {};
/* ---------- 그림(스프라이트) 채우기 ---------- */
L.fillSprites = function(root){
  (root||document).querySelectorAll('img[data-s]').forEach(function(im){
    var k = im.getAttribute('data-s'); if (window.SPRITE && SPRITE[k]) im.src = SPRITE[k];
  });
};
L.setFace = function(img, key){ if(img && window.SPRITE && SPRITE[key]){ img.src = SPRITE[key]; img.setAttribute('data-s',key);} };
/* ---------- 난수 ---------- */
L.rng = function(seed){
  var a = seed>>>0;
  var f = function(){ a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a>>>15, 1 | a); t = t + Math.imul(t ^ t>>>7, 61 | t) ^ t; return ((t ^ t>>>14)>>>0)/4294967296; };
  f.gauss = function(){ var u=0,v=0; while(u===0)u=f(); while(v===0)v=f(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); };
  return f;
};
/* ---------- 활성화 함수 ---------- */
function erf(x){ var s=x<0?-1:1; x=Math.abs(x); var t=1/(1+0.3275911*x); var y=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-0.284496736)*t+0.254829592)*t*Math.exp(-x*x); return s*y; }
L.erf = erf;
var SQ2 = Math.SQRT2, INV_SQ2PI = 1/Math.sqrt(2*Math.PI);
L.ACT = {
  none:   {ko:'없음(그대로)', f:function(z){return z;}, d:function(z){return 1;}},
  sigmoid:{ko:'시그모이드', f:function(z){return 1/(1+Math.exp(-z));}, d:function(z){var s=1/(1+Math.exp(-z));return s*(1-s);}},
  tanh:   {ko:'tanh', f:function(z){return Math.tanh(z);}, d:function(z){var t=Math.tanh(z);return 1-t*t;}},
  relu:   {ko:'ReLU', f:function(z){return z>0?z:0;}, d:function(z){return z>0?1:0;}},
  leaky:  {ko:'Leaky ReLU', f:function(z){return z>0?z:0.01*z;}, d:function(z){return z>0?1:0.01;}},
  gelu:   {ko:'GELU', f:function(z){return 0.5*z*(1+erf(z/SQ2));}, d:function(z){return 0.5*(1+erf(z/SQ2)) + z*INV_SQ2PI*Math.exp(-z*z/2);}},
  silu:   {ko:'SiLU', f:function(z){return z/(1+Math.exp(-z));}, d:function(z){var s=1/(1+Math.exp(-z));return s*(1+z*(1-s));}}
};
/* ---------- 작은 신경망 (완전연결, 출력 1개 또는 여러 개) ---------- */
L.Net = function(sizes, act, opt){
  opt = opt || {};
  var r = L.rng(opt.seed||1);
  this.sizes = sizes; this.act = act; this.out = opt.out || 'linear';
  this.W = []; this.b = [];
  for (var l=0; l<sizes.length-1; l++){
    var nin=sizes[l], nout=sizes[l+1];
    var sd = opt.init==='he' ? Math.sqrt(2/nin) : opt.init==='small' ? 0.05 : opt.init==='big' ? 1.6/Math.sqrt(nin)*Math.sqrt(3) : Math.sqrt(1/nin);
    var W = new Float64Array(nin*nout), b = new Float64Array(nout);
    for (var i=0;i<W.length;i++) W[i] = r.gauss()*sd;
    if (opt.biasShift && l < sizes.length-2) for (var j=0;j<nout;j++) b[j]=opt.biasShift;
    this.W.push(W); this.b.push(b);
  }
  this.mW = this.W.map(function(w){return new Float64Array(w.length);}); this.vW = this.W.map(function(w){return new Float64Array(w.length);});
  this.mb = this.b.map(function(w){return new Float64Array(w.length);}); this.vb = this.b.map(function(w){return new Float64Array(w.length);});
  this.t = 0;
};
L.Net.prototype.nParams = function(){ var n=0; for (var l=0;l<this.W.length;l++) n+=this.W[l].length+this.b[l].length; return n; };
L.Net.prototype.forward = function(x){
  var A = L.ACT[this.act], zs=[], as=[x], a=x;
  for (var l=0;l<this.W.length;l++){
    var nin=this.sizes[l], nout=this.sizes[l+1], W=this.W[l], b=this.b[l];
    var z = new Float64Array(nout);
    for (var j=0;j<nout;j++){ var s=b[j]; for (var i=0;i<nin;i++) s+=W[j*nin+i]*a[i]; z[j]=s; }
    zs.push(z);
    var last = l===this.W.length-1;
    var na = new Float64Array(nout);
    if (!last){ for (var k=0;k<nout;k++) na[k]=A.f(z[k]); }
    else if (this.out==='sigmoid'){ for (k=0;k<nout;k++) na[k]=1/(1+Math.exp(-z[k])); }
    else if (this.out==='softmax'){ var mx=-1e9; for(k=0;k<nout;k++) mx=Math.max(mx,z[k]); var sm=0; for(k=0;k<nout;k++){na[k]=Math.exp(z[k]-mx);sm+=na[k];} for(k=0;k<nout;k++) na[k]/=sm; }
    else { for (k=0;k<nout;k++) na[k]=z[k]; }
    as.push(na); a=na;
  }
  return {zs:zs, as:as, y:a};
};
/* 손실의 출력 쪽 기울기 dL/dz_last 를 받아 거꾸로 전한다. 각 층 W의 기울기와 층마다 기울기 크기를 돌려준다. */
L.Net.prototype.backward = function(fw, dzLast, gW, gb, norms){
  var A = L.ACT[this.act], dz = dzLast;
  for (var l=this.W.length-1; l>=0; l--){
    var nin=this.sizes[l], nout=this.sizes[l+1], W=this.W[l], a=fw.as[l];
    var GW=gW[l], Gb=gb[l], s2=0;
    for (var j=0;j<nout;j++){ Gb[j]+=dz[j]; for (var i=0;i<nin;i++){ var g=dz[j]*a[i]; GW[j*nin+i]+=g; s2+=g*g; } }
    if (norms) norms[l]+=Math.sqrt(s2);
    if (l>0){
      var da = new Float64Array(nin), zprev=fw.zs[l-1];
      for (i=0;i<nin;i++){ var s=0; for (j=0;j<nout;j++) s+=W[j*nin+i]*dz[j]; da[i]=s*A.d(zprev[i]); }
      dz = da;
    }
  }
};
L.Net.prototype.zeroGrads = function(){ return {gW:this.W.map(function(w){return new Float64Array(w.length);}), gb:this.b.map(function(w){return new Float64Array(w.length);})}; };
/* 한 번 학습(전체 묶음). X: 배열의 배열, Y: 회귀면 숫자, 분류(sigmoid)면 0/1, softmax면 정수 */
L.Net.prototype.step = function(X, Y, lr, method, norms){
  var G = this.zeroGrads(), n = X.length, loss = 0, correct = 0;
  for (var p=0;p<n;p++){
    var fw = this.forward(X[p]), y=fw.y, dz;
    if (this.out==='sigmoid'){ var t=Y[p]; loss += -(t*Math.log(y[0]+1e-12)+(1-t)*Math.log(1-y[0]+1e-12)); dz=new Float64Array([ (y[0]-t)/n ]); if ((y[0]>0.5)===(t>0.5)) correct++; }
    else if (this.out==='softmax'){ var c=Y[p]; loss += -Math.log(y[c]+1e-12); dz=new Float64Array(y.length); var best=0; for (var k=0;k<y.length;k++){ dz[k]=(y[k]-(k===c?1:0))/n; if(y[k]>y[best]) best=k;} if(best===c) correct++; }
    else { var e=y[0]-Y[p]; loss += 0.5*e*e; dz=new Float64Array([e/n]); }
    this.backward(fw, dz, G.gW, G.gb, norms);
  }
  this.apply(G, lr, method||'adam');
  return {loss: loss/n, acc: correct/n};
};
L.Net.prototype.apply = function(G, lr, method){
  this.t++;
  var b1=0.9,b2=0.999,eps=1e-8,t=this.t;
  for (var l=0;l<this.W.length;l++){
    var arrs=[[this.W[l],G.gW[l],this.mW[l],this.vW[l]],[this.b[l],G.gb[l],this.mb[l],this.vb[l]]];
    for (var q=0;q<2;q++){
      var P=arrs[q][0],g=arrs[q][1],m=arrs[q][2],v=arrs[q][3];
      for (var i=0;i<P.length;i++){
        if (method==='sgd'){ P[i]-=lr*g[i]; }
        else { m[i]=b1*m[i]+(1-b1)*g[i]; v[i]=b2*v[i]+(1-b2)*g[i]*g[i]; P[i]-=lr*(m[i]/(1-Math.pow(b1,t)))/(Math.sqrt(v[i]/(1-Math.pow(b2,t)))+eps); }
      }
    }
  }
};
L.Net.prototype.evalSet = function(X,Y){
  var loss=0,correct=0,n=X.length;
  for (var p=0;p<n;p++){ var y=this.forward(X[p]).y;
    if (this.out==='sigmoid'){ var t=Y[p]; loss += -(t*Math.log(y[0]+1e-12)+(1-t)*Math.log(1-y[0]+1e-12)); if ((y[0]>0.5)===(t>0.5)) correct++; }
    else if (this.out==='softmax'){ loss += -Math.log(y[Y[p]]+1e-12); var best=0; for(var k=1;k<y.length;k++) if(y[k]>y[best]) best=k; if(best===Y[p]) correct++; }
    else { var e=y[0]-Y[p]; loss+=0.5*e*e; } }
  return {loss:loss/n, acc:correct/n};
};
/* ---------- 데이터 ---------- */
L.spiral = function(n, seed, noise){
  var r=L.rng(seed||3), X=[], Y=[];
  for (var c=0;c<2;c++) for (var i=0;i<n;i++){
    var t=i/n*3.2+0.25, ang=t*2.0+c*Math.PI;
    X.push([t*Math.cos(ang)/3.4+(r.gauss()*(noise||0.05)), t*Math.sin(ang)/3.4+(r.gauss()*(noise||0.05))]); Y.push(c);
  }
  return {X:X,Y:Y};
};
L.moons = function(n, seed, noise){
  var r=L.rng(seed||5), X=[], Y=[];
  for (var i=0;i<n;i++){ var t=Math.PI*i/n;
    X.push([Math.cos(t)-0.5+r.gauss()*noise, Math.sin(t)-0.25+r.gauss()*noise]); Y.push(0);
    X.push([1-Math.cos(t)-0.5+r.gauss()*noise, 0.25-Math.sin(t)+r.gauss()*noise]); Y.push(1); }
  return {X:X,Y:Y};
};
/* ---------- 그래프 ---------- */
L.Plot = function(cv, o){
  this.cv=cv; this.o=o; this.ctx=cv.getContext('2d');
  this.pad = o.pad || {l:44,r:14,t:14,b:32};
  this.resize();
};
L.Plot.prototype.resize = function(){
  var cv=this.cv, dpr=Math.min(window.devicePixelRatio||1,2);
  var w=cv.clientWidth||cv.parentNode.clientWidth||600, h=Math.round(w*(this.o.ratio||0.5));
  if (this.o.minH) h=Math.max(h,this.o.minH); if (this.o.maxH) h=Math.min(h,this.o.maxH);
  cv.style.height=h+'px'; cv.width=Math.round(w*dpr); cv.height=Math.round(h*dpr);
  this.W=w; this.H=h; this.ctx.setTransform(dpr,0,0,dpr,0,0);
};
L.Plot.prototype.X = function(x){ var o=this.o,p=this.pad; return p.l+(x-o.x0)/(o.x1-o.x0)*(this.W-p.l-p.r); };
L.Plot.prototype.Y = function(y){ var o=this.o,p=this.pad; return this.H-p.b-(y-o.y0)/(o.y1-o.y0)*(this.H-p.t-p.b); };
L.Plot.prototype.clear = function(){
  var c=this.ctx,o=this.o,p=this.pad; c.clearRect(0,0,this.W,this.H); c.fillStyle='#fff'; c.fillRect(0,0,this.W,this.H);
  c.font='12px "IBM Plex Sans KR",sans-serif'; c.lineWidth=1;
  var gx=o.gx||niceStep(o.x1-o.x0), gy=o.gy||niceStep(o.y1-o.y0);
  c.strokeStyle='#eef1f6'; c.fillStyle='#7a8194';
  for (var x=Math.ceil(o.x0/gx)*gx; x<=o.x1+1e-9; x+=gx){ var X=this.X(x); c.beginPath(); c.moveTo(X,p.t); c.lineTo(X,this.H-p.b); c.stroke(); if(!o.noXlab) c.fillText(fmt(x, o.xfmt),X-8,this.H-p.b+16); }
  for (var y=Math.ceil(o.y0/gy)*gy; y<=o.y1+1e-9; y+=gy){ var Y=this.Y(y); c.beginPath(); c.moveTo(p.l,Y); c.lineTo(this.W-p.r,Y); c.stroke(); if(!o.noYlab) c.fillText(fmt(y, o.yfmt),4,Y+4); }
  c.strokeStyle='#b8bfcd';
  if (o.y0<0&&o.y1>0){ c.beginPath(); c.moveTo(p.l,this.Y(0)); c.lineTo(this.W-p.r,this.Y(0)); c.stroke(); }
  if (o.x0<0&&o.x1>0){ c.beginPath(); c.moveTo(this.X(0),p.t); c.lineTo(this.X(0),this.H-p.b); c.stroke(); }
  c.strokeRect(p.l,p.t,this.W-p.l-p.r,this.H-p.t-p.b);
  if (o.xlab){ c.fillStyle='#5d6577'; c.textAlign='right'; c.fillText(o.xlab,this.W-p.r-2,this.H-p.b-6); c.textAlign='left'; }
  if (o.ylab){ c.fillStyle='#5d6577'; c.fillText(o.ylab,p.l+6,p.t+14); }
};
function niceStep(r){ var s=Math.pow(10,Math.floor(Math.log10(r/5))); var m=r/5/s; return (m<1.5?1:m<3.5?2:m<7.5?5:10)*s; }
function fmt(v,f){ if (f) return f(v); var a=Math.abs(v); if (a===0) return '0'; if (a>=1000) return (v/1000).toFixed(a>=10000?0:1)+'k'; if (a<0.01) return v.toExponential(0); return +v.toFixed(2)+''; }
L.Plot.prototype.fn = function(f, color, w, dash){
  var c=this.ctx,o=this.o,n=Math.max(120,Math.round(this.W)); c.save(); c.beginPath(); c.strokeStyle=color; c.lineWidth=w||2.4; if(dash) c.setLineDash(dash);
  this.clip(); var started=false;
  for (var i=0;i<=n;i++){ var x=o.x0+(o.x1-o.x0)*i/n, y=f(x); if(!isFinite(y)){started=false;continue;} var X=this.X(x),Y=this.Y(y); if(!started){c.moveTo(X,Y);started=true;} else c.lineTo(X,Y); }
  c.stroke(); c.restore();
};
L.Plot.prototype.clip = function(){ var c=this.ctx,p=this.pad; c.beginPath(); c.rect(p.l,p.t,this.W-p.l-p.r,this.H-p.t-p.b); c.clip(); c.beginPath(); };
L.Plot.prototype.line = function(pts, color, w, dash){
  var c=this.ctx; c.save(); this.clip(); c.strokeStyle=color; c.lineWidth=w||2.2; if(dash) c.setLineDash(dash); c.beginPath();
  for (var i=0;i<pts.length;i++){ var X=this.X(pts[i][0]),Y=this.Y(pts[i][1]); if(i) c.lineTo(X,Y); else c.moveTo(X,Y);} c.stroke(); c.restore();
};
L.Plot.prototype.dots = function(pts, color, r, stroke){
  var c=this.ctx; c.save(); this.clip(); c.fillStyle=color;
  for (var i=0;i<pts.length;i++){ c.beginPath(); c.arc(this.X(pts[i][0]),this.Y(pts[i][1]),r||3.5,0,7); c.fill(); if(stroke){c.strokeStyle=stroke;c.lineWidth=1;c.stroke();} }
  c.restore();
};
L.Plot.prototype.vline = function(x,color,dash,label){ var c=this.ctx,p=this.pad; c.save(); c.strokeStyle=color; c.lineWidth=1.5; if(dash)c.setLineDash(dash); c.beginPath(); c.moveTo(this.X(x),p.t); c.lineTo(this.X(x),this.H-p.b); c.stroke(); if(label){c.fillStyle=color;c.font='12px "IBM Plex Sans KR",sans-serif';c.fillText(label,this.X(x)+4,p.t+14);} c.restore(); };
L.Plot.prototype.hline = function(y,color,dash,label){ var c=this.ctx,p=this.pad; c.save(); c.strokeStyle=color; c.lineWidth=1.5; if(dash)c.setLineDash(dash); c.beginPath(); c.moveTo(p.l,this.Y(y)); c.lineTo(this.W-p.r,this.Y(y)); c.stroke(); if(label){c.fillStyle=color;c.font='12px "IBM Plex Sans KR",sans-serif';c.fillText(label,p.l+6,this.Y(y)-5);} c.restore(); };
L.Plot.prototype.text = function(x,y,s,color,align,size){ var c=this.ctx; c.save(); c.fillStyle=color||'#1d2230'; c.font=(size||13)+'px "IBM Plex Sans KR",sans-serif'; c.textAlign=align||'left'; c.fillText(s,this.X(x),this.Y(y)); c.restore(); };
L.Plot.prototype.dot = function(x,y,color,r){ var c=this.ctx; c.save(); c.fillStyle=color; c.beginPath(); c.arc(this.X(x),this.Y(y),r||6,0,7); c.fill(); c.strokeStyle='#fff'; c.lineWidth=2; c.stroke(); c.restore(); };
L.Plot.prototype.bars = function(vals, colors, labels){
  var c=this.ctx,o=this.o,n=vals.length, w=(this.W-this.pad.l-this.pad.r)/n;
  for (var i=0;i<n;i++){ var x0=this.pad.l+i*w+w*0.15, bw=w*0.7, y=this.Y(Math.max(o.y0,Math.min(o.y1,vals[i]))), yb=this.Y(Math.max(o.y0,0));
    c.fillStyle=colors[i%colors.length]; c.fillRect(x0,Math.min(y,yb),bw,Math.abs(yb-y));
    if (labels){ c.fillStyle='#5d6577'; c.font='11px "IBM Plex Sans KR",sans-serif'; c.textAlign='center'; c.fillText(labels[i],x0+bw/2,this.H-this.pad.b+15); c.textAlign='left'; } }
};
/* 2D 분류 경계 칠하기 */
L.Plot.prototype.field = function(f, res){
  var c=this.ctx,o=this.o,p=this.pad, r=res||6;
  for (var px=p.l; px<this.W-p.r; px+=r) for (var py=p.t; py<this.H-p.b; py+=r){
    var x=o.x0+(px+r/2-p.l)/(this.W-p.l-p.r)*(o.x1-o.x0), y=o.y1-(py+r/2-p.t)/(this.H-p.t-p.b)*(o.y1-o.y0);
    var v=f(x,y); c.fillStyle = v>0.5 ? 'rgba(37,99,235,'+(0.08+0.22*(v-0.5)*2)+')' : 'rgba(32,34,43,'+(0.06+0.18*(0.5-v)*2)+')';
    c.fillRect(px,py,r,r);
  }
};
/* ---------- 공통 UI ---------- */
L.onResize = function(fn){ var t; window.addEventListener('resize',function(){ clearTimeout(t); t=setTimeout(fn,120); }); };
L.bindRange = function(id, fn, fmtFn){
  var el=document.getElementById(id), out=document.getElementById(id+'V');
  var h=function(){ var v=+el.value; if(out) out.textContent = fmtFn?fmtFn(v):v; fn(v); };
  el.addEventListener('input',h); return h;
};
L.seg = function(groupId, fn){
  var g=document.getElementById(groupId); if(!g) return;
  var bs=g.querySelectorAll('.bt');
  bs.forEach(function(b){ b.addEventListener('click',function(){ bs.forEach(function(x){x.setAttribute('aria-pressed','false');}); b.setAttribute('aria-pressed','true'); fn(b.getAttribute('data-v')); }); });
};
/* 퀴즈 */
L.quiz = function(){
  document.querySelectorAll('.qitem').forEach(function(q){
    var ans=q.getAttribute('data-ans'), fb=q.querySelector('.fb');
    q.querySelectorAll('.opts .bt').forEach(function(b){
      b.addEventListener('click',function(){
        var ok = b.getAttribute('data-v')===ans;
        q.querySelectorAll('.opts .bt').forEach(function(x){x.classList.remove('on');}); b.classList.add('on');
        fb.className='fb '+(ok?'ok':'no'); fb.innerHTML=(ok?'맞아요. ':'다시 생각해 볼까요? ')+(ok?q.getAttribute('data-ok'):q.getAttribute('data-no'));
      });
    });
  });
};
/* 라운드 판정과 점수판 */
var SC={u:0,b:0,hit:0,n:0}; L.hooks={}; L.score=SC;
L.rounds = function(){
  var board=document.getElementById('board');
  function draw(){ if(!board) return; board.querySelector('.u b').textContent=SC.u; board.querySelector('.b b').textContent=SC.b; board.querySelector('.me').textContent='내 예측 '+SC.hit+'/'+SC.n; }
  document.querySelectorAll('.round').forEach(function(r){
    var win=r.getAttribute('data-win'), done=false;
    r.querySelectorAll('.pick .bt').forEach(function(b){
      b.addEventListener('click',function(){
        if(done) return; done=true;
        if (L.hooks[r.id]){ var h=L.hooks[r.id](); win=h.win; r.setAttribute('data-win',win); var vt=r.querySelector('.vtext'); if(vt) vt.innerHTML=h.html; }
        var wt=r.querySelector('.wtxt'); if(wt) wt.textContent='판정: '+{u:'주판봇 USER팀 1점',b:'초파리와 features팀 1점',d:'무승부 · 두 팀 0.5점씩'}[win];
        var me=b.getAttribute('data-v'); r.classList.add('open','win-'+win);
        r.querySelectorAll('.pick .bt').forEach(function(x){x.disabled=true;}); b.classList.add('on');
        if (win==='u') SC.u+=1; else if (win==='b') SC.b+=1; else { SC.u+=0.5; SC.b+=0.5; }
        if (me!=='skip'){ SC.n++; if (me===win) SC.hit++; }
        var my=r.querySelector('.mine'); if(my) my.textContent = me==='skip' ? '' : (me===win ? '내 예측이 맞았어요.' : (win==='d'?'무승부예요. 두 팀 말이 반씩 맞았어요.':'내 예측과 판정이 달라요. 판정 이유를 읽어 보세요.'));
        draw(); L.fillSprites(r);
      });
    });
  });
  draw();
};
/* 용어 말풍선 */
L.tips = function(){
  var tip=document.getElementById('tip'); if(!tip) return;
  function show(e){ var t=e.currentTarget; tip.innerHTML='<b>'+t.textContent+'</b> — '+t.getAttribute('data-t'); tip.style.display='block';
    var r=t.getBoundingClientRect(), w=Math.min(300,window.innerWidth-20); tip.style.maxWidth=w+'px';
    var x=Math.min(window.innerWidth-w-10,Math.max(10,r.left)); tip.style.left=x+'px'; tip.style.top=(r.bottom+8)+'px'; }
  document.querySelectorAll('.jt').forEach(function(j){ j.setAttribute('tabindex','0'); j.addEventListener('mouseenter',show); j.addEventListener('focus',show); j.addEventListener('click',show);
    j.addEventListener('mouseleave',function(){tip.style.display='none';}); j.addEventListener('blur',function(){tip.style.display='none';}); });
  window.addEventListener('scroll',function(){tip.style.display='none';},{passive:true});
};
L.progress = function(){ var p=document.getElementById('prog'); if(!p) return; window.addEventListener('scroll',function(){ var h=document.documentElement; p.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%'; },{passive:true}); };
L.reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
L.init = function(){ L.fillSprites(); L.quiz(); L.rounds(); L.tips(); L.progress(); };
})();
window.face = function(k){ return k; };
/* 아주 작은 비율을 지수 표기 없이 읽기 쉽게 */
window.LAB.pct = function(v){ var p=v*100; if (!isFinite(p)) return '-'; if (p>=1000) return Math.round(p).toLocaleString('ko-KR')+'%'; if (p>=1) return p.toFixed(p>=10?0:1)+'%'; if (p>=1e-6){ var d=Math.min(8,-Math.floor(Math.log10(p))+1); return p.toFixed(d)+'%'; } return '0.000001%보다 작음(사실상 0)'; };
window.LAB.small = function(v){ var a=Math.abs(v); if (a===0) return '0'; if (a>=0.001 && a<1e6) return (+v.toPrecision(3)).toLocaleString('ko-KR'); if (a<0.001) return a<1e-8 ? '0.00000001보다 작음(사실상 0)' : v.toFixed(Math.min(10,-Math.floor(Math.log10(a))+1)); return Math.round(v).toLocaleString('ko-KR')+' (아주 큼)'; };
