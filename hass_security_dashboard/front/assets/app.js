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
            if (document.getElementById('downloadReport')) {
                document.getElementById('downloadReport').innerText = data.downloadReport;
            }
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
    const scan = data.scan;
    let html =
        translations.openPorts + ': ' + scan.open_ports.join(', ') +
        '<br>' + translations.sslDaysLeft + ': ' + scan.ssl_days_left +
        '<br>' + translations.mqttSecure + ': ' + scan.mqtt_secure +
        '<br>' + translations.cloudflareProtected + ': ' + scan.cloudflare_protected +
        '<br>' + translations.duckdnsMatch + ': ' + scan.duckdns_match +
        '<br>' + translations.configSecurity + ': ' + JSON.stringify(scan.config_security) +
        '<br>' + translations.sshAddon + ': ' + JSON.stringify(scan.ssh_addon) +
        '<br>' + translations.coreInfo + ': ' + JSON.stringify(scan.core);
    document.getElementById('score').innerHTML = html;
    document.getElementById('recommendations').innerHTML =
        translations.recommendations + ':<br>' + data.recommendations.join('<br>');
}

function downloadReport() {
    window.location.href = '/report';
}

function scan() {
    fetch('/scan', {method: 'POST'})
    .then(response => response.json())
    .then(data => {
        lastScanData = data;
        displayScanResults(data);
        document.getElementById('downloadReport').style.display = 'inline-block';
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const lang = localStorage.getItem('lang') || 'en';
    switchLanguage(lang);
    const btn = document.getElementById('downloadReport');
    if (btn) {
        btn.style.display = 'none';
    }
});
