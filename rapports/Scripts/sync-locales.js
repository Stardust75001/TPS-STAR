const fs = require('fs');
const path = require('path');

const localesDir = path.join(__dirname, 'locales');
const enFile = path.join(localesDir, 'en.default.json');
const enData = JSON.parse(fs.readFileSync(enFile, 'utf8'));

fs.readdirSync(localesDir).forEach(file => {
  if (file === 'en.default.json' || !file.endsWith('.json')) return;
  const filePath = path.join(localesDir, file);
  const localeData = JSON.parse(fs.readFileSync(filePath, 'utf8'));

  // Add missing keys from enData
  let changed = false;
  Object.keys(enData).forEach(key => {
    if (!(key in localeData)) {
      localeData[key] = ""; // or enData[key] if you want to copy English text
      changed = true;
    }
  });

  if (changed) {
    fs.writeFileSync(filePath, JSON.stringify(localeData, null, 2), 'utf8');
    console.log(`Updated ${file}`);
  }
});
