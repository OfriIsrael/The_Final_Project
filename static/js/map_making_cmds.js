// function purpose: adds a point to the global 'map_points' variable and
// does a couple of check to see the input is correct
function SetPointName() {
    var inputElement = document.getElementById('point_name');
    var inputValue = inputElement.value;
    if (map_points.slice(-1) !="/" && map_points != "")
  {
    map_points = map_points+inputValue+"/";
      inputElement.value =""
  }
  else
  {
    document.getElementById("msg").innerHTML = " Please Press On A Place's name";
  }
}
//function deletes most recent click
function DelPoint()
{
    if (map_points.length !=0)
    {
        if (map_points.slice(-1) =="/")
        {
            var i = map_points.length-2;
        }
        if (map_points.slice(-1)== "-")
        {
            var i = map_points.length-1;
        }
        while (map_points[i]!= "/")
            i= i-1;
        map_points = map_points.substring(0,i+1);
        console.log(map_points)
        var zoomTarget = document.getElementById('zoomTarget');
        zoomTarget.removeChild(zoomTarget.lastChild);
    }

}


// function purpose: gets the information once the user finishes making
// the map and sends it to the server as a json request
function SendToDatabase()
{
    var inputElement = document.getElementById('map_name');
    // Get the value of the input element
    var map_name = inputElement.value;
    var image = document.getElementById('img1');
    var imageSource = image.src;
    const data = {
                MAP_NAME: map_name,
                MAP_POINTS: map_points,
                MAP_LINK: imageSource
            };
    fetch('/api/map_creation', { // Use a relative URL here
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })

    window.alert("Map Successfully Uploaded! You may leave the page now");
}