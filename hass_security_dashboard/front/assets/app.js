function scan() {
    fetch('/scan', {method: 'POST'})
    .then(response => response.json())
    .then(data => {
        document.getElementById('score').innerHTML = 'Open Ports: ' + data.scan.open_ports.join(', ') +
            '<br>SSL Days Left: ' + data.scan.ssl_days_left +
            '<br>MQTT Secure: ' + data.scan.mqtt_secure +
            '<br>Cloudflare Protected: ' + data.scan.cloudflare_protected;
        document.getElementById('recommendations').innerHTML = 'Recommendations:<br>' + data.recommendations.join('<br>') +
            '<br><a href="/report" download>Download Report</a>';
    });
}