function startApp(){
    window.location.href = "/onboarding";
}

function goDevice(){
    window.location.href = "/device";
}

function callBackend(route){
    fetch("/" + route)
}

function powerOn(){
    callBackend("power")
}

function walkingMode(){
    callBackend("walking")
    window.location.href = "/walking_page";
}

function companionMode(){
    callBackend("companion")
    window.location.href = "/companion_page";
}
