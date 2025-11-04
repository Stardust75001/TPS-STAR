// TPS-STAR Account Verification Script
// Copiez ce script dans la console de votre navigateur sur thepetsociety.paris

console.log('🔍 TPS-STAR Account Verification');
console.log('================================');

// Check current configuration
if (typeof TPS !== 'undefined' && TPS.integrations) {
    console.log('📊 Configuration actuelle:');
    console.log('  - Clarity ID:', TPS.integrations.clarity_id || 'Non configuré');
    console.log('  - Hotjar ID:', TPS.integrations.hotjar_id || 'Non configuré');

    if (TPS.integrations.clarity_id) {
        console.log('🪟 Microsoft Clarity:');
        console.log('  - Dashboard: https://clarity.microsoft.com');
        console.log('  - Recherchez le projet ID:', TPS.integrations.clarity_id);
    }

    if (TPS.integrations.hotjar_id) {
        console.log('🔥 Hotjar:');
        console.log('  - Dashboard: https://insights.hotjar.com');
        console.log('  - Recherchez le site ID:', TPS.integrations.hotjar_id);
    }
} else {
    console.log('❌ Configuration TPS non trouvée');
}

// Check if trackers are loaded and provide next steps
console.log('\n🎯 Vérification des comptes:');
console.log('1. Ouvrez https://clarity.microsoft.com');
console.log('2. Connectez-vous avec vos emails potentiels:');
console.log('   - Email personnel');
console.log('   - Email professionnel');
console.log('   - Email Shopify');
console.log('3. Cherchez le projet "tzvd9w6rjs"');
console.log('');
console.log('4. Ouvrez https://insights.hotjar.com');
console.log('5. Répétez avec les mêmes emails');
console.log('6. Cherchez le site "6564192"');

console.log('\n📧 Emails potentiels à tester:');
console.log('- Votre email principal');
console.log('- Email utilisé pour Shopify');
console.log('- Email utilisé pour autres outils analytics');

// Advanced check - look for any identifying information in loaded scripts
setTimeout(() => {
    console.log('\n🔍 Analyse des scripts chargés...');

    // Check Clarity
    const clarityScripts = document.querySelectorAll('script[src*="clarity.ms"]');
    if (clarityScripts.length > 0) {
        console.log('✅ Script Clarity détecté');
        console.log('   URL:', clarityScripts[0].src);
    }

    // Check Hotjar
    const hotjarScripts = document.querySelectorAll('script[src*="hotjar.com"], script[src*="contentsquare.net"]');
    if (hotjarScripts.length > 0) {
        console.log('✅ Script Hotjar détecté');
        console.log('   URL:', hotjarScripts[0].src);
    }

    console.log('\n💡 Astuce: Les propriétaires des comptes peuvent être identifiés');
    console.log('   en vérifiant qui a accès aux dashboards avec ces IDs.');

}, 2000);
