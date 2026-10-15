// Pure logic tests; no browser automation or external dependencies.
const assert = require('node:assert/strict');
const c = require('../docs/javascripts/reader.js');
const hash = 'a'.repeat(64), nextHash = 'b'.repeat(64);
const page = (id='a.md',h=hash) => ({id,url:id.replace('.md','/'),title:'A',summary:'Intro',change_summary:'',topic:'overview',content_hash:h});
const catalog = pages => ({schema_version:'1.0',artifact_kind:'portal_reader_catalog',project_id:'test',revision:hash,pages});
let count=0;
function test(name, fn){fn();count++;process.stdout.write(`ok ${count} - ${name}\n`);}
test('normal catalog and blank project state',()=>{assert.equal(c.validateCatalog(catalog([page()])).pages.length,1);assert.equal(c.validateState(c.blank('test'),'test').baseline,null);});
test('first use makes no historical claims',()=>assert.equal(c.changesSince(catalog([page()]),null),null));
test('same snapshot has no changes',()=>{const current=catalog([page()]);assert.deepEqual(c.changesSince(current,c.baselineFor(current)),{added:[],changed:[],removed:[]});});
test('added modified removed are distinct',()=>{const before=catalog([page(),page('old.md')]),after=catalog([page('a.md',nextHash),page('new.md')]);const d=c.changesSince(after,c.baselineFor(before));assert.deepEqual(d.added.map(p=>p.id),['new.md']);assert.deepEqual(d.changed.map(p=>p.id),['a.md']);assert.deepEqual(d.removed.map(p=>p.id),['old.md']);});
test('read page requires new review after change',()=>assert.equal(c.effectiveStatus(page('a.md',nextHash),{'a.md':{status:'read',content_hash:hash}}),'recheck'));
test('new read mark clears recheck',()=>assert.equal(c.effectiveStatus(page(),{'a.md':{status:'read',content_hash:hash}}),'read'));
test('question mark is retained and not converted to read',()=>assert.equal(c.effectiveStatus(page(),{'a.md':{status:'question',content_hash:nextHash}}),'question'));
test('future version and other project state rejected',()=>{assert.throws(()=>c.validateState({...c.blank('test'),schema_version:'99'},'test'));assert.throws(()=>c.validateState(c.blank('another'),'test'));});
test('unknown mark rejected',()=>assert.throws(()=>c.validateState({...c.blank('test'),marks:{'a.md':{status:'safe',content_hash:hash}}},'test')));
test('unsafe catalog URLs and duplicate ids rejected',()=>{for(const url of ['https://example.org','../outside/','//example.org','javascript:alert(1)'])assert.throws(()=>c.validateCatalog(catalog([{...page(),url}])));assert.throws(()=>c.validateCatalog(catalog([page(),page()])));});
test('invalid baseline rejected',()=>assert.throws(()=>c.validateState({...c.blank('test'),baseline:{revision:hash,pages:[{id:'../outside.md',content_hash:hash,title:'X'}]}},'test')));
test('acknowledging changes does not alter marks',()=>{const s=c.blank('test');s.marks['a.md']={status:'question',content_hash:hash};const old=JSON.stringify(s.marks);s.baseline=c.baselineFor(catalog([page()]));assert.equal(JSON.stringify(s.marks),old);});
process.stdout.write(`${count} reader logic tests passed (not application tests).\n`);
