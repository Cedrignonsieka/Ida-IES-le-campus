const SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSAR_4pCD4X3GkeT2N7GxXNgUd8qBH3tYvfUV-BWP286w9c6LwhADlQcDkVRipeG5D2NabPlwyAfB0j/pub?gid=0&single=true&output=csv";

async function chargerClassement() {
    try {
        const response = await fetch(SHEET_URL);
        const data = await response.text();
        const lignes = data.split('\n').slice(1); // enlève la ligne des titres

        const tableau = document.getElementById('classement-body');
        tableau.innerHTML = '';

        lignes.forEach((ligne, index) => {
            const colonnes = ligne.split(',');
            if(colonnes[0] && colonnes[0]!== '') {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${colonnes[0]}</td>
                    <td>${colonnes[1]}</td>
                    <td><b>${colonnes[2]}</b></td>
                `;
                tableau.appendChild(tr);
            }
        });
    } catch (error) {
        console.log("Erreur chargement:", error);
        document.getElementById('classement-body').innerHTML = '<tr><td colspan="4">Erreur de chargement</td></tr>';
    }
}

// Charger au début
chargerClassement();

// Recharger toutes les 30 secondes
setInterval(chargerClassement, 30000);
