// TPS-STAR Advanced Production Diagnostic
// Copy and paste this entire script into your browser console on thepetsociety.paris

console.log('🔍 TPS-STAR Advanced Diagnostic Starting...');
console.log('=====================================');

// Step 1: Check TPS object availability
console.log('📋 Step 1: TPS Object Status');
if (typeof TPS !== 'undefined') {
    console.log('✅ TPS object exists');
    if (TPS.integrations) {
        console.log('✅ TPS.integrations exists');
        console.log('📊 Current integrations config:', TPS.integrations);
    } else {
        console.log('❌ TPS.integrations missing');
    }
} else {
    console.log('❌ TPS object not found');
}

// Step 2: Check metafield configuration element
console.log('\n📋 Step 2: Configuration Source Check');
const configEl = document.getElementById('tps-integrations');
if (configEl) {
    console.log('✅ Config element found');
    try {
        const rawConfig = configEl.textContent;
        console.log('📄 Raw config:', rawConfig);
        const parsedConfig = JSON.parse(rawConfig);
        console.log('📊 Parsed config:', parsedConfig);

        // Check specific IDs
        console.log('\n🔑 Metafield Values:');
        console.log('  - Clarity ID:', parsedConfig.clarity_id || 'NOT SET');
        console.log('  - Hotjar ID:', parsedConfig.hotjar_id || 'NOT SET');
        console.log('  - GA4 Token:', parsedConfig.ga4 || 'NOT SET');
        console.log('  - Meta Pixel ID:', parsedConfig.meta_pixel_id || 'NOT SET');

    } catch (e) {
        console.log('❌ Config parsing error:', e);
    }
} else {
    console.log('❌ Config element not found');
}

// Step 3: Check for tracker objects with retry
console.log('\n📋 Step 3: Tracker Object Detection (with 10-second retry)');

function checkTrackers() {
    const trackers = {
        'Microsoft Clarity': typeof clarity !== 'undefined' ? '✅' : '❌',
        'Hotjar': typeof hj !== 'undefined' ? '✅' : '❌',
        'GA4 (gtag)': typeof gtag !== 'undefined' ? '✅' : '❌',
        'Meta Pixel (fbq)': typeof fbq !== 'undefined' ? '✅' : '❌'
    };

    console.log('🎯 Current tracker status:');
    Object.entries(trackers).forEach(([name, status]) => {
        console.log(`  ${status} ${name}`);
    });

    return trackers;
}

// Initial check
const initialResults = checkTrackers();

// Retry after 10 seconds for slow-loading trackers
setTimeout(() => {
    console.log('\n🔄 Retrying tracker detection after 10 seconds...');
    const retryResults = checkTrackers();

    // Compare results
    console.log('\n📈 Status Change Summary:');
    Object.keys(initialResults).forEach(tracker => {
        if (initialResults[tracker] !== retryResults[tracker]) {
            console.log(`  📍 ${tracker}: ${initialResults[tracker]} → ${retryResults[tracker]}`);
        }
    });
}, 10000);

// Step 4: Check for script tags in DOM
console.log('\n📋 Step 4: Script Tag Analysis');
const clarityScripts = document.querySelectorAll('script[src*="clarity.ms"]');
const hotjarScripts = document.querySelectorAll('script[src*="hotjar.com"]');
const ga4Scripts = document.querySelectorAll('script[src*="googletagmanager.com/gtag"]');
const metaScripts = document.querySelectorAll('script[src*="connect.facebook.net"]');

console.log('🔍 Script tags found:');
console.log(`  - Clarity scripts: ${clarityScripts.length}`);
console.log(`  - Hotjar scripts: ${hotjarScripts.length}`);
console.log(`  - GA4 scripts: ${ga4Scripts.length}`);
console.log(`  - Meta scripts: ${metaScripts.length}`);

// Step 5: Network request monitoring
console.log('\n📋 Step 5: Network Monitoring Setup');
console.log('📡 Monitoring network requests for tracking platforms...');

// Monitor for 15 seconds
const monitorStart = Date.now();
const originalFetch = window.fetch;
const requestLog = [];

window.fetch = function(...args) {
    const url = args[0];
    if (typeof url === 'string') {
        if (url.includes('clarity.ms') ||
            url.includes('hotjar.com') ||
            url.includes('googletagmanager.com') ||
            url.includes('connect.facebook.net')) {
            requestLog.push({
                timestamp: Date.now() - monitorStart,
                url: url,
                platform: url.includes('clarity.ms') ? 'Clarity' :
                         url.includes('hotjar.com') ? 'Hotjar' :
                         url.includes('googletagmanager.com') ? 'GA4' :
                         url.includes('connect.facebook.net') ? 'Meta' : 'Unknown'
            });
        }
    }
    return originalFetch.apply(this, args);
};

setTimeout(() => {
    console.log('\n📊 Network Requests Summary (15 seconds):');
    if (requestLog.length > 0) {
        requestLog.forEach(req => {
            console.log(`  ${req.timestamp}ms: ${req.platform} - ${req.url}`);
        });
    } else {
        console.log('  ⚠️  No tracking requests detected');
    }

    // Restore original fetch
    window.fetch = originalFetch;
}, 15000);

// Step 6: Final recommendations
setTimeout(() => {
    console.log('\n🎯 DIAGNOSTIC COMPLETE');
    console.log('=====================================');
    console.log('📋 Next Steps:');
    console.log('1. Check your Shopify metafields in Admin → Settings → Custom data');
    console.log('2. Ensure clarity_id = "tzvd9w6rjs" and hotjar_id = "6564192"');
    console.log('3. If metafields are correct, check browser console for loading errors');
    console.log('4. Try refreshing the page and running this diagnostic again');
    console.log('\n📞 If issues persist, share this diagnostic output for further analysis.');
}, 20000);

console.log('\n⏱️  Diagnostic will complete in 20 seconds with full analysis...');
