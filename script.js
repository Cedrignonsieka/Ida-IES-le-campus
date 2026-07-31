// TES LIENS GOOGLE SHEET
const URL_CLASSEMENT = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQULxJOCxlp-vjeYfhXexfaKTBHl-aLBiq37_ROaPxB008hH1Rjr1Sp-Qr5rgOTBDo6jdTO7VPzZQTk/pub?gid=0&single=true&output=csv";
const URL_MATCHS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQULxJOCxlp-vjeYfhXexfaKTBHl-aLBiq37_ROaPxB008hH1Rjr1Sp-Qr5rgOTBDo6jdTO7VPzZQTk/pub?gid=413650798&single=true&output=csv";

// Fonction pour lire CSV
async function fetchCSV(url) {
    const res = await fetch(url);
    const data = await res.text();
    const rows = data.split('\n').slice(1);
    return rows.map(r => r.split(','));
}

// Charger tout
async function chargerDonnees() {
    const [classementData, matchsData] = await Promise.all([
        fetchCSV(URL_CLASSEMENT),
        fetchCSV(URL_MATCHS)
    ]);

    // Classement
    const classementHTML = classementData.map(r => 
        `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td><td>${r[4]}</td></tr>`
    ).join('');
    document.getElementById('classement-body').innerHTML = classementHTML;

    // Matchs
    const matchs = matchsData.map(r => ({
        e1: r[0], s1: r[1], e2: r[2], s2: r[3], 
        date: r[4], heure: r[5], statut: r[6], poule: r[7]
    }));

    const live = matchs.find(m => m.statut === "EN COURS");
    const aVenir = matchs.filter(m => m.statut === "À VENIR");
    const termines = matchs.filter(m => m.statut === "TERMINÉ");

    // Afficher Live format: Ziondrou 1 - 0 Zibo
    document.getElementById('live-match').innerHTML = live
       ? `<div class="card live-card">${live.e1} ${live.s1} - ${live.s2} ${live.e2}<br><small>Poule ${live.poule}</small></div>`
        : 'Aucun match en cours';

    // Afficher listes
    document.getElementById('matchs-a-venir').innerHTML = aVenir.map(m => 
        `<div class="card">${m.e1} vs ${m.e2} - ${m.date} ${m.heure}</div>`
    ).join('');
    
    document.getElementById('matchs-termines').innerHTML = termines.map(m => 
        `<div class="card">${m.e1} ${m.s1} - ${m.s2} ${m.e2}</div>`
    ).join('');
}

// Lancer au démarrage + actualiser toutes les 10 secondes
chargerDonnees();
setInterval(chargerDonnees, 10000);
