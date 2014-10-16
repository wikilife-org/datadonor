
function drawStepsGraph(data) {
    var maxValue = 0;
    for (var i in data.days) {
        if (data.days[i] > maxValue) maxValue = data.days[i];
    }
    var adapter = new StepsAdapter();
    var result = adapter.getParameters(data, 380, maxValue);

    elements = result.elements;
    $(elements).each(function (index, elem) {
        elem.value = Math.max(0.02 * 423, elem.value);
    });

    var r_6_1 = Raphael('canvas_6_1', 1093, 423);
    doubleAxisParams2 = {
        axis: 'both',
        barsAxis: 'x',
        drawAxis: true,
        drawLabels: true,
        elements: elements,
        rotateBarLabels: true,
        xAxis: {
            length: 1093,
            'stroke-width': 2,
            color: '#F1F2F2',
            labelsType: 'custom_bubbles',
            name: 'Day',
            labels: result.xLabels
        },
        yAxis: {
            length: 423,
            'stroke-width': 0,
            name: 'Steps',
            labels: result.yLabels
        },
        centerx: 30,
        centery: 400,
        canvasSize: [
            1093,
            425
        ]
    }
    doubleAxisBars2 = new EdBarChart(r_6_1, doubleAxisParams2);
    doubleAxisBars2.draw();
    $('#data_6_1 .bloq.left .number_stat h2') .html(data.avg);
}