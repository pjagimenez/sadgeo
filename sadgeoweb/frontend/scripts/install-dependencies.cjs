// Keep node_modules across Maven clean builds; only reuse a successful installation.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { spawnSync } = require('node:child_process');

const root = path.resolve(__dirname, '..');
process.chdir(root);
const marker = path.join('node_modules', '.sadgeo-install.json');
const hash = crypto.createHash('sha256');
for (const file of ['package.json', 'package-lock.json', '.npmrc', __filename]) {
  hash.update(file);
  hash.update(fs.existsSync(file) ? fs.readFileSync(file) : '<absent>');
}
hash.update(JSON.stringify([process.version, process.platform, process.arch]));
const fingerprint = hash.digest('hex');
const windows = process.platform === 'win32';
const installedLock = path.join('node_modules', '.package-lock.json');
const lockHash = () => crypto.createHash('sha256').update(fs.readFileSync(installedLock)).digest('hex');
const tools = ['typescript/bin/tsc', 'vite/bin/vite.js', windows ? '.bin/tsc.cmd' : '.bin/tsc', windows ? '.bin/vite.cmd' : '.bin/vite'];
try {
  const previous = JSON.parse(fs.readFileSync(marker, 'utf8'));
  if (previous.fingerprint === fingerprint && previous.installedLock === lockHash()
      && tools.every(file => fs.existsSync(path.join('node_modules', file)))) {
    console.log('Dependencias frontend inalteradas: reutilizando node_modules (npm ci dispensado).');
    process.exit(0);
  }
} catch { /* Missing/invalid marker or installation: run npm ci. */ }

// A failed reinstall must never leave a valid reuse marker.
fs.rmSync(marker, { force: true });
console.log('Instalando dependencias frontend: npm ci --include=dev --bin-links=true');
const result = windows
  ? spawnSync(process.env.ComSpec || 'cmd.exe', ['/d', '/s', '/c', 'npm.cmd ci --include=dev --bin-links=true'], { stdio: 'inherit' })
  : spawnSync('npm', ['ci', '--include=dev', '--bin-links=true'], { stdio: 'inherit' });
if (result.error || result.status !== 0) {
  console.error(result.error?.message || `npm ci falhou (codigo ${result.status}).`);
  process.exit(result.status || 1);
}
if (!fs.existsSync(installedLock) || !tools.every(file => fs.existsSync(path.join('node_modules', file)))) {
  console.error('Instalacao incompleta: ferramentas TypeScript/Vite ou executaveis locais ausentes.');
  process.exit(1);
}
fs.writeFileSync(marker, JSON.stringify({ fingerprint, installedLock: lockHash() }) + '\n');
