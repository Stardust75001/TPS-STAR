#!/bin/bash

# TPS-STAR Trackers Verification Script
# Vérifie que tous les trackers fonctionnent et envoient des données

echo "🧪 TPS-STAR TRACKERS VERIFICATION"
echo "================================="
echo ""
echo "🚀 Lancez ce test dans la console de votre site :"
echo ""

cat << 'EOF'
// === TPS-STAR TRACKERS VERIFICATION SCRIPT ===
console.group('🧪 TPS-STAR Trackers Test');

// Test 1: Vérifier que TPS est chargé
console.log('1. 🔍 TPS Status:', typeof TPS === 'object' ? '✅ Loaded' : '❌ Missing');

// Test 2: Vérifier chaque tracker
const trackers = {
  'Meta Pixel (fbq)': typeof fbq,
  'Google Analytics (gtag)': typeof gtag,
  'Microsoft Clarity (clarity)': typeof clarity,
  'Hotjar (hj)': typeof hj,
  'Sentry': typeof Sentry
};

console.log('2. 📊 Trackers Status:');
Object.entries(trackers).forEach(([name, type]) => {
  console.log(`   ${type === 'function' ? '✅' : '❌'} ${name}: ${type}`);
});

// Test 3: Envoyer des événements de test
console.log('3. 🎯 Sending test events...');

// Test Meta Pixel
if (typeof fbq === 'function') {
  fbq('track', 'Lead', {
    test_source: 'tps_star',
    timestamp: Date.now()
  });
  console.log('   ✅ Meta Pixel test event sent');
}

// Test GA4
if (typeof gtag === 'function') {
  gtag('event', 'tps_test', {
    test_source: 'tps_star',
    timestamp: Date.now()
  });
  console.log('   ✅ GA4 test event sent');
}

// Test Clarity
if (typeof clarity === 'function') {
  clarity('set', 'test_source', 'tps_star');
  clarity('identify', 'test-user-' + Date.now());
  console.log('   ✅ Clarity test data sent');
}

// Test Hotjar
if (typeof hj === 'function') {
  hj('identify', 'test-user-' + Date.now(), {
    test_source: 'tps_star',
    timestamp: Date.now()
  });
  console.log('   ✅ Hotjar test data sent');
}

// Test 4: Afficher la configuration TPS
if (typeof TPS === 'object' && TPS.integrations) {
  console.log('4. ⚙️ TPS Configuration:');
  console.log('   Active platforms:', Object.keys(TPS.integrations).filter(k => TPS.integrations[k]));
}

console.log('');
console.log('🎯 NEXT STEPS:');
console.log('   1. Wait 2-10 minutes for data to appear');
console.log('   2. Check dashboards:');
console.log('      • Clarity: https://clarity.microsoft.com');
console.log('      • Hotjar: https://insights.hotjar.com');
console.log('      • GA4: https://analytics.google.com (Real-time)');
console.log('      • Meta: https://business.facebook.com/events_manager');
console.log('');
console.groupEnd();
EOF

echo ""
echo "📋 CHECKLIST DE VÉRIFICATION :"
echo ""
echo "⏱️  Attendre 2-10 minutes après le test"
echo ""
echo "✅ Microsoft Clarity (clarity.microsoft.com) :"
echo "   - Sessions en temps réel apparaissent"
echo "   - Recordings de vos actions"
echo "   - Status 'Active' dans Settings"
echo ""
echo "✅ Hotjar (insights.hotjar.com) :"
echo "   - 'Tracking Status: Active' vert"
echo "   - Nouvelles recordings/sessions"
echo "   - Test: Settings → Verify Installation"
echo ""
echo "✅ Google Analytics 4 (analytics.google.com) :"
echo "   - Real-time → Utilisateurs actifs (vous)"
echo "   - Events → page_view + vos événements test"
echo "   - Pages visitées apparaissent"
echo ""
echo "✅ Meta Business (business.facebook.com/events_manager) :"
echo "   - Test Events → Activité récente"
echo "   - PageView + Lead events"
echo "   - Pixel status 'Active'"
echo ""
echo "🆘 SI AUCUNE DONNÉE N'APPARAÎT :"
echo "   1. Vérifiez que vous n'êtes pas en navigation privée"
echo "   2. Désactivez temporairement les ad-blockers"
echo "   3. Testez depuis une autre connexion/appareil"
echo "   4. Vérifiez les metafields Shopify (custom_integrations)"
echo ""
echo "🎯 TOUT FONCTIONNE ? Votre TPS-STAR est 100% opérationnel ! 🚀"
