const URL_CLASSEMENT = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQULxJOCxlp-vjeYfhXexfaKTBHl-aLBiq37_ROaPxB008hH1Rjr1Sp-Qr5rgOTBDo6jdTO7VPzZQTk/pub?gid=0&single=true&output=csv";
const URL_MATCHS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQULxJOCxlp-vjeYfhXexfaKTBHl-aLBiq37_ROaPxB008hH1Rjr1Sp-Qr5rgOTBDo6jdTO7VPzZQTk/pub?gid=413650798&single=true&output=csv";

const LOGOS = {
    "Ziondrou": "https://i.imgur.com/8Km9tLL.png",
    "Fc Man": "https://i.imgur.com/8Km9tLL.png",
    "Kahi Fc": "https://i.imgur.com/8Km9tLL.png",
    "Guekpe": "https://i.imgur.com/8Km9tLL.png",
    "Bangolo": "https://i.imgur.com/8Km9tLL.png",
    "Man": "https://i.imgur.com/8Km9tLL.png",
    "default": "https://i.imgur.com/8Km9tLL.png"
};

let ancienScore = {};
let chronoInterval = null;

async function fetchCSV(url) {
    const res = await fetch(url);
    const data = await res.text();
    return data.split('\n').slice(1).filter(r => r.trim()!== '').map(r => r.split(','));
}

function getLogo(equipe) {
    return LOGOS[equipe.trim()] || LOGOS["default"];
}

function calculerMinute(dateStr, heureStr) {
    try {
        let [jour, mois, annee] = dateStr.trim().split('/');
        let [heure, minute] = heureStr.trim().split(':');
        const debutMatch = new Date(Number(annee), Number(mois) - 1, Number(jour), Number(heure), Number(minute));
        if(isNaN(debutMatch.getTime())) return "LIVE";

        const diffMs = new Date() - debutMatch;
        const diffMinutes = Math.floor(diffMs / 1000 / 60);

        if(diffMinutes < 0) return "0'";
        if(diffMinutes >= 45 && diffMinutes <= 47) return "MT";
        if(diffMinutes >= 90) return "90'";
        return `${diffMinutes}'`;
    } catch(e) { return "LIVE"; }
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
    const [classementData, matchsData] = await Promise.all([fetchCSV(URL_CLASSEMENT), fetchCSV(URL_MATCHS)]);

    const poules = {};
    classementData.forEach(r => { if(r[0]){ if(!poules[r[0]]) poules[r[0]] = []; poules[r[0]].push(r); }});

    let classementHTML = '';
    for(const poule in poules) {
        classementHTML += `<h3 class="poule-title">POULE ${poule}</h3><table><thead><tr><th>Équipe</th><th>V</th><th>D</th><th>Pts</th></tr></thead><tbody>`;
        classementHTML += poules[poule].map(r => `<tr><td><img src="${getLogo(r[1])}">${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td><td>${r[4]}</td></tr>`).join('');
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
    } else { clearInterval(chronoInterval); }

    // AFFICHAGE EN DIRECT
    document.getElementById('live-match').innerHTML = live
 ? `<div class="match-card live-card">
            <span id="chrono">${calculerMinute(live.date, live.heure)}</span>
            <div class="live-score">
                <div class="equipe"><img class="logo" src="${getLogo(live.e1)}"> ${live.e1}</div>
                <div class="score">${live.s1} - ${live.s2}</div>
                <div class="equipe equipe-droite">${live.e2} <img class="logo" src="${getLogo(live.e2)}"></div>
            </div>
            <small>Poule ${live.poule}</small>
          </div>`
        : 'Aucun match en cours';

    // AFFICHAGE À VENIR - NOUVEAU FORMAT
    document.getElementById('matchs-a-venir').innerHTML = aVenir.length > 0? aVenir.map(m =>
        `<div class="match-card">
            <div class="equipe"><img class="logo" src="${getLogo(m.e1)}"> ${m.e1}</div>
            <div class="vs">VS</div>
            <div class="equipe equipe-droite">${m.e2} <img class="logo" src="${getLogo(m.e2)}"></div>
            <div class="date-heure"><div class="date">${m.date}</div><div class="heure">${m.heure}</div></div>
        </div>`
    ).join('') : 'Aucun match à venir';

    // AFFICHAGE TERMINÉS - NOUVEAU FORMAT
    document.getElementById('matchs-termines').innerHTML = termines.length > 0? termines.map(m =>
        `<div class="match-card">
            <div class="equipe"><img class="logo" src="${getLogo(m.e1)}"> ${m.e1}</div>
            <div class="score">${m.s1} - ${m.s2}</div>
            <div class="equipe equipe-droite">${m.e2} <img class="logo" src="${getLogo(m.e2)}"></div>
        </div>`
    ).join('') : 'Aucun match terminé';
}

chargerDonnees();
setInterval(chargerDonnees, 10000);
