function showTime(){
    var date = new Date();
    var h = date.getHours(); // 0 - 23
    var m = date.getMinutes(); // 0 - 59
    var s = date.getSeconds(); // 0 - 59
    var d = date.getDay();
    // var session = "AM";

    var j_days = { 0:"یکشنبه", 1:"دوشنبه", 2:"سه‌شنبه", 3:"چهارشنبه", 4:"پنج‌شنبه", 5:"جمعه", 6:"شنبه" }
    
    if(h == 0){
        h = 12;
    }
    
    /*if(h > 12){
        h = h - 12;
        session = "PM";
    }*/
    
    h = (h < 10) ? "0" + h : h;
    m = (m < 10) ? "0" + m : m;
    s = (s < 10) ? "0" + s : s;
    
    // var time = h + ":" + m + ":" + s + " " + session;
    var j_date = new Intl.DateTimeFormat('fa-IR').format(date);
    var time = h + ":" + m + ":" + s;
    document.getElementById("MyClockDisplay").innerText = time;
    document.getElementById("MyClockDisplay").textContent = time;

    document.getElementById("MyDateDisplay").innerText = j_date;
    document.getElementById("MyDateDisplay").textContent = j_date;

    document.getElementById("MyDayDisplay").innerText = d;
    document.getElementById("MyDayDisplay").textContent = j_days[d];
    
    setTimeout(showTime, 1000);
    
}

showTime();