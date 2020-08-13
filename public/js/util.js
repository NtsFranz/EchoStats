
function round(number, decimalPlaces) {
    number *= decimalPlaces * 10;
    number = Math.round(number);
    number /= decimalPlaces * 10;
    return number;
}

function magnitude(x, y, z) {
    return Math.sqrt(x * x + y * y + z * z);
}

function timeSince(date) {

    var seconds = Math.floor((new Date() - date) / 1000);

    var interval = seconds / 31536000;

    if (interval > 1) {
        return Math.floor(interval) + " years";
    }
    interval = seconds / 2592000;
    if (interval > 1) {
        return Math.floor(interval) + " months";
    }
    interval = seconds / 86400;
    if (interval > 1) {
        return Math.floor(interval) + " days";
    }
    interval = seconds / 3600;
    if (interval > 1) {
        return round(interval, 1) + " hours";
    }
    interval = seconds / 60;
    if (interval > 1) {
        return Math.floor(interval) + " minutes";
    }
    return Math.floor(seconds) + " seconds";
}

function write(className, data) {
    var elements = document.getElementsByClassName(className);
    Array.from(elements).forEach(e => {
        e.innerHTML = data;
        e.style.opacity = "1";
    });
}

function setImage(className, src_) {
    var elements = document.getElementsByClassName(className);
    Array.from(elements).forEach(e => {
        e.src = src_;
        e.style.opacity = "1";
    });
}

function sumOfStats(playerData) {
    return playerData.points +
        playerData.assists +
        playerData.saves +
        playerData.steals +
        playerData.stuns +
        playerData.play_time;
}

// returns a pretty percentation of param1 to param2
function teamCentage(team, total) {
    var a = Math.round(team / total * 100)
    if (a > 0) {
        return a;
    } else {
        return '0';
    }
}

// adds numeric values from ob2 to ob1
function mergeSum(ob1, ob2) {
    var sum = {}
    Object.keys(ob1).forEach(key => {
        if (ob2.hasOwnProperty(key)) {
            if ((typeof ob2[key]) == "number") {
                sum[key] = ob1[key] + ob2[key]
            } else {
                sum[key] = ob1[key];
            }
        }
    })
    return sum;
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

function toMinutesString(seconds) {
    var mins = seconds / 60;
    var secs = Math.round(seconds % 60);
    if (secs < 10) {
        secs = "0" + secs;
    }

    return Math.floor(mins) + ":" + secs;
}