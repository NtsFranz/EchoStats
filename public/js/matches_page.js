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


    firebase.auth().signInAnonymously().catch(function (error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        // ...
        console.log("failed auth");
    });

    var db = firebase.firestore()

    firebase.analytics();

    var seasonsDiv = document.getElementById('seasons');
    var seasonDivTemplate = document.getElementsByClassName('season_box')[0];
    var matchRow = document.getElementsByClassName('team_player_stats_row')[0];

    // get season names

    // loop through season names

    db.collection('series').doc('vrml_season_2').collection('matches').get().then((querySnapshot) => {
        querySnapshot.docs.map((doc) => {
            var rowNode = matchRow.cloneNode(true);
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