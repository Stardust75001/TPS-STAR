# 🚀 DÉPLOIEMENT TPS-STAR integrations.liquid

## 📋 **Checklist de Déploiement**

### **Étape 1 : Accéder au Theme Editor**
1. Admin Shopify → **Online Store** → **Themes**
2. Thème actif → **Actions** → **Edit code**
3. Section **Snippets** dans la sidebar

### **Étape 2 : Localiser/Créer le fichier**
- Si `integrations.liquid` existe → l'ouvrir
- Si n'existe pas → **Add a new snippet** → nommer `integrations`

### **Étape 3 : Remplacer le contenu complet**
⚠️ **BACKUP IMPORTANT** : Copiez l'ancien contenu avant de le remplacer !

---

## 📦 **CONTENU COMPLET À COPIER-COLLER**

```liquid
{%- comment -%}
  THE PET SOCIETY — Enhanced Integrations Bootstrap
  TPS-STAR Universal Tracking System v2.0
  
  🔧 CORRECTIONS APPLIQUÉES :
  - Metafields robust (lowercase + CamelCase fallback)
  - Sentry syntax fixed + SRI removed
  - Amplitude SRI removed
  - GTM priority maintained over GA4
{%- endcomment -%}

{%- liquid
  assign integ = shop.metafields.custom_integrations

  comment 'TPS-STAR Metafields - Robust key handling (lowercase first, CamelCase fallback)'
  comment 'Core analytics platforms - Shopify standard lowercase keys'
  assign ga4_token              = integ.ga4_token              | default: integ.GA4_Token              | strip
  assign meta_pixel_id          = integ.meta_pixel_id          | default: integ.Meta_Pixel_ID           | strip
  assign sentry_dsn             = integ.sentry_dsn             | default: integ.Sentry_DSN              | strip
  assign cloudflare_beacon_token= integ.cloudflare_beacon_token| default: integ.Cloudflare_Token        | strip
  assign slack_webhook_url      = integ.slack_webhook_url      | default: integ.Slack_Webhook_URL       | strip
  assign ahrefs_api_key         = integ.ahrefs_api_key         | default: integ.AHREFS_API_KEY          | strip
  assign domain_principal       = integ.domain                 | default: integ.Domaine_principal       | strip

  comment 'FREE Analytics Platforms - Zero Cost, Maximum Value'
  assign clarity_id             = integ.clarity_id             | default: integ.Clarity_ID              | strip
  assign hotjar_id              = integ.hotjar_id              | default: integ.Hotjar_ID               | strip
  assign amplitude_key          = integ.amplitude_key          | default: integ.Amplitude_Key           | strip

  comment 'Extended tracking platforms (add as needed)'
  assign gtm_id                 = integ.gtm_id                 | strip
  assign tiktok_pixel           = integ.tiktok_pixel           | strip
  assign snapchat_pixel         = integ.snapchat_pixel         | strip
  assign pinterest_tag          = integ.pinterest_tag          | strip
  assign mixpanel_token         = integ.mixpanel_token         | strip
  assign shopify_pixel          = integ.shopify_pixel          | strip

  comment 'Verification meta tags'
  assign gsc_verification       = integ.gsc_verification       | strip
  assign ahrefs_verification    = integ.ahrefs_verification    | strip
-%}

{%- comment -%} ───────── Meta Verification Tags ───────── {%- endcomment -%}
{%- if gsc_verification != blank -%}
  <meta name="google-site-verification" content="{{ gsc_verification }}">
{%- endif -%}
{%- if ahrefs_verification != blank -%}
  <meta name="ahrefs-site-verification" content="{{ ahrefs_verification }}">
{%- endif -%}

{%- comment -%} ───────── Domain Principal Info ───────── {%- endcomment -%}
{%- if domain_principal != blank -%}
  <!-- TPS-STAR Domain: {{ domain_principal }} -->
{%- endif -%}

<script id="tps-integrations" type="application/json">
  {
    "gtm_id": "{{ gtm_id | escape }}",
    "ga4": "{{ ga4_token | escape }}",
    "meta_pixel_id": "{{ meta_pixel_id | escape }}",
    "sentry_dsn": "{{ sentry_dsn | escape }}",
    "cloudflare_beacon_token": "{{ cloudflare_beacon_token | escape }}",
    "shopify_pixel": "{{ shopify_pixel | escape }}",
    "clarity_id": "{{ clarity_id | escape }}",
    "hotjar_id": "{{ hotjar_id | escape }}",
    "amplitude_key": "{{ amplitude_key | escape }}",
    "tiktok_pixel": "{{ tiktok_pixel | escape }}",
    "snapchat_pixel": "{{ snapchat_pixel | escape }}",
    "pinterest_tag": "{{ pinterest_tag | escape }}",
    "mixpanel_token": "{{ mixpanel_token | escape }}",
    "domain": "{{ domain_principal | default: shop.permanent_domain | escape }}"
  }
</script>

<script>
  (function () {
    var cfgEl = document.getElementById('tps-integrations');
    var cfg = {};
    try { cfg = JSON.parse(cfgEl.textContent||'{}'); } catch(e){ cfg = {}; }

    window.TPS = window.TPS || {};
    window.TPS.integrations = Object.assign({}, window.TPS.integrations || {}, cfg);

    function loadScript(src, id, attrs) {
      return new Promise(function(resolve, reject){
        if (id && document.getElementById(id)) return resolve();
        var s = document.createElement('script');
        s.src = src; s.async = true; if (id) s.id = id;
        if (attrs) Object.keys(attrs).forEach(k => s.setAttribute(k, attrs[k]));
        s.onload = resolve; s.onerror = reject;
        document.head.appendChild(s);
      });
    }

    // === GOOGLE TAG MANAGER ===
    if (cfg.gtm_id && !window.dataLayer) {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({'gtm.start': new Date().getTime(), event: 'gtm.js'});

      loadScript('https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(cfg.gtm_id), 'gtm')
      .then(() => {
        console.log('[TPS-STAR] GTM loaded:', cfg.gtm_id);
      }).catch(() => {
        console.warn('[TPS] GTM load failed');
      });
    }

    // === GOOGLE ANALYTICS 4 (Direct - only if no GTM) ===
    else if (cfg.ga4_token && !cfg.gtm_id) {
      loadScript('https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(cfg.ga4_token), 'ga4')
      .then(() => {
        window.dataLayer = window.dataLayer || [];
        function gtag(){ dataLayer.push(arguments); }
        window.gtag = window.gtag || gtag;
        gtag('js', new Date());
        gtag('config', cfg.ga4_token, { 'anonymize_ip': true });
        console.log('[TPS-STAR] GA4 loaded:', cfg.ga4_token);
      }).catch(() => {
        console.warn('[TPS] GA4 load failed');
      });
    }

    // === SENTRY (FIXED - No SRI + Proper Syntax) ===
    if (cfg.sentry_dsn) {
      loadScript('https://browser.sentry-cdn.com/8.36.0/bundle.tracing.replay.min.js', 'sentry-sdk')
      .then(function(){
        // eslint-disable-next-line no-undef
        Sentry.init({
          dsn: cfg.sentry_dsn,
          integrations: [
            // eslint-disable-next-line no-undef
            Sentry.browserTracingIntegration(),
            // eslint-disable-next-line no-undef
            Sentry.replayIntegration({ maskAllText: false, blockAllMedia: false })
          ],
          tracesSampleRate: 1.0,
          replaysSessionSampleRate: 0.1,
          replaysOnErrorSampleRate: 1.0,
          environment: "{{ request.locale.iso_code | upcase }}",
          release: "tps-star@{{ 'now' | date: '%Y-%m-%d' }}",
          autoSessionTracking: true,
          initialScope: {
            tags: {
              "store": "{{ shop.permanent_domain }}",
              "theme": "tps-star", 
              "locale": "{{ request.locale.iso_code }}",
              "page_type": "{{ request.page_type }}",
              "device_type": "web"
            },
            user: {
              id: "{{ customer.id | default: 'anonymous' }}",
              email: "{{ customer.email | default: null }}"
            }
          }
        });
        console.log('[TPS-STAR] Sentry initialized');
      })
      .catch(function(){ 
        console.warn('[TPS] Sentry SDK load failed'); 
      });
    }

    // === META PIXEL (Enhanced Debug) ===
    if (cfg.meta_pixel_id && cfg.meta_pixel_id !== 'null' && cfg.meta_pixel_id !== '') {
      (function(f,b,e,v,n,t,s){
        if(f.fbq)return;n=f.fbq=function(){n.callMethod?
          n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;
        s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s);
      })(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');

      try {
        console.log('[TPS] meta id:', cfg.meta_pixel_id, typeof cfg.meta_pixel_id);
        fbq('init', cfg.meta_pixel_id);
        fbq('track', 'PageView');
        console.log('[TPS-STAR] Meta Pixel initialized:', cfg.meta_pixel_id);
      }
      catch(e) {
        console.warn('[TPS] Meta Pixel failed:', e);
      }
    } else {
      console.warn('[TPS] Meta Pixel ID not configured or invalid:', cfg.meta_pixel_id);
    }

    // === CLOUDFLARE BEACON ===
    if (cfg.cloudflare_beacon_token) {
      loadScript('https://static.cloudflareinsights.com/beacon.min.js', 'cf-beacon', {
        'defer': '',
        'data-cf-beacon': JSON.stringify({ token: cfg.cloudflare_beacon_token })
      });
    }

    // === HOTJAR (Fixed URL + Logs) ===
    if (cfg.hotjar_id) {
      (function (c, s, q, u, a, r, e) {
        c.hj=c.hj||function(){(c.hj.q=c.hj.q||[]).push(arguments)};
        c._hjSettings = { hjid: parseInt(a, 10), hjsv: 6 };
        r = s.getElementsByTagName('head')[0];
        e = s.createElement('script');
        e.async = true;
        e.src = q + c._hjSettings.hjid + u;
        r.appendChild(e);
      })(window, document, 'https://static.hotjar.com/c/hotjar-', '.js?sv=', cfg.hotjar_id);
      console.log('🔥 Hotjar loaded:', cfg.hotjar_id);
    }

    // === MICROSOFT CLARITY (With Logs) ===
    if (cfg.clarity_id) {
      (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
      })(window, document, "clarity", "script", cfg.clarity_id);
      console.log('🪟 Clarity loaded:', cfg.clarity_id);
    }

    // === AMPLITUDE (SRI Removed) ===
    if (cfg.amplitude_key) {
      (function(e,t){var n=e.amplitude||{_q:[],_iq:{}};var r=t.createElement("script");r.type="text/javascript";r.async=true;r.src="https://cdn.amplitude.com/libs/amplitude-8.21.9-min.gz.js";r.onload=function(){if(!e.amplitude.runQueuedFunctions){console.log("[Amplitude] Error: could not load SDK")}};var i=t.getElementsByTagName("script")[0];i.parentNode.insertBefore(r,i);function s(e,t){e.prototype[t]=function(){this._q.push([t].concat(Array.prototype.slice.call(arguments,0)));return this}}var o=function(){this._q=[];return this};var a=["add","append","clearAll","prepend","set","setOnce","unset","preInsert","postInsert","remove"];for(var c=0;c<a.length;c++){s(o,a[c])}n.Identify=o;var u=function(){this._q=[];return this};var l=["setProductId","setQuantity","setPrice","setRevenueType","setEventProperties"];for(var p=0;p<l.length;p++){s(u,l[p])}n.Revenue=u;var d=["init","logEvent","logRevenue","setUserId","setUserProperties","setOptOut","setVersionName","setDomain","setDeviceId","enableTracking","setGlobalUserProperties","identify","clearUserProperties","setGroup","logRevenueV2","regenerateDeviceId","groupIdentify","onInit","logEventWithTimestamp","logEventWithGroups","setSessionId","resetSessionId"];function v(e){function t(t){e[t]=function(){e._q.push([t].concat(Array.prototype.slice.call(arguments,0)))}}for(var n=0;n<d.length;n++){t(d[n])}}v(n);n.getInstance=function(e){e=(!e||e.length===0?"$default_instance":e).toLowerCase();if(!Object.prototype.hasOwnProperty.call(n._iq,e)){n._iq[e]={_q:[]};v(n._iq[e])}return n._iq[e]};e.amplitude=n})(window,document);

      amplitude.getInstance().init(cfg.amplitude_key, null, {
        includeUtm: true,
        includeReferrer: true,
        platform: 'Web',
        saveEvents: true,
        includeGclid: true,
        includeFbclid: true
      });

      amplitude.getInstance().logEvent('Page View', {
        page_type: '{{ request.page_type }}',
        page_title: '{{ page_title | escape }}',
        shop_name: '{{ shop.name | escape }}',
        currency: '{{ shop.currency }}',
        locale: '{{ request.locale.iso_code }}',
        customer_logged_in: {{ customer.id | default: false }},
        url: window.location.href,
        referrer: document.referrer || 'direct'
      });

      console.log('[TPS-STAR] Amplitude initialized');
    }

    // === TPS-STAR GLOBAL FUNCTIONS ===
    window.TPS.debug = {
      enable: function() {
        console.group('🔍 TPS-STAR Debug Info');
        console.log('📊 Config:', cfg);
        console.log('🎯 Active platforms:', Object.keys(cfg).filter(k => cfg[k]));
        console.groupEnd();
      }
    };

    // Initialize when DOM ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        console.log('[TPS-STAR] System initialized');
      });
    } else {
      console.log('[TPS-STAR] System initialized');
    }
  })();
</script>

{%- comment -%} GTM Noscript Fallback {%- endcomment -%}
{%- if gtm_id != blank -%}
  <noscript>
    <iframe src="https://www.googletagmanager.com/ns.html?id={{ gtm_id }}"
            height="0" width="0" style="display:none;visibility:hidden"></iframe>
  </noscript>
{%- endif -%}
```

---

## ⚙️ **CONFIGURATION METAFIELDS REQUISE**

Après le déploiement, configurez ces metafields dans l'Admin Shopify :

**Settings** → **Metafields** → **Shop** → **Add definition**

| Namespace | Key | Type | Value |
|-----------|-----|------|-------|
| `custom_integrations` | `ga4_token` | Single line text | `G-E4NPI2ZZM3` |
| `custom_integrations` | `meta_pixel_id` | Single line text | `1973238620087976` |
| `custom_integrations` | `sentry_dsn` | Single line text | `votre-dsn-complet` |
| `custom_integrations` | `clarity_id` | Single line text | `tzvd9w6rjs` |
| `custom_integrations` | `hotjar_id` | Single line text | `6564192` |
| `custom_integrations` | `cloudflare_beacon_token` | Single line text | `21fd2470...` |

⚠️ **Important** : Activez "Storefront API access" pour chaque metafield !

---

## 🧪 **TEST POST-DÉPLOIEMENT**

1. **Ouvrez votre site** en navigation privée
2. **Console du navigateur** (F12) 
3. **Tapez** : `TPS.debug.enable()`

**✅ Logs attendus :**
```
[TPS-STAR] System initialized
🪟 Clarity loaded: tzvd9w6rjs
🔥 Hotjar loaded: 6564192
[TPS] meta id: 1973238620087976 string
[TPS-STAR] Meta Pixel initialized: 1973238620087976
[TPS-STAR] Sentry initialized
```

**❌ Plus d'erreurs :**
- "integrity metadata check"
- "Invalid PixelID: null"
- "ReferenceError: Sentry is not defined"

---

## 🚀 **MÉTHODE 2 : Via Shopify CLI (Avancée)**

Si vous avez Shopify CLI installé :

```bash
# Dans votre dossier de thème local
shopify theme dev
# Puis copiez le fichier et push
shopify theme push
```

---

Copiez-collez le contenu liquid ci-dessus dans votre snippet `integrations.liquid` et configurez les metafields !
