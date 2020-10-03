var matchRow;
var list;
var db;
var matches = [];

function Start(db) {

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
}



