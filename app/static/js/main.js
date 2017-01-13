$( document ).ready(function() {
    $.getJSON($SCRIPT_ROOT+"/get_data", function (data) {
        console.log("Success")
        var transportations_min_max = getMaxAndMinTransportationNumbers(data);
        createGraph(data, transportations_min_max)
    });


});

function findMaxXandY(json_data){
    var max_x = 0;
    var max_y = 0;
    $.each(json_data['facility'], function (key1, value1) {
        $.each(value1["boundaries"], function (key, value){
            if (value[0] > max_x){
                max_x = value[0]
            }
            if (value[1] > max_y){
                max_y = value[1]
            }
        })
    });
    var max_values = [max_x, max_y]
    return max_values

}
function scalePoints(height, width, json_data, key, max_x_y, xLinearScale, yLinearScale){
    var points = [];

    $.each(json_data['facility'][key]['boundaries'], function (key, value) {
        var scaled_x_y = [xLinearScale(value[0]),yLinearScale(value[1])];
        points.push(scaled_x_y);
    });
    return points
}

function getMaxAndMinTransportationNumbers(json_data) {
    var max_transportation_number = 0;
    var min_transportation_number = 100000;
    $.each(json_data['edges'], function (key,value) {
        var number = json_data['edges'][key][2];
        if (number > max_transportation_number) {
            max_transportation_number = number;
        }
        if (number < min_transportation_number){
            min_transportation_number = number;
        }
        });
    return [max_transportation_number, min_transportation_number]
}

function genereteLineColor(number, max_transportation_number, min_transportation_number) {
    var scale_number = ((max_transportation_number-number)/max_transportation_number);
    if (scale_number < 50) {
        var r = Math.floor(255 * (scale_number/ 50))
        var g = 255;
    } else {
        var r = 255;
        var g = Math.floor((255 * ((50 - scale_number % 50) / 50)))
    }
    return [r,g,0]
}

function getColor(value, max_transportation_number){
    //value from 0 to 1
    var hue = Math.floor((max_transportation_number - value) * 120 / max_transportation_number).toString(10)
    var saturation = Math.abs(value - 50)/50;
    return ["hsl(",hue,","+saturation+"%,70%)"].join("");
}



function createGraph(json_data, transportation_ranges) {

    var height = document.getElementById("factory_transp_container").offsetHeight;
    var width = document.getElementById("factory_transp_container").offsetWidth;
    var max_x_y = findMaxXandY(json_data)
    //console.log(transportation_ranges)
    var xLinearScale = d3.scaleLinear()
        .domain([0, max_x_y[0]])
        .range([0,width]);

    var yLinearScale = d3.scaleLinear()
        .domain([0,max_x_y[1]])
        .range([0,height]);

    var svgContainer = d3.select("#factory_transp_container")
        .append("svg")
            .attr('height',height)
            .attr('width', width);

    $.each(json_data['facility'],function (key, value) {
                svgContainer.append('polygon')
                        .style("stroke-width", 5)
                        .attr("points", scalePoints(height, width,json_data,key, max_x_y, xLinearScale, yLinearScale))
                        .attr("stroke", 'black')
                        .attr("fill", '#dbe9ee')
                       // .attr("transform","scale(1,-1) translate(0,"+(-yLinearScale(max_x_y[1]))+")");
                svgContainer.append('circle')
                        .attr("cx", -(xLinearScale(json_data['facility'][key]['points']['centroid'][0])))
                        .attr("cy", -(yLinearScale(json_data['facility'][key]['points']['centroid'][1])))
                        .attr('r', 5)
                        .attr("fill", "black")
                       // .attr("transform","scale(-1, -1) translate(0,"+-(yLinearScale(max_x_y[1]))+")")
                svgContainer.append('text')
                        .style("fill", "black")
                        .attr("x", -(xLinearScale(json_data['facility'][key]['points']['centroid'][0])))
                        .attr("y",-(yLinearScale(json_data['facility'][key]['points']['centroid'][1])))
                        .attr("font-size", "9px")
                        .attr("dy", "-.85em")
                        .attr("font-family", "Lato")
                        .attr("text-anchor", "middle")
                        .text(key)
                      //  .attr("transform","translate(0,"+-(yLinearScale(108)+")"))
//                        .attr("transform","scale(1,-1)")

    });
    $.each(json_data['edges'], function(key,value){
        var color = genereteLineColor(value[2],transportation_ranges[0], transportation_ranges[1])
        var color2 = getColor(value[2],transportation_ranges[0])

        svgContainer.append("line")
            //.style("stroke", d3.rgb(color[0],color[1],color[2]))
            .style("stroke", d3.color(color2))
            .style("stroke-width", 2)
            .attr("x1", -xLinearScale(json_data['facility'][value[0].split('.')[0]]['points']['centroid'][0]))
            .attr("y1", -yLinearScale(json_data['facility'][value[0].split('.')[0]]['points']['centroid'][1]))
            .attr("x2", -xLinearScale(json_data['facility'][value[1].split('.')[0]]['points']['centroid'][0]))
            .attr("y2", -yLinearScale(json_data['facility'][value[1].split('.')[0]]['points']['centroid'][1]))
  //          .attr("transform","scale(1,-1) translate(0,"+(-yLinearScale(max_x_y[1]))+")")
    })};