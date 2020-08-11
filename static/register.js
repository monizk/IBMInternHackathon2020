const position = {
  latitude: null,
  longitude: null
}

const getLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(processLocation);
  } else {
    alert("Geolocation is not supported by this browser.");
  }
}

const processLocation = (pos) => {
  document.querySelector("#latitudeInput").value = pos.coords.latitude.toFixed(2);
  document.querySelector("#longitudeInput").value = pos.coords.longitude.toFixed(2);
}