var canvas; 

function onNewStatus(data, status) {
   for (var key in data) {
      if ( key in canvas.mic_components ) 
         canvas.mic_components[key].set_state( data[key] );
   }   
   canvas.redraw();
}

function transducer( name, prec, units, x_pos, y_pos ) {
    var button = canvas.display.rectangle({
        x: x_pos,
        y: y_pos,
        origin: { x: "center", y: "center" },
        width: 70,
        height: 20,
        fill: "#fff",
        stroke: "2px #00",
    });
    var buttonText = canvas.display.text({
        x: 0,
        y: 0,
        origin: { x: "center", y: "center" },
        align: "center",
        font: "bold 10px sans-serif",
        text: "xxxx",
        fill: "#00",

        mic_units: units,
        mic_prec: prec,
    });
    button.addChild(buttonText);

    button.set_state = function( state ) {
        buttonText.text = state.toFixed(buttonText.mic_prec) + ' ' + buttonText.mic_units 
    };

    button.mic_left = function() {
        return button.x - button.width/2;
    };

    button.mic_right = function() {
        return button.x + button.width/2;
    };

    canvas.addChild(button);
    canvas.mic_components[name] = button;
    return button;
}

function valve( name, x_pos, y_pos ) {
    var valve = canvas.display.arc({
        x: x_pos, 
        y: y_pos,
        radius: 10,
        start: 0,
        end: 360,
        fill: "#fff",
        pieSection: false,
        stroke: "2px #000",
        valve_type: 'H',
    });

    var valve_bar = canvas.display.rectangle({
        x: 0, 
        y: 0,
        origin: { x: "center", y: "center" },
        width: valve.radius*2,
        height: 2,
        fill: "#00",
        stroke: "2px #00",
    });
    valve.addChild(valve_bar);

    var valveText = canvas.display.text({
        x: x_pos,
        y: y_pos + valve.radius + 10,
        origin: { x: "center", y: "center" },
        align: "center",
        font: "bold 10px sans-serif",
        text: name,
        fill: "#00",
    });
    canvas.addChild(valveText);

    valve.set_state = function( state ) {
        if ( ( state && valve.valve_type == 'H' ) 
             || ( !state && valve.valve_type != 'H') )
            valve.rotation = 0;
        else 
            valve.rotation = 90;
    };

    var form_name = "dialog-form-valve-"+name;
    $("#dialog-list").append("<div id=\""+form_name+"\" title=\"Set "+name+" Valve\"></div>");
    $("#"+form_name ).dialog({
      autoOpen: false,
      height: 150,
      width: 250,
      modal: true,
      buttons: {
        "Cancel": function() {
          $( this ).dialog( "close" );
        },
        "Open": function() {
            $.post("/instrument/actuate/", 
                   {cmd:"set_valve", 
                    data:JSON.stringify({valve:name, position:true})},
                    onNewStatus );
            $( this ).dialog( "close" );
        },
        "Close": function() {
            $.post("/instrument/actuate/", 
                   {cmd:"set_valve", 
                    data:JSON.stringify({valve:name, position:false})},
                    onNewStatus );
            $( this ).dialog( "close" );
        },
      },
    });

    canvas.addChild(valve);

    valve.bind("click", function () {
      $( "#"+form_name ).dialog( "open" );
    });

    valve.mic_left = function() {
        return valve.x - valve.radius;
    };

    valve.mic_right = function() {
        return valve.x + valve.radius;
    };

    canvas.mic_components[name] = valve;
    return valve;
}

function rectangle( X1, Y1, X2, Y2, fill ) {
    var rect = canvas.display.rectangle({
        x: X1,
        y: Y1,
        origin: { x: "left", y: "top" },
        width: X2-X1,
        height: Y2-Y1,
        fill: fill,
        stroke: "2px #00",
        join: "round"
    });
    canvas.addChild(rect);
}
function line( eps ) {
    for ( var i = 0; i < eps.length-1; i++ ) {
        var x1 = eps[i][0];
        var x2 = eps[i+1][0];
        var y1 = eps[i][1];
        var y2 = eps[i+1][1];

        var rect = canvas.display.rectangle({
            x: x1,
            y: y1,
            origin: { x: "left", y: "top" },
            width: x2-x1,
            height: y2-y1,
            fill: "#fff",
            stroke: "4px #000",
            join: "round"
        });
        canvas.addChild(rect);
    }
}

function schematic(  ) {

    var canvas = oCanvas.create({
	    canvas: "#schematic"
    });
    canvas.mic_components = {}

	var updateInterval = 500;
	function update() {
		$.ajax({
			url: "/instrument/schematic_status/",
			type: "GET",
			dataType: "json",
			success: onNewStatus,
		});
        setTimeout(update, updateInterval);
    }
	update();

    canvas.mic_valve = valve;
    canvas.mic_transducer = transducer;
    canvas.mic_rectangle = rectangle;
    canvas.mic_line = line;

    return canvas;
}
