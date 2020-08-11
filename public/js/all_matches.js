var matchRow;
var list;
var db;
var matches = [];

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
                console.log("failed precondition for persistence");
            } else if (err.code == 'unimplemented') {
                // The current browser does not support all of the
                // features required to enable persistence
                // ...
                console.log("browser doesn't support persistence");
            }
        });
    // Subsequent queries will use persistence, if it was enabled successfully

    db = firebase.firestore();

    // Initialize the FirebaseUI Widget using Firebase.
    var ui = new firebaseui.auth.AuthUI(firebase.auth());

    firebase.auth().signInAnonymously().catch(function (error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        // ...
        console.log("failed auth");
    });




    matchRow = document.getElementsByClassName('list-group-item')[0];
    list = document.getElementById('match_list');

    // get season names
    if (series_name == "") {
        series_name = "vrml_season_2";
    }

    // loop through matches
    db.collection('series').doc(series_name).collection('match_stats')
        .orderBy("match_time", "desc")
        .limit(30)
        .onSnapshot(querySnapshot => {
            if (!querySnapshot.empty) {
                matches.forEach(m => {
                    list.removeChild(m);
                })
                querySnapshot.docs.forEach(doc => {
                    addMatch(doc);
                });
            }
        });
});


// adds a row to the end of the table
function addMatch(doc) {
    var rowNode = matchRow.cloneNode(true);

    rowNode.classList.remove('hide');
    rowNode.getElementsByClassName('match_id')[0].innerText = doc.id;
    rowNode.getElementsByClassName('custom_id')[0].innerText = doc.data()['custom_id'];
    rowNode.getElementsByClassName('match_time')[0].innerText = doc.data()['match_time'];
    rowNode.getElementsByClassName('session_id')[0].innerText = doc.data()['session_id'];
    rowNode.getElementsByClassName('client_name')[0].innerText = doc.data()['client_name'];
    rowNode.getElementsByClassName('blue_team_score')[0].innerText = doc.data()['blue_team_score'];
    rowNode.getElementsByClassName('orange_team_score')[0].innerText = doc.data()['orange_team_score'];
    rowNode.getElementsByClassName('finish_reason')[0].innerText = doc.data()['finish_reason'];
    
    var dateStr = doc.data()['match_time'];
    dateStr = dateStr.replace(" ", "T");
    dateStr += "Z";
    rowNode.getElementsByClassName('match_time_elapsed')[0].innerText = timeSince(new Date(dateStr));
    
    list.appendChild(rowNode);
    matches.push(rowNode);

}
