<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <!-- <script src='https://api.mapbox.com/mapbox-gl-js/v0.34.0/mapbox-gl.js'></script> -->
    <script src='https://npmcdn.com/@turf/turf/turf.min.js'></script>
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script src="https://connect.facebook.net/en_US/all.js"></script>

<script src='https://api.mapbox.com/mapbox-gl-js/v2.3.1/mapbox-gl.js'></script>
<link href='https://api.mapbox.com/mapbox-gl-js/v2.3.1/mapbox-gl.css' rel='stylesheet' />

    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.2.0/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.2.0/dist/leaflet.js"></script>
    <!-- <link href='https://api.mapbox.com/mapbox-gl-js/v0.34.0/mapbox-gl.css' rel='stylesheet' /> -->
    <link rel="stylesheet" href="https://bootswatch.com/4/cosmo/bootstrap.min.css" />
</head>
<body>
<script>
  window.fbAsyncInit = function() {
    console.log("start");
    FB.init({
      appId      : '224454914692898',
      // autoLogAppEvents : true,
      // status           : true,
      xfbml      : true,
      version    : 'v2.10'
    });
    console.log("log");
    FB.AppEvents.logPageView();
    console.log("token?");
  // FACEBOOK TOKEN
  // FB.getAuthResponse();
FB.getLoginStatus(function(response) {
  console.log(response);
  if (response.status === 'connected') {
    var token = response.authResponse.accessToken;
    console.log(token);
  }
} );
  };

  (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "//connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));

  function visu(){
    token = document.getElementById("inputoken").value;
    url = "./index.php?key="+token;
    window.location.replace(url);
  }
</script>

<b>My FB insight</b>　　to visualize your data:<br>
1. Get yout access_token <a href="https://developers.facebook.com/tools/explorer/?method=GET&path=me%3Ffields%3Did%2Cname&version=v2.11" target="_blank">here</a> <br>
2. paste your access token here →　<input type="text" id="inputoken" value="your access token"><br>
3. <a href="#" onclick="visu()">VISUALIZE</a>
<div id="map" style="width:100%; height:700px"></div>
<div id="json"></div>
<script>



function processAlbum(albums){
    for(var j=0; j < albums.length; j++){
    // albums.forEach(function(alb){
      //in one album, first page
      if(albums[j].id=="1495671911263"){
        a=1;
      }
      if(albums[j].photos){
      photo = albums[j].photos.data;

          for(var i=0; i < photo.length; i++){
            // photo.forEach(function(pic){
                  thumb = photo[i].picture;
                  if(photo[i].place && photo[i].place.location){
                    // if(a==1){console.log([place_name,lon,lat]);}
                    place_name = photo[i].place.name
                    lon = photo[i].place.location.longitude;
                    lat = photo[i].place.location.latitude;
                    addGeojson(thumb,place_name,lon,lat);
                } else {
                  // console.log([thumb,place_name,lon,lat]);
                }
            }
          // console.log(photo);
          if(albums[j].photos.paging.next){
            nextpagePhoto(albums[j].photos.paging.next);
          }
        }
    }
}
function nextpagePhoto(url){
  axios.get(url).then(function(result){
    // console.log(result);
    photo=result.data.data;
    photo.forEach(function(pic){
      if (pic.place && pic.place.location){
          // if(a==1){console.log([place_name,lon,lat]);}
          thumb = pic.picture;
          place_name = pic.place.name
          lon = pic.place.location.longitude;
          lat = pic.place.location.latitude;
          addGeojson(thumb,place_name,lon,lat);
        }
    });
        // console.log(photo);
        if(result.data.paging.next){
          nextpagePhoto(result.data.paging.next);
        }
  });
}


function nextpageAlbum(url){
  axios.get(url).then(function(result){
    albums = result.data.data;
    // console.log(result);
    processAlbum(albums);

      //next page album
      if(result.data.paging.next){
        // console.log("!!");
        nextpageAlbum(result.data.paging.next);
      } else {
        // console.log(inbjson);
          var inbjson = turf.featureCollection(inbounds);
          console.log(inbjson);
          loadmap(inbjson);
      }

  });
}

function addGeojson(thumb,place_name,lon,lat){
    if(lon && lat){
    var feature = turf.point([lon, lat], {name: place_name, img:thumb});
    inbounds.push(feature);
  }
}


function loadmap(inbjson){
mapboxgl.accessToken = 'pk.eyJ1IjoiYm9yZG9yYXkiLCJhIjoiY2tqbThwaXpzNTd5YjMzbnlzb2h3MWN2MiJ9.a-ofbh89FAqM5VJS88WtfQ';
// Create a popup, but don't add it to the map yet.
var popup = new mapboxgl.Popup({
    closeButton: false
});

//generate map
var map = new mapboxgl.Map({
    container: 'map',
    center: [137.5, 37.5],
    zoom: 4.5,
    // minZoom: 4,
    interactive : true,
    style: 'mapbox://styles/bordoray/ckjm8tv9i1n2t19ruvknhkbkh'
});

  map.on('load',function(){

        // // sources
        //     map.addSource('mierune', {
        //         'type': 'raster',
        //         'tiles': [
        //             murl
        //         ],
        //         'tileSize': 256
        //     });
        //
        //       map.addLayer({
        //         'id': 'wms-test-layer',
        //         'type': 'raster',
        //         'source': 'mierune' ,
        //         'paint': {}
        //     });

            // sources
                console.log(inbjson);
                console.log("wait...");
                setTimeout(function(){
                  console.log(inbjson);
                                  map.addSource('inbounds', {
                                        "type":"geojson",
                                        "data":inbjson
                                  });


                                  map.addLayer({
                                      "id": "places",
                                      "source": "inbounds",
                                      "type": "circle",
                                      "paint": {
                                          "circle-radius": 3.5,
                                          "circle-color": "#ff00aa",
                                          "circle-opacity":0.6
                                      }
                                    },
                                  );
                },2000);


  map.on('mousemove', function (e) {
    var fe = map.queryRenderedFeatures(e.point, {layers: ['places']});
    if(fe.length){
         clon = fe[0].geometry.coordinates[0];
         clat = fe[0].geometry.coordinates[1];
         place_name = fe[0].properties.name;
         popupcontent = place_name+"<br><table><tr>";
         for(var j=0; j < fe.length; j++){
            if (j<3){
              var n = fe.length - j-1;
              // console.log(n);
            //  n = Math.round(Math.random()*fe.length);
             img_url = fe[n].properties.img;
             popupcontent += "<td>　<img src='"+img_url+"'/>　</td>";
           }
         }
             popup.setLngLat([clon,clat])
             .setHTML(popupcontent+"</tr></table>")
             .addTo(map);
    } else {
      popup.remove();
    }
  });

      });

document.getElementById("inputoken").value = "Done!";
        // map.getSource('inbounds').setData(inbjson);
}

var a=0;
var inbounds=[];

var token = '<?php echo $_GET["key"]; ?>';
// "EAADMIZCt1VyIBANBycVIVIaSoLRp3jS328ovPXazt9OiC5Si4ZAgAfASSzqputtN6NtNpy9wbM7AHXXdRcgjlFBRTz4GdZC3n6Hv6X4AKnbxbgOp64qwfZAB7ujZCa4owBy0WliCbVl18NnpJ7NgC8PKZCyDylgVxhNIE9bn8qXrCcC5S7X4d4NgxJDaLCx8sZD";
var url = "https://graph.facebook.com/v11.0/me?fields=albums%7Bphotos.limit(600)%7Bpicture%2Cplace%7D%7D&limit=800&access_token="+token;

// MIERUNE tiles
var style ='<?php echo $_GET["style"]; ?>';
var murl= "https://tile.cdn.mierune.co.jp/styles/"+style+"/{z}/{x}/{y}.png?key=xzW_kHFn4dy8g-3NLR2-eM_q2_xqaB8Oqq7OrDJEhd1hFlQuBroj-9MjCtpo76rD";


axios.get(url).then(function(result){
  document.getElementById("inputoken").value = "Wait...";

  albums=result.data.albums.data;
  // console.log(albums);
  processAlbum(albums);

  //next page album
  if(result.data.albums.paging.next){
    // console.log("!!");
    nextpageAlbum(result.data.albums.paging.next);
  } else {
      var inbjson = turf.featureCollection(inbounds);
      loadmap(inbjson);
  }

});

</script>



</body>
</html>
