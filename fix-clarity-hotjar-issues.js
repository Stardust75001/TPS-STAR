// TPS-STAR - Fix Hotjar & Clarity Loading Issues
// Diagnostic basé sur les captures d'écran du 2 novembre 2025

console.log('🔧 TPS-STAR - Correction des problèmes Clarity & Hotjar');
console.log('=========================================================');

// Configuration confirmée d'après les dashboards
const CONFIRMED_IDS = {
    clarity: 'tzvd9w6rjs',  // ✅ Projet actif "The Pet Society PARIS"
    hotjar: '6564192'       // ✅ Compte "Alexandre" actif
};

console.log('📋 IDs confirmés dans les dashboards:');
console.log('  - Microsoft Clarity:', CONFIRMED_IDS.clarity);
console.log('  - Hotjar:', CONFIRMED_IDS.hotjar);

// Vérifier la configuration actuelle
if (typeof TPS !== 'undefined' && TPS.integrations) {
    console.log('\n🔍 Configuration TPS actuelle:');
    console.log('  - Clarity configuré:', TPS.integrations.clarity_id || 'NON');
    console.log('  - Hotjar configuré:', TPS.integrations.hotjar_id || 'NON');

    // Vérifier si les IDs correspondent
    const clarityMatch = TPS.integrations.clarity_id === CONFIRMED_IDS.clarity;
    const hotjarMatch = TPS.integrations.hotjar_id === CONFIRMED_IDS.hotjar;

    console.log('\n✅ Correspondance des IDs:');
    console.log('  - Clarity:', clarityMatch ? '✅ CORRECT' : '❌ INCORRECT');
    console.log('  - Hotjar:', hotjarMatch ? '✅ CORRECT' : '❌ INCORRECT');

    if (!clarityMatch || !hotjarMatch) {
        console.log('\n🚨 PROBLÈME DÉTECTÉ:');
        console.log('Les IDs dans vos metafields Shopify ne correspondent pas aux dashboards !');
        console.log('\n🔧 Action requise:');
        console.log('1. Allez dans Shopify Admin → Settings → Custom data');
        console.log('2. Mettez à jour les metafields:');
        if (!clarityMatch) {
            console.log(`   - clarity_id: "${CONFIRMED_IDS.clarity}"`);
        }
        if (!hotjarMatch) {
            console.log(`   - hotjar_id: "${CONFIRMED_IDS.hotjar}"`);
        }
    }
} else {
    console.log('❌ Configuration TPS non trouvée - problème plus grave');
}

// Test de chargement des trackers
console.log('\n🧪 Test de chargement:');
setTimeout(() => {
    const clarityLoaded = typeof clarity !== 'undefined';
    const hotjarLoaded = typeof hj !== 'undefined';

    console.log('  - Clarity:', clarityLoaded ? '✅ CHARGÉ' : '❌ Non chargé');
    console.log('  - Hotjar:', hotjarLoaded ? '✅ CHARGÉ' : '❌ Non chargé');

    if (clarityLoaded) {
        console.log('🪟 Clarity: Prêt pour le tracking');
    } else {
        console.log('🪟 Clarity: Vérifiez les metafields Shopify');
    }

    if (hotjarLoaded) {
        console.log('🔥 Hotjar: Prêt pour le tracking');
    } else {
        console.log('🔥 Hotjar: Terminez l\'installation dans le dashboard');
        console.log('   → https://insights.hotjar.com');
    }
}, 3000);

// Instructions spécifiques basées sur les captures
console.log('\n📋 Actions spécifiques d\'après vos dashboards:');
console.log('\n1. MICROSOFT CLARITY (✅ Fonctionnel):');
console.log('   - Projet configuré correctement');
console.log('   - Attendez quelques minutes pour voir les données');
console.log('   - Les sessions apparaîtront après navigation sur le site');

console.log('\n2. HOTJAR (🔧 Installation à terminer):');
console.log('   - Compte actif mais installation incomplète');
console.log('   - Allez sur https://insights.hotjar.com');
console.log('   - Terminez l\'installation du code de tracking');
console.log('   - Le code devrait se charger automatiquement après');

console.log('\n🎯 Résultat attendu après corrections:');
console.log('   - Clarity: ✅ Données en temps réel');
console.log('   - Hotjar: ✅ Heatmaps et recordings');
console.log('   - Les 4 plateformes TPS-STAR: 100% fonctionnelles');
