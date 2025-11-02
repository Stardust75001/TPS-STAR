// 🎯 TPS-STAR CONFIGURATION CHECKER
// Vérifiez la configuration complète de tous vos trackers

console.log('🎯 TPS-STAR - VÉRIFICATION COMPLÈTE DES TRACKERS');
console.log('===============================================');

// Configuration officielle basée sur vos données
const OFFICIAL_CONFIG = {
    // Core Analytics (GRATUITS)
    clarity_id: 'tzvd9w6rjs',        // alexjet2000@gmail.com
    hotjar_id: '6564192',            // alfalconx@gmail.com

    // Plateformes payantes (déjà configurées)
    ga4_token: 'G-E4NPI2ZZM3',       // Google Analytics 4
    meta_pixel_id: '1973238620087976', // Meta Business

    // Infrastructure & Monitoring
    slack_webhook: 'hooks.slack.com/services/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',
    google_ads: '100-529-5680',       // asc2000@gmail.com
    smtp_user: 'hello@thepetsociety.paris'
};

// Vérifier la configuration TPS actuelle
function checkTPSConfiguration() {
    console.log('📋 1. VÉRIFICATION CONFIGURATION TPS');

    if (typeof TPS !== 'undefined' && TPS.integrations) {
        console.log('✅ TPS.integrations trouvé');

        const config = TPS.integrations;

        // Vérifier chaque tracker
        console.log('\n🔍 Comparaison avec configuration officielle:');

        // Clarity
        const clarityMatch = config.clarity_id === OFFICIAL_CONFIG.clarity_id;
        console.log(`🔥 Clarity: ${clarityMatch ? '✅' : '❌'} (${config.clarity_id || 'NON CONFIGURÉ'})`);

        // Hotjar
        const hotjarMatch = config.hotjar_id === OFFICIAL_CONFIG.hotjar_id;
        console.log(`📊 Hotjar: ${hotjarMatch ? '✅' : '❌'} (${config.hotjar_id || 'NON CONFIGURÉ'})`);

        // GA4
        const ga4Match = config.ga4 === OFFICIAL_CONFIG.ga4_token;
        console.log(`📈 GA4: ${ga4Match ? '✅' : '❌'} (${config.ga4 || 'NON CONFIGURÉ'})`);

        // Meta
        const metaMatch = config.meta_pixel_id === OFFICIAL_CONFIG.meta_pixel_id;
        console.log(`📘 Meta: ${metaMatch ? '✅' : '❌'} (${config.meta_pixel_id || 'NON CONFIGURÉ'})`);

        console.log(`🚨 Sentry: ${config.sentry_dsn ? '✅ Configuré' : '❌ NON CONFIGURÉ'}`);
        console.log(`⚡ Cloudflare: ${config.cloudflare_beacon_token ? '✅ Configuré' : '❌ NON CONFIGURÉ'}`);

    } else {
        console.log('❌ TPS.integrations NON TROUVÉ - Problème critique !');
    }
}

// Vérifier le chargement des trackers
function checkTrackerLoading() {
    console.log('\n📋 2. VÉRIFICATION CHARGEMENT DES TRACKERS');

    const trackers = {
        'Microsoft Clarity': typeof clarity !== 'undefined',
        'Hotjar': typeof hj !== 'undefined',
        'Google Analytics': typeof gtag !== 'undefined',
        'Meta Pixel': typeof fbq !== 'undefined',
        'Sentry': typeof Sentry !== 'undefined'
    };

    Object.entries(trackers).forEach(([name, loaded]) => {
        console.log(`${loaded ? '✅' : '❌'} ${name}: ${loaded ? 'CHARGÉ' : 'NON CHARGÉ'}`);
    });
}

// Tests fonctionnels
function runFunctionalTests() {
    console.log('\n📋 3. TESTS FONCTIONNELS');

    // Test Clarity
    if (typeof clarity !== 'undefined') {
        try {
            clarity('set', 'test_user', 'tps_star_user');
            console.log('✅ Clarity: Test event envoyé');
        } catch(e) {
            console.log('❌ Clarity: Erreur -', e.message);
        }
    }

    // Test Hotjar
    if (typeof hj !== 'undefined') {
        try {
            hj('event', 'tps_star_test');
            console.log('✅ Hotjar: Test event envoyé');
        } catch(e) {
            console.log('❌ Hotjar: Erreur -', e.message);
        }
    }

    // Test GA4
    if (typeof gtag !== 'undefined') {
        try {
            gtag('event', 'tps_star_test', {
                'custom_parameter': 'configuration_check'
            });
            console.log('✅ GA4: Test event envoyé');
        } catch(e) {
            console.log('❌ GA4: Erreur -', e.message);
        }
    }

    // Test Meta
    if (typeof fbq !== 'undefined') {
        try {
            fbq('trackCustom', 'TPS_STAR_Test');
            console.log('✅ Meta Pixel: Test event envoyé');
        } catch(e) {
            console.log('❌ Meta Pixel: Erreur -', e.message);
        }
    }
}

// Recommandations de configuration
function showConfigurationGuide() {
    console.log('\n📋 4. GUIDE DE CONFIGURATION SHOPIFY');
    console.log('=====================================');
    console.log('Allez dans Shopify Admin → Settings → Custom data → Shop');
    console.log('Namespace: custom_integrations');
    console.log('');
    console.log('Metafields à configurer:');
    console.log('• clarity_id = "tzvd9w6rjs"');
    console.log('• hotjar_id = "6564192"');
    console.log('• ga4_token = "G-E4NPI2ZZM3"');
    console.log('• meta_pixel_id = "1973238620087976"');
    console.log('• slack_webhook_url = "https://hooks.slack.com/services/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"');

    console.log('\n🎯 Après configuration, rechargez la page et relancez ce test !');
}

// Lancer tous les tests
console.log('🚀 Lancement des vérifications...\n');

checkTPSConfiguration();
setTimeout(() => {
    checkTrackerLoading();
    setTimeout(() => {
        runFunctionalTests();
        showConfigurationGuide();
    }, 2000);
}, 1000);

console.log('\n⏱️  Tests complets dans 3 secondes...');
