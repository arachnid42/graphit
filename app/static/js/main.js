$( document ).ready(function() {
    $.getJSON($SCRIPT_ROOT+"/get_data", function (data) {
        console.log("Success");
        var transportations_min_max = getMaxAndMinTransportationNumbers(data);
        createGraph(data, transportations_min_max)
        createInfoTable(data, getMaxAndMinTransportationNumbers(data)[0]);

        $("#e3").daterangepicker({
             datepickerOptions : {
             numberOfMonths : 3,
                // minDate: '-2M',
                // maxDate: '+28D',
         }.onClick(console.log("Test"))
     });
    });
});

var scale = 0.945;

/*
<tr>
    <td style="background-color: green"></td>
    <td>TLO</td>
    <td>32</td>
    <td>123421</td>
    <td>INS</td>
</tr>
*/


function createInfoTable(json_data, max_transportation_value) {
    var color = 0;
    $.each(json_data['edges'], function (key,value) {
        color = getColor(value[2], max_transportation_value);
        $("#info_table").append("<tr><td style='background-color:" + color +"'></td>" +
            "<td>"+value[0].split(".")[0]+"</td>" +
            "<td>"+value[3]+"</td>" +
            "<td>"+value[2]+"</td>" +
            "<td>"+value[1].split(".")[0]+"</td></tr>")
    });
    $(".tablesorter").tablesorter({
        headers: { 0: { sorter: false}},
        sortList: [[3,0]]
    })

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
    //console.log(value);
    //console.log(max_transportation_number);
    var hue = Math.floor((max_transportation_number - value) * 120 / max_transportation_number).toString(10)
    var saturation = Math.abs(value - 50)/50;
    return ["hsl(",hue,","+saturation+"%,70%)"].join("");
}

function createGraph(json_data, transportation_ranges) {
    var height = document.getElementById("factory_transp_container").offsetHeight;
    var width = document.getElementById("factory_transp_container").offsetWidth;
    var max_x_y = findMaxXandY(json_data)
    var xLinearScale = d3.scaleLinear()
        .domain([0, max_x_y[0]])
        .range([(1-scale)*width,width*scale]);

    var yLinearScale = d3.scaleLinear()
        .domain([0,max_x_y[1]])
        .range([(1-scale)*height,height*scale]);

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
        svgContainer.transition()
            .duration(10000)
            .call(zoom.scaleBy(svgContainer, 1.5));
    }

    function zoom_out() {
        svgContainer.transition()
            .duration(10000)
            .call(zoom.scaleBy(svgContainer, 0.66), d3.zoomIdenti);
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
        var times = value[3];
        var color2 = getColor(value[2],transportation_ranges[0]);
        svgContainer.append("line")
            .style("stroke", d3.color(color2))
            .style("stroke-width", 5)
            .attr("value", value[2])
            .attr("x1", xLinearScale(json_data['facility'][value[0].split('.')[0]]['points']['centroid'][0]))
            .attr("y1", yLinearScale(json_data['facility'][value[0].split('.')[0]]['points']['centroid'][1]))
            .attr("x2", xLinearScale(json_data['facility'][value[1].split('.')[0]]['points']['centroid'][0]))
            .attr("y2", yLinearScale(json_data['facility'][value[1].split('.')[0]]['points']['centroid'][1]))
            .on("mouseover", function (d) {
                var value = d3.select(this).attr("value");
                d3.select('.viz_info_text')
                    .style("font-style", "normal")
                    .text(src+"\t - \t"+dest+"Quantity:"+value+",Times:"+times)
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
    })
  //  var arr = getSortedTransportationRecords(json_data);
  //  draw_color_legend(arr)
};