#!/usr/bin/env python3
"""
TPS-STAR Master Dashboard Guide - PDF Ultimate
Guide PDF complet avec checklist, actions et dépannage
"""

import os
import sys
from datetime import datetime

def create_master_dashboard_guide():
    """Crée le guide maître complet pour les dashboards"""

    html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TPS-STAR - Guide Maître de Vérification des Dashboards</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
        }

        .cover {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 30px;
            border-radius: 15px;
            margin-bottom: 40px;
            page-break-after: always;
        }

        .cover h1 {
            margin: 0;
            font-size: 3em;
            font-weight: 300;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .cover .subtitle {
            font-size: 1.4em;
            margin: 20px 0;
            opacity: 0.9;
        }

        .cover .version {
            font-size: 1em;
            margin-top: 30px;
            opacity: 0.8;
        }

        .toc {
            background: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 10px;
            padding: 30px;
            margin: 30px 0;
            page-break-inside: avoid;
        }

        .toc h2 {
            text-align: center;
            color: #495057;
            margin-top: 0;
            font-size: 1.8em;
        }

        .toc ul {
            list-style: none;
            padding: 0;
        }

        .toc li {
            padding: 10px 0;
            border-bottom: 1px solid #dee2e6;
            font-size: 1.1em;
        }

        .toc li:last-child {
            border-bottom: none;
        }

        .section {
            margin: 40px 0;
            page-break-before: auto;
        }

        .section h2 {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 30px 0 20px 0;
            font-size: 1.8em;
            text-align: center;
        }

        .platform {
            background: #ffffff;
            border: 3px solid #e9ecef;
            border-radius: 12px;
            padding: 30px;
            margin: 30px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            page-break-inside: avoid;
        }

        .platform.clarity {
            border-color: #6f42c1;
            background: linear-gradient(135deg, #ffffff 0%, #f8f4ff 100%);
        }
        .platform.hotjar {
            border-color: #fd7e14;
            background: linear-gradient(135deg, #ffffff 0%, #fff8f1 100%);
        }
        .platform.ga4 {
            border-color: #28a745;
            background: linear-gradient(135deg, #ffffff 0%, #f1f8f4 100%);
        }
        .platform.meta {
            border-color: #007bff;
            background: linear-gradient(135deg, #ffffff 0%, #f1f6ff 100%);
        }

        .platform h3 {
            margin-top: 0;
            color: #2c3e50;
            font-size: 2em;
            border-bottom: 3px solid #ecf0f1;
            padding-bottom: 15px;
            text-align: center;
        }

        .url-card {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 1.2em;
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        }

        .checklist-section {
            background: #d4edda;
            border: 2px solid #c3e6cb;
            border-radius: 10px;
            padding: 25px;
            margin: 20px 0;
        }

        .checklist-section h4 {
            color: #155724;
            margin-top: 0;
            font-size: 1.4em;
            text-align: center;
        }

        .checklist-section ul {
            margin: 15px 0;
            padding-left: 25px;
        }

        .checklist-section li {
            color: #155724;
            margin: 10px 0;
            font-size: 1.05em;
        }

        .actions-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin: 20px 0;
        }

        .actions-section h4 {
            color: #495057;
            margin-top: 0;
            font-size: 1.4em;
            text-align: center;
        }

        .action-step {
            display: flex;
            align-items: center;
            margin: 15px 0;
            padding: 15px;
            background: white;
            border-radius: 8px;
            border-left: 5px solid #17a2b8;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .step-number {
            background: #17a2b8;
            color: white;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 20px;
            flex-shrink: 0;
            font-size: 1.1em;
        }

        .step-content {
            flex: 1;
        }

        .step-content strong {
            color: #2c3e50;
            font-size: 1.1em;
        }

        .timing-box {
            background: linear-gradient(135deg, #e7f3ff, #cce7ff);
            border: 2px solid #007bff;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }

        .timing-box h4 {
            color: #0056b3;
            margin-top: 0;
            font-size: 1.3em;
        }

        .troubleshoot-box {
            background: linear-gradient(135deg, #ffe6e6, #ffcccc);
            border: 2px solid #dc3545;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }

        .troubleshoot-box h4 {
            color: #721c24;
            margin-top: 0;
            font-size: 1.3em;
            text-align: center;
        }

        .code-block {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.95em;
            margin: 15px 0;
            overflow-x: auto;
            border: 1px solid #34495e;
        }

        .summary-table {
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            background: white;
        }

        .summary-table th,
        .summary-table td {
            border: 1px solid #ddd;
            padding: 15px;
            text-align: left;
        }

        .summary-table th {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            font-weight: 600;
            color: #495057;
            font-size: 1.1em;
        }

        .summary-table tr:nth-child(even) {
            background: #f8f9fa;
        }

        .final-validation {
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            border: 3px solid #28a745;
            border-radius: 15px;
            padding: 30px;
            margin: 40px 0;
            text-align: center;
        }

        .final-validation h3 {
            color: #155724;
            margin-top: 0;
            font-size: 2em;
        }

        .test-script-master {
            background: linear-gradient(135deg, #f1f3f4, #e8eaed);
            border: 3px solid #5f6368;
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
        }

        .test-script-master h3 {
            margin-top: 0;
            color: #1a73e8;
            font-size: 1.6em;
            text-align: center;
        }

        @media print {
            body { margin: 0; padding: 15px; }
            .platform { page-break-inside: avoid; }
            .cover { page-break-after: always; }
            .section { page-break-before: auto; }
        }
    </style>
</head>
<body>
    <!-- PAGE DE COUVERTURE -->
    <div class="cover">
        <h1>🚀 TPS-STAR</h1>
        <div class="subtitle">
            Guide Maître de Vérification des Dashboards
        </div>
        <div class="subtitle">
            Système de Tracking Universel Shopify
        </div>
        <div class="version">
            Version 2.0 • """ + datetime.now().strftime("%d/%m/%Y") + """<br>
            Guide complet avec checklist, actions étape par étape et dépannage
        </div>
    </div>

    <!-- TABLE DES MATIÈRES -->
    <div class="toc">
        <h2>📋 Table des Matières</h2>
        <ul>
            <li><strong>1. Instructions Préliminaires</strong> - Prérequis et préparation</li>
            <li><strong>2. Microsoft Clarity</strong> - Checklist et actions (ID: tzvd9w6rjs)</li>
            <li><strong>3. Hotjar</strong> - Checklist et actions (ID: 6564192)</li>
            <li><strong>4. Google Analytics 4</strong> - Checklist et actions (ID: G-E4NPI2ZZM3)</li>
            <li><strong>5. Meta Business</strong> - Checklist et actions (ID: 1973238620087976)</li>
            <li><strong>6. Timing et Tableau Récapitulatif</strong> - Délais d'apparition</li>
            <li><strong>7. Script de Test Maître</strong> - Test automatique global</li>
            <li><strong>8. Dépannage Global</strong> - Solutions aux problèmes courants</li>
            <li><strong>9. Validation Finale</strong> - Confirmation du succès</li>
        </ul>
    </div>

    <!-- SECTION 1: INSTRUCTIONS PRÉLIMINAIRES -->
    <div class="section">
        <h2>1. 📋 Instructions Préliminaires</h2>

        <div style="background: linear-gradient(135deg, #d1ecf1, #b8daff); border: 2px solid #007bff; border-radius: 15px; padding: 30px; margin: 30px 0;">
            <h3 style="margin-top: 0; color: #0c5460; text-align: center; font-size: 1.6em;">🎯 Prérequis Obligatoires</h3>

            <div style="font-size: 1.1em; color: #0c5460;">
                <p><strong>✅ Système TPS-STAR déployé :</strong> Votre système doit être actif sur votre site Shopify</p>
                <p><strong>✅ Test de base réussi :</strong> <code>TPS.debug.enable()</code> doit fonctionner sans erreur dans la console</p>
                <p><strong>✅ Navigation active :</strong> Naviguez sur 3-5 pages de votre site avant de vérifier</p>
                <p><strong>✅ Timing respecté :</strong> Attendez 2-10 minutes après navigation pour voir les données</p>
                <p><strong>✅ Navigateur propre :</strong> Désactivez les ad-blockers, sortez du mode privé</p>
            </div>
        </div>

        <div style="background: #fff3cd; border: 2px solid #ffc107; border-radius: 10px; padding: 20px; margin: 20px 0;">
            <h4 style="color: #856404; margin-top: 0;">⚠️ Important</h4>
            <p style="color: #856404; margin: 0;">Ce guide suppose que votre TPS-STAR fonctionne. Si <code>TPS.debug.enable()</code> ne fonctionne pas, résolvez d'abord les problèmes d'installation avant de vérifier les dashboards.</p>
        </div>
    </div>

    <!-- SECTION 2: MICROSOFT CLARITY -->
    <div class="section">
        <h2>2. 🪟 Microsoft Clarity</h2>

        <div class="platform clarity">
            <h3>Microsoft Clarity Dashboard</h3>

            <div class="url-card">
                🔗 URL : https://clarity.microsoft.com
            </div>

            <div style="text-align: center; font-size: 1.2em; color: #6f42c1; margin: 20px 0;">
                <strong>🆔 ID Configuré : tzvd9w6rjs</strong>
            </div>

            <div class="checklist-section">
                <h4>✅ Checklist de Vérification</h4>
                <ul>
                    <li><strong>Dashboard principal</strong> → Nouvelles sessions apparaissent en temps réel</li>
                    <li><strong>Real-time</strong> → Activité en cours avec votre localisation</li>
                    <li><strong>Recordings</strong> → Enregistrements vidéo de vos actions</li>
                    <li><strong>Heatmaps</strong> → Cartes de chaleur des clics et scrolls</li>
                    <li><strong>Insights</strong> → Métriques d'engagement utilisateur</li>
                </ul>
            </div>

            <div class="actions-section">
                <h4>🎯 Actions Étape par Étape</h4>

                <div class="action-step">
                    <div class="step-number">1</div>
                    <div class="step-content">
                        <strong>Se connecter</strong><br>
                        Utilisez votre compte Microsoft associé au projet
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">2</div>
                    <div class="step-content">
                        <strong>Sélectionner le projet</strong><br>
                        Choisissez votre projet TPS-STAR dans la liste
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">3</div>
                    <div class="step-content">
                        <strong>Vérifier le Dashboard</strong><br>
                        Sessions actives et métriques des dernières 24h visibles
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">4</div>
                    <div class="step-content">
                        <strong>Tester les Recordings</strong><br>
                        Cliquez sur une session récente → vidéo de navigation
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">5</div>
                    <div class="step-content">
                        <strong>Examiner les Heatmaps</strong><br>
                        Heatmaps → page → zones de clics/scrolls actives
                    </div>
                </div>
            </div>

            <div class="timing-box">
                <h4>⏱️ Timing d'Apparition</h4>
                <p><strong>Données apparaissent en :</strong> 2-5 minutes</p>
                <p><strong>Délai maximum :</strong> 15 minutes</p>
            </div>

            <div class="troubleshoot-box">
                <h4>🔧 Dépannage Clarity</h4>
                <p><strong>Si aucune donnée n'apparaît, testez dans la console :</strong></p>
                <div class="code-block">
// Test de Microsoft Clarity
typeof clarity  // Doit retourner "function"
clarity('identify', 'test-user-clarity-' + Date.now())
clarity('set', 'test_source', 'tps_star_verification')
console.log('✅ Test Clarity envoyé')
                </div>
            </div>
        </div>
    </div>

    <!-- SECTION 3: HOTJAR -->
    <div class="section">
        <h2>3. 🔥 Hotjar</h2>

        <div class="platform hotjar">
            <h3>Hotjar Analytics Dashboard</h3>

            <div class="url-card">
                🔗 URL : https://insights.hotjar.com
            </div>

            <div style="text-align: center; font-size: 1.2em; color: #fd7e14; margin: 20px 0;">
                <strong>🆔 ID Configuré : 6564192</strong>
            </div>

            <div class="checklist-section">
                <h4>✅ Checklist de Vérification</h4>
                <ul>
                    <li><strong>Dashboard Status</strong> → "Tracking Status: Active" en vert</li>
                    <li><strong>Recordings</strong> → Sessions d'enregistrement récentes</li>
                    <li><strong>Heatmaps</strong> → Données de clics/scrolls actives</li>
                    <li><strong>Verify Installation</strong> → Validation ✅ dans Settings</li>
                    <li><strong>Surveys & Feedback</strong> → Outils disponibles</li>
                </ul>
            </div>

            <div class="actions-section">
                <h4>🎯 Actions Étape par Étape</h4>

                <div class="action-step">
                    <div class="step-number">1</div>
                    <div class="step-content">
                        <strong>Se connecter</strong><br>
                        Accédez à votre compte Hotjar
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">2</div>
                    <div class="step-content">
                        <strong>Vérifier le statut</strong><br>
                        "Tracking Status: Active" (voyant vert) en haut
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">3</div>
                    <div class="step-content">
                        <strong>Examiner les Recordings</strong><br>
                        Recordings → sessions de navigation récentes
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">4</div>
                    <div class="step-content">
                        <strong>Tester les Heatmaps</strong><br>
                        Heatmaps → vérifiez les données de clics
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">5</div>
                    <div class="step-content">
                        <strong>Valider l'installation</strong><br>
                        Settings → Installation → "Verify Installation" ✅
                    </div>
                </div>
            </div>

            <div class="timing-box">
                <h4>⏱️ Timing d'Apparition</h4>
                <p><strong>Données apparaissent en :</strong> 3-10 minutes</p>
                <p><strong>Délai maximum :</strong> 20 minutes</p>
            </div>

            <div class="troubleshoot-box">
                <h4>🔧 Dépannage Hotjar</h4>
                <p><strong>Si "Tracking Inactive", testez dans la console :</strong></p>
                <div class="code-block">
// Test de Hotjar
typeof hj  // Doit retourner "function"
hj('identify', 'test-user-hotjar-' + Date.now(), {
    test_source: 'tps_star',
    verification: true
})
console.log('✅ Test Hotjar envoyé')
                </div>
            </div>
        </div>
    </div>

    <!-- SECTION 4: GOOGLE ANALYTICS 4 -->
    <div class="section">
        <h2>4. 📈 Google Analytics 4</h2>

        <div class="platform ga4">
            <h3>Google Analytics 4 Dashboard</h3>

            <div class="url-card">
                🔗 URL : https://analytics.google.com
            </div>

            <div style="text-align: center; font-size: 1.2em; color: #28a745; margin: 20px 0;">
                <strong>🆔 ID Configuré : G-E4NPI2ZZM3</strong>
            </div>

            <div class="checklist-section">
                <h4>✅ Checklist de Vérification</h4>
                <ul>
                    <li><strong>Realtime</strong> → Utilisateurs actifs (vous) visibles immédiatement</li>
                    <li><strong>Events</strong> → page_view, session_start, user_engagement</li>
                    <li><strong>Pages and screens</strong> → Vos pages avec métriques</li>
                    <li><strong>Locations</strong> → Votre géolocalisation correcte</li>
                    <li><strong>Traffic acquisition</strong> → Source de trafic identifiée</li>
                </ul>
            </div>

            <div class="actions-section">
                <h4>🎯 Actions Étape par Étape</h4>

                <div class="action-step">
                    <div class="step-number">1</div>
                    <div class="step-content">
                        <strong>Se connecter</strong><br>
                        Sélectionnez la propriété avec l'ID correct
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">2</div>
                    <div class="step-content">
                        <strong>Aller dans Realtime</strong><br>
                        Menu gauche → Reports → Realtime
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">3</div>
                    <div class="step-content">
                        <strong>Vérifier "Users in last 30 minutes"</strong><br>
                        Le chiffre doit être ≥ 1 (vous) pendant navigation
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">4</div>
                    <div class="step-content">
                        <strong>Examiner les Events</strong><br>
                        "Event count by Event name" → événements récents
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">5</div>
                    <div class="step-content">
                        <strong>Contrôler la géolocalisation</strong><br>
                        "Users by country" → votre pays affiché
                    </div>
                </div>
            </div>

            <div class="timing-box">
                <h4>⏱️ Timing d'Apparition</h4>
                <p><strong>Données temps réel :</strong> IMMÉDIAT (0-2 minutes)</p>
                <p><strong>Délai maximum :</strong> 5 minutes</p>
            </div>

            <div class="troubleshoot-box">
                <h4>🔧 Dépannage GA4</h4>
                <p><strong>Si pas de données temps réel, testez dans la console :</strong></p>
                <div class="code-block">
// Test de Google Analytics 4
typeof gtag  // Doit retourner "function"
gtag('event', 'tps_verification', {
    test_parameter: 'dashboard_check',
    timestamp: Date.now()
})
console.log('✅ Test GA4 envoyé')
                </div>
            </div>
        </div>
    </div>

    <!-- SECTION 5: META BUSINESS -->
    <div class="section">
        <h2>5. 📱 Meta Business (Facebook Pixel)</h2>

        <div class="platform meta">
            <h3>Meta Business Events Manager</h3>

            <div class="url-card">
                🔗 URL : https://business.facebook.com/events_manager
            </div>

            <div style="text-align: center; font-size: 1.2em; color: #007bff; margin: 20px 0;">
                <strong>🆔 ID Configuré : 1973238620087976</strong>
            </div>

            <div class="checklist-section">
                <h4>✅ Checklist de Vérification</h4>
                <ul>
                    <li><strong>Events</strong> → PageView événements en temps réel</li>
                    <li><strong>Test Events</strong> → Activité récente depuis votre IP</li>
                    <li><strong>Pixel Quality</strong> → Score "Good" ou "Great"</li>
                    <li><strong>Data Sources</strong> → Pixel status "Active"</li>
                    <li><strong>Overview</strong> → Métriques d'événements actives</li>
                </ul>
            </div>

            <div class="actions-section">
                <h4>🎯 Actions Étape par Étape</h4>

                <div class="action-step">
                    <div class="step-number">1</div>
                    <div class="step-content">
                        <strong>Se connecter</strong><br>
                        Accédez à votre compte Business Manager
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">2</div>
                    <div class="step-content">
                        <strong>Sélectionner le Pixel</strong><br>
                        Events Manager → Data Sources → pixel TPS-STAR
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">3</div>
                    <div class="step-content">
                        <strong>Vérifier Test Events</strong><br>
                        Onglet "Test Events" → événements PageView récents
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">4</div>
                    <div class="step-content">
                        <strong>Examiner Events</strong><br>
                        Onglet "Events" → nombre d'événements récents
                    </div>
                </div>

                <div class="action-step">
                    <div class="step-number">5</div>
                    <div class="step-content">
                        <strong>Contrôler Overview</strong><br>
                        Pixel status "Active" et métriques connectées
                    </div>
                </div>
            </div>

            <div class="timing-box">
                <h4>⏱️ Timing d'Apparition</h4>
                <p><strong>Test Events :</strong> 1-5 minutes</p>
                <p><strong>Events standard :</strong> 5-10 minutes</p>
            </div>

            <div class="troubleshoot-box">
                <h4>🔧 Dépannage Meta Business</h4>
                <p><strong>Si pas d'événements, testez dans la console :</strong></p>
                <div class="code-block">
// Test de Meta Pixel
typeof fbq  // Doit retourner "function"
fbq('track', 'Lead', {
    test_source: 'tps_star_verification',
    timestamp: Date.now()
})
console.log('✅ Test Meta Pixel envoyé')
                </div>
            </div>
        </div>
    </div>

    <!-- SECTION 6: TIMING ET TABLEAU -->
    <div class="section">
        <h2>6. ⏱️ Timing et Tableau Récapitulatif</h2>

        <table class="summary-table">
            <thead>
                <tr>
                    <th>Plateforme</th>
                    <th>URL Dashboard</th>
                    <th>ID Configuré</th>
                    <th>Temps d'apparition</th>
                    <th>Où vérifier en priorité</th>
                    <th>Délai maximum</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Microsoft Clarity</strong></td>
                    <td>clarity.microsoft.com</td>
                    <td>tzvd9w6rjs</td>
                    <td>2-5 minutes</td>
                    <td>Real-time dashboard</td>
                    <td>15 minutes</td>
                </tr>
                <tr>
                    <td><strong>Hotjar</strong></td>
                    <td>insights.hotjar.com</td>
                    <td>6564192</td>
                    <td>3-10 minutes</td>
                    <td>Recordings/Dashboard</td>
                    <td>20 minutes</td>
                </tr>
                <tr>
                    <td><strong>Google Analytics 4</strong></td>
                    <td>analytics.google.com</td>
                    <td>G-E4NPI2ZZM3</td>
                    <td>Immédiat-2 minutes</td>
                    <td>Real-time reports</td>
                    <td>5 minutes</td>
                </tr>
                <tr>
                    <td><strong>Meta Business</strong></td>
                    <td>business.facebook.com/events_manager</td>
                    <td>1973238620087976</td>
                    <td>1-5 minutes</td>
                    <td>Test Events</td>
                    <td>10 minutes</td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- SECTION 7: SCRIPT DE TEST MAÎTRE -->
    <div class="section">
        <h2>7. 🧪 Script de Test Maître</h2>

        <div class="test-script-master">
            <h3>Script de Test Automatique Global</h3>
            <p style="text-align: center; font-size: 1.1em; margin-bottom: 20px;">
                <strong>Copiez-collez ce code dans la console de votre site pour tester tous les trackers :</strong>
            </p>

            <div class="code-block">
// ===============================================
// === TPS-STAR MASTER VERIFICATION SCRIPT ===
// ===============================================

console.group('🚀 TPS-STAR Master Verification');

// Étape 1: Vérifier que TPS est chargé
console.log('1. 🔍 TPS System Status:', typeof TPS === 'object' ? '✅ Loaded' : '❌ Missing');

// Étape 2: Vérifier chaque tracker individuellement
const trackers = {
  '🪟 Microsoft Clarity (clarity)': typeof clarity,
  '🔥 Hotjar (hj)': typeof hj,
  '📈 Google Analytics (gtag)': typeof gtag,
  '📱 Meta Pixel (fbq)': typeof fbq
};

console.log('2. 📊 Individual Trackers Status:');
Object.entries(trackers).forEach(([name, type]) => {
  const status = type === 'function' ? '✅ ACTIVE' : '❌ MISSING';
  console.log(`   ${status} ${name}: ${type}`);
});

// Étape 3: Envoyer des événements de test pour chaque tracker
console.log('3. 🎯 Sending comprehensive test events...');

const timestamp = Date.now();
const testId = 'tps-master-test-' + timestamp;

// Test Microsoft Clarity
if (typeof clarity === 'function') {
  clarity('set', 'test_source', 'tps_star_master');
  clarity('identify', testId);
  console.log('   ✅ Microsoft Clarity: Test data sent');
} else {
  console.log('   ❌ Microsoft Clarity: UNAVAILABLE');
}

// Test Hotjar
if (typeof hj === 'function') {
  hj('identify', testId, {
    test_source: 'tps_star_master',
    timestamp: timestamp,
    verification: 'master_test'
  });
  console.log('   ✅ Hotjar: Test identification sent');
} else {
  console.log('   ❌ Hotjar: UNAVAILABLE');
}

// Test Google Analytics 4
if (typeof gtag === 'function') {
  gtag('event', 'tps_master_verification', {
    test_source: 'tps_star_master',
    test_id: testId,
    timestamp: timestamp,
    verification_type: 'comprehensive'
  });
  console.log('   ✅ Google Analytics 4: Test event sent');
} else {
  console.log('   ❌ Google Analytics 4: UNAVAILABLE');
}

// Test Meta Pixel
if (typeof fbq === 'function') {
  fbq('track', 'Lead', {
    test_source: 'tps_star_master',
    test_id: testId,
    timestamp: timestamp,
    verification: 'master_test'
  });
  console.log('   ✅ Meta Pixel: Test Lead event sent');
} else {
  console.log('   ❌ Meta Pixel: UNAVAILABLE');
}

// Étape 4: Résumé final
console.log('4. 📋 VERIFICATION SUMMARY:');
const activeTrackers = Object.values(trackers).filter(type => type === 'function').length;
const totalTrackers = Object.keys(trackers).length;

console.log(`   Active Trackers: ${activeTrackers}/${totalTrackers}`);
console.log(`   Test ID: ${testId}`);
console.log(`   Timestamp: ${new Date(timestamp).toLocaleString()}`);

if (activeTrackers === totalTrackers) {
  console.log('   🎉 STATUS: ALL TRACKERS ACTIVE - TPS-STAR 100% OPERATIONAL!');
  console.log('   📊 Check dashboards in 2-10 minutes for test data');
} else {
  console.log('   ⚠️  STATUS: SOME TRACKERS MISSING - CHECK CONFIGURATION');
  console.log('   🔧 Review metafields and TPS-STAR installation');
}

console.groupEnd();

// Instructions finales
console.log('');
console.log('📋 NEXT STEPS:');
console.log('1. Wait 2-10 minutes for data to appear in dashboards');
console.log('2. Check each platform using the URLs in your guide');
console.log('3. Look for the test events with ID:', testId);
console.log('4. Verify all 4 platforms show recent activity');
console.log('');
console.log('🚀 TPS-STAR Master Verification Complete!');
            </div>
        </div>
    </div>

    <!-- SECTION 8: DÉPANNAGE GLOBAL -->
    <div class="section">
        <h2>8. 🆘 Dépannage Global</h2>

        <div style="background: linear-gradient(135deg, #fff3cd, #ffeaa1); border: 3px solid #ffc107; border-radius: 15px; padding: 30px; margin: 30px 0;">
            <h3 style="color: #856404; margin-top: 0; text-align: center; font-size: 1.6em;">🔧 Solutions aux Problèmes Courants</h3>

            <div style="background: white; border-radius: 10px; padding: 25px; margin: 20px 0;">
                <h4 style="color: #721c24; margin-top: 0;">❌ Si AUCUNE donnée n'apparaît dans AUCUN dashboard :</h4>
                <ul style="color: #856404; font-size: 1.05em;">
                    <li><strong>Navigation privée :</strong> Sortez du mode navigation privée</li>
                    <li><strong>Ad-blockers :</strong> Désactivez temporairement tous les bloqueurs</li>
                    <li><strong>Autre appareil :</strong> Testez depuis une connexion/appareil différent</li>
                    <li><strong>Metafields Shopify :</strong> Vérifiez namespace "custom_integrations"</li>
                    <li><strong>TPS Debug :</strong> Confirmez que <code>TPS.debug.enable()</code> fonctionne</li>
                </ul>
            </div>

            <div style="background: white; border-radius: 10px; padding: 25px; margin: 20px 0;">
                <h4 style="color: #721c24; margin-top: 0;">⚠️ Si seulement CERTAINES plateformes ne fonctionnent pas :</h4>
                <ul style="color: #856404; font-size: 1.05em;">
                    <li><strong>IDs spécifiques :</strong> Vérifiez les IDs dans les metafields Shopify</li>
                    <li><strong>Fonctions individuelles :</strong> Testez chaque tracker dans la console</li>
                    <li><strong>Logs d'erreur :</strong> Consultez F12 → Console pour les erreurs</li>
                    <li><strong>Storefront API :</strong> Vérifiez l'accès pour tous les metafields</li>
                    <li><strong>Case sensitivity :</strong> Respectez majuscules/minuscules des clés</li>
                </ul>
            </div>

            <div style="background: white; border-radius: 10px; padding: 25px; margin: 20px 0;">
                <h4 style="color: #721c24; margin-top: 0;">🔍 Tests de diagnostic avancés :</h4>
                <div class="code-block">
// Diagnostic avancé - dans la console de votre site
console.log('=== TPS-STAR DIAGNOSTIC ===');
console.log('TPS Object:', typeof TPS);
console.log('TPS Debug Available:', typeof TPS?.debug?.enable);

// Test chaque metafield
const metafields = ['microsoftClarity', 'hotjar', 'googleAnalytics', 'metaPixel'];
metafields.forEach(field => {
  console.log(`Metafield ${field}:`, window.tpsConfig?.[field] || 'Missing');
});

// Vérifier les erreurs réseau
console.log('Network errors in Console tab - look for failed script loads');
                </div>
            </div>
        </div>
    </div>

    <!-- SECTION 9: VALIDATION FINALE -->
    <div class="section">
        <h2>9. 🎉 Validation Finale</h2>

        <div class="final-validation">
            <h3>🚀 Votre TPS-STAR est 100% Opérationnel !</h3>

            <div style="font-size: 1.2em; margin: 25px 0;">
                <strong>Une fois que vous voyez des données dans LES 4 dashboards :</strong>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 30px 0; text-align: left;">
                <div style="background: rgba(255,255,255,0.8); padding: 20px; border-radius: 10px;">
                    <h4 style="color: #155724; margin-top: 0;">🪟 Microsoft Clarity</h4>
                    <p style="color: #155724; margin: 0;">✅ Sessions et enregistrements visibles</p>
                </div>

                <div style="background: rgba(255,255,255,0.8); padding: 20px; border-radius: 10px;">
                    <h4 style="color: #155724; margin-top: 0;">🔥 Hotjar</h4>
                    <p style="color: #155724; margin: 0;">✅ Status "Active" + recordings disponibles</p>
                </div>

                <div style="background: rgba(255,255,255,0.8); padding: 20px; border-radius: 10px;">
                    <h4 style="color: #155724; margin-top: 0;">📈 Google Analytics 4</h4>
                    <p style="color: #155724; margin: 0;">✅ Utilisateurs temps réel ≥ 1</p>
                </div>

                <div style="background: rgba(255,255,255,0.8); padding: 20px; border-radius: 10px;">
                    <h4 style="color: #155724; margin-top: 0;">📱 Meta Business</h4>
                    <p style="color: #155724; margin: 0;">✅ Événements test + PageView actifs</p>
                </div>
            </div>

            <div style="font-size: 1.3em; font-weight: bold; color: #155724; margin-top: 30px;">
                🎊 FÉLICITATIONS ! 🎊<br>
                Votre système TPS-STAR fonctionne parfaitement !<br>
                Toutes les plateformes reçoivent correctement les données !
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <div style="text-align: center; margin-top: 50px; padding: 30px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 15px; color: #6c757d;">
        <p style="font-size: 1.3em; font-weight: bold; margin: 0 0 10px 0;">🚀 TPS-STAR Universal Tracking System</p>
        <p style="font-size: 1.1em; margin: 0 0 10px 0;">Guide Maître de Vérification des Dashboards</p>
        <p style="margin: 0 0 20px 0;">Version 2.0 - Guide généré le """ + datetime.now().strftime("%d/%m/%Y à %H:%M") + """</p>
        <p style="font-size: 1.1em; font-weight: bold; color: #28a745; margin: 0;">
            Une fois tous les dashboards validés, votre tracking universel est pleinement opérationnel ! 🎉
        </p>
    </div>
</body>
</html>
    """

    # Créer le fichier HTML
    html_file = "TPS-STAR-Master-Dashboard-Guide.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Guide Maître HTML créé : {html_file}")
    return html_file

if __name__ == "__main__":
    print("🚀 TPS-STAR - Génération du Guide Maître des Dashboards")
    print("=" * 60)

    guide_file = create_master_dashboard_guide()

    print()
    print("🎯 GUIDE MAÎTRE CRÉÉ AVEC SUCCÈS !")
    print(f"📁 Fichier : {guide_file}")
    print()
    print("📖 Ce guide maître contient TOUT :")
    print("   • Page de couverture professionnelle")
    print("   • Table des matières complète")
    print("   • Instructions préliminaires détaillées")
    print("   • Checklist + Actions pour chaque plateforme")
    print("   • Tableau récapitulatif des timings")
    print("   • Script de test maître automatique")
    print("   • Solutions de dépannage complètes")
    print("   • Validation finale avec félicitations")
    print()
    print("🌟 Guide professionnel de 9 sections pour une vérification complète !")
