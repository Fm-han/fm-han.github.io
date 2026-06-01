import re, os

scripts = {
'lottery': """const poolIn=document.createElement('textarea');poolIn.className='tool-textarea';poolIn.placeholder='输入参与名单，每行一个...';
const countIn=document.createElement('input');countIn.type='number';countIn.value='1';countIn.min='1';countIn.style='width:80px;padding:6px;border:1px solid #e0e0e0;border-radius:6px;font-size:14px;';
const btn=document.createElement('button');btn.className='tool-btn';btn.textContent='开始抽奖';
const result=document.createElement('div');result.className='tool-result';result.style.display='none';
const anim=document.createElement('div');anim.style='font-size:32px;text-align:center;margin:16px 0;color:#4285f4;font-weight:bold;display:none;';
const c=document.getElementById('toolContent');c.innerHTML='';
c.appendChild(document.createElement('div'));c.lastChild.className='tool-label';c.lastChild.textContent='参与名单';
c.appendChild(poolIn);
c.appendChild(document.createElement('div'));c.lastChild.className='tool-label';c.lastChild.textContent='抽取人数';c.lastChild.style.marginTop='12px';
c.appendChild(countIn);
c.appendChild(document.createElement('div'));c.lastChild.style.marginTop='8px';c.lastChild.appendChild(btn);
c.appendChild(anim);
c.appendChild(result);
btn.onclick=function(){
  const names=poolIn.value.split('\\n').map(s=>s.trim()).filter(s=>s);
  if(!names.length){alert('请输入参与名单');return;}
  const n=Math.min(parseInt(countIn.value)||1,names.length);
  result.style.display='none';anim.style.display='block';
  let steps=0,maxSteps=30;
  const iv=setInterval(()=>{
    anim.textContent=names[Math.floor(Math.random()*names.length)];
    steps++;if(steps>=maxSteps){clearInterval(iv);
      const winners=[];const copy=[...names];
      for(let j=0;j<n;j++){const idx=Math.floor(Math.random()*copy.length);winners.push(copy.splice(idx,1)[0]);}
      anim.style.display='none';result.style.display='block';
      result.innerHTML='<div style="font-size:18px;color:#176f2c;margin-bottom:8px;">🎉 中奖名单：</div>'+winners.map((w,i)=>'<div style="font-size:20px;padding:6px 0;">'+(i+1)+'. '+w+'</div>').join('');
    }
  },80);
};""",

'url-encode': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入内容</div><textarea class="tool-textarea" id="tin" placeholder="输入文本..."></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="enc()">URL 编码</button><button class="tool-btn" onclick="dec()">URL 解码</button><button class="tool-btn secondary" onclick="copyR()">复制结果</button></div><div class="tool-result" id="r" style="display:none;"></div>';
function enc(){const v=document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';r.innerText=encodeURIComponent(v);}
function dec(){const v=document.getElementById('tin').value;const r=document.getElementById('r');try{r.style.display='block';r.innerText=decodeURIComponent(v);}catch(e){r.innerText='解码失败：'+e.message;}}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'url-parser': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入 URL</div><input type="text" class="tool-textarea" id="tin" style="min-height:48px;" placeholder="https://example.com/path?query=1"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="parse()">解析</button></div><div class="tool-result" id="r" style="display:none;"></div>';
function parse(){const v=document.getElementById('tin').value;const r=document.getElementById('r');try{const u=new URL(v);r.style.display='block';r.innerHTML='协议: '+u.protocol+'\\n主机: '+u.host+'\\n主机名: '+u.hostname+'\\n端口: '+u.port+'\\n路径: '+u.pathname+'\\n查询: '+u.search+'\\n哈希: '+u.hash+'\\n参数:';new URLSearchParams(u.search).forEach((val,key)=>{r.innerHTML+='\\n  '+key+' = '+val;});}catch(e){r.style.display='block';r.innerText='解析失败：'+e.message;}}""",

'base64': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入内容</div><textarea class="tool-textarea" id="tin" placeholder="输入文本..."></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="enc()">Base64 编码</button><button class="tool-btn" onclick="dec()">Base64 解码</button><button class="tool-btn secondary" onclick="copyR()">复制结果</button></div><div class="tool-result" id="r" style="display:none;"></div>';
function enc(){const v=document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';r.innerText=btoa(unescape(encodeURIComponent(v)));}
function dec(){const v=document.getElementById('tin').value;const r=document.getElementById('r');try{r.style.display='block';r.innerText=decodeURIComponent(escape(atob(v)));}catch(e){r.innerText='解码失败：'+e.message;}}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'hash': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入内容</div><textarea class="tool-textarea" id="tin" placeholder="输入文本..."></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="calc(\\'MD5\\')">MD5</button><button class="tool-btn" onclick="calc(\\'SHA-1\\')">SHA-1</button><button class="tool-btn" onclick="calc(\\'SHA-256\\')">SHA-256</button></div><div class="tool-result" id="r" style="display:none;"></div>';
async function calc(algo){const v=document.getElementById('tin').value;const r=document.getElementById('r');const enc=new TextEncoder();const data=enc.encode(v);const hashName=algo==='MD5'?'MD5':algo==='SHA-1'?'SHA-1':'SHA-256';const buf=await crypto.subtle.digest(hashName,data);const arr=Array.from(new Uint8Array(buf));r.style.display='block';r.innerText=algo+': '+arr.map(b=>b.toString(16).padStart(2,'0')).join('');}""",

'html-entity': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入内容</div><textarea class="tool-textarea" id="tin" placeholder="输入 HTML 或文本..."></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="enc()">编码为 HTML 实体</button><button class="tool-btn" onclick="dec()">解码 HTML 实体</button><button class="tool-btn secondary" onclick="copyR()">复制结果</button></div><div class="tool-result" id="r" style="display:none;"></div>';
function enc(){const v=document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';r.innerText=v.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\\"/g,'&quot;');}
function dec(){const v=document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';r.innerText=v.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'\\"').replace(/&amp;/g,'&');}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'json-formatter': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入 JSON</div><textarea class="tool-textarea" id="tin" placeholder="粘贴 JSON..."></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="fmt()">格式化</button><button class="tool-btn" onclick="min()">压缩</button><button class="tool-btn secondary" onclick="copyR()">复制结果</button></div><div class="tool-result" id="r" style="display:none;"></div>';
function fmt(){const v=document.getElementById('tin').value;const r=document.getElementById('r');try{r.style.display='block';r.innerText=JSON.stringify(JSON.parse(v),null,2);}catch(e){r.innerText='JSON 错误：'+e.message;}}
function min(){const v=document.getElementById('tin').value;const r=document.getElementById('r');try{r.style.display='block';r.innerText=JSON.stringify(JSON.parse(v));}catch(e){r.innerText='JSON 错误：'+e.message;}}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'password-generator': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">密码长度：<span id="plen">16</span></div><input type="range" id="len" min="4" max="64" value="16" style="width:200px;" oninput="document.getElementById(\\'plen\\').innerText=this.value"><div class="tool-row" style="margin-top:8px;"><label><input type="checkbox" id="num" checked> 数字</label><label><input type="checkbox" id="lower" checked> 小写字母</label><label><input type="checkbox" id="upper"> 大写字母</label><label><input type="checkbox" id="sym"> 特殊符号</label></div><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="go()">生成密码</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;font-size:18px;"></div>';
function go(){let cs='';if(document.getElementById('num').checked)cs+='0123456789';if(document.getElementById('lower').checked)cs+='abcdefghijklmnopqrstuvwxyz';if(document.getElementById('upper').checked)cs+='ABCDEFGHIJKLMNOPQRSTUVWXYZ';if(document.getElementById('sym').checked)cs+='!@#$%^&*()_+-=[]{}|;:,.<>?';if(!cs){alert('请至少选一种字符');return;}const len=+document.getElementById('len').value;let s='';for(let i=0;i<len;i++)s+=cs[Math.floor(Math.random()*cs.length)];const r=document.getElementById('r');r.style.display='block';r.innerText=s;}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'uuid-list': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">生成数量</div><input type="number" id="cnt" value="5" min="1" max="100" style="width:80px;padding:6px;border:1px solid #e0e0e0;border-radius:6px;"><label style="margin-left:12px;font-size:14px;"><input type="checkbox" id="upper"> 大写</label><label style="margin-left:12px;font-size:14px;"><input type="checkbox" id="noDash"> 去除横线</label><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="go()">生成</button><button class="tool-btn secondary" onclick="copyR()">复制全部</button></div><div class="tool-result" id="r" style="display:none;"></div>';
function go(){const cnt=+document.getElementById('cnt').value;const upper=document.getElementById('upper').checked;const noDash=document.getElementById('noDash').checked;let h='';for(let i=0;i<cnt;i++){let u=crypto.randomUUID();if(upper)u=u.toUpperCase();if(noDash)u=u.replace(/-/g,'');h+=u+'\\n';}const r=document.getElementById('r');r.style.display='block';r.innerText=h.trim();}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'qrcode': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入内容</div><textarea class="tool-textarea" id="tin" placeholder="输入网址或文本..."></textarea><div class="tool-row" style="margin-top:8px;"><label style="font-size:14px;">尺寸：</label><select id="size" style="padding:6px;border:1px solid #e0e0e0;border-radius:6px;"><option value="150">150x150</option><option value="200" selected>200x200</option><option value="300">300x300</option><option value="400">400x400</option></select><button class="tool-btn" onclick="gen()" style="margin-left:12px;">生成二维码</button><button class="tool-btn secondary" onclick="dl()">下载</button></div><div id="r" style="text-align:center;margin-top:16px;"></div>';
function gen(){const v=document.getElementById('tin').value;const size=+document.getElementById('size').value;if(!v){alert('请输入内容');return;}const api='https://api.qrserver.com/v1/create-qr-code/?size='+size+'x'+size+'&data='+encodeURIComponent(v);document.getElementById('r').innerHTML='<img id="qimg" src="'+api+'" style="border:1px solid #eee;padding:8px;border-radius:8px;">';}
function dl(){const img=document.getElementById('qimg');if(!img){alert('先生成二维码');return;}const a=document.createElement('a');a.href=img.src;a.download='qrcode.png';a.click();}""",

'timestamp': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">当前时间戳（秒）</div><div style="font-size:28px;font-weight:bold;color:#4285f4;" id="tsSec"></div><div class="tool-label" style="margin-top:12px;">当前时间戳（毫秒）</div><div style="font-size:28px;font-weight:bold;color:#4285f4;" id="tsMs"></div><div class="tool-label" style="margin-top:16px;">时间戳转日期</div><input type="text" id="tin" placeholder="输入时间戳（秒或毫秒）" style="width:200px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;font-size:14px;"><button class="tool-btn" onclick="conv()" style="margin-left:8px;">转换</button><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function update(){const now=Date.now();document.getElementById('tsSec').innerText=Math.floor(now/1000);document.getElementById('tsMs').innerText=now;}
update();setInterval(update,1000);
function conv(){const v=document.getElementById('tin').value.trim();const r=document.getElementById('r');let ts=+v;if(v.length<=10)ts*=1000;const d=new Date(ts);r.style.display='block';r.innerText=d.toLocaleString('zh-CN',{hour12:false})+'\\n'+d.toISOString();}""",

'date-calculator': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">日期 A</div><input type="date" id="da" style="padding:8px;border:1px solid #e0e0e0;border-radius:6px;font-size:14px;"><div class="tool-label" style="margin-top:12px;">日期 B</div><input type="date" id="db" style="padding:8px;border:1px solid #e0e0e0;border-radius:6px;font-size:14px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="calc()">计算相差天数</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function calc(){const a=new Date(document.getElementById('da').value);const b=new Date(document.getElementById('db').value);if(isNaN(a)||isNaN(b)){alert('请选择两个日期');return;}const diff=Math.abs(b-a);const days=Math.ceil(diff/(1000*60*60*24));const r=document.getElementById('r');r.style.display='block';r.innerText='相差 '+days+' 天\\n约 '+Math.floor(days/30)+' 个月\\n约 '+Math.floor(days/365.25)+' 年';}""",

'countdown-timer': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">目标时间</div><input type="datetime-local" id="target" style="padding:8px;border:1px solid #e0e0e0;border-radius:6px;font-size:14px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="start()">开始倒计时</button><button class="tool-btn secondary" onclick="stop()">停止</button></div><div id="r" style="font-size:36px;text-align:center;margin-top:20px;color:#4285f4;font-weight:bold;"></div>';
let iv=null;
function start(){const t=new Date(document.getElementById('target').value);if(isNaN(t)){alert('请选择目标时间');return;}if(iv)clearInterval(iv);iv=setInterval(()=>{const now=Date.now();const diff=t-now;if(diff<=0){clearInterval(iv);document.getElementById('r').innerText='时间到！';return;}const d=Math.floor(diff/86400000);const h=Math.floor((diff%86400000)/3600000);const m=Math.floor((diff%3600000)/60000);const s=Math.floor((diff%60000)/1000);document.getElementById('r').innerText=d+'天 '+String(h).padStart(2,'0')+':'+String(m).padStart(2,'0')+':'+String(s).padStart(2,'0');},1000);}
function stop(){if(iv)clearInterval(iv);document.getElementById('r').innerText='';}""",

'stopwatch': """const c=document.getElementById('toolContent');
c.innerHTML='<div id="r" style="font-size:48px;text-align:center;margin:20px 0;color:#333;font-family:monospace;">00:00:00.000</div><div class="tool-row" style="justify-content:center;"><button class="tool-btn" onclick="start()">开始</button><button class="tool-btn secondary" onclick="pause()">暂停</button><button class="tool-btn secondary" onclick="reset()">重置</button></div>';
let startTime=0,elapsed=0,iv=null,running=false;
function fmt(ms){const h=Math.floor(ms/3600000);const m=Math.floor((ms%3600000)/60000);const s=Math.floor((ms%60000)/1000);const f=ms%1000;return String(h).padStart(2,'0')+':'+String(m).padStart(2,'0')+':'+String(s).padStart(2,'0')+'.'+String(f).padStart(3,'0');}
function tick(){elapsed=Date.now()-startTime;document.getElementById('r').innerText=fmt(elapsed);}
function start(){if(running)return;running=true;startTime=Date.now()-elapsed;iv=setInterval(tick,10);}
function pause(){if(!running)return;running=false;clearInterval(iv);}
function reset(){pause();elapsed=0;document.getElementById('r').innerText='00:00:00.000';}""",

'timezone-converter': """const c=document.getElementById('toolContent');
const zones=[{n:'北京时间',z:'Asia/Shanghai'},{n:'东京',z:'Asia/Tokyo'},{n:'纽约',z:'America/New_York'},{n:'伦敦',z:'Europe/London'},{n:'悉尼',z:'Australia/Sydney'},{n:'洛杉矶',z:'America/Los_Angeles'}];
c.innerHTML='<div class="tool-label">选择时间</div><input type="datetime-local" id="dt" style="padding:8px;border:1px solid #e0e0e0;border-radius:6px;font-size:14px;"><div class="tool-row" style="margin-top:8px;"><label>从：</label><select id="fz" style="padding:6px;">'+zones.map((z,i)=>'<option value="'+z.z+'">'+z.n+'</option>').join('')+'</select><label style="margin-left:12px;">到：</label><select id="tz" style="padding:6px;">'+zones.map((z,i)=>'<option value="'+z.z+'"'+(i===3?' selected':'')+'>'+z.n+'</option>').join('')+'</select><button class="tool-btn" onclick="conv()" style="margin-left:8px;">转换</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function conv(){const v=document.getElementById('dt').value;if(!v){alert('请选择时间');return;}const fz=document.getElementById('fz').value;const tz=document.getElementById('tz').value;const d=new Date(v);const utc=d.getTime()+d.getTimezoneOffset()*60000;const src=new Date(d.toLocaleString('en-US',{timeZone:fz}));const srcOff=src.getTime()-d.getTime();const tgt=new Date(utc+srcOff);const tgtStr=tgt.toLocaleString('zh-CN',{timeZone:tz,hour12:false});const r=document.getElementById('r');r.style.display='block';r.innerText='转换结果: '+tgtStr;}""",

'workday-calculator': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">开始日期</div><input type="date" id="s" style="padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:12px;">结束日期</div><input type="date" id="e" style="padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="calc()">计算工作日</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function calc(){const s=new Date(document.getElementById('s').value);const e=new Date(document.getElementById('e').value);if(isNaN(s)||isNaN(e)){alert('请选择日期');return;}let days=0;const cur=new Date(s);while(cur<=e){const wd=cur.getDay();if(wd!==0&&wd!==6)days++;cur.setDate(cur.getDate()+1);}const r=document.getElementById('r');r.style.display='block';r.innerText='工作日: '+days+' 天\\n总天数: '+((e-s)/86400000+1)+' 天';}""",

'word-counter': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入文本</div><textarea class="tool-textarea" id="tin" placeholder="粘贴文本..."></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="count()">统计</button><button class="tool-btn secondary" onclick="c()">清空</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function count(){const v=document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';const chars=v.length;const cn=v.match(/[\\u4e00-\\u9fa5]/g)||[];const words=v.trim().split(/\\s+/).filter(s=>s).length;r.innerText='字符总数: '+chars+'\\n中文字数: '+cn.length+'\\n单词数: '+words+'\\n行数: '+v.split('\\n').length;}
function c(){document.getElementById('tin').value='';document.getElementById('r').style.display='none';}""",

'regex-test': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">正则表达式</div><input type="text" id="re" placeholder="例如: [a-z]+" style="width:100%;padding:8px;border:1px solid #e0e0e0;border-radius:6px;font-family:monospace;font-size:14px;"><div class="tool-label" style="margin-top:12px;">测试文本</div><textarea class="tool-textarea" id="tin" placeholder="输入测试文本..."></textarea><div class="tool-row" style="margin-top:8px;"><label><input type="checkbox" id="gi" checked> 全局匹配</label><label><input type="checkbox" id="ci"> 忽略大小写</label><button class="tool-btn" onclick="test()" style="margin-left:12px;">测试</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function test(){const p=document.getElementById('re').value;const t=document.getElementById('tin').value;const r=document.getElementById('r');if(!p||!t){alert('请输入正则和文本');return;}try{let flags='';if(document.getElementById('gi').checked)flags+='g';if(document.getElementById('ci').checked)flags+='i';const re=new RegExp(p,flags);const m=t.match(re);r.style.display='block';if(m&&m.length){r.innerHTML='匹配 '+m.length+' 个结果:';m.forEach((x,i)=>r.innerHTML+='\\n'+(i+1)+'. '+x);}else{r.innerText='无匹配结果';}}catch(e){r.style.display='block';r.innerText='正则错误: '+e.message;}}""",

'markdown-editor': """const c=document.getElementById('toolContent');
c.innerHTML='<div style="display:flex;gap:12px;height:400px;"><textarea class="tool-textarea" id="tin" placeholder="输入 Markdown..." style="flex:1;height:100%;"></textarea><div id="preview" style="flex:1;height:100%;background:#f8f9fa;border:1px solid #e0e0e0;border-radius:8px;padding:12px;overflow:auto;font-size:14px;"></div></div><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="render()">预览</button><button class="tool-btn secondary" onclick="copyH()">复制 HTML</button></div>';
function render(){const v=document.getElementById('tin').value;let h=v;h=h.replace(new RegExp('^### (.*$)','gim'),'<h3>$1</h3>');h=h.replace(new RegExp('^## (.*$)','gim'),'<h2>$1</h2>');h=h.replace(new RegExp('^# (.*$)','gim'),'<h1>$1</h1>');h=h.replace(/\\*\\*(.*?)\\*\\*/g,'<strong>$1</strong>');h=h.replace(/\\*(.*?)\\*/g,'<em>$1</em>');h=h.replace(/\\`([^\\`]+)\\`/g,'<code style="background:#f0f0f0;padding:2px 4px;border-radius:3px;">$1</code>');h=h.replace(/\\n/g,'<br>');document.getElementById('preview').innerHTML=h;}
function copyH(){navigator.clipboard.writeText(document.getElementById('preview').innerHTML).then(()=>alert('已复制'));}""",

'slug-generator': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入标题或文本</div><textarea class="tool-textarea" id="tin" placeholder="例如：你好 世界！"></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="gen()">生成 Slug</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;"></div>';
function gen(){const v=document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';r.innerText=v.trim().toLowerCase().replace(/[^\\w\\u4e00-\\u9fa5\\s-]/g,'').replace(/\\s+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'');}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'color-convert': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入颜色</div><input type="text" id="tin" placeholder="#4285f4 或 rgb(66,133,244)" style="width:250px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><button class="tool-btn" onclick="conv()" style="margin-left:8px;">转换</button><div id="preview" style="width:100%;height:60px;border-radius:8px;margin-top:12px;display:none;"></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function conv(){const v=document.getElementById('tin').value.trim();const r=document.getElementById('r');const p=document.getElementById('preview');let hex='';if(v.startsWith('#')){hex=v;}else if(v.startsWith('rgb')){const m=v.match(/\\d+/g);if(m&&m.length>=3){hex='#'+m.slice(0,3).map(x=>parseInt(x).toString(16).padStart(2,'0')).join('');}}if(!hex){r.style.display='block';r.innerText='无法识别颜色格式';p.style.display='none';return;}p.style.display='block';p.style.background=hex;const rr=parseInt(hex.slice(1,3),16);const gg=parseInt(hex.slice(3,5),16);const bb=parseInt(hex.slice(5,7),16);r.style.display='block';r.innerText='HEX: '+hex+'\\nRGB: '+rr+', '+gg+', '+bb;}""",

'hex-rgb': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">HEX 颜色</div><input type="text" id="hex" placeholder="#4285f4" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><button class="tool-btn" onclick="toRgb()" style="margin-left:8px;">→ RGB</button><div class="tool-label" style="margin-top:12px;">RGB 颜色</div><input type="text" id="rgb" placeholder="66, 133, 244" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><button class="tool-btn" onclick="toHex()" style="margin-left:8px;">→ HEX</button><div id="preview" style="width:100%;height:60px;border-radius:8px;margin-top:12px;display:none;"></div>';
function toRgb(){const h=document.getElementById('hex').value.trim();const p=document.getElementById('preview');p.style.display='block';p.style.background=h;const r=parseInt(h.slice(1,3),16);const g=parseInt(h.slice(3,5),16);const b=parseInt(h.slice(5,7),16);document.getElementById('rgb').value=r+', '+g+', '+b;}
function toHex(){const v=document.getElementById('rgb').value;const m=v.match(/\\d+/g);if(m&&m.length>=3){const h='#'+m.slice(0,3).map(x=>parseInt(x).toString(16).padStart(2,'0')).join('');document.getElementById('hex').value=h;document.getElementById('preview').style.display='block';document.getElementById('preview').style.background=h;}}""",

'color-gradient': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">起始颜色</div><input type="color" id="c1" value="#4285f4" style="width:60px;height:40px;border:none;"><div class="tool-label" style="margin-top:12px;">结束颜色</div><input type="color" id="c2" value="#ea4335" style="width:60px;height:40px;border:none;"><div class="tool-row" style="margin-top:8px;"><label>步数：</label><input type="number" id="steps" value="5" min="2" max="20" style="width:60px;padding:6px;"><button class="tool-btn" onclick="gen()" style="margin-left:8px;">生成渐变</button></div><div id="r" style="margin-top:12px;"></div>';
function gen(){const s1=document.getElementById('c1').value;const s2=document.getElementById('c2').value;const n=+document.getElementById('steps').value;const r1=parseInt(s1.slice(1,3),16),g1=parseInt(s1.slice(3,5),16),b1=parseInt(s1.slice(5,7),16);const r2=parseInt(s2.slice(1,3),16),g2=parseInt(s2.slice(3,5),16),b2=parseInt(s2.slice(5,7),16);let h='';for(let i=0;i<n;i++){const t=i/(n-1);const rr=Math.round(r1+(r2-r1)*t);const gg=Math.round(g1+(g2-g1)*t);const bb=Math.round(b1+(b2-b1)*t);const col='#'+rr.toString(16).padStart(2,'0')+gg.toString(16).padStart(2,'0')+bb.toString(16).padStart(2,'0');h+='<div style="display:flex;align-items:center;gap:8px;margin:4px 0;"><div style="width:40px;height:40px;border-radius:6px;background:'+col+';"></div><span style="font-size:13px;color:#555;">'+col+'</span></div>';}document.getElementById('r').innerHTML=h;}""",

'color-blend': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">颜色 A</div><input type="color" id="c1" value="#ff0000" style="width:60px;height:40px;border:none;"><div class="tool-label" style="margin-top:12px;">颜色 B</div><input type="color" id="c2" value="#0000ff" style="width:60px;height:40px;border:none;"><div class="tool-label" style="margin-top:12px;">混合比例 A:B</div><input type="range" id="ratio" min="0" max="100" value="50" style="width:200px;"><span id="rv" style="margin-left:8px;font-size:14px;">50%</span><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="blend()">混合</button></div><div id="preview" style="width:100%;height:80px;border-radius:8px;margin-top:12px;display:none;"></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
document.getElementById('ratio').oninput=function(){document.getElementById('rv').innerText=this.value+'%';};
function blend(){const s1=document.getElementById('c1').value;const s2=document.getElementById('c2').value;const t=+document.getElementById('ratio').value/100;const r1=parseInt(s1.slice(1,3),16),g1=parseInt(s1.slice(3,5),16),b1=parseInt(s1.slice(5,7),16);const r2=parseInt(s2.slice(1,3),16),g2=parseInt(s2.slice(3,5),16),b2=parseInt(s2.slice(5,7),16);const rr=Math.round(r1+(r2-r1)*t);const gg=Math.round(g1+(g2-g1)*t);const bb=Math.round(b1+(b2-b1)*t);const col='#'+rr.toString(16).padStart(2,'0')+gg.toString(16).padStart(2,'0')+bb.toString(16).padStart(2,'0');document.getElementById('preview').style.display='block';document.getElementById('preview').style.background=col;const r=document.getElementById('r');r.style.display='block';r.innerText='混合结果: '+col+'\\nRGB: '+rr+', '+gg+', '+bb;}""",

'ip-lookup': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入 IP 地址（留空查询本机）</div><input type="text" id="tin" placeholder="例如：8.8.8.8" style="width:250px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><button class="tool-btn" onclick="lookup()" style="margin-left:8px;">查询</button><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function lookup(){const v=document.getElementById('tin').value.trim();const r=document.getElementById('r');r.style.display='block';r.innerText='正在查询...';fetch('https://ipapi.co/'+encodeURIComponent(v||'')+'/json/').then(x=>x.json()).then(d=>{r.innerText='IP: '+(d.ip||v||'N/A')+'\\n城市: '+(d.city||'N/A')+'\\n地区: '+(d.region||'N/A')+'\\n国家: '+(d.country_name||'N/A')+'\\n运营商: '+(d.org||'N/A')+'\\n时区: '+(d.timezone||'N/A');}).catch(e=>{r.innerText='查询失败，请重试';});}""",

'mime-types': """const c=document.getElementById('toolContent');
const mimes={'.html':'text/html','.htm':'text/html','.css':'text/css','.js':'application/javascript','.json':'application/json','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.gif':'image/gif','.svg':'image/svg+xml','.pdf':'application/pdf','.zip':'application/zip','.txt':'text/plain','.xml':'application/xml','.mp3':'audio/mpeg','.mp4':'video/mp4','.woff':'font/woff','.woff2':'font/woff2'};
c.innerHTML='<div class="tool-label">输入文件扩展名</div><input type="text" id="tin" placeholder="例如：.png 或 png" style="width:200px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><button class="tool-btn" onclick="lookup()" style="margin-left:8px;">查询</button><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div><div style="margin-top:16px;font-size:13px;color:#888;">常用类型: '+Object.keys(mimes).slice(0,10).join(', ')+'...</div>';
function lookup(){const v=document.getElementById('tin').value.trim().toLowerCase();const ext=v.startsWith('.')?v:'.'+v;const r=document.getElementById('r');r.style.display='block';r.innerText=mimes[ext]||'未知类型（未收录）';}""",

'char-encoding': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入文本</div><textarea class="tool-textarea" id="tin" placeholder="输入文本..."></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="toUni()">转 Unicode</button><button class="tool-btn" onclick="fromUni()">Unicode 转文本</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function toUni(){const v=document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';r.innerText=Array.from(v).map(ch=>'U+'+ch.codePointAt(0).toString(16).toUpperCase().padStart(4,'0')).join(' ');}
function fromUni(){const v=document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';r.innerText=v.replace(/U\\+/gi,'').split(/\\s+/).map(h=>String.fromCodePoint(parseInt(h,16))).join('');}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'base-converter': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入数值</div><input type="text" id="tin" placeholder="输入数字" style="width:200px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><label>从：</label><select id="fb" style="padding:6px;"><option value="10">十进制</option><option value="2">二进制</option><option value="8">八进制</option><option value="16">十六进制</option></select><label style="margin-left:12px;">到：</label><select id="tb" style="padding:6px;"><option value="2">二进制</option><option value="8">八进制</option><option value="10">十进制</option><option value="16" selected>十六进制</option></select><button class="tool-btn" onclick="conv()" style="margin-left:8px;">转换</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function conv(){const v=document.getElementById('tin').value.trim();const fb=+document.getElementById('fb').value;const tb=+document.getElementById('tb').value;const r=document.getElementById('r');try{const dec=parseInt(v,fb);if(isNaN(dec)){r.style.display='block';r.innerText='无效的数字';return;}r.style.display='block';r.innerText=dec.toString(tb).toUpperCase();}catch(e){r.style.display='block';r.innerText='转换失败：'+e.message;}}""",

'binary-converter': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入数值</div><input type="text" id="tin" placeholder="输入数字" style="width:200px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="toBin()">→ 二进制</button><button class="tool-btn" onclick="fromBin()">二进制 →</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function toBin(){const v=+document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';r.innerText=v.toString(2);}
function fromBin(){const v=document.getElementById('tin').value.trim();const r=document.getElementById('r');r.style.display='block';r.innerText=parseInt(v,2);}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'ascii-art': """const c=document.getElementById('toolContent');
const font={'A':['  ##  ',' #  # ','######','#    #','#    #'],'B':['##### ','#    #','##### ','#    #','##### '],'C':[' #####','#     ','#     ','#     ',' #####'],'D':['##### ','#    #','#    #','#    #','##### '],'E':['######','#     ','##### ','#     ','######'],'F':['######','#     ','##### ','#     ','#     '],'G':[' #####','#     ','#  ###','#    #',' #####'],'H':['#    #','#    #','######','#    #','#    #'],'I':['######','  ##  ','  ##  ','  ##  ','######'],'J':['     #','     #','     #','#    #',' #####'],'K':['#    #','#   # ','####  ','#   # ','#    #'],'L':['#     ','#     ','#     ','#     ','######'],'M':['#    #','##  ##','# ## #','#    #','#    #'],'N':['#    #','##   #','# #  #','#  # #','#   ##'],'O':[' #### ','#    #','#    #','#    #',' #### '],'P':['##### ','#    #','##### ','#     ','#     '],'Q':[' #### ','#    #','#    #','#  # #',' #### '],'R':['##### ','#    #','##### ','#   # ','#    #'],'S':[' #####','#     ',' #####','     #','##### '],'T':['######','  ##  ','  ##  ','  ##  ','  ##  '],'U':['#    #','#    #','#    #','#    #',' #### '],'V':['#    #','#    #','#    #',' #  # ','  ##  '],'W':['#    #','#    #','# ## #','##  ##','#    #'],'X':['#    #',' #  # ','  ##  ',' #  # ','#    #'],'Y':['#    #',' #  # ','  ##  ','  ##  ','  ##  '],'Z':['######','    # ','   #  ','  #   ','######']};
c.innerHTML='<div class="tool-label">输入文本（建议大写英文字母）</div><textarea class="tool-textarea" id="tin" placeholder="输入文本..."></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="gen()">生成 ASCII 艺术</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;font-family:monospace;white-space:pre;"></div>';
function gen(){const v=document.getElementById('tin').value.toUpperCase();const r=document.getElementById('r');let lines=['','','','',''];for(const ch of v){const art=font[ch]||['      ','      ','  ??  ','      ','      '];for(let i=0;i<5;i++)lines[i]+=art[i]+'  ';}r.style.display='block';r.innerText=lines.join('\\n');}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'cron-parser': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入 Cron 表达式</div><input type="text" id="tin" placeholder="* * * * *" style="width:200px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;font-family:monospace;"><div style="font-size:12px;color:#888;margin-top:4px;">格式：分 时 日 月 周</div><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="parse()">解析</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function parse(){const v=document.getElementById('tin').value.trim();const r=document.getElementById('r');if(!v){alert('请输入表达式');return;}const p=v.split(/\\s+/);if(p.length!==5){r.style.display='block';r.innerText='格式错误，需要5个字段（分 时 日 月 周）';return;}const labels=['分钟','小时','日期','月份','星期'];r.style.display='block';r.innerText=p.map((x,i)=>labels[i]+': '+x).join('\\n')+'\\n\\n常用示例：\\n0 0 * * *  每天午夜\\n*/5 * * * *  每5分钟\\n0 9 * * 1  每周一早9点';}""",

'crontab-generator': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">分钟 (0-59)</div><input type="text" id="m" value="0" style="width:100px;padding:6px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:8px;">小时 (0-23)</div><input type="text" id="h" value="0" style="width:100px;padding:6px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:8px;">日期 (1-31, *表示每天)</div><input type="text" id="d" value="*" style="width:100px;padding:6px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:8px;">月份 (1-12, *表示每月)</div><input type="text" id="mo" value="*" style="width:100px;padding:6px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:8px;">星期 (0-6, *表示每天, 0=周日)</div><input type="text" id="w" value="*" style="width:100px;padding:6px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="gen()">生成 Cron 表达式</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;font-family:monospace;"></div>';
function gen(){const m=document.getElementById('m').value;const h=document.getElementById('h').value;const d=document.getElementById('d').value;const mo=document.getElementById('mo').value;const w=document.getElementById('w').value;const r=document.getElementById('r');r.style.display='block';r.innerText=m+' '+h+' '+d+' '+mo+' '+w;}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'bmi-calculator': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">身高（厘米）</div><input type="number" id="h" placeholder="170" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:12px;">体重（公斤）</div><input type="number" id="w" placeholder="65" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="calc()">计算 BMI</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function calc(){const h=+document.getElementById('h').value/100;const w=+document.getElementById('w').value;if(!h||!w){alert('请输入身高和体重');return;}const bmi=(w/(h*h)).toFixed(1);let status='';if(bmi<18.5)status='偏瘦';else if(bmi<24)status='正常';else if(bmi<28)status='超重';else status='肥胖';const r=document.getElementById('r');r.style.display='block';r.innerText='BMI: '+bmi+'\\n状态: '+status;}""",

'loan-calculator': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">贷款金额（万元）</div><input type="number" id="amt" value="100" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:12px;">年利率（%）</div><input type="number" id="rate" value="4.2" step="0.1" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:12px;">贷款期限（年）</div><input type="number" id="years" value="30" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="calc()">计算月供</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function calc(){const p=+document.getElementById('amt').value*10000;const r=+document.getElementById('rate').value/100/12;const n=+document.getElementById('years').value*12;const monthly=(p*r*Math.pow(1+r,n))/(Math.pow(1+r,n)-1);const total=monthly*n;const interest=total-p;const res=document.getElementById('r');res.style.display='block';res.innerText='月供: '+monthly.toFixed(2)+' 元\\n还款总额: '+total.toFixed(2)+' 元\\n利息总额: '+interest.toFixed(2)+' 元';}""",

'tax-calculator': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">税前月收入（元）</div><input type="number" id="income" value="10000" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:12px;">五险一金扣除（元）</div><input type="number" id="deduct" value="2000" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:12px;">专项附加扣除（元）</div><input type="number" id="special" value="0" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="calc()">计算个税</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function calc(){const income=+document.getElementById('income').value;const deduct=+document.getElementById('deduct').value;const special=+document.getElementById('special').value;const taxable=income-5000-deduct-special;if(taxable<=0){document.getElementById('r').style.display='block';document.getElementById('r').innerText='应纳税所得额: 0\\n个税: 0 元\\n税后收入: '+income.toFixed(2)+' 元';return;}let tax=0;if(taxable<=3000)tax=taxable*0.03;else if(taxable<=12000)tax=taxable*0.1-210;else if(taxable<=25000)tax=taxable*0.2-1410;else if(taxable<=35000)tax=taxable*0.25-2660;else if(taxable<=55000)tax=taxable*0.3-4410;else if(taxable<=80000)tax=taxable*0.35-7160;else tax=taxable*0.45-15160;const r=document.getElementById('r');r.style.display='block';r.innerText='应纳税所得额: '+taxable.toFixed(2)+' 元\\n个税: '+tax.toFixed(2)+' 元\\n税后收入: '+(income-tax).toFixed(2)+' 元';}""",

'exchange-rate': """const c=document.getElementById('toolContent');
const rates={'CNY':1,'USD':7.2,'EUR':7.8,'JPY':0.048,'GBP':9.1,'HKD':0.92,'KRW':0.0053,'AUD':4.7};
c.innerHTML='<div class="tool-label">金额</div><input type="number" id="amt" value="100" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><label>从：</label><select id="fc" style="padding:6px;">'+Object.keys(rates).map(k=>'<option value="'+k+'"'+(k==='USD'?' selected':'')+'>'+k+'</option>').join('')+'</select><label style="margin-left:12px;">到：</label><select id="tc" style="padding:6px;">'+Object.keys(rates).map(k=>'<option value="'+k+'"'+(k==='CNY'?' selected':'')+'>'+k+'</option>').join('')+'</select><button class="tool-btn" onclick="conv()" style="margin-left:8px;">换算</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div><div style="margin-top:12px;font-size:12px;color:#888;">注：汇率为参考值，非实时</div>';
function conv(){const amt=+document.getElementById('amt').value;const fc=document.getElementById('fc').value;const tc=document.getElementById('tc').value;const cny=amt*rates[fc];const res=cny/rates[tc];const r=document.getElementById('r');r.style.display='block';r.innerText=amt+' '+fc+' = '+res.toFixed(2)+' '+tc;}""",

'calorie-calculator': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">体重（公斤）</div><input type="number" id="w" value="65" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:12px;">身高（厘米）</div><input type="number" id="h" value="170" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:12px;">年龄</div><input type="number" id="a" value="30" style="width:150px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-label" style="margin-top:12px;">性别</div><select id="g" style="padding:6px;"><option value="m">男</option><option value="f">女</option></select><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="calc()">计算基础代谢</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function calc(){const w=+document.getElementById('w').value;const h=+document.getElementById('h').value;const a=+document.getElementById('a').value;const g=document.getElementById('g').value;let bmr=0;if(g==='m')bmr=88.362+(13.397*w)+(4.799*h)-(5.677*a);else bmr=447.593+(9.247*w)+(3.098*h)-(4.330*a);const r=document.getElementById('r');r.style.display='block';r.innerText='基础代谢率 (BMR): '+bmr.toFixed(0)+' 千卡/天\\n久坐: '+(bmr*1.2).toFixed(0)+'\\n轻度活动: '+(bmr*1.375).toFixed(0)+'\\n中度活动: '+(bmr*1.55).toFixed(0)+'\\n重度活动: '+(bmr*1.725).toFixed(0);}""",

'age-calculator': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">出生日期</div><input type="date" id="bd" style="padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="calc()">计算年龄</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function calc(){const bd=new Date(document.getElementById('bd').value);if(isNaN(bd)){alert('请选择出生日期');return;}const now=new Date();let years=now.getFullYear()-bd.getFullYear();let months=now.getMonth()-bd.getMonth();let days=now.getDate()-bd.getDate();if(days<0){months--;days+=30;}if(months<0){years--;months+=12;}const r=document.getElementById('r');r.style.display='block';r.innerText='年龄: '+years+' 岁 '+months+' 个月\\n约 '+Math.floor((now-bd)/31536000000)+' 岁\\n出生天数: '+Math.floor((now-bd)/86400000)+' 天';}""",

'caesar-cipher': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入文本</div><textarea class="tool-textarea" id="tin" placeholder="输入文本..."></textarea><div class="tool-label" style="margin-top:8px;">位移量</div><input type="number" id="shift" value="3" min="1" max="25" style="width:80px;padding:6px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="enc()">加密</button><button class="tool-btn" onclick="dec()">解密</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function caesar(s,shift,enc){let r='';for(const ch of s){const code=ch.charCodeAt(0);if(code>=65&&code<=90){const base=65;const offset=enc?(code-base+shift)%26:(code-base-shift+26)%26;r+=String.fromCharCode(base+offset);}else if(code>=97&&code<=122){const base=97;const offset=enc?(code-base+shift)%26:(code-base-shift+26)%26;r+=String.fromCharCode(base+offset);}else{r+=ch;}}return r;}
function enc(){const v=document.getElementById('tin').value;const s=+document.getElementById('shift').value;const r=document.getElementById('r');r.style.display='block';r.innerText=caesar(v,s,true);}
function dec(){const v=document.getElementById('tin').value;const s=+document.getElementById('shift').value;const r=document.getElementById('r');r.style.display='block';r.innerText=caesar(v,s,false);}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'morse-code': """const c=document.getElementById('toolContent');
const morse={'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.','0':'-----'};
const rev={};for(const k in morse)rev[morse[k]]=k;
c.innerHTML='<div class="tool-label">输入文本</div><textarea class="tool-textarea" id="tin" placeholder="输入英文字母或摩斯电码..."></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="toMorse()">→ 摩斯电码</button><button class="tool-btn" onclick="fromMorse()">摩斯电码 →</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function toMorse(){const v=document.getElementById('tin').value.toUpperCase();const r=document.getElementById('r');r.style.display='block';r.innerText=v.split('').map(ch=>morse[ch]||ch).join(' ');}
function fromMorse(){const v=document.getElementById('tin').value.trim();const r=document.getElementById('r');r.style.display='block';r.innerText=v.split(/\\s+/).map(x=>rev[x]||x).join('');}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'emoji-picker': """const c=document.getElementById('toolContent');
const emojis=['😀','😂','😍','🤔','😎','😭','😡','👍','👎','👏','🙏','💪','❤️','💔','🔥','⭐','🎉','🎁','🚀','💡','🌈','☀️','🌙','⚡','☕','🍎','🍕','🍺','🎵','📱','💻','🔒','🔑','✅','❌','➡️','⬅️','⬆️','⬇️','⚠️','❓','❗','✨','💯','🆗'];
c.innerHTML='<div class="tool-label">点击复制表情</div><div id="grid" style="display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;"></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
const grid=document.getElementById('grid');
emojis.forEach(e=>{const d=document.createElement('div');d.style='font-size:28px;cursor:pointer;padding:8px;border-radius:8px;border:1px solid #eee;text-align:center;min-width:40px;';d.textContent=e;d.onclick=()=>{navigator.clipboard.writeText(e).then(()=>{const r=document.getElementById('r');r.style.display='block';r.innerText='已复制: '+e;});};grid.appendChild(d);});""",

'lipsum-generator': """const c=document.getElementById('toolContent');
const words=['lorem','ipsum','dolor','sit','amet','consectetur','adipiscing','elit','sed','do','eiusmod','tempor','incididunt','ut','labore','et','dolore','magna','aliqua','ut','enim','ad','minim','veniam','quis','nostrud','exercitation','ullamco','laboris','nisi','ut','aliquip','ex','ea','commodo','consequat'];
c.innerHTML='<div class="tool-label">段落数量</div><input type="number" id="cnt" value="3" min="1" max="20" style="width:80px;padding:6px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="gen()">生成</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function gen(){const cnt=+document.getElementById('cnt').value;let h='';for(let p=0;p<cnt;p++){let sent='';for(let s=0;s<5;s++){let w=[];for(let i=0;i<10+Math.floor(Math.random()*10);i++)w.push(words[Math.floor(Math.random()*words.length)]);sent+=w.join(' ')+'. ';}h+='<p style="margin:8px 0;">'+sent+'</p>';}const r=document.getElementById('r');r.style.display='block';r.innerHTML=h;}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'chinese-number-game': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入阿拉伯数字</div><input type="number" id="tin" value="12345" style="width:200px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="toCn()">转中文大写</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
const cnNums=['零','壹','贰','叁','肆','伍','陆','柒','捌','玖'];const cnUnits=['','拾','佰','仟'];const cnBigUnits=['','万','亿'];
function toCn(){const n=+document.getElementById('tin').value;const r=document.getElementById('r');if(n===0){r.style.display='block';r.innerText='中文大写: 零';return;}const s=String(n);let res='';let gi=0;for(let i=s.length;i>0;i-=4){const g=s.slice(Math.max(0,i-4),i);let gr='';let z=false;for(let j=0;j<g.length;j++){const d=+g[j];const p=g.length-1-j;if(d===0){if(!z&&gr)gr+=cnNums[0];z=true;}else{gr+=cnNums[d]+cnUnits[p];z=false;}}if(gr)res=gr+cnBigUnits[gi]+res;gi++;}r.style.display='block';r.innerText='中文大写: '+res.replace(/零+/g,'零').replace(/零$/,'');}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'number-to-chinese': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入数字</div><input type="number" id="tin" value="2024" style="width:200px;padding:8px;border:1px solid #e0e0e0;border-radius:6px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="toCn()">转中文</button><button class="tool-btn" onclick="toCnUpper()">转中文大写</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
const nums=['零','一','二','三','四','五','六','七','八','九'];const units=['','十','百','千'];const bigUnits=['','万','亿'];
const upNums=['零','壹','贰','叁','肆','伍','陆','柒','捌','玖'];const upUnits=['','拾','佰','仟'];const upBigUnits=['','万','亿'];
function numToCn(n,upper){const ns=upper?upNums:nums;const us=upper?upUnits:units;const bus=upper?upBigUnits:bigUnits;if(n===0)return ns[0];const s=String(n);let res='';let gi=0;for(let i=s.length;i>0;i-=4){const g=s.slice(Math.max(0,i-4),i);let gr='';let z=false;for(let j=0;j<g.length;j++){const d=+g[j];const p=g.length-1-j;if(d===0){if(!z&&gr)gr+=ns[0];z=true;}else{gr+=ns[d]+us[p];z=false;}}if(gr)res=gr+bus[gi]+res;gi++;}return res.replace(/零+/g,'零').replace(/零$/,'');}
function toCn(){const n=+document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';r.innerText='中文: '+numToCn(n,false);}
function toCnUpper(){const n=+document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';r.innerText='中文大写: '+numToCn(n,true);}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'pinyin-converter': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入中文</div><textarea class="tool-textarea" id="tin" placeholder="输入中文..."></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="conv()">提取拼音首字母</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div><div style="margin-top:12px;font-size:12px;color:#888;">注：本工具仅提取拼音首字母，完整拼音需服务端支持</div>';
function conv(){const v=document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';const map={'\u4e00':'y','\u4e8c':'e','\u4e09':'s','\u56db':'s','\u4e94':'w','\u516d':'l','\u4e03':'q','\u516b':'b','\u4e5d':'j','\u5341':'s'};let h='';for(const ch of v){const code=ch.charCodeAt(0);if(code>=0x4e00&&code<=0x9fa5){h+=map[ch]||'('+ch+')';}else{h+=ch;}}r.innerText=h;}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'pomodoro': """const c=document.getElementById('toolContent');
c.innerHTML='<div id="r" style="font-size:64px;text-align:center;margin:20px 0;color:#4285f4;font-weight:bold;">25:00</div><div class="tool-row" style="justify-content:center;"><button class="tool-btn" onclick="start()">开始</button><button class="tool-btn secondary" onclick="pause()">暂停</button><button class="tool-btn secondary" onclick="reset()">重置</button></div><div style="text-align:center;margin-top:12px;font-size:14px;color:#888;">工作25分钟 → 休息5分钟</div>';
let sec=1500,iv=null,running=false;
function fmt(s){const m=Math.floor(s/60);return String(m).padStart(2,'0')+':'+String(s%60).padStart(2,'0');}
function tick(){sec--;document.getElementById('r').innerText=fmt(sec);if(sec<=0){clearInterval(iv);running=false;document.getElementById('r').innerText='时间到！';alert('番茄钟结束！');}}
function start(){if(running)return;running=true;iv=setInterval(tick,1000);}
function pause(){if(!running)return;running=false;clearInterval(iv);}
function reset(){pause();sec=1500;document.getElementById('r').innerText='25:00';}""",

'roll-call': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入人员名单（每行一个）</div><textarea class="tool-textarea" id="tin" placeholder="张三\\n李四\\n王五"></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="start()">开始点名</button><button class="tool-btn secondary" onclick="reset()">重置</button></div><div id="r" style="font-size:36px;text-align:center;margin-top:20px;color:#4285f4;font-weight:bold;display:none;"></div>';
let iv=null;
function start(){const names=document.getElementById('tin').value.split('\\n').map(s=>s.trim()).filter(s=>s);if(!names.length){alert('请输入名单');return;}if(iv)clearInterval(iv);const r=document.getElementById('r');r.style.display='block';let cnt=0;iv=setInterval(()=>{r.innerText=names[Math.floor(Math.random()*names.length)];cnt++;if(cnt>=20){clearInterval(iv);}},80);}
function reset(){if(iv)clearInterval(iv);document.getElementById('r').style.display='none';}""",

'image-base64': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">选择图片文件</div><input type="file" id="file" accept="image/*" style="padding:8px;"><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="convert()">转 Base64</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;word-break:break-all;max-height:300px;overflow:auto;"></div><img id="preview" style="max-width:200px;max-height:200px;margin-top:12px;display:none;border-radius:8px;">';
function convert(){const f=document.getElementById('file').files[0];if(!f){alert('请选择图片');return;}const r=document.getElementById('r');const reader=new FileReader();reader.onload=function(e){r.style.display='block';r.innerText=e.target.result;document.getElementById('preview').src=e.target.result;document.getElementById('preview').style.display='block';};reader.readAsDataURL(f);}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'yaml-converter': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入 YAML / JSON</div><textarea class="tool-textarea" id="tin" placeholder="输入 YAML 或 JSON..."></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="toJson()">→ JSON</button><button class="tool-btn" onclick="toYaml()">→ YAML</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div><div style="margin-top:8px;font-size:12px;color:#888;">注：YAML 转 JSON 为简化实现</div>';
function toJson(){const v=document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';const lines=v.split('\\n');const obj={};let current=obj;const stack=[obj];for(const line of lines){const m=line.match(/^(\\s*)(\\w+):\\s*(.*)$/);if(m){const key=m[2];const val=m[3].trim();if(!val){current[key]={};current=current[key];stack.push(current);}else{current[key]=isNaN(+val)?val:+val;}}}r.innerText=JSON.stringify(obj,null,2);}
function toYaml(){const v=document.getElementById('tin').value;const r=document.getElementById('r');try{const obj=JSON.parse(v);r.style.display='block';r.innerText=jsonToYaml(obj);}catch(e){r.innerText='JSON 解析失败: '+e.message;}}
function jsonToYaml(obj,indent=0){const sp=' '.repeat(indent);let s='';for(const k in obj){const v=obj[k];if(typeof v==='object'&&v!==null){s+=sp+k+':\\n'+jsonToYaml(v,indent+2);}else{s+=sp+k+': '+v+'\\n';}}return s;}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'xml-formatter': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入 XML</div><textarea class="tool-textarea" id="tin" placeholder="<root>\\n  <item>value</item>\\n</root>"></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="fmt()">格式化</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;white-space:pre;"></div>';
function fmt(){const v=document.getElementById('tin').value;const r=document.getElementById('r');r.style.display='block';r.innerText=v.replace(/>\\s*</g,'>\\n<').split('\\n').map(line=>{const open=(line.match(/<[^/\\s][^>]*>/g)||[]).length;const close=(line.match(/<\\//g)||[]).length;return '  '.repeat(Math.max(0,open-close))+line.trim();}).join('\\n');}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",

'jwt-decoder': """const c=document.getElementById('toolContent');
c.innerHTML='<div class="tool-label">输入 JWT Token</div><textarea class="tool-textarea" id="tin" placeholder="eyJhbGciOiJIUzI1NiIs..."></textarea><div class="tool-row" style="margin-top:8px;"><button class="tool-btn" onclick="decode()">解码</button><button class="tool-btn secondary" onclick="copyR()">复制</button></div><div class="tool-result" id="r" style="display:none;margin-top:8px;"></div>';
function b64Decode(s){s+='=='.slice(0,(4-s.length%4)%4);return decodeURIComponent(escape(atob(s.replace(/-/g,'+').replace(/_/g,'/'))));}
function decode(){const v=document.getElementById('tin').value.trim();const r=document.getElementById('r');if(!v){alert('请输入JWT');return;}const parts=v.split('.');if(parts.length!==3){r.style.display='block';r.innerText='格式错误：JWT应有3部分';return;}try{const header=JSON.stringify(JSON.parse(b64Decode(parts[0])),null,2);const payload=JSON.stringify(JSON.parse(b64Decode(parts[1])),null,2);r.style.display='block';r.innerText='HEADER:\\n'+header+'\\n\\nPAYLOAD:\\n'+payload;}catch(e){r.style.display='block';r.innerText='解码失败: '+e.message;}}
function copyR(){navigator.clipboard.writeText(document.getElementById('r').innerText).then(()=>alert('已复制'));}""",
}

fixed = 0
for url, script in scripts.items():
    fn = url + '.html'
    if not os.path.exists(fn):
        print('MISSING:', fn)
        continue
    with open(fn, 'r', encoding='utf-8') as f:
        html = f.read()
    idx = html.rfind('<script>')
    if idx == -1:
        print('NO SCRIPT:', fn)
        continue
    end_idx = html.rfind('</script>')
    new_html = html[:idx + 8] + '\n' + script + '\n' + html[end_idx:]
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(new_html)
    fixed += 1
    print('FIXED:', fn)

print('Total fixed:', fixed)
