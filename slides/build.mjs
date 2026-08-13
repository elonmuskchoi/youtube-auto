import { cp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
await rm('dist',{recursive:true,force:true});
await mkdir('dist',{recursive:true});
let html=await readFile('index.html','utf8');
for(const name of ['student-proof-a.webp','student-proof-b.webp','student-proof-c.webp']){
  const data=(await readFile(`assets/${name}`)).toString('base64');
  html=html.replaceAll(`assets/${name}`,`data:image/webp;base64,${data}`);
}
await writeFile('dist/index.html',html,'utf8');
await cp('assets','dist/assets',{recursive:true});
