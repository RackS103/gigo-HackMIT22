let result = "lol"
async function fetchAsync () {
  fetch('/update')
  .then((response) => response.json())
  .then((data) => update_website(data));
}

var t=setInterval(fetchAsync,1000);
var ctx = document.getElementById("result").getContext("2d")
function update_website(data){
if (data.img != "default"){
  console.log(data)
  const img = new Image();   // Create new img element
  img.addEventListener('load', () => {
  ctx.drawImage(img,0,0,256,256)
  }, false);
  img.src = data.img; // Set source path
  document.getElementById("which_bin").innerHTML = data.material
  document.getElementById("sugg").innerHTML = data.suggestion
}
}