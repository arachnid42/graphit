$( document ).ready(function() {
    $.getJSON($SCRIPT_ROOT+"/get_data", function (data) {
        console.log("Success")
        createGraph(data)
    });
});

function createGraph(json_data) {

    var height = document.getElementById("facility").offsetHeight;
    var width = document.getElementById("facility").offsetWidth;


    console.log(width)
    console.log(height)

    var svgContainer = d3.select("#facility")
        .append("svg")
            .attr('height',1200 )
            .attr('width',1900);

    $.each(json_data['departments'],function (key, value) {
            console.log(key,value)
                svgContainer
                    .append('polygon')
                        .attr("points", json_data['departments'][key]['points'])
                        .attr("stroke", 'black')
                        .attr("fill", '#dbe9ee')
                        .attr("transform","scale(5,-5) translate(0, -110)")
    });
}