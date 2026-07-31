const URL_CLASSEMENT = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQULxJOCxlp-vjeYfhXexfaKTBHl-aLBiq37_ROaPxB008hH1Rjr1Sp-Qr5rgOTBDo6jdTO7VPzZQTk/pub?gid=0&single=true&output=csv";
const URL_MATCHS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQULxJOCxlp-vjeYfhXexfaKTBHl-aLBiq37_ROaPxB008hH1Rjr1Sp-Qr5rgOTBDo6jdTO7VPzZQTk/pub?gid=413650798&single=true&output=csv";

const LOGOS = {
    "E1": "https://i.imgur.com/8Km9tLL.png",
    "E2": "https://i.imgur.com/8Km9tLL.png",
    "default": "https://i.imgur.com/8Km9tLL.png"
};

let ancienScore = {};
let chronoInterval = null;

async function fetchCSV(url) {
    const res = await fetch(url);
    const data = await res.text();
    return data.split('\n').slice(1).filter(r => r.trim()!== '').map(r => r.split(','));
}

function getLogo(equipe) { return LOGOS[equipe.trim()] || LOGOS["default"]; }

function calculerMinute(dateStr, heureStr) {
    try {
        let [jour, mois, annee] = dateStr.trim().split('/');
        let [heure, minute] = heureStr.trim().split(':');
        const debutMatch = new Date(Number(annee), Number(mois) - 1, Number(jour), Number(heure), Number(minute));
        if(isNaN(debutMatch.getTime())) return "LIVE";
        const diffMinutes = Math.floor((new Date() - debutMatch) / 1000 / 60);
        if(diffMinutes < 0) return "0'";
        if(diffMinutes >= 45 && diffMinutes <= 47) return "MT";
        if(diffMinutes >= 90) return "90'";
        return `${diffMinutes}'`;
    } catch(e) { return "LIVE"; }
}

function lancerChrono(date, heure) {
    clearInterval(chronoInterval);
    chronoInterval = setInterval(() => {
        const minute = calculerMinute(date, heure);
        const el = document.getElementById('live-time');
        if(el) el.innerText = minute;
        if(minute === "90'") clearInterval(chronoInterval);
    }, 1000);
}

async function chargerDonnees() {
    const [classementData, matchsData] = await Promise.all([fetchCSV(URL_CLASSEMENT), fetchCSV(URL_MATCHS)]);

    const poules = {};
    classementData.forEach(r => { if(r[0]){ if(!poules[r[0]]) poules[r[0]] = []; poules[r[0]].push(r); }});

    let classementHTML = '';
    for(const poule in poules) {
        classementHTML += `<div class="poule-title">POULE ${poule}</div><table><thead><tr><th>Équipe</th><th>V</th><th>D</th><th>Pts</th></tr></thead><tbody>`;
        classementHTML += poules[poule].map(r => `<tr><td style="text-align:left"><img src="${getLogo(r[1])}">${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td><td>${r[4]}</td></tr>`).join('');
        classementHTML += `</tbody></table>`;
    }
    document.getElementById('classement-par-poule').innerHTML = classementHTML;

    const matchs = matchsData.map(r => ({ e1: r[0], s1: r[1], e2: r[2], s2: r[3], date: r[4], heure: r[5], statut: r[6], poule: r[7] }));

    const live = matchs.find(m => m.statut && m.statut.trim() === "EN COURS");
    const aVenir = matchs.filter(m => m.statut && m.statut.trim() === "À VENIR");
    const termines = matchs.filter(m => m.statut && m.statut.trim() === "TERMINÉ");

    if(live) {
        lancerChrono(live.date, live.heure);
    } else { clearInterval(chronoInterval); }

    // EN DIRECT
    document.getElementById('live-match').innerHTML = live
? `<div class="match live">
            <div class="match-top">
                <div class="team"><img class="logo" src="${getLogo(live.e1)}"> ${live.e1}</div>
                <div><div id="live-time" class="live-time">${calculerMinute(live.date, live.heure)}</div><div class="score">${live.s1} - ${live.s2}</div></div>
                <div class="team team-right">${live.e2} <img class="logo" src="${getLogo(live.e2)}"></div>
            </div>
          </div>`
        : '<div class="match">Aucun match en cours</div>';

    // À VENIR - NOUVEAU FORMAT AVEC FOOTER
    document.getElementById('matchs-a-venir').innerHTML = aVenir.length > 0? aVenir.map(m =>
        `<div class="match">
            <div class="match-top">
                <div class="team"><img class="logo" src="${getLogo(m.e1)}"> ${m.e1}</div>
                <div class="vs">vs</div>
                <div class="team team-right">${m.e2} <img class="logo" src="${getLogo(m.e2)}"></div>
            </div>
            <div class="match-bottom">
                <span class="poule">Poule ${m.poule}</span>
                <span>${m.date} - ${m.heure}</span>
            </div>
        </div>`
    ).join('') : '<div class="match">Aucun match à venir</div>';

    // TERMINÉS
    document.getElementById('matchs-termines').innerHTML = termines.length > 0? termines.map(m =>
        `<div class="match">
            <div class="match-top">
                <div class="team"><img class="logo" src="${getLogo(m.e1)}"> ${m.e1}</div>
                <div class="score">${m.s1} - ${m.s2}</div>
                <div class="team team-right">${m.e2} <img class="logo" src="${getLogo(m.e2)}"></div>
            </div>
          </div>`
    ).join('') : '<div class="match">Aucun match terminé</div>';
}

chargerDonnees();
setInterval(chargerDonnees, 10000);
