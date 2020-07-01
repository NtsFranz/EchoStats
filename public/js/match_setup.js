var matchRow;
var matchRowAddSplitter;
var sortableList;
var db;

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
    matchRowSplitter = document.getElementsByClassName('match_group_splitter')[0];
    sortableList = document.getElementById('match_list');

    get_upcoming_matches();

});

// get upcoming matches
function get_upcoming_matches() {
    var url = "/get_upcoming_matches"
    httpGetAsync(url, showUpcomingMatches);
}

function showUpcomingMatches(data) {
    data = JSON.parse(data);
    console.log(data);
    data.forEach(match => {
        addMatch(match);
    });
}

function httpGetAsync(theUrl, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}

// adds a row to the end of the table
function addMatch(data) {
    var rowNode = matchRow.cloneNode(true);
    rowNode.classList.remove('hide');

    // rowNode.getElementsByClassName('match_id')[0].innerText = doc.id;
    rowNode.getElementsByClassName('match_time')[0].innerText = data['DateScheduled'];
    rowNode.getElementsByClassName('home_team_logo')[0].getElementsByTagName("img")[0].src = data['HomeTeamLogo'];
    rowNode.getElementsByClassName('home_team_name')[0].innerText = data['HomeTeam'];
    rowNode.getElementsByClassName('away_team_name')[0].innerText = data['AwayTeam'];
    rowNode.getElementsByClassName('away_team_logo')[0].getElementsByTagName("img")[0].src = data['AwayTeamLogo'];
    rowNode.getElementsByClassName('casters')[0].innerText = data['CasterName'];
    
    if (client_name != "") {
        var createClickHandler = function(row) {
            return function() {
                console.log("clicked: " + data['HomeTeam'] + " vs " + data['AwayTeam']);
                db.collection("caster_preferences").doc(client_name).update({
                    home_team: data['HomeTeam'],
                    home_logo: data['HomeTeamLogo'],
                    away_logo: data['AwayTeamLogo'],
                    away_team: data['AwayTeam']
                })
                .catch(function(error) {
                    // The document probably doesn't exist.
                    console.error("Error updating document: ", error);
                });
            };
        };

        rowNode.onclick = createClickHandler(rowNode);
    }
    sortableList.appendChild(rowNode);
}