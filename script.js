const SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSAR_4pCD4X3GkeT2N7GxXNgUd8qBH3tYvfUV-BWP286w9c6LwhADlQcDkVRipeG5D2NabPlwyAfB0j/pub?gid=0&single=true&output=csv";

async function chargerClassement() {
    try {
        const response = await fetch(SHEET_URL);
        const data = await response.text();
        const lignes = data.split('\n').slice(1); // on enlève la ligne des titres

        // On transforme en tableau et on trie par Points décroissant
        const equipes = lignes
           .map(ligne => ligne.split(','))
           .filter(col => col[0] && col[0].trim()!== '') // enlever lignes vides
           .sort((a, b) => Number(b[3]) - Number(a[3])); // Colonne D = Point

        const tableau = document.getElementById('classement-body');
        tableau.innerHTML = '';

        equipes.forEach((colonnes, index) => {
            const equipe = colonnes[0]; // Col A
            const victoire = colonnes[1]; // Col B
            const defaite = colonnes[2]; // Col C
            const points = colonnes[3]; // Col D

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${index + 1}</td>
                <td>${equipe}</td>
                <td>${victoire}V - ${defaite}D</td>
                <td><b>${points}</b></td>
            `;
            tableau.appendChild(tr);
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
