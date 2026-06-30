#!/usr/bin/env node

/**
 * ---------------------------------------------------------
 * Enterprise Playbook PDF Generator
 * Version : 2.0
 * Author  : Sanjay Kr. Singh
 * ---------------------------------------------------------
 */

const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");

const ROOT = __dirname;

const HTML_FILE = path.join(ROOT, "playbook", "playbook.html");

const OUTPUT_FILE = path.join(
    ROOT,
    "playbook",
    "Enterprise-ERP-UI-Blueprint.pdf"
);

async function launchBrowser() {

    return puppeteer.launch({

        headless: true,

        defaultViewport: null,

        args: [
            "--disable-dev-shm-usage",
            "--font-render-hinting=medium",
            "--no-sandbox",
            "--disable-setuid-sandbox"
        ]
    });

}

async function loadPage(browser) {

    const page = await browser.newPage();

    await page.goto(
        "file://" + HTML_FILE,
        {
            waitUntil: "networkidle0"
        }
    );

    await page.emulateMediaType("print");

    await page.evaluateHandle("document.fonts.ready");

    return page;

}

async function exportPDF(page) {

    await page.pdf({

        path: OUTPUT_FILE,

        format: "A4",

        printBackground: true,

        preferCSSPageSize: true,

        margin: {

            top: "0mm",

            right: "0mm",

            bottom: "0mm",

            left: "0mm"

        }

    });

}

async function run() {

    if (!fs.existsSync(HTML_FILE)) {

        throw new Error(
            "playbook.html not found."
        );

    }

    console.log("");

    console.log("====================================");
    console.log(" Enterprise PDF Generator v2 ");
    console.log("====================================");

    const browser = await launchBrowser();

    try {

        const page = await loadPage(browser);

        console.log("✓ HTML Loaded");

        await exportPDF(page);

        console.log("✓ PDF Generated");

    }

    finally {

        await browser.close();

    }

    console.log("Done.");

}

run().catch(error => {

    console.error(error);

    process.exit(1);

});