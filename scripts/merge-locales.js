#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const getArg = (name) => {
  const i = args.indexOf(name);
  return i === -1 ? null : args[i + 1];
};
const STAR_DIR = path.resolve(getArg('--star') || '');
const RAW_DIR  = path.resolve(getArg('--raw')  || '');
const WRITE = args.includes('--write');

if (!STAR_DIR || !RAW_DIR) {
  console.error('❌ Missing --star or --raw paths.\nExample: node scripts/merge-locales.js --star ./locales --raw ../TPS-RAW/locales [--write]');
  process.exit(1);
}

const isObj = (v) => v && typeof v === 'object' && !Array.isArray(v);

function deepUnionMerge(star, raw, stats) {
  if (Array.isArray(star) || Array.isArray(raw)) {
    if (Array.isArray(star)) return star;
    if (Array.isArray(raw))  { stats.added++; return raw; }
    return star;
  }
  if (isObj(star) && isObj(raw)) {
    const out = { ...star };
    for (const key of Object.keys(raw)) {
      if (!(key in star)) {
        out[key] = raw[key]; stats.added++;
      } else {
        if (isObj(star[key]) || Array.isArray(star[key])) {
          out[key] = deepUnionMerge(star[key], raw[key], stats);
        } else {
          stats.kept++;
        }
      }
    }
    return out;
  }
  if (star !== undefined) { stats.kept++; return star; }
  if (raw  !== undefined) { stats.added++; return raw; }
  return star;
}

function sortKeysDeep(obj) {
  if (Array.isArray(obj)) return obj.map(sortKeysDeep);
  if (!isObj(obj)) return obj;
  return Object.keys(obj).sort().reduce((acc,k)=>{ acc[k]=sortKeysDeep(obj[k]); return acc; },{});
}

function loadJSON(fp) {
  try { return JSON.parse(fs.readFileSync(fp,'utf8')); }
  catch(e){ throw new Error(`Invalid JSON: ${fp}\n${e.message}`); }
}

(function main(){
  const starFiles = fs.readdirSync(STAR_DIR).filter(f=>f.endsWith('.json'));
  const rawFiles  = fs.readdirSync(RAW_DIR).filter(f=>f.endsWith('.json'));
  const set = new Set([...starFiles, ...rawFiles]);

  let totalAdded=0, totalKept=0, processed=0;

  for (const file of set) {
    const starPath = path.join(STAR_DIR,file);
    const rawPath  = path.join(RAW_DIR,file);
    if (!fs.existsSync(starPath) && !fs.existsSync(rawPath)) continue;

    const starJSON = fs.existsSync(starPath) ? loadJSON(starPath) : {};
    const rawJSON  = fs.existsSync(rawPath)  ? loadJSON(rawPath)  : {};

    const stats={added:0,kept:0};
    const merged = sortKeysDeep(deepUnionMerge(starJSON, rawJSON, stats));

    totalAdded += stats.added; totalKept += stats.kept; processed++;
    console.log(`• ${WRITE?'📝 write':'👀 dry-run'} ${file}: +${stats.added} added, ${stats.kept} kept`);
    if (WRITE) fs.writeFileSync(starPath, JSON.stringify(merged,null,2)+'\n','utf8');
  }
  console.log(`\n✅ Done (${processed} files). Added: ${totalAdded}, Kept: ${totalKept}. ${WRITE?'Written.':'No changes.'}`);
})();
