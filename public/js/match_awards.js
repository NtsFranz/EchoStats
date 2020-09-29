function Start(db) {
    getCurrentMatchStats(db, long = true, live = false, onlyaftercasterprefs = false, processMatchStats);
}

function processMatchStats(data) {
    console.log(data);

    // most possession time
    var max = {
        "name": "",
        "color": "",
        "val": 0
    };
    Object.keys(data.player_stats).forEach(player => {
        if (data.player_stats[player].possession_time > max.val) {
            max.val = data.player_stats[player].possession_time;
            max.name = player;
            max.color = data.player_stats[player].team_color;
        }
    });
    addAward("Most Possession Time", max.name, round(max.val, 2) + " s", max.color);

    // highest avg speed
    var max = {
        "name": "",
        "color": "",
        "val": 0
    };
    Object.keys(data.player_stats).forEach(player => {
        if (data.player_stats[player].average_speed > max.val) {
            max.val = data.player_stats[player].average_speed;
            max.name = player;
            max.color = data.player_stats[player].team_color;
        }
    });
    addAward("Highest Average Speed", max.name, round(max.val, 2) + " m/s", max.color);

    // fastest hands
    var max = {
        "name": "",
        "color": "",
        "val": 0
    };
    Object.keys(data.player_stats).forEach(player => {
        var val = (data.player_stats[player].average_speed_lhand + data.player_stats[player].average_speed_rhand) / 2;
        if (val > max.val) {
            max.val = val;
            max.name = player;
            max.color = data.player_stats[player].team_color;
        }
    });
    addAward("Fastest Average Hand Speed", max.name, round(max.val, 2) + " m/s", max.color);

    // avg ping
}

function addAward(title, player_name, value, color) {
    // parent object for new awards
    var awards_parent = document.getElementById("match_awards");

    var div = document.createElement("div");
    div.classList.add("match_award");
    div.classList.add(color);
    var title_elem = document.createElement("p");
    title_elem.classList.add("title");
    var player_name_elem = document.createElement("p");
    player_name_elem.classList.add("player_name");
    var value_elem = document.createElement("p");
    value_elem.classList.add("value");

    title_elem.innerText = title;
    player_name_elem.innerText = player_name;
    value_elem.innerText = value;

    div.appendChild(player_name_elem);
    div.appendChild(title_elem);
    div.appendChild(value_elem);

    awards_parent.appendChild(div);
}
