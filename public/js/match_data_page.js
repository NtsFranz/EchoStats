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



    firebase.firestore().enablePersistence()
        .catch(function (err) {
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

    var db = firebase.firestore()

    db.collection('series').doc('vrml_season_1').collection('match_stats')
        .orderBy("match_time", "desc")
        .limit(1)
        .get()
        .then(querySnapshot => {
            if (!querySnapshot.empty) {
                //We know there is one doc in the querySnapshot
                const lastMatchDoc = querySnapshot.docs[0];

                console.log(lastMatchDoc.data());

                // get all players
                lastMatchDoc.ref.collection('players')
                    .onSnapshot(playersQuery => {
                        if (!playersQuery.empty) {

                            bluePlayersTable = "";
                            orangePlayersTable = "";

                            // loop through all players
                            playersQuery.docs.map(player => {

                                p = player.data();
                                console.log(p);

                                table = "";
                                table +=
                                    "<tr><td>" + p.player_name +
                                    "</td><td>" + p.points +
                                    "</td><td>" + p.assists +
                                    "</td><td>" + p.saves +
                                    "</td><td>" + p.steals +
                                    "</td><td>" + p.stuns +
                                    "</td></tr>";

                                if (p.team_color == "blue") {
                                    bluePlayersTable += table;

                                } else if (p.team_color == "orange") {
                                    orangePlayersTable += table;

                                }
                            });

                            write("blueplayerhead", "<tr><td>PLAYER</td><td>POINTS</td><td>ASSISTS</td><td>SAVES</td><td>STEALS</td><td>STUNS</td></tr>");
                            write("blueplayerstable", bluePlayersTable);


                            write("orangeplayerhead", "<tr><td>PLAYER</td><td>POINTS</td><td>ASSISTS</td><td>SAVES</td><td>STEALS</td><td>STUNS</td></tr>");
                            write("orangeplayerstable", orangePlayersTable);

                        }
                    });
            }
        });
});

function write(id, data) {
    var element = document.getElementById(id);
    element.innerHTML = data;
    element.style.visibility = 'visible';
}