const userLocation = document.querySelector("#form-address");
  const markericon = document.querySelector('.marker-img');
  const crossicon = document.querySelector('.cross-img');

  const status = document.querySelector(".locStatus");
  const spinner = document.querySelector(".spinner");

  const LongiValue = document.querySelector(".LongiValue");
  const LattiValue = document.querySelector(".LattiValue");

  const map = document.querySelector(".map");
  let state;


  const startDate = document.querySelector("#startdate");
  const endDate = document.querySelector("#enddate");

  const search = document.querySelector("#search-btn");

  
  let latitude ="",longitude ="";
  
  const app_id = "mEmcQorNDxKT5Mat31QK";//here's api
  const app_code="G6yKNlD9jS6U_QRN7PCINw";//here's api
  const hapikey = "QgpYzyuJVwnmVsc3WJBuEL26B_PAUjGg4fkJyhsBMrQ";//here's api
  const w_key="4c14c1a61b22493a98a122059191012";//world weather online api

  userLocation.addEventListener("input",function(){
    
      if(userLocation.value != ""){
        markericon.style.zIndex=-1;
      }else{
        markericon.style.zIndex=2;  
      }
  })
   markericon.addEventListener("click",()=>{
    findLocation();
   })

  crossicon.addEventListener("click",function(){
    userLocation.value = "";
    markericon.style.zIndex=2;
  })

  function findLocation(){

      function success(position) {
      latitude  = position.coords.latitude;
      longitude = position.coords.longitude;
       console.log(latitude,longitude);
      
      const distanceUpto = 250;
      
      
    
     //Location Request
     axios.get(`https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?prox=${latitude},${longitude},
     ${distanceUpto}&mode=retrieveAddresses&maxresults=1&gen=9&app_id=${app_id}&app_code=${app_code}`)
     .then(res =>{
      spinner.className = "d-none";
         const DetectedLoc = res.data.Response.View[0].Result[0].Location.Address.Label;
         userLocation.value = DetectedLoc;


         var latlong = document.querySelector('#latlong')
         latlong.value = latitude;
         state = res.data.Response.View[0].Result[0].Location.Address.AdditionalData[1].value;
         console.log(state);
        
       var data = new FormData();  
      data.append('lat', latitude);
      data.append('long',longitude);
      data.append('state',state);
      var xhr = new XMLHttpRequest(); xhr.open('POST', '/example', true); 
      xhr.onload = function () { console.log(this.responseText); }; xhr.send(data);

      map.src = `https://image.maps.ls.hereapi.com/mia/1.6/mapview?apikey=QgpYzyuJVwnmVsc3WJBuEL26B_PAUjGg4fkJyhsBMrQ&c=${latitude},${longitude}&u=5m&z=8`;

     })
     .catch(err=> {
       console.log(err);
      spinner.className = "d-none";
      status.textContent ="Unable to Detect Location";
     });
   
     

  }

  function error() {
      status.textContent = 'Unable to retrieve your location';
  }

      if (!navigator.geolocation) 
        status.textContent = 'Geolocation is not supported by your browser';
      else {
        spinner.className = "d-block";
        navigator.geolocation.getCurrentPosition(success, error);
     }
  }

   search.addEventListener('click',(e)=>{
     e.preventDefault();
 //if location not autodetcted
    if(latitude== "" || longitude ==""){
      axios.get(`https://geocoder.ls.hereapi.com/6.2/geocode.json?apikey=${hapikey}&searchtext=${userLocation.value}`)
      .then(res=>{
         latitude=res.data.Response.View[0].Result[0].Location.DisplayPosition.Latitude;
         longitude=res.data.Response.View[0].Result[0].Location.DisplayPosition.Longitude;
         state = res.data.Response.View[0].Result[0].Location.Address.AdditionalData[1].value;

         map.src = `https://image.maps.ls.hereapi.com/mia/1.6/mapview?apikey=QgpYzyuJVwnmVsc3WJBuEL26B_PAUjGg4fkJyhsBMrQ&c=${latitude},${longitude}&u=5m&z=8`;

         var data = new FormData();  
         data.append('lat', latitude);
         data.append('long',longitude);
         data.append('state',state);
         var xhr = new XMLHttpRequest(); xhr.open('POST', '/example', true); 
         xhr.onload = function () { console.log(this.responseText); }; xhr.send(data);
      }).then((e)=>{
        loadRes();
      })
      .catch(err=>{
        console.log(err);
        alert("Unable to located this place,Try autodetect Location");
      })
    }
     //Weather Request
   });

   //AutoDetect Location from input

   (function() {
var placesAutocomplete = places({
  appId: 'pl1NPK6DVMJ8',
  apiKey: '05a79c264601030bc900633357c3029f',
  container: document.querySelector('#form-address'),
  templates: {
    value: function(suggestion) {
      return suggestion.name;
    }
  }
}).configure({
  type: 'city',
});
})();


function loadRes() {
  var xhr = new XMLHttpRequest(); xhr.open('GET', '/result', true); 
      xhr.onload = function () { document.querySelector('#res').innerHTML = this.responseText }; xhr.send();
}