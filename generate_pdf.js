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

const HTML_FILE = path.join(ROOT, "playbook", "index.html");

const OUTPUT_FILE = path.join(
    ROOT,
    "playbook",
    "Enterprise-ERP-UI-Blueprint.pdf"
);

function fail(message, fix) {
    console.error("");
    console.error("PDF generation failed.");
    console.error(`  Why: ${message}`);
    if (fix) {
        console.error(`  Fix: ${fix}`);
    }
    process.exit(1);
}

async function launchBrowser() {
    try {
        return await puppeteer.launch({
            headless: true,
            defaultViewport: null,
            args: [
                "--disable-dev-shm-usage",
                "--font-render-hinting=medium",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        });
    } catch (error) {
        fail(
            error.message,
            "run 'npm install' in the project root and ensure Chromium can launch."
        );
    }
}

async function loadPage(browser) {
    const page = await browser.newPage();

    try {
        await page.goto("file://" + HTML_FILE, {
            waitUntil: "networkidle0",
            timeout: 120000
        });
    } catch (error) {
        fail(
            `unable to load ${path.relative(ROOT, HTML_FILE)} (${error.message})`,
            "generate HTML first with 'python generate_playbook.py' and verify local assets load correctly."
        );
    }

    await page.emulateMediaType("print");
    await page.evaluateHandle("document.fonts.ready");

    return page;
}

async function exportPDF(page) {
    try {
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
    } catch (error) {
        fail(
            error.message,
            "verify the generated HTML is valid and Puppeteer has permission to write to playbook/."
        );
    }
}

async function run() {
    if (!fs.existsSync(HTML_FILE)) {
        fail(
            "playbook/index.html was not found.",
            "run 'python generate_playbook.py' to generate HTML before exporting the PDF."
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

        if (!fs.existsSync(OUTPUT_FILE)) {
            fail(
                "Enterprise-ERP-UI-Blueprint.pdf was not created.",
                "check Puppeteer output and disk permissions for the playbook/ folder."
            );
        }

        console.log("✓ PDF Generated");
    } finally {
        await browser.close();
    }

    console.log("Done.");
}

run().catch((error) => {
    fail(error.message, "review the stack trace above and retry after fixing the root cause.");
});
