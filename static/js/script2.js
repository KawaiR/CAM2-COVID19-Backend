

// disable if scroll snap is enabled
window.addEventListener("wheel", event => {
    //left = positive
    //up = positive
    
    if (event.wheelDeltaX == 0 && event.wheelDeltaY >= -1 || event.wheelDeltaY <= -3){
        event.preventDefault()
        var mult = -0.50

        var delta = mult * event.wheelDelta; 

        console.log('wheeldata', delta)
        console.log("xdelta", event.wheelDeltaX)
        console.log("ydelta", event.wheelDeltaY)
        console.log("details", event)


        var pst = $('.container').scrollLeft() + delta;
        $('.container').scrollLeft(pst);
    }
}, {passive: false});


// jQuery(function($) {
//     $(".container").panelSnap();
// });
