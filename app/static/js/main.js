var START_DATE = null;
var END_DATE = null;
var SCALE = 0.945;

$( document ).ready(function() {
    $.getJSON($SCRIPT_ROOT+"/get_data", function (data) {
        START_DATE = data['date_boundaries'][0].split(" ")[0];
        END_DATE = data['date_boundaries'][1].split(" ")[0];
        getVisualization(data);
        toggleLoading(0, 100);
    });
});

function getVisualization(data) {
    var transportations_min_max = getMaxAndMinTransportationNumbers(data);
    createGraph(data, transportations_min_max);
    createInfoTable(data, getMaxAndMinTransportationNumbers(data)[0]);
    createStatisticsTable(data);
    createDateRangePicker(data);
}

function createDateRangePicker(data) {
    $("#e4").daterangepicker({
                 presetRanges: [{
                     text: 'Full range',
                     dateStart: function() { return moment(START_DATE) },
                     dateEnd: function() { return moment(END_DATE) }
                 }, {
                     text: 'Previous year',
                     dateStart: function() { return moment().subtract(1, "years") },
                     dateEnd: function() { return moment() }
                 }, {
                     text: 'Previous 3 months',
                     dateStart: function() { return moment().subtract(3, "months") },
                     dateEnd: function() { return moment() }
                 }, {

                     text: 'Previous month',
                     dateStart: function() { return moment().subtract(1,"months") },
                     dateEnd: function() { return moment() }
                 }, {
                     text: 'Next month',
                     dateStart: function() { return moment() },
                     dateEnd: function() { return moment().add(1, "months") }
                 }, {
                     text: 'Next 3 months',
                     dateStart: function() { return moment() },
                     dateEnd: function() { return moment().add(3, "months") }
                 }, {

                     text: 'Next year',
                     dateStart: function() { return moment() },
                     dateEnd: function() { return moment().add(1, "years") }
                 }],
                 applyOnMenuSelect: true,
                 datepickerOptions : {
                     numberOfMonths : 3,
                     dateFormat: 'yy-mm-dd',
                     minDate: START_DATE,
                     maxDate: END_DATE,
         },
            change: function(event, data) {
                var selectedDateRange = JSON.parse($("#e4").val());
                toggleLoading(1, 180);
                $.getJSON($SCRIPT_ROOT+"/get_data_filtered", {
                    start: selectedDateRange['start'],
                    end: selectedDateRange['end']
                }, function (data) {
                    d3.select("svg").remove();
                    getVisualization(data);
                    toggleLoading(0, 100);
                });
            }
        });
}

function createStatisticsTable(json_data){
    var dummy_transportations_amount = 0;
    var total_transportations_times = 0;
    var total_items_transported = 0;
    $.each(json_data['edges'], function (key, value) {
        if(value[0].split(".")[0]=="DUMMY"||value[1].split(".")[0] == "DUMMY"){
            dummy_transportations_amount+=value[2];
        }
        total_transportations_times+=value[3];
        total_items_transported+=value[2];
    });
    $(".total_amount_of_transportations").empty().append(total_transportations_times);
    $(".total_items_transported").empty().append(total_items_transported);
    $(".dummy_count").empty().append(dummy_transportations_amount);
    $(".dep_involved").empty().append(json_data["involved_edges_count"]+" from 14");
    $(".date_range").empty().append(json_data['date_boundaries'][0].split(" ")[0]+" - "+json_data['date_boundaries'][1].split(" ")[0]);
    $(".omitted_self-edges").empty().append(json_data['self_edges_total_weight']);
}

function toggleLoading(opacity, speed){
    var overlay = $("#full_page_overlay");
    if(opacity) overlay.show();
    overlay.stop().fadeTo(speed, opacity);
    $("#header").stop().fadeTo(speed, 1-opacity);
    $("#viz_container").stop().fadeTo(speed, 1-opacity);
    $("#footer_container").stop().fadeTo(speed, 1-opacity);
    if(!opacity) overlay.hide();
}

function toggleVizRebuildOverlays(opacity) {
    var overlay = $(".gen_overlay");
    if(opacity) overlay.show();
    overlay.stop().fadeTo(180, opacity);
    if(!opacity) overlay.hide();
}

function createInfoTable(json_data, max_transportation_value) {
    var color = 0;
    var append_str = '';
    var table = $('table');
    $.tablesorter.clearTableBody = function (table) {
                $('tbody', table).empty();
    };
    $.tablesorter.clearTableBody(table[0]);
    $.each(json_data['edges'], function (key,value) {
        color = getColor(value[2], max_transportation_value);
        append_str += "<tr><td style='background-color:" + d3.color(color) +"'></td>" +
            "<td>"+value[0].split(".")[0]+"</td>" +
            "<td>"+value[3]+"</td>" +
            "<td>"+value[2]+"</td>" +
            "<td>"+value[4]['distance']+"</td>" +
            "<td>"+value[4]['time']+"</td>" +
            "<td>"+value[1].split(".")[0]+"</td></tr>";
    });
    table.append(append_str).trigger('update');
    $(".tablesorter").tablesorter({
        headers: { 0: { sorter: false}},
        theme: 'blue',
        sortList: [[3,0]]
    });
}
/*
Return the max and min X and Y of the department boundaries
Used for department scaling
 */
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
    var max_values = [max_x, max_y];
    return max_values
}


/*
Takes all transportation records from json and sort it
Need for color legend drawing
return: sorted array of transportation records numbers
 */
function getSortedTransportationRecords(json_data) {
    var arr = [];
    $.each(json_data['edges'], function (key, value) {
        arr.push(value[2])
    });
    return arr.sort(function (a,b) {return a-b})
}

/*
As input takes integer array of transportation records numbers
Draw the color legend
 */
function draw_color_legend(arr){
    var max_transportation_value  = Math.max.apply(Math, arr);
    console.log(max_transportation_value);
    for(var i=0; i<arr.length;i++){
        var hsv = getColor(arr[i], max_transportation_value);
        var item = "<li style='background-color:" + getColor(arr[i], max_transportation_value) + "'></li>";
        $("#ul_color_map").append(item);
     //   d3.select("#ul_color_map").append(item);
    }
}
function scalePoints(json_data, key, xLinearScale, yLinearScale){
    var points = [];
    $.each(json_data['facility'][key]['boundaries'], function (key, value) {
        var scaled_x_y = [xLinearScale(value[0]),yLinearScale(value[1])];
        points.push(scaled_x_y);
    });
    return points
}

function getMaxAndMinTransportationNumbers(json_data) {
    var max_transportation_number = 0;
    var min_transportation_number = 1000000;
    $.each(json_data['edges'], function (key, value) {
        var number = value[2];
        if (number > max_transportation_number) {
            max_transportation_number = number;
        }
        if (number < min_transportation_number){
            min_transportation_number = number;
        }
        });
    return [max_transportation_number, min_transportation_number]
}

function generateLineColor(number, max_transportation_number) {
    var scale_number = ((max_transportation_number-number)/max_transportation_number);
    if (scale_number < 50) {
        var r = Math.floor(255 * (scale_number/ 50));
        var g = 255;
    } else {
        var r = 255;
        var g = Math.floor((255 * ((50 - scale_number % 50) / 50)))
    }
    return [r,g,0]
}

function getColor(value, max_transportation_number){
    console.log(max_transportation_number);
    var hue = Math.floor((max_transportation_number - value) * 120 / max_transportation_number).toString(10)
    var saturation = Math.abs(value - 75)/20;
    return ["hsl(",hue,","+saturation+"%,70%)"].join("");
}

function createGraph(json_data, transportation_ranges) {
    var height = document.getElementById("factory_transp_container").offsetHeight;
    var width = document.getElementById("factory_transp_container").offsetWidth;
    var max_x_y = findMaxXandY(json_data)
    var xLinearScale = d3.scaleLinear()
        .domain([0, max_x_y[0]])
        .range([(1-SCALE)*width,width*SCALE]);

    var yLinearScale = d3.scaleLinear()
        .domain([0,max_x_y[1]])
        .range([(1-SCALE)*height,height*SCALE]);

    var zoom = d3.zoom()
        .scaleExtent([1,10])
        .translateExtent([[0, 0], [width, height]])
        .on("zoom", zoomed);

    function zoomed() {
        d3.select('#factory_transp_container').select("svg")
            .attr('transform', d3.event.transform);
    }

    var svgContainer = d3.select("#factory_transp_container")
        .append("svg")
        .attr('height',height)
        .attr('width', width)
        .call(zoom);

    d3.select("#reset")
        .on("click", resetted);

    d3.select("#zoom_in")
        .on("click", zoom_in);

    d3.select("#zoom_out")
        .on("click", zoom_out);

    function resetted() {
        svgContainer.transition()
            .duration(750)
            .call(zoom.transform, d3.zoomIdentity);
    }

    function zoom_in(){
        svgContainer.call(zoom.scaleBy(svgContainer, 1.5));
    }

    function zoom_out() {
        svgContainer.call(zoom.scaleBy(svgContainer, 0.66));

    }

    $.each(json_data['facility'],function (key, value) {
                svgContainer.append('polygon')
                    .style("stroke-width", 5)
                    .attr("points", scalePoints(json_data,key, xLinearScale, yLinearScale))
                    .attr("stroke", '#444444')
                    .style("pointer-events", "all")
                    .attr("fill", '#dbe9ee')
    });
    $.each(json_data['edges'], function(key, value){
        var src = value[0].split(".")[0];
        var dest = value[1].split(".")[0];
        var trtime = value[4]['time'];
        var distance = value[4]['distance'];
        var times = value[3];
        var color2 = getColor(value[2],transportation_ranges[0]);
        svgContainer.append("line")
            .style("stroke", d3.color(color2))
            .style("stroke-width", 3)
            .attr("value", value[2])
            .attr("x1", xLinearScale(json_data['facility'][value[0].split('.')[0]]['points']['centroid'][0]))
            .attr("y1", yLinearScale(json_data['facility'][value[0].split('.')[0]]['points']['centroid'][1]))
            .attr("x2", xLinearScale(json_data['facility'][value[1].split('.')[0]]['points']['centroid'][0]))
            .attr("y2", yLinearScale(json_data['facility'][value[1].split('.')[0]]['points']['centroid'][1]))
            .on("mouseover", function (d) {
                var value = d3.select(this).attr("value");
                d3.select('.viz_info_text')
                    .style("font-style", "normal")
                    .text(src+" - "+dest+": Quantity: "+value+", Times: "+times+", Distance: "+distance+"m , Transportation Time: "+trtime+" min")

            })
            .on("mouseout", function (d) {
                    d3.select('.viz_info_text')
                        .style("font-style","italic")
                        .text('no additional info to display');
                });


    });
    $.each(json_data['facility'],function (key, value) {
        svgContainer.append('circle')
            .attr("cx", xLinearScale(value['points']['centroid'][0]))
            .attr("cy", yLinearScale(value['points']['centroid'][1]))
            .attr('r', 5)
            .attr("fill", "#444444")
        svgContainer.append('text')
            .style("fill", "#444444")
            .attr("x", xLinearScale(value['points']['centroid'][0]))
            .attr("y", yLinearScale(value['points']['centroid'][1]))
            .attr("font-size", "15px")
            .attr("dy", "-.85em")
            .attr("font-family", "Lato")
            .attr("text-anchor", "middle")
            .text(key)
    });
};