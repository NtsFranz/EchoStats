document.addEventListener('DOMContentLoaded', function () {
    // // 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
    // // The Firebase SDK is initialized and available here!
    //
    // firebase.auth().onAuthStateChanged(user => { });
    // firebase.database().ref('/path/to/ref').on('value', snapshot => { });
    // firebase.messaging().requestPermission().then(() => { });
    // firebase.storage().ref('/path/to/ref').getDownloadURL().then(() => { });
    //
    // // 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥

    //firebase.analytics();

    firebase.firestore().enablePersistence()
        .catch(function(err) {
            if (err.code == 'failed-precondition') {
                // Multiple tabs open, persistence can only be enabled
                // in one tab at a a time.
                // ...
            } else if (err.code == 'unimplemented') {
                // The current browser does not support all of the
                // features required to enable persistence
                // ...
            }
        });
    // Subsequent queries will use persistence, if it was enabled successfully

    var db = firebase.firestore();

    teamsDiv = document.getElementById('teams');
    teamDivTemplate = document.getElementsByClassName('team_box')[0];
    playerRow = document.getElementsByClassName('team_player_stats_row')[0];

    db.collection('series').doc('vrml_season_1').collection('teams').get().then((querySnapshot) => {
        var tempDoc = querySnapshot.docs.map((doc) => {
            var node = teamDivTemplate.cloneNode(true);
            node.classList.remove('hide');
            var d = doc.data();
            node.getElementsByClassName('team_name')[0].innerText = doc.id;

            // team stats
            node.getElementsByClassName('rank')[0].innerText = d.rank;
            node.getElementsByClassName('division')[0].innerText = d.division;
            node.getElementsByClassName('region')[0].innerText = d.region;
            node.getElementsByClassName('games')[0].innerText = d.games_played;
            node.getElementsByClassName('points')[0].innerText = d.points;
            //node.getElementsByClassName('possession_time_percentage')[0].innerText = d.rank;
            node.getElementsByClassName('wins')[0].innerText = d.wins;
            node.getElementsByClassName('losses')[0].innerText = d.losses;
            if (d.games_played > 0) {
                node.getElementsByClassName('wr')[0].innerText = Math.round(100.0 * d.wins / d.games_played) + "%";
            }
            node.getElementsByClassName('mmr')[0].innerText = d.mmr;
            node.getElementsByClassName('team_logo')[0].src = d.team_logo;

            // player stats
            d.roster.forEach(e => {
                var rowNode = playerRow.cloneNode(true);
                rowNode.classList.remove('hide');
                rowNode.getElementsByClassName('team_player_name')[0].innerText = e;

                db.collection('players').doc(e).get().then((doc) => {
                    if (doc.exists) {
                        img = document.createElement('img');
                        img.setAttribute('loading', "lazy");
                        img.src = doc.data().player_logo;
                        rowNode.getElementsByClassName('team_player_logo')[0].appendChild(img);
                    }
                });

                node.getElementsByClassName('stats_table')[1].appendChild(rowNode);
            });



            teamsDiv.appendChild(node);
        });
    });

});

function teamFilter() {
    input = document.getElementById('teamSearchBox');
    teamBoxes = document.getElementsByClassName('team_box');
    filter = input.value.toLowerCase();

    Array.from(teamBoxes).forEach(t => {
        if (filter.length == 0 || t.getElementsByClassName('team_name')[0].innerText.toLowerCase().indexOf(filter) > -1) {
            t.classList.remove('filtered_out');
        } else {
            t.classList.add('filtered_out');
        }
    });
}