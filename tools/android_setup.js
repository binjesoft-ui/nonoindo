// Applies NonoIndo's settings to the Android project made by `npx cap add android`.
// Run from the repo root before `npx cap sync android`: node tools/android_setup.js
const fs = require('fs');
const path = require('path');

const RES = 'android/app/src/main/res';
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));

// `ready` says whether the file already has the setting, so the script can run again safely.
function edit(file, change, ready) {
  const before = fs.readFileSync(file, 'utf8');
  if (ready(before)) return;
  const after = change(before);
  if (after === before) throw new Error(`No change made to ${file}; the Capacitor template may have changed`);
  fs.writeFileSync(file, after);
}

// Portrait only.
edit('android/app/src/main/AndroidManifest.xml', xml =>
  xml.replace(/<activity(?![^>]*screenOrientation)/, '<activity android:screenOrientation="portrait"'),
  xml => xml.includes('android:screenOrientation="portrait"'));

// Version shown to players, and a build number that grows with every GitHub build.
const code = Number(process.env.GITHUB_RUN_NUMBER || 1);
edit('android/app/build.gradle', gradle => gradle
  .replace(/versionCode \d+/, `versionCode ${code}`)
  .replace(/versionName "[^"]*"/, `versionName "${pkg.version}"`),
  gradle => gradle.includes(`versionCode ${code}`) && gradle.includes(`versionName "${pkg.version}"`));

// Replace the template's splash images, then copy NonoIndo's icons and splash.
for (const dir of fs.readdirSync(RES)) {
  const file = path.join(RES, dir, 'splash.png');
  if (dir.startsWith('drawable') && fs.existsSync(file)) fs.rmSync(file);
}
fs.cpSync('assets/android/res', RES, { recursive: true });
edit(path.join(RES, 'values/ic_launcher_background.xml'), xml =>
  xml.replace(/>#?[0-9A-Fa-f]{6,8}</, '>#FFF9E8<'),
  xml => xml.includes('>#FFF9E8<'));

console.log(`Android project set up: portrait, version ${pkg.version} (${code}), icons, splash`);
