const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function convertMasterToPDF() {
    console.log('🚀 Conversion du Guide Maître vers PDF...');

    const htmlFile = 'TPS-STAR-Master-Dashboard-Guide.html';
    const pdfFile = 'TPS-STAR-Master-Dashboard-Guide.pdf';

    if (!fs.existsSync(htmlFile)) {
        console.error('❌ Fichier HTML non trouvé :', htmlFile);
        process.exit(1);
    }

    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();

        // Charger le fichier HTML
        const htmlPath = path.resolve(htmlFile);
        await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });

        // Générer le PDF avec options avancées
        await page.pdf({
            path: pdfFile,
            format: 'A4',
            printBackground: true,
            margin: {
                top: '15mm',
                right: '15mm',
                bottom: '15mm',
                left: '15mm'
            },
            displayHeaderFooter: true,
            headerTemplate: '<div style="font-size: 10px; text-align: center; width: 100%; color: #666;">TPS-STAR - Guide Maître de Vérification des Dashboards</div>',
            footerTemplate: '<div style="font-size: 10px; text-align: center; width: 100%; color: #666;">Page <span class="pageNumber"></span> sur <span class="totalPages"></span></div>'
        });

        await browser.close();

        console.log('✅ Guide Maître PDF créé avec succès :', pdfFile);
        console.log('📄 Taille du fichier :', Math.round(fs.statSync(pdfFile).size / 1024), 'KB');
        console.log('📋 Fonctionnalités : Header/Footer, numérotation de pages, mise en page optimisée');

    } catch (error) {
        console.error('❌ Erreur lors de la conversion :', error.message);
        process.exit(1);
    }
}

convertMasterToPDF();
