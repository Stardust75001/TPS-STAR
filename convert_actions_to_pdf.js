const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function convertActionsToPDF() {
    console.log('⚡ Conversion du guide Actions Rapides vers PDF...');

    const htmlFile = 'TPS-STAR-Actions-Rapides-Guide.html';
    const pdfFile = 'TPS-STAR-Actions-Rapides-Guide.pdf';

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

        // Générer le PDF
        await page.pdf({
            path: pdfFile,
            format: 'A4',
            printBackground: true,
            margin: {
                top: '20mm',
                right: '20mm',
                bottom: '20mm',
                left: '20mm'
            }
        });

        await browser.close();

        console.log('✅ Guide Actions Rapides PDF créé :', pdfFile);
        console.log('📄 Taille du fichier :', Math.round(fs.statSync(pdfFile).size / 1024), 'KB');

    } catch (error) {
        console.error('❌ Erreur lors de la conversion :', error.message);
        process.exit(1);
    }
}

convertActionsToPDF();
