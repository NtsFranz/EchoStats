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

    var db = firebase.firestore();

    if (client_name == "") {
        console.log("No client_name");
        document.body.innerHTML = "<div style='color:black;'>Must specify a client_name. ex: <a href=\'/live_events_overlay?client_name=NtsFranz\'>prematch_overlay?client_name=NtsFranz</a></div>";
    } else {
        setupEventsOverlay(db);
    }
});

var completedEvents = {};
var freshPage = true;

function setupEventsOverlay(db) {
    db.collection('series').doc(series_name).collection('match_stats')
        .orderBy("match_time", "desc")
        .where("client_name", "==", client_name)
        .limit(1)
        .onSnapshot(querySnapshot => {
            if (!querySnapshot.empty) {
                querySnapshot.docs[0].ref.collection('events')
                    .where("event_type", "==", "joust_speed")
                    .onSnapshot(eventsSnapshot => {
                        if (!eventsSnapshot.empty) {
                            // loop through all the events for this match
                            eventsSnapshot.docs.forEach(e => {
                                // if we haven't already used this event
                                if (!completedEvents.hasOwnProperty(e.id)) {
                                    completedEvents[e.id] = "";
                                    if (!freshPage) {
                                        var d = e.data();
                                        console.log("Joust time: " + (d['other_player_id'] / 1000.0) + " s, Final speed: " + magnitude(d['x2'], d['y2'], d['z2']) + " m/s")
                                        if (d['other_player_id'] < 10000) {
                                            var color = d['other_player_name'];
                                            write('joust_time_' + color, round(d['other_player_id'] / 1000.0, 2) + " s");
                                            write('joust_speed_' + color, round(magnitude(d['x2'], d['y2'], d['z2']), 1) + " m/s");

                                            var joustStatsElem = document.getElementById('joust_stats_' + color);
                                            joustStatsElem.classList.add('visible');
                                            var clonedNode = joustStatsElem.cloneNode(true);
                                            joustStatsElem.parentNode.replaceChild(clonedNode, joustStatsElem);
                                        }
                                    }
                                }
                            });
                            freshPage = false;
                        }
                    });
            }
        });
}

function round(number, decimalPlaces) {
    number *= decimalPlaces * 10;
    number = Math.round(number);
    number /= decimalPlaces * 10;
    return number;
}

function magnitude(x, y, z) {
    return Math.sqrt(x * x + y * y + z * z);
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