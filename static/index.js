let forecast;

const changeTab = (tab) => {
  $(".opt").removeClass("selectOpt");
  $(tab).addClass("selectOpt");
  console.log(tab.tabIndex);
  $(".optContent").removeClass("selectContent");
  $($(".optContent")[tab.tabIndex]).addClass("selectContent");
}

const getLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(processLocation);
  } else {
    alert("Geolocation is not supported by this browser.");
  }
}

const processLocation = (pos) => {
  x = document.querySelector("#content > p:nth-child(2)")
  x.innerHTML = "Latitude: " + pos.coords.latitude +
    "<br>Longitude: " + pos.coords.longitude;

  position.latitude = pos.coords.latitude;
  position.longitude = pos.coords.longitude;

  getForecast();
}

const getForecast = () => {
  let gotDailyResult = false
  let gotForecastResult = false
  $.get($SCRIPT_ROOT + "daily_forecast", position, (data) => {
    gotDailyResult = true
    //forecast = data;
    //alert(JSON.stringify(data));
    populateDashboard(data)
  });

  setTimeout(() => {
    if (!gotDailyResult) {
      alert("ALERT: fetching daily forecast is taking a while...")
    }
  }, 5000)

  $.get($SCRIPT_ROOT + "forecast", position, (data) => {
    gotForecastResult = true
    forecast = data;
    reccomend(data)
  });

  setTimeout(() => {
    if (!gotForecastResult) {
      alert("ALERT: fetching hourly forecast is taking a while...")
    }
  }, 5000)
}

const populateDashboard = (data) => {
  $("#dashboard-temp").html((!!data.min_temp ? data.min_temp + "&#176;F" : "N/A") + " - " + (!!data.max_temp ? data.max_temp + "&#176;F" : "N/A"));
  $("#dashboard-overcast").html(data.overcast);
  $("#dashboard-percipitation").html(data.precip.toFixed(4) + " inches");
  $("#dashboard-description").html(data.narrative);
}

const reccomend = (data) => {
  //----------Dashboard Tab----------
  $("#recc-total").html(data.total_precip.toFixed(4) + " in");

  let avoidTimes = []
  for (let i = 0; i < data.precip_rate.length; i++) {
    //console.log(convertTime(data.time[i]), data.precip_rate[i]);
    if (data.precip_rate[i] > .001) {
      let time = convertTime(data.time[i])
      avoidTimes.push({ start: time, end: addTime(time, 15),amount:data.precip_rate[i] })
    }
  }

  let first=null
  let total=0
  if (avoidTimes.length > 0) {
    first = avoidTimes[0]
  }
  for (let i = 1; i < avoidTimes.length; i++) {
    if (avoidTimes[i-1].end == avoidTimes[i].start && i != avoidTimes.length-1) {
      total+=avoidTimes[i].amount
    }
    else{
      $("#recc-avoid").append(`<li>${first.start}- ${avoidTimes[i].end} (${total.toFixed(3)} inches)</li>`)
      if (i != avoidTimes.length - 1) {
        first = avoidTimes[i + 1]
        total=0
      }
    }
  }

  //----------Weather Tab----------
  console.log(data);
  let labels=[];
  for(let i=0;i<data.time.length;i++){
    if(i%2==0){
      labels.push("");
    }else{
      labels.push(convertTime(data.time[i]));
    }
  }
  bargraph("graph-precip",data.precip_rate,labels)
}

const showUsage=(data)=>{
  //----------Stats Tab----------
  let labels=new Array(data.data.length).fill('');
  labels[labels.length-1]="| today";
  labels[labels.length-8]="| last week";
  for(let i=2;i<labels.length;i++){
    labels[labels.length-1-(i*7)]="| "+i+" weeks ago";
  }
  bargraph("graph-usage",data.data,labels);
  hours_saved = data.hours_saved.toFixed(2);
  gallons_saved = data.gallons_saved.toFixed(2);
  $("#summary-hours-saved").html(hours_saved);
  $("#summary-gallons-saved").html(gallons_saved);
}

$(document).ready(() => {
  getForecast();
  $.get($SCRIPT_ROOT + "schedule", (data) => {
    //alert(JSON.stringify(data));
    if (data.frequency == 0) {
      $("#recc-dur").parent().html("Due to the volume of rain today, there is no need to turn on your irrigation system.");
      $("#recc-freq").parent().html("");
    } else {
      $("#recc-dur").html(data.duration);
      $("#recc-freq").html(data.frequency);
    }
  })

  $.get($SCRIPT_ROOT + "usage", (data) => {
    //TODO: it'd be nicer for the graph to return the dates along with the usage data
    showUsage(data);
  })
});

function addTime(time, mins) {
  nums = time.split(':')
  hours = parseInt(nums[0])
  minutes = parseInt(nums[1])
  hours += Math.floor((minutes + mins) / 60)
  if(hours<10){
    hours="0"+hours.toString();
  }
  minutes = (minutes + mins) % 60
  if (minutes < 10) {
    minutes = "0" + minutes.toString();
  }
  return (hours + ":" + minutes)
}
function convertTime(time) {
  return time.replace(/^.*T/, '').replace(/[-+].*$/, '').replace(/:..$/, '');
}