const URL_CLASSEMENT = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQULxJOCxlp-vjeYfhXexfaKTBHl-aLBiq37_ROaPxB008hH1Rjr1Sp-Qr5rgOTBDo6jdTO7VPzZQTk/pub?gid=0&single=true&output=csv";
const URL_MATCHS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQULxJOCxlp-vjeYfhXexfaKTBHl-aLBiq37_ROaPxB008hH1Rjr1Sp-Qr5rgOTBDo6jdTO7VPzZQTk/pub?gid=413650798&single=true&output=csv";

const LOGOS = {
    "Ziondrou": "https://i.imgur.com/8Km9tLL.png",
    "Fc Man": "https://i.imgur.com/8Km9tLL.png",
    "Kahi Fc": "https://i.imgur.com/8Km9tLL.png",
    "Guekpe": "https://i.imgur.com/8Km9tLL.png",
    "default": "https://i.imgur.com/8Km9tLL.png" // Mets ici le logo par défaut de ton tournoi
};

let ancienScore = {};
let chronoInterval = null;

async function fetchCSV(url) {
    const res = await fetch(url);
    const data = await res.text();
    const rows = data.split('\n').slice(1).filter(r => r.trim()!== '');
    return rows.map(r => r.split(','));
}

function getLogo(equipe) {
    return LOGOS[equipe] || LOGOS["default"];
}

// Version sécurisée pour éviter NaN
function calculerMinute(dateStr, heureStr) {
    try {
        const [jour, mois, annee] = dateStr.trim().split('/');
        const [heure, minute] = heureStr.trim().split(':');
        const debutMatch = new Date(annee, mois - 1, jour, heure, minute);
        
        if(isNaN(debutMatch)) return "00:00"; // si date invalide

        const maintenant = new Date();
        const diffMs = maintenant - debutMatch;
        const diffMinutes = Math.floor(diffMs / 1000 / 60);

        if(diffMinutes < 0) return "0'";
        if(diffMinutes >= 45 && diffMinutes < 46) return "MT";
        if(diffMinutes >= 90) return "90'";
        return `${diffMinutes}'`;
    } catch(e) {
        return "00:00"; // si erreur
    }
}

function lancerChronoAuto(date, heure) {
    clearInterval(chronoInterval);
    chronoInterval = setInterval(() => {
        const minute = calculerMinute(date, heure);
        const chronoEl = document.getElementById('chrono');
        if(chronoEl) chronoEl.innerText = minute;
        if(minute === "90'") clearInterval(chronoInterval);
    }, 1000);
}

async function chargerDonnees() {
    const [classementData, matchsData] = await Promise.all([
        fetchCSV(URL_CLASSEMENT),
        fetchCSV(URL_MATCHS)
    ]);

    const poules = {};
    classementData.forEach(r => {
        if(!poules[r[0]]) poules[r[0]] = [];
        poules[r[0]].push(r);
    });

    let classementHTML = '';
    for(const poule in poules) {
        classementHTML += `<h3 class="poule-title">POULE ${poule}</h3>`;
        classementHTML += `<table><thead><tr><th>Équipe</th><th>V</th><th>D</th><th>Pts</th></tr></thead><tbody>`;
        classementHTML += poules[poule].map(r =>
            `<tr><td><img src="${getLogo(r[1])}">${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td><td>${r[4]}</td></tr>`
        ).join('');
        classementHTML += `</tbody></table>`;
    }
    document.getElementById('classement-par-poule').innerHTML = classementHTML;

    const matchs = matchsData.map(r => ({
        e1: r[0], s1: r[1], e2: r[2], s2: r[3],
        date: r[4], heure: r[5], statut: r[6], poule: r[7]
    }));

    const live = matchs.find(m => m.statut && m.statut.trim() === "EN COURS");
    const aVenir = matchs.filter(m => m.statut && m.statut.trim() === "À VENIR");
    const termines = matchs.filter(m => m.statut && m.statut.trim() === "TERMINÉ");

    if(live) {
        const scoreKey = `${live.e1}-${live.e2}`;
        const nouveauScore = `${live.s1}-${live.s2}`;
        if(ancienScore[scoreKey] && ancienScore[scoreKey]!== nouveauScore) {
            document.getElementById('live-match').classList.add('but-animation');
            setTimeout(() => document.getElementById('live-match').classList.remove('but-animation'), 800);
        }
        ancienScore[scoreKey] = nouveauScore;
        lancerChronoAuto(live.date, live.heure);
    } else {
        clearInterval(chronoInterval);
    }

    document.getElementById('live-match').innerHTML = live
  ? `<div class="card live-card">
            <div><span id="chrono">${calculerMinute(live.date, live.heure)}</span></div>
            <div><img class="logo" src="${getLogo(live.e1)}"> ${live.e1} ${live.s1} - ${live.s2} ${live.e2} <img class="logo" src="${getLogo(live.e2)}"></div>
            <small>Poule ${live.poule}</small>
          </div>`
        : 'Aucun match en cours';

    document.getElementById('matchs-a-venir').innerHTML = aVenir.length > 0? aVenir.map(m =>
        `<div class="card"><img class="logo" src="${getLogo(m.e1)}">${m.e1} vs ${m.e2} <img class="logo" src="${getLogo(m.e2)}"> - ${m.date} ${m.heure}</div>`
    ).join('') : 'Aucun match à venir';

    document.getElementById('matchs-termines').innerHTML = termines.length > 0? termines.map(m =>
        `<div class="card"><img class="logo" src="${getLogo(m.e1)}">${m.e1} ${m.s1} - ${m.s2} ${m.e2} <img class="logo" src="${getLogo(m.e2)}"></div>`
    ).join('') : 'Aucun match terminé';
}

chargerDonnees();
setInterval(chargerDonnees, 10000);
