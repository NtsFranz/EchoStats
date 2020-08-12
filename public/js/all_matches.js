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
                    addMatchOverview(doc, matchRow, list, matches);
                });
            }
        });
});



