
//PURPOSE: CREATE A RED DOT INDICATING A LOCATION
//AND SAVE IT IN "map_points" VARIABLE
var zoomTarget = document.getElementById('zoomTarget');
var map_points = ""
zoomTarget.addEventListener('click', function(e) {
  const { left, top, width, height } = this.getBoundingClientRect();
  const x = (e.clientX - left) / width;
  const y = (e.clientY - top) / height;
  this.style.transformOrigin = `${x * 100}% ${y * 100}%`;
  if (map_points.slice(-1) !="-")
  {
      map_points = map_points+`${x * 100}% ${y * 100}%`+"-";
      var redDot = document.createElement('div');
          redDot.className = 'red-dot';
          redDot.style.left = `${x * 100}% `;
          redDot.style.top = `${y * 100}% `;
          console.log(`${x * 100 }%`)
          console.log(`${y * 100 }%`)
          zoomTarget.parentElement.appendChild(redDot);
  }
  else{
  document.getElementById("msg").innerHTML = " Please Submit A Place's name";
  }
});