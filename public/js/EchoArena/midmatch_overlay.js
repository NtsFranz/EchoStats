var completedEvents = {};
var freshPage = !show_on_load;

function Start(db) {
    getTeamNameLogo(db);
    setupEventsOverlay(db);
    getCasters(game = "echoarena")
}
