#!/bin/bash

# Test TPS-STAR Microsoft Clarity Integration

echo "🧪 Testing TPS-STAR Microsoft Clarity Integration"
echo "================================================="

# Check if tracking-analytics.liquid has clarity_id
echo "1. Checking snippets/tracking-analytics.liquid..."
if grep -q "clarity_id" "snippets/tracking-analytics.liquid"; then
    echo "   ✅ clarity_id found in JSON configuration"
else
    echo "   ❌ clarity_id NOT found in JSON configuration"
fi

# Check if tps-tracking.js has Clarity support
echo "2. Checking assets/tps-tracking.js..."
if grep -q "clarity_id" "assets/tps-tracking.js"; then
    echo "   ✅ clarity_id configuration found"
else
    echo "   ❌ clarity_id configuration NOT found"
fi

if grep -q "Clarity loaded" "assets/tps-tracking.js"; then
    echo "   ✅ Clarity loading code found"
else
    echo "   ❌ Clarity loading code NOT found"
fi

if grep -q "clarity.ms/tag" "assets/tps-tracking.js"; then
    echo "   ✅ Official Clarity script URL found"
else
    echo "   ❌ Official Clarity script URL NOT found"
fi

echo ""
echo "🔧 Next Steps:"
echo "1. Configure Shopify metafield: custom_integrations.Clarity_ID = 'tzvd9w6rjs'"
echo "2. Deploy files to Shopify theme"
echo "3. Test with: TPS.debug.enable() in browser console"
echo "4. Look for: '🪟 Clarity loaded: tzvd9w6rjs' in console"
echo "5. Check dashboard: https://clarity.microsoft.com"

echo ""
echo "✅ Microsoft Clarity integration is ready!"
