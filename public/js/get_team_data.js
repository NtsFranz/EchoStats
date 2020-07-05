var left_side;
var right_side;

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

    try {
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
    } catch (e) {
        console.log("Persistence already running");
    }

    firebase.auth().signInAnonymously().catch(function (error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        // ...
        console.log("failed auth");
    });

    var db = firebase.firestore()

    // var series_name = ""; // TODO set this from a dropdown or something
    // var client_name = ""; // TODO set this from a dropdown or something
    // var custom_id = ""; // TODO set this from a dropdown or something

    if (client_name == "") {
        console.log("No client_name");
        document.body.innerHTML = "<div style='color:black;'>Must specify a client_name. ex: <a href=\'/prematch_overlay?client_name=NtsFranz\'>prematch_overlay?client_name=NtsFranz</a></div>";
    } else {
        buildpregame(db);
    }
});

function buildpregame(db) {
    db.collection("caster_preferences").doc(client_name)
        .get()
        .then(doc => {
            if (doc.exists) {
                console.log(doc.data()['swap_sides']);
                if (doc.data()['swap_sides']) {
                    left_side = "away";
                    right_side = "home";
                } else {
                    left_side = "home";
                    right_side = "away"
                }

                // set logos
                setImage(left_side + "logo", doc.data()['home_logo']);
                setImage(right_side + "logo", doc.data()['away_logo']);

                // set team names
                write(left_side + "_team_name", doc.data()['home_team']);
                write(right_side + "_team_name", doc.data()['away_team']);

                // write "vs" title
                write("match_title", doc.data()['home_team'] + " vs " + doc.data()['away_team']);

                // get home team data via firestore...
                db.collection("series").doc("vrml_season_2").collection("teams").doc(doc.data()[left_side + '_team'])
                    .get()
                    .then(function (team) {
                        if (team.exists) {

                            // set division...
                            setImage("homerank", team.data()['division_logo']);

                            // set home mmr
                            write("homemmr", "MMR: " + team.data()['mmr'] + " (" + team.data()['wins'] + " - " + team.data()['losses'] + ")");

                            // add home roster...
                            entry = "";
                            Object.keys(team.data()['roster']).forEach(key => {
                                entry += "<tr><th>" + team.data()['roster'][key] + "</th></tr>";
                            });
                            write("homeroster", entry);

                        } else {
                            setImage("homerank", "");
                            write("homemmr", " ");
                            write("homeroster", " ");
                        }
                    });

                // get away team data via firestore...
                db.collection("series").doc("vrml_season_2").collection("teams").doc(doc.data()[right_side + '_team'])
                    .get()
                    .then(function (team) {
                        if (team.exists) {

                            // set division...
                            setImage("awayrank", team.data()['division_logo']);

                            // set home mmr
                            write("awaymmr", "MMR: " + team.data()['mmr'] + " (" + team.data()['wins'] + " - " + team.data()['losses'] + ")");

                            // add home roster...
                            entry = "";
                            Object.keys(team.data()['roster']).forEach(key => {
                                entry += "<tr><th>" + team.data()['roster'][key] + "</th></tr>";
                            });
                            write("awayroster", entry);

                        } else {
                            setImage("awayrank", "");
                            write("awaymmr", " ");
                            write("awayroster", " ");
                        }


                        document.getElementById("background_container").style.opacity = 1;
                    });
            }
        });
}

function write(id, data) {
    var element = document.getElementById(id);
    if (element) {
        element.innerHTML = data;
        element.style.visibility = 'visible';
    }
}

function setImage(id, src_) {
    var element = document.getElementById(id);
    if (element) {
        element.src = src_;
        element.style.visibility = 'visible';
    }
}