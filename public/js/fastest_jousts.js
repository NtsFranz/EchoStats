var matchRow;
var list;
var db;
var matches = [];


function Start(db) {

    matchRow = document.getElementsByClassName('list-group-item')[0];
    list = document.getElementById('match_list');

    // loop through matches
    // db.collection('series').doc(series_name).collection('match_stats').collectionGroup('events')
    db.collectionGroup('events')
        .where("event_type", "==", "joust_speed")
        .orderBy("other_player_id", "asc")
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
}


// adds a row to the end of the table
function addMatchFastestJousts(doc) {
    var rowNode = matchRow.cloneNode(true);

    rowNode.classList.remove('hide');
    rowNode.getElementsByClassName('match_id')[0].innerText = doc.id;
    rowNode.getElementsByClassName('custom_id')[0].innerText = doc.data()['custom_id'];
    rowNode.getElementsByClassName('match_time')[0].innerText = doc.data()['match_time'];
    rowNode.getElementsByClassName('session_id')[0].innerText = doc.data()['session_id'];
    rowNode.getElementsByClassName('player_name')[0].innerText = doc.data()['player_name'];
    rowNode.getElementsByClassName('joust_time')[0].innerText = round(doc.data()['other_player_id'] / 1000.0, 4) + " s";
    rowNode.getElementsByClassName('joust_speed')[0].innerText = round(doc.data()['x2'], 4) + " m/s";
    rowNode.getElementsByClassName('tube_exit_speed')[0].innerText = round(doc.data()['y2'], 4) + " m/s";

    var dateStr = doc.data()['match_time'];
    dateStr = dateStr.replace(" ", "T");
    dateStr += "Z";
    rowNode.getElementsByClassName('match_time_elapsed')[0].innerText = timeSince(new Date(dateStr));

    list.appendChild(rowNode);
    matches.push(rowNode);

}
