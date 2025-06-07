let translations = {};
let lastScanData = null;

function loadLanguage(lang) {
    return fetch(`assets/${lang}.json`)
        .then(resp => resp.json())
        .then(data => {
            translations = data;
            document.title = data.title;
            document.getElementById('appName').innerText = data.appName;
            document.getElementById('runScan').innerText = data.runScan;
            document.getElementById('langLabel').innerText = data.language + ':';
        });
}

function switchLanguage(lang) {
    loadLanguage(lang).then(() => {
        if (lastScanData) {
            displayScanResults(lastScanData);
        }
        localStorage.setItem('lang', lang);
        document.getElementById('lang-select').value = lang;
    });
}

function displayScanResults(data) {
    document.getElementById('score').innerHTML =
        translations.openPorts + ': ' + data.scan.open_ports.join(', ') +
        '<br>' + translations.sslDaysLeft + ': ' + data.scan.ssl_days_left +
        '<br>' + translations.mqttSecure + ': ' + data.scan.mqtt_secure +
        '<br>' + translations.cloudflareProtected + ': ' + data.scan.cloudflare_protected;
    document.getElementById('recommendations').innerHTML =
        translations.recommendations + ':<br>' + data.recommendations.join('<br>');
}

function scan() {
    fetch('/scan', {method: 'POST'})
    .then(response => response.json())
    .then(data => {
        lastScanData = data;
        displayScanResults(data);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const lang = localStorage.getItem('lang') || 'en';
    switchLanguage(lang);
});
