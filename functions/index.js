const functions = require('firebase-functions');
const express = require('express');
const https = require('https');

// firestore
const admin = require('firebase-admin');
admin.initializeApp();
let db = admin.firestore();

const engines = require('consolidate');

const app = express();
app.engine('hbs', engines.handlebars);
app.set('views', './views');
app.set('view engine', 'hbs');

app.get('/', (req, res) => {
    res.render('index');
});





//////////////// ECHO ARENA //////////////////

app.get('/prematch_overlay', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("EchoArena/prematch_rosters", {
        client_name,
        custom_id,
        series_name,
        live
    });
});

app.get('/prematch_overlay_old', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("EchoArena/prematch_overlay_old", {
        client_name,
        custom_id,
        series_name,
        live
    });
});

app.get('/midmatch_overlay', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const live = req.query.live || false;
    const show_on_load = req.query.show_on_load || false;

    res.render("EchoArena/midmatch_overlay", {
        client_name,
        custom_id,
        series_name,
        live,
        show_on_load
    });
});

app.get('/prematch_overlay_2', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("EchoArena/prematch_overlay_2", {
        client_name,
        custom_id,
        series_name,
        live
    });
});

app.get('/most_recent_match', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("EchoArena/most_recent_match", {
        client_name,
        custom_id,
        series_name,
        live
    });
});

app.get('/group_recent_matches', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;

    res.render("EchoArena/group_recent_matches", {
        client_name,
        custom_id,
        series_name
    });
});

app.get('/all_recent_matches', (req, res) => {
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("EchoArena/all_recent_matches", {
        series_name,
        live
    });
});

app.get('/fastest_jousts', (req, res) => {
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("EchoArena/fastest_jousts", {
        series_name,
        live
    });
});

app.get('/casterdesk', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;
    const live = req.query.live || true;   // live by default

    res.render("EchoArena/casterdesk", {
        client_name,
        series_name,
        live
    });
});

app.get('/match_setup', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;

    res.render("EchoArena/match_setup", {
        client_name,
        custom_id,
        series_name
    });
});

app.get('/get_upcoming_matches', (req, res) => {
    https.get("https://vrmasterleague.com/Services.asmx/GetMatchesThisWeek?game=echoarena&max=100", (resp) => {
        let data = '';

        // A chunk of data has been recieved.
        resp.on('data', (chunk) => {
            data += chunk;
        });

        // The whole response has been received. Print out the result.
        resp.on('end', () => {
            res.send(JSON.parse(data));
        });

    }).on("error", (err) => {
        console.log("Error: " + err.message);
        res.send(err.message);
    });
});

app.get('/scoreboard', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("EchoArena/scoreboard", {
        client_name,
        series_name,
        live
    });
});







//////////////// Onward //////////////////

app.get('/onward/scoreboard', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const live = req.query.live || false;
    const show_on_load = req.query.show_on_load || false;

    res.render("Onward/scoreboard_onward", {
        client_name,
        custom_id,
        series_name,
        live,
        show_on_load
    });
});

app.get('/onward/preshow', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;
    const live = req.query.live || false;
    const show_on_load = req.query.show_on_load || false;

    res.render("Onward/preshow_onward", {
        client_name,
        custom_id,
        series_name,
        live,
        show_on_load
    });
});


app.get('/onward/match_setup', (req, res) => {
    const client_name = req.query.client_name;
    const custom_id = req.query.custom_id;
    const series_name = req.query.series_name;

    res.render("Onward/match_setup_onward", {
        client_name,
        custom_id,
        series_name
    });
});

app.get('/onward/casterdesk', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;

    res.render("Onward/casterdesk", {
        client_name,
        series_name
    });
});

app.get('/onward/caster_1', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;

    res.render("Onward/caster_1", {
        client_name
    });
});

app.get('/onward/caster_2', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;

    res.render("Onward/caster_2", {
        client_name
    });
});

app.get('/onward/caster_3', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;

    res.render("Onward/caster_3", {
        client_name
    });
});

app.get('/onward/analyst', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;

    res.render("Onward/analyst", {
        client_name
    });
});

app.get('/onward/home_team_logo', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;

    res.render("Onward/home_team_logo", {
        client_name
    });
});

app.get('/onward/away_team_logo', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;

    res.render("Onward/away_team_logo", {
        client_name
    });
});

app.get('/onward/home_team_name', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;

    res.render("Onward/home_team_name", {
        client_name
    });
});

app.get('/onward/away_team_name', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;

    res.render("Onward/away_team_name", {
        client_name
    });
});




//////////////// CVRE //////////////////

app.get('/match_awards', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;

    res.render("CVRE/match_awards", {
        client_name,
        series_name
    });
});

app.get('/cvre_stats_blue', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("CVRE/cvre_stats_blue", {
        client_name,
        series_name,
        live
    });
});

app.get('/cvre_stats_orange', (req, res) => {
    const client_name = req.query.client_name;
    const series_name = req.query.series_name;
    const live = req.query.live || false;

    res.render("CVRE/cvre_stats_orange", {
        client_name,
        series_name,
        live
    });
});











exports.app = functions.https.onRequest(app);