const fs = require('fs');
const path = require('path');

const localesDir = path.join(__dirname, 'locales');

function fixJsonFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');

    // Remove comments (// and /* */)
    content = content.replace(/\/\/.*|\/\*[\s\S]*?\*\//g, '');

    // Remove trailing commas
    content = content.replace(/,\s*([}\]])/g, '$1');

    // Parse and re-stringify to remove duplicate keys (keeps last)
    let parsed;
    try {
      parsed = JSON.parse(content);
    } catch (e) {
      console.error(`❌ Error parsing ${filePath}: ${e.message}`);
      return;
    }

    // Write back pretty-printed JSON
    fs.writeFileSync(filePath, JSON.stringify(parsed, null, 2), 'utf8');
    console.log(`✅ Fixed: ${filePath}`);
  } catch (err) {
    console.error(`❌ Failed to process ${filePath}: ${err.message}`);
  }
}

fs.readdirSync(localesDir)
  .filter(f => f.endsWith('.json'))
  .forEach(f => fixJsonFile(path.join(localesDir, f)));
