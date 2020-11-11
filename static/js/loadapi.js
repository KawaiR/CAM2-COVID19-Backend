const api_key = "AIzaSyDUlueLd9Uh5vmtOeXBZ_7B0_XMWNPVbjE";
function loadScript() {
    var API = document.createElement('script');
    API.type = 'text/javascript';
    API.src = 'https://maps.googleapis.com/maps/api/js?libraries=places&key='+api_key+'&callback=initMap'; 
    API.defer = true;
    document.body.appendChild(API);
    console.log("API loaded")
  }
  
  window.onload = loadScript;