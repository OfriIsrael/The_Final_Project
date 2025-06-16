
/* script purpose: verifies if the user's click position in the game section  */
var zoomTarget = document.getElementById('zoomTarget');
var map_points = ""
zoomTarget.addEventListener('click', function(e) {
  const { left, top, width, height } = this.getBoundingClientRect();
  const x = 100*(e.clientX - left) / width;
  const y = 100*(e.clientY - top) / height;

