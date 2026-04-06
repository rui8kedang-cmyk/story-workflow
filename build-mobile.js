// build-mobile.js - generates mobile.html with correct UTF-8 encoding
const fs = require('fs');
const path = require('path');

const dir = path.dirname(__filename || process.argv[1]);
const outFile = path.join(dir, 'mobile.html');

// Read all parts
const parts = [];
for (let i = 1; i <= 5; i++) {
  const f = path.join(dir, `_part${i}.txt`);
  if (fs.existsSync(f)) {
    parts.push(fs.readFileSync(f, 'utf8'));
  }
}

const content = parts.join('\n');
fs.writeFileSync(outFile, content, 'utf8');
console.log('Written mobile.html:', content.length, 'bytes');
console.log('Has 小故事:', content.includes('小故事'));
console.log('Has 头脑风暴:', content.includes('头脑风暴'));

// Clean up parts
for (let i = 1; i <= 5; i++) {
  const f = path.join(dir, `_part${i}.txt`);
  if (fs.existsSync(f)) fs.unlinkSync(f);
}
fs.unlinkSync(process.argv[1]);
console.log('Cleaned up temp files');
