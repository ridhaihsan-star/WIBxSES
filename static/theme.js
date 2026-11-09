// Tema terang/gelap. Dimuat sinkron di <head> agar halaman tidak berkedip putih; pilihan disimpan per browser,
// bila belum pernah memilih mengikuti pengaturan perangkat.
(()=>{const KEY='wib-theme',root=document.documentElement,dark=matchMedia('(prefers-color-scheme: dark)');
let saved=()=>{try{return localStorage.getItem(KEY)}catch(e){return null}};
const MOON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>',
SUN='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
function apply(t){root.dataset.theme=t;document.querySelectorAll('.theme-toggle').forEach(b=>{let d=t==='dark';b.innerHTML=b.classList.contains('theme-switch')?`${MOON}<span class="ts-label">Mode gelap</span><span class="ts-track"><i></i></span>`:d?SUN:MOON;b.setAttribute('aria-checked',d);b.title=d?'Ganti ke mode terang':'Ganti ke mode gelap';b.setAttribute('aria-label',b.title)})}
apply(saved()||(dark.matches?'dark':'light'));
dark.addEventListener?.('change',e=>{if(!saved())apply(e.matches?'dark':'light')});
document.addEventListener('DOMContentLoaded',()=>{apply(root.dataset.theme);document.querySelectorAll('.theme-toggle').forEach(b=>b.addEventListener('click',()=>{let t=root.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem(KEY,t)}catch(e){}apply(t)}))})})();
