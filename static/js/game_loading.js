//                  DEFINING SOME GLOBAL VARIABLES AND STARTING THE FUNCTION
var xValues = [];
var yValues = [];
var countryNames = [];
document.addEventListener("DOMContentLoaded", async function() {
    response = await fetch("/api/get_game_points", { method: "POST" });
    data = await response.json();

    //                   GETTING COORDINATES AND COUNTRY NAMES

    var dataPoints = data.map_points.trim().split("/");
    dataPoints.forEach(dataPoint => {
        var [xy, country] = dataPoint.split("-");
        var [x, y] = xy.split("%");
        xValues.push(parseFloat(x));
        yValues.push(parseFloat(y));
        countryNames.push(country);
    });
    xValues.pop()
    yValues.pop()
    countryNames.pop()

    //                                        LOADING THE RED DOTS

    for (let i = 0; i < xValues.length; i++) {
        var redDot = document.createElement('div');
          redDot.className = 'red-dot';
          redDot.style.left = xValues[i]+"%";
          redDot.style.top = yValues[i]+"%";
          zoomTarget.parentElement.appendChild(redDot);
    }

});
//                               MAIN CODE
async function start_game(){
    var startgamebutton = document.getElementById('start_button');
    startgamebutton.remove();
    startTimer();
    index_arr = [...Array(xValues.length).keys()];
    setTimeout(1000);
    index_arr = shuffleArray(index_arr);
    setTimeout(1000);
    var wrongarr = [];
    var rightarr = [];
    for (let i = 0; i < index_arr.length; i=i) {
        index = index_arr.pop();
        document.getElementById("place_name").innerHTML = countryNames[index];
        var {x,y} =await get_click();
        if (x<xValues[index]+5 && x>xValues[index]-5 )
        {
            if (y<yValues[index]+5 && y>yValues[index]-5 )
            {
                var dotindex = -1;
                for (var j = 0; j < countryNames.length; j++) {
                    if (countryNames[j] === countryNames[index] && xValues[j] === xValues[index] && yValues[j] === yValues[index]) {
                    dotindex = j;
                    break;
                    }
                }
                var redDotElement = document.querySelectorAll('.red-dot')[dotindex];
                redDotElement.style.backgroundColor = "blue";
                rightarr.push(countryNames[index])
            }
            else
            {
                var dotindex = -1;
                for (var j = 0; j < countryNames.length; j++) {
                    if (countryNames[j] === countryNames[index] && xValues[j] === xValues[index] && yValues[j] === yValues[index]) {
                    dotindex = j;
                    break;
                    }
                }
                var redDotElement = document.querySelectorAll('.red-dot')[dotindex];
                redDotElement.style.backgroundColor = "red";
                wrongarr.push(countryNames[index])
            }
        }
        else
        {

            var dotindex = -1;
            for (var j = 0; j < countryNames.length; j++) {
                if (countryNames[j] === countryNames[index] && xValues[j] === xValues[index] && yValues[j] === yValues[index]) {
                dotindex = j;
                break;
                }
            }
                var redDotElement = document.querySelectorAll('.red-dot')[dotindex];
                redDotElement.style.backgroundColor = "red";
            wrongarr.push(countryNames[index])
        }
    }
    stopTimer()
    document.getElementById("first_msg").innerHTML = "Results:";
    document.getElementById("success_list").innerHTML = "You were right in: "+rightarr;
    document.getElementById("failed_list").innerHTML = "You were wrong in: "+wrongarr;
    document.getElementById('place_name').remove();
}

//                                   TIMER FUNCTION SECTION

    let timerInterval;
    let hours = 0, minutes = 0, seconds = 0;

    function startTimer() {
        timerInterval = setInterval(updateTimer, 1000);

    }

    function stopTimer() {
        clearInterval(timerInterval);
    }

    function updateTimer() {
        seconds++;
        if (seconds >= 60) {
            seconds = 0;
            minutes++;
            if (minutes >= 60) {
                minutes = 0;
                hours++;
            }
        }

        const formattedTime = padNumber(hours) + ":" + padNumber(minutes) + ":" + padNumber(seconds);
        document.getElementById("timer").innerText = formattedTime;
    }

    function padNumber(num) {
        return num.toString().padStart(2, '0');
    }

//                        GETTING A RANDOM LIST OF NUMBERS TO CHOOSE POINT ORDER

function create_array()
{
    let i = 0;
    let arr = [];
    while (i<xValues.length)
    {
        arr.push(i)
        i = i+1;
    }
    return arr
}


function shuffleArray(arraya) {
    array = arraya
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}
//                                    GETS CLICK COORDINATES
function get_click() {
    return new Promise((resolve) => {
        var zoomTarget = document.getElementById('zoomTarget');
        function clickHandler(e) {
            zoomTarget.removeEventListener('click', clickHandler);
            const { left, top, width, height } = zoomTarget.getBoundingClientRect();
            const x = 100 * (e.clientX - left) / width;
            const y = 100 * (e.clientY - top) / height;
            resolve({ x, y });
        }
        zoomTarget.addEventListener('click', clickHandler);
    });
}