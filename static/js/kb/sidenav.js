var isOpenNav = true;
var opener = document.getElementById("nav-opener");
var openerArrow = document.getElementsByTagName("i")[0].getElementsByTagName("div")[0];
var sidenav = document.getElementById("sidenav");

function openNav() {
    isOpenNav = true;
    sidenav.style.left = "0px";
    document.getElementById("main").style.marginLeft = "220px";  
    openerArrow.setAttribute('uk-icon', 'triangle-left');
    opener.onclick = function(){ closeNav(); };
}

function closeNav() {
    isOpenNav = false;
    sidenav.style.left = "-220px";
    document.getElementById("main").style.marginLeft = "0px";
    openerArrow.setAttribute('uk-icon', 'triangle-right');
    opener.onclick = function(){ openNav(); };
}

function hoverNav(state) {
    if(!isOpenNav && state == 'hover'){
        opener.style.width = "20px";
        document.getElementsByTagName("i")[0].style.left = "15%";
    }
    else {
        opener.style.width = "5px";
        document.getElementsByTagName("i")[0].style.left = "-25%";
    }
}

function projectClick(index) {
    var url = '/board/';
    var form = $("<form action='" + url + "'method='GET'>" + "{% csrf_token %}" +
    "<input type='text' name='projNum' value='" + index + "' />" +
    "</form>");
    $('body').append(form);
    form.submit();
}
