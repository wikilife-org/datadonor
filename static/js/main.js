var pieChart;
var animatedPie;
var doubleAxisBars;
var animatedQuarterPie;
var doubleAxisParams;
var SingleBarChart;
var cronicalGraphs = {
};
var emotionGraphs = {
};
var cronicalsList = {
};
var complainsTop5 = {
};
var complainsList = {
};
var emotionsList = {
};
var addedComplains = [
];
//_api_env = 'hard';
_api_env = 'prod';
function workCallback(args) {
    //$('#age_input li a[data-key=15-25]');
    //console.log(args);
    $('#age_input li a[data-key=' + args[0] + ']') .click();
}
var sortObjectByKey = function (obj) {
    var keys = [
    ];
    var sorted_obj = {
    };
    for (var key in obj) {
        if (obj.hasOwnProperty(key)) {
            keys.push(key);
        }
    }
    // sort keys

    keys.sort();
    // create new array based on Sorted Keys
    jQuery.each(keys, function (i, key) {
        sorted_obj[key] = obj[key];
    });
    return sorted_obj;
};
function drawSocialGraph(json) {
    //console.log(json);
    var global_data = json.global_data;
    $('.block.twitter ul li span.global_data') .html(pad(global_data.twitter.count, 2));
    $('.block.facebook ul li span.global_data') .html(pad(global_data.facebook.count, 2));
    $('.block.google_plus ul li span.global_data') .html(pad(global_data.gmail.count, 2));
    $('.block.linkedin ul li span.global_data') .html(pad(global_data.linkedin.count, 2));
    $('.block.foursquare ul li span.global_data') .html(pad(global_data.foursquare.count, 2));
    var user_data = json.user_data;
    $('.block.twitter ul li span.user_data') .html(pad(user_data.twitter.count, 2));
    $('.block.facebook ul li span.user_data') .html(pad(user_data.facebook.count, 2));
    $('.block.google_plus ul li span.user_data') .html(pad(user_data.gmail.count, 2));
    $('.block.linkedin ul li span.user_data') .html(pad(user_data.linkedin.count, 2));
    $('.block.foursquare ul li span.user_data') .html(pad(user_data.foursquare.count, 2));
}
function drawShareGraphs(data) {
    var adapter = new SocialShareAdapter();
    var graphConfig = {
        centerx: 105,
        centery: 101,
        useAnimationDelay: true,
        animationTime: 900,
        easing: 'bounce',
        fontSize: '40',
        drawLabels: false,
        perimeter: {
            display: false,
            radius: 100,
            color: '#ECEDED'
        }
    };
    var maxPercentage = 80;
    var elements1 = adapter.getParameters(
        [
            data.global_data.facebook.posts,
            data.user_data.facebook.posts
        ],
        maxPercentage,
        100
    );

    var r_2_1 = Raphael('canvas_2_1', 210, 210);
    if (maxPercentage < 100) graphConfig.perimeter.display = true;
    $('#data_2_1 .global_data') .html(pad(data.global_data.facebook.posts, 2));
    $('#data_2_1 .user_data') .html(pad(data.user_data.facebook.posts, 2));
    dotChart = new EdDotChart(r_2_1, elements1, graphConfig);
    dotChart.draw();
    var maxPercentage = 100;
    var elements1 = adapter.getParameters(
        [
            data.global_data.twitter.tweets,
            data.user_data.twitter.tweets
        ],
        maxPercentage,
        100
    );

    var r_2_2 = Raphael('canvas_2_2', 210, 210);
    if (maxPercentage < 100) graphConfig.perimeter.display = true;
    $('#data_2_2 .global_data') .html(pad(data.global_data.twitter.tweets, 2));
    $('#data_2_2 .user_data') .html(pad(data.user_data.twitter.tweets, 2));
    dotChart2 = new EdDotChart(r_2_2, elements1, graphConfig);
    dotChart2.draw();
    var maxPercentage = 100;
    var elements1 = adapter.getParameters([data.global_data.facebook.likes,
    data.user_data.facebook.likes], maxPercentage, 100);

    var r_2_3 = Raphael('canvas_2_3', 210, 210);
    if (maxPercentage < 100) graphConfig.perimeter.display = true;
    $('#data_2_3 .global_data') .html(pad(data.global_data.facebook.likes, 2));
    $('#data_2_3 .user_data') .html(pad(data.user_data.facebook.likes, 2));
    dotChart3 = new EdDotChart(r_2_3, elements1, graphConfig);
    dotChart3.draw();
    var maxPercentage = 100;
    var elements1 = adapter.getParameters([data.global_data.twitter.retweets,
    data.user_data.twitter.retweets], maxPercentage, 100);
    var r_2_4 = Raphael('canvas_2_4', 210, 210);
    if (maxPercentage < 100) graphConfig.perimeter.display = true;
    $('#data_2_4 .global_data') .html(pad(data.global_data.twitter.retweets, 2));
    $('#data_2_4 .user_data') .html(pad(data.user_data.twitter.retweets, 2));
    dotChart4 = new EdDotChart(r_2_4, elements1, graphConfig);
    dotChart4.draw();
}
function drawEducationGraph(data) {
    var adapter = new EducationAdapter();
    var elements = adapter.getParameters(data);
    //console.log('QUARTER PIE ADAPTER');
    //console.log(elements);
    var r_3_1 = Raphael('canvas_3_1', 435, 428);
    animatedQuarterPie = new EdQuarterAnimatedPie(r_3_1, elements, {
        animationTime: 900,
        easing: '<',
        useAnimationDelay: false,
        lineWidth: 45,
        fontSize: 20,
        centerx: 435,
        centery: 430,
        radius: 400,
        drawReferences: false
    });
    animatedQuarterPie.draw();
    for (var i in elements) {
        $('li[ref=' + i + '] span.perc_number') .html(Math.round(elements[i].percentage));
        $('li[ref=' + i + '] a span') .html(elements[i].text);
        if (elements[i].selected) {
            $('li[ref=' + i + ']') .addClass('active');
            $('.hat_bottom') .addClass('red');
        }
    }
}
function drawWorkGraph(data) {
    //console.log('PRE PARAMS WORK');
    data.global_data = sortObjectByKey(data.global_data);
    var maxValue = 0;
    for (var i in data.global_data) {
        if (data.global_data[i].value > maxValue) maxValue = data.global_data[i].value;
    }
    if (data.user_data.user_experience.value > maxValue) maxValue = data.user_data.user_experience.value;
    var adapter = new WorkAdapter();
    var result = adapter.getParameters(data, 423, maxValue + 10, workCallback);
    //console.log('POST PARAMS WORK');
    var r_4_1 = Raphael('canvas_4_1', 1093, 423);
    doubleAxisParams = {
        axis: 'both',
        barsAxis: 'x',
        drawAxis: true,
        drawLabels: true,
        elements: result.elements,
        xAxis: {
            length: 1093,
            'stroke-width': 2,
            color: '#F1F2F2',
            labels: [
            ]
        },
        yAxis: {
            length: 423,
            'stroke-width': 0,
            name: 'years',
            labels: result.yLabels
        },
        centerx: 30,
        centery: 400,
        canvasSize: [
            1093,
            425
        ]
    }
    $('#data_1_4 .left .number_stat h2') .html(pad(data.avg, 2));
    $('#data_1_4 .right .number_stat h2') .html(pad(data.user_data.user_experience.value, 2));
    doubleAxisBars = new EdBarChart(r_4_1, doubleAxisParams);
    doubleAxisBars.draw();
}
function drawExerciseGraphs(data) {
    var adapter = new SocialShareAdapter();
    var graphConfig = {
        centerx: 105,
        centery: 101,
        useAnimationDelay: true,
        animationTime: 900,
        easing: 'bounce',
        fontSize: '40',
        drawLabels: false,
        perimeter: {
            display: true,
            radius: 100,
            color: '#B3B3B3'
        }
    };
    var maxPercentage = 100;
    var elements1 = adapter.getParameters([parseInt(data[0].global_times),
    parseInt(data[0].user_times)], maxPercentage, 100);
    var r_5_1 = Raphael('canvas_5_1', 210, 210);
    if (maxPercentage < 100) graphConfig.perimeter.display = true;
    $('#data_5_1 .global_data') .html(pad(data[0].global_times, 2));
    $('#data_5_1 .user_data') .html(pad(data[0].user_times, 2));
    var dotChart = new EdDotChart(r_5_1, elements1, graphConfig);
    dotChart.draw();
    var maxPercentage = 100;
    var elements1 = adapter.getParameters([parseInt(data[1].global_times),
    parseInt(data[1].user_times)], maxPercentage, 100);
    var r_5_2 = Raphael('canvas_5_2', 210, 210);
    if (maxPercentage < 100) graphConfig.perimeter.display = true;
    $('#data_5_2 .global_data') .html(pad(data[1].global_times, 2));
    $('#data_5_2 .user_data') .html(pad(data[1].user_times, 2));
    var dotChart = new EdDotChart(r_5_2, elements1, graphConfig);
    dotChart.draw();
    var maxPercentage = 100;
    var elements1 = adapter.getParameters([parseInt(data[2].global_times),
    parseInt(data[2].user_times)], maxPercentage, 100);
    var r_5_3 = Raphael('canvas_5_3', 210, 210);
    if (maxPercentage < 100) graphConfig.perimeter.display = true;
    $('#data_5_3 .global_data') .html(pad(data[2].global_times, 2));
    $('#data_5_3 .user_data') .html(pad(data[2].user_times, 2));
    var dotChart = new EdDotChart(r_5_3, elements1, graphConfig);
    dotChart.draw();
}
function drawStepsGraph(data) {
    var maxValue = 0;
    for (var i in data.days) {
        if (data.days[i].global_steps > maxValue) maxValue = data.days[i].global_steps;
        if (data.days[i].user_steps > maxValue) maxValue = data.days[i].user_steps;
    }
    var adapter = new StepsAdapter();
    var result = adapter.getParameters(data, 380, maxValue);
    var r_6_1 = Raphael('canvas_6_1', 1093, 423);
    doubleAxisParams2 = {
        axis: 'both',
        barsAxis: 'x',
        drawAxis: true,
        drawLabels: true,
        elements: result.elements,
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
    $('#data_6_1 .bloq.right .number_stat h2') .html(pad(data.user_avg_steps, 2));
    $('#data_6_1 .bloq.left .number_stat h2') .html(pad(data.global_avg_steps, 2));
}
function drawMilesGraph(data) {
    var maxValue = 0;
    for (var i in data.days) {
        if (data.days[i].global_miles > maxValue) maxValue = data.days[i].global_miles;
        if (data.days[i].user_miles > maxValue) maxValue = data.days[i].user_miles;
    }
    var adapter = new MilesAdapter();
    var result = adapter.getParameters(data, 350, maxValue, [
        10,
        30,
        50,
        70
    ]);
    var r_7_1 = Raphael('canvas_7_1', 530, 400);
    doubleAxisParams3 = {
        axis: 'both',
        barsAxis: 'x',
        drawAxis: true,
        drawLabels: true,
        elements: result.elements,
        xAxis: {
            length: 1093,
            'stroke-width': 2,
            color: '#E6E2DF',
            labelsType: 'custom_bubbles',
            labels: result.xLabels
        },
        yAxis: {
            length: 423,
            'stroke-width': 0,
            name: 'miles',
            labels: result.yLabels
        },
        centerx: 10,
        centery: 370,
        canvasSize: [
            530,
            400
        ]
    }
    doubleAxisBars3 = new EdBarChart(r_7_1, doubleAxisParams3);
    doubleAxisBars3.draw();
    $('#data_7_1 .left .number_stat h2') .html(pad(data.global_avg_miles));
    $('#data_7_1 .right .number_stat h2') .html(pad(data.user_avg_miles));
}
function drawHoursGraph(data) {
    var maxValue = 0;
    for (var i in data.days) {
        if (data.days[i].global_hours > maxValue) maxValue = data.days[i].global_hours;
        if (data.days[i].user_hours > maxValue) maxValue = data.days[i].user_hours;
    }
    var adapter = new HoursAdapter();
    var result = adapter.getParameters(data, 340, maxValue, [
        1,
        3,
        5,
        7
    ]);
    var r_7_2 = Raphael('canvas_7_2', 530, 400);
    doubleAxisParams4 = {
        axis: 'both',
        barsAxis: 'x',
        drawAxis: true,
        drawLabels: true,
        elements: result.elements,
        xAxis: {
            length: 1093,
            'stroke-width': 2,
            color: '#E6E2DF',
            labelsType: 'custom_bubbles',
            labels: result.xLabels
        },
        yAxis: {
            length: 423,
            'stroke-width': 0,
            name: 'h',
            labels: result.yLabels
        },
        centerx: 10,
        centery: 370,
        canvasSize: [
            530,
            400
        ]
    }
    doubleAxisBars4 = new EdBarChart(r_7_2, doubleAxisParams4);
    doubleAxisBars4.draw();
    $('#data_7_2 .left .number_stat h2') .html(pad(data.global_avg_hours, 2));
    $('#data_7_2 .right .number_stat h2') .html(pad(data.user_avg_hours, 2));
}
function drawNutrientProportionGraph(data) {
    var global_colors = [
        '#B48AEA',
        '#8A45E5',
        '#7737C7',
        '#3E3EA5'
    ];
    var user_colors = [
        '#FF9C8C',
        '#FF836F',
        '#E56666',
        '#D44B5F'
    ];
    data_keys = Object.keys(data.user_data);
    for (i = 0; i < data_keys.length; i++) {
        var user_percent = data.user_data[data_keys[i]].percentage;
        var global_percent = data.global_data[data_keys[i]].percentage;
        var userColor = user_colors[i];
        var globalColor = global_colors[i];
        var userWidth = (user_percent * 620) / 100;
        var globalWidth = (global_percent * 620) / 100;

        var content = $('#nutrient_template_data') .html();
        content = content.replace(/\[\[name\]\]/g, data.user_data[data_keys[i]].title);
        content = content.replace(/\[\[user_perc\]\]/g, user_percent);
        content = content.replace(/\[\[global_perc\]\]/g, global_percent);
        content = content.replace(/\[\[user_data_style\]\]/g, 'width:' + userWidth + 'px; background-color:' + userColor + ';');
        content = content.replace(/\[\[global_data_style\]\]/g, 'width:' + globalWidth + 'px; background-color:' + globalColor + ';');
        content = content.replace(/\[\[user_text_style\]\]/g, 'color:' + userColor + ';');
        content = content.replace(/\[\[global_text_style\]\]/g, 'color:' + globalColor + ';');

        $('.nutrient_data .block.right') .append(content);
    }
}

function doCronicalConditionsSection() {
    $.getJSON(_api_urls[_api_env].cronical_conditions_user, function (user_data) {
        $.getJSON(_api_urls[_api_env].cronical_conditions_top5, function (data) {
            for (var i in data) {
                var num = parseInt(i) + 1;
                drawCronicalConditionsGraph(data[i], num, user_data);
            }
        });
    });
}

function drawCronicalConditionsGraph(data, num, user_data) {
    var adapter = new CronicalConditionsAdapter();
    var params = adapter.getParameters(data, '#7737c7');
    var np = num - 1;
    var preffix = 'canvas_11_';
    animatedPie = drawVariableCircle(params, num, preffix);
    cronicalGraphs[data.id] = animatedPie;
    var selectedGraphs = [
    ];
    for (var i in user_data) {
        //console.log('user cronical? '+data.id+' = '+user_data[i].id_condition);
        if (data.id == user_data[i].id_condition) {
            var result = [
                animatedPie,
                data,
                user_data[i]
            ]
            selectedGraphs.push(result);
        }
        if ($('#cronical_id_' + user_data[i].id_condition) .length == 0) {
            var type_name = '';
            if (typeof user_data[i].type_name != 'undefined') {
                type_name = user_data[i].type_name;
            }
            addCronicalCard(user_data[i].name, type_name, user_data[i].id_condition);
        }
    }
    setTimeout(function () {
        for (var i in selectedGraphs) {
            var graph = selectedGraphs[i][0];
            var data = selectedGraphs[i][1];
            var user_data = selectedGraphs[i][2];
            //console.log('COLORING USER EMOTION!');
            //console.log(user_data);
            graph.lines[0].animate({
                'stroke': '#E56666'
            }, 500);
            graph.texts[0].animate({
                'fill': '#E56666'
            }, 500);
            graph.texts[1].animate({
                'fill': '#E56666'
            }, 500);
            //$(this).addClass('sent');
        }
    }, 1000);
    //Setup info
    $($('.cronical_container') [np]) .find('.face.front .bubble_msj h2') .html(data.name);
    $($('.cronical_container') [np]) .find('.face.back .container_data h2') .html(data.name);
    var cronicalTypes = '';
    if (data.types.length) {
        for (var i in data.types) {
            cronicalTypes += '<option value="' + data.types[i].id + '">' + data.types[i].name + '</option>';
        }
        $($('.cronical_container') [np]) .click(function (event) {
            event.preventDefault();
            $('#graphs_conditions .condition') .removeClass('active');
            $(this) .addClass('active');
            doCronicalConditionsSection();
        });
        $($('.cronical_container') [np]) .find('.done_condition') .on('click', {
            id_condition: data.id,
            container: $($('.cronical_container') [np]),
            graph: animatedPie,
            json: data
        }, function (event) {
            if (!$(this) .hasClass('sent')) {
                var el = $(this);
                var typeId = event.data.container.find('.face.back select.select_stats') .val();
                var typeText = event.data.container.find('.face.back select.select_stats option:selected') .text();
                //console.log('TYPE ID: '+typeId);
                $.post(_api_urls[_api_env].cronical_conditions_post, {
                    id_condition: event.data.id_condition,
                    id_type: typeId
                });
                addCronicalCard(event.data.json.name, typeText, event.data.id_condition);
                setTimeout(function () {
                    el.parent() .parent() .parent() .parent() .removeClass('active');
                    //console.log(el.parent().parent().parent().parent());
                }, 50);
                //Change color
                event.data.graph.lines[0].animate({
                    'stroke': '#E56666'
                }, 500);
                event.data.graph.texts[0].animate({
                    'fill': '#E56666'
                }, 500);
                event.data.graph.texts[1].animate({
                    'fill': '#E56666'
                }, 500);
                $(this) .addClass('sent');
            }
        });
    } else {
        $($('.cronical_container') [np]) .click({
            id_condition: data.id,
            graph: animatedPie,
            json: data
        }, function (event) {
            event.preventDefault
            //if(!$(this).hasClass('sent')){
            if ($('#cronical_id_' + event.data.id_condition) .length == 0) {
                //Send data... change color
                $.post(_api_urls[_api_env].cronical_conditions_post, {
                    id_condition: event.data.id_condition
                });
                addCronicalCard(event.data.json.name, '', event.data.id_condition);
                event.data.graph.lines[0].animate({
                    'stroke': '#E56666'
                }, 500);
                event.data.graph.texts[0].animate({
                    'fill': '#E56666'
                }, 500);
                event.data.graph.texts[1].animate({
                    'fill': '#E56666'
                }, 500);
                //$(this).addClass('sent');
            }
        });
    }
    $($('.cronical_container') [np]) .find('.face.back .select_stats') .html(cronicalTypes);
    $($('.cronical_container') [np]) .find('.face.back .select_stats') .combobox();
}
function drawEmotionsGraph(data, num, user_data) {
    var adapter = new CronicalConditionsAdapter();
    var params = adapter.getParameters(data, '#7737c7');
    var np = num - 1;
    var preffix = 'canvas_15_';
    animatedPie = drawVariableCircle(params, num, preffix);
    //cronicalGraphs[data.id] = animatedPie;
    emotionGraphs[data.id] = animatedPie;
    var selectedGraphs = [
    ];
    for (var i in user_data) {
        //console.log('user emotion? '+data.id+' = '+user_data[i].id_emotion);
        if (data.id == user_data[i].id_emotion) {
            var result = [
                animatedPie,
                data
            ]
            selectedGraphs.push(result);
        }
    }
    setTimeout(function () {
        for (var i in selectedGraphs) {
            var graph = selectedGraphs[i][0];
            var data = selectedGraphs[i][1];
            //console.log('COLORING USER EMOTION!');
            graph.lines[0].animate({
                'stroke': '#E56666'
            }, 500);
            graph.texts[0].animate({
                'fill': '#E56666'
            }, 500);
            graph.texts[1].animate({
                'fill': '#E56666'
            }, 500);
            //$(this).addClass('sent');
            addEmotionCard(data.name, '', data.id);
        }
    }, 1000);
    //Setup info
    $($('.emotion_container') [np]) .find('.face.front .bubble_msj h2') .html(data.name);
    $($('.emotion_container') [np]) .find('.face.back .container_data h2') .html(data.name);
    var cronicalTypes = '';
    $($('.emotion_container') [np]) .click({
        id_emotion: data.id,
        graph: animatedPie,
        json: data
    }, function (event) {
        event.preventDefault
        if (!$(this) .hasClass('sent')) {
            //Send data... change color
            $.post(_api_urls[_api_env].emotions_post, {
                id_emotion: event.data.id_emotion
            });
            addEmotionCard(event.data.json.name, '', event.data.id_emotion);
            event.data.graph.lines[0].animate({
                'stroke': '#E56666'
            }, 500);
            event.data.graph.texts[0].animate({
                'fill': '#E56666'
            }, 500);
            event.data.graph.texts[1].animate({
                'fill': '#E56666'
            }, 500);
            $(this) .addClass('sent');
        }
    });
    $($('.emotion_container') [np]) .find('.face.back .select_stats') .html(cronicalTypes);
    $($('.emotion_container') [np]) .find('.face.back .select_stats') .combobox();
}
function drawVariableCircle(params, num, preffix) {
    var r = Raphael(preffix + num, 310, 310);
    var animatedPie = new EdAnimatedPie(r, params, {
        animationTime: 900,
        easing: '<',
        useAnimationDelay: false,
        lineWidth: 55,
        fontSize: 20,
        centerx: 155,
        centery: 155,
        radius: 122,
        borderColor: '#F7F2ED',
        borderMargin: 0,
        drawReferences: false,
        drawCenterImage: false,
        drawCenterText: true,
        bubbleColor: '#3F4B5B',
        centerText: {
            color: '#7737c7',
            size: '60',
            font: 'Omnes-Semibold',
            text: Math.round(params[0].percentage),
            xOffset: [
                0,
                0
            ],
            unit: '%',
            unitFont: 'Omnes-Semibold',
            unitSize: 30,
            unitOffset: [
                45,
                30
            ],
            unitOffsetTop: 5
        }
    });
    animatedPie.draw();
    return animatedPie;
}
function pad(num, size) {
    var s = num + '';
    while (s.length < size) s = '0' + s;
    return s;
}
function setupAddCronicals(data) {
    //console.log('setupAddCronicals');
    var cronicals = '';
    for (var i in data) {
        cronicals += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
    }
    $('.select_stats.add_more_1') .html(cronicals);
    $('.select_stats.add_more_1') .combobox();
    $('#graphs_conditions .condition.add_more') .click(function (event) {
        event.preventDefault
        $('#graphs_conditions .condition') .removeClass('active');
        $(this) .addClass('active');
    });
    $('#graphs_conditions .done_condition') .on('click', {
        cronicalsList: cronicalsList
    }, function (event) {
        event.preventDefault();
        if ($(this) .hasClass('next_subsector')) {
            //console.log('ENTRA EN EL 1ER IF');
            $(this) .removeClass('next_subsector');
            $(this) .parent() .parent() .find('.graph_container') .addClass('second_active');
            //Completo el 2do combobox y lo inicializo
            var currentCronical = $('.select_stats.add_more_1') .val();
            var currentCronicalName = $('.select_stats.add_more_1 option:selected') .text();
            var cronicalTypes = '';
            $('#graphs_conditions .second_condition h2') .html(currentCronicalName);
            //console.log(cronicalsList);
            for (var i in cronicalsList) {
                if (cronicalsList[i].id == currentCronical) {
                    if (cronicalsList[i].types.length != 0) {
                        $('.select_stats.add_more_2') .parent() .parent() .show();
                        for (var j in cronicalsList[i].types) {
                            var cronicalEl = cronicalsList[i];
                            cronicalTypes += '<option value="' + cronicalEl.types[j].id + '">' + cronicalEl.types[j].name + '</option>';
                        }
                    } else {
                        $('.select_stats.add_more_2') .parent() .parent() .hide();
                    }
                    $('.select_stats.add_more_2') .html(cronicalTypes);
                    $('.select_stats.add_more_2') .combobox();
                }
            }
            $(this) .find('span') .hide() .html('Done!') .fadeIn(300);
        } else if ($(this) .parent() .parent() .find('.graph_container') .hasClass('second_active')) {
            //console.log('ENTRA EN EL 2DO IF');
            //Envio los datos por POST y agrego la CARD
            $.post(_api_urls[_api_env].cronical_conditions_post, {
                id_condition: $('.select_stats.add_more_1') .val(),
                id_type: $('.select_stats.add_more_2') .val()
            });
            addCronicalCard($('.select_stats.add_more_1 option:selected') .text(), $('.select_stats.add_more_2 option:selected') .text(), $('.select_stats.add_more_1') .val());
            setTimeout(function () {
                try {
                    $('.select_stats.add_more_2') .combobox('destroy');
                } catch (err) {
                    //Do nothing...
                }
            }, 300);
            $(this) .addClass('next_subsector');
            $('#graphs_conditions .condition') .removeClass('active');
            $('.graph_container') .removeClass('second_active');
            $(this) .find('span') .hide() .html('Next') .fadeIn(300);
        } else {
            console.log('ENTRA EN EL ELSE');
            //Nunca entra aca...
            $('#graphs_conditions .condition') .removeClass('active');
            $(this) .find('span') .hide() .html('Next') .fadeIn(300);
        }
    });
}
function setupAddEmotions(data) {
    //console.log('setupAddEmotions');
    var cronicals = '';
    for (var i in data) {
        cronicals += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
    }
    $('.select_stats.add_more_emo_1') .html(cronicals);
    $('.select_stats.add_more_emo_1') .combobox();
    $('#graphs_emotions .condition.add_more') .click(function (event) {
        event.preventDefault
        $('#graphs_emotions .condition') .removeClass('active');
        $(this) .addClass('active');
    });
    $('#graphs_emotions .done_condition') .on('click', {
        cronicalsList: emotionsList
    }, function (event) {
        event.preventDefault();
        if ($(this) .hasClass('next_subsector')) {
            //console.log('ENTRA EN EL 1ER IF');
            $(this) .removeClass('next_subsector');
            $(this) .parent() .parent() .find('.graph_container') .addClass('second_active');
            //Completo el 2do combobox y lo inicializo
            var currentCronical = $('.select_stats.add_more_emo_1') .val();
            var currentCronicalName = $('.select_stats.add_more_emo_1 option:selected') .text();
            var cronicalTypes = '';
            $('#graphs_emotions .second_condition h2') .html(currentCronicalName);
            //console.log(emotionsList);
            for (var i in emotionsList) {
                if (emotionsList[i].id == currentCronical) {
                    $('.select_stats.add_more_emo_2') .parent() .parent() .hide();
                    $('.select_stats.add_more_emo_2') .html(cronicalTypes);
                    $('.select_stats.add_more_emo_2') .combobox();
                }
            }
            $(this) .find('span') .hide() .html('Done!') .fadeIn(300);
        } else if ($(this) .parent() .parent() .find('.graph_container') .hasClass('second_active')) {
            //console.log('ENTRA EN EL 2DO IF');
            //Envio los datos por POST y agrego la CARD
            $.post(_api_urls[_api_env].emotions_post, {
                id_emotion: $('.select_stats.add_more_emo_1') .val()
            });
            addEmotionCard($('.select_stats.add_more_emo_1 option:selected') .text(), $('.select_stats.add_more_emo_2 option:selected') .text(), $('.select_stats.add_more_emo_1') .val());
            setTimeout(function () {
                try {
                    $('.select_stats.add_more_emo_2') .combobox('destroy');
                } catch (err) {
                    //Do nothing...
                }
            }, 300);
            $(this) .addClass('next_subsector');
            $('#graphs_emotions .condition') .removeClass('active');
            $('#graphs_emotions .graph_container') .removeClass('second_active');
            $(this) .find('span') .hide() .html('Next') .fadeIn(300);
        } else {
            //console.log('ENTRA EN EL ELSE'); //Nunca entra aca...
            $('#graphs_emotions .condition') .removeClass('active');
            $(this) .find('span') .hide() .html('Next') .fadeIn(300);
        }
    });
}
function addCronicalCard(label, typeLabel, id) {
    if ($('#cronical_id_' + id) .length == 0) {
        var el = $('.cronical_conditions_cards ul');
        if (typeLabel) {
            el.html(el.html() + '<li id="cronical_id_' + id + '" data-id="' + id + '" data-param="id_condition"><p><span>' + label + '</span><br />Type: ' + typeLabel + '</p><a href="#" class="close_tab close_cronical_card">close</a></li>');
        } else {
            el.html(el.html() + '<li id="cronical_id_' + id + '" data-id="' + id + '" data-param="id_condition"><p><span>' + label + '</span><br /></p><a href="#" class="close_tab close_cronical_card">close</a></li>');
        }
    }
}
function addEmotionCard(label, typeLabel, id) {
    if ($('#emotion_id_' + id) .length == 0) {
        var el = $('.emotion_cards ul');
        el.html(el.html() + '<li id="emotion_id_' + id + '" data-id="' + id + '" data-param="id_emotion"><p><span>' + label + '</span><br /></p><a href="#" class="close_tab close_emotion_card">close</a></li>');
    }
}
function drawComplainsTop5Item(data, num) {
    var adapter = new CronicalConditionsAdapter();
    var params = adapter.getParameters(data, '#7737c7');
    var np = num - 1;
    var preffix = 'canvas_12_';
    var itemHtml = '';
    itemHtml = $('#complains_item_template') .html();
    itemHtml = itemHtml.replace(/\[\[id\]\]/g, data.id);
    itemHtml = itemHtml.replace(/\[\[name\]\]/g, data.name);
    itemHtml = itemHtml.replace(/\[\[perc\]\]/g, Math.round(data.percentage));
    $('#complains_top5') .append(itemHtml);
    //Start graph
    //drawComplainGraph(params, num, preffix);
    drawComplainGraph(params, data.id, preffix);
}
function drawComplainGraph(params, num, preffix) {
    var radius = 43;
    if (params[0].percentage >= 9) radius = 56;
    var raf = Raphael(preffix.toString() + num.toString(), 130, 130);
    //console.log('draw complain params: ');
    //console.log(params);
    var animatedPie = new EdAnimatedPie(raf, params, {
        animationTime: 900,
        easing: '<',
        useAnimationDelay: false,
        lineWidth: 5,
        fontSize: 20,
        centerx: 65,
        centery: 65,
        radius: radius,
        borderColor: '#F2EBE7',
        borderMargin: 0,
        drawReferences: false,
        drawCenterImage: false,
        drawCenterText: true,
        bubbleColor: '#3F4B5B',
        centerText: {
            color: params[0].color,
            size: '52',
            font: 'Omnes-Semibold',
            text: Math.round(params[0].percentage),
            xOffset: [
                - 10,
                - 4
            ],
            unit: '%',
            unitFont: 'Omnes-bold',
            unitSize: 31,
            unitOffset: [
                35,
                25
            ],
            unitOffsetTop: 5
        }
    });
    animatedPie.draw();
}
function createComplainsAutocompleter(data) {
    var complainOptions = '';
    for (var i in data) {
        if (i == 5) break;
        complainOptions += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
    }
    var selectElem = $('#select_complaints .add_container.general_add select.select_stats');
    selectElem.html(complainOptions);
    selectElem.combobox();
    $('#select_complaints .done_stat') .on('click', function (event) {
        event.preventDefault();
        $(this) .parent() .parent() .removeClass('active');
        var id = selectElem.val();
        var name = $('#select_complaints .add_container.general_add select.select_stats option:selected') .text();
        addNewComplain(id, name, data);
    });
}
// XXX: Never used???
function addNewComplain(id, name, data) {
    //content = content.replace(/{{name}}/g, elem.attr('data-title'));
    if (addedComplains.length < 5) {
        var repeated = false;
        for (var i in addedComplains) {
            if (addedComplains[i].id == id) {
                repeated = true;
                console.log('repeated!');
            }
        }
        if (!repeated) {
            console.log('adding complain');
            var content = $('#complain_template') .html();
            //content = content.replace(/{{name}}/g, name);
            //content = content.replace(/{{id}}/g, id);
            content = content.replace(/\[\[name\]\]/g, name);
            content = content.replace(/\[\[id\]\]/g, id);
            //console.log(content);
            var ulElem = $('#select_complaints ul');
            ulElem.prepend(content);
            var itemData = {
            };
            for (var i in data) {
                if (data[i].id == id) {
                    itemData = data[i];
                    addedComplains.push(data[i]);
                    break;
                }
            }
            //console.log('ITEM DATA');
            ///console.log(itemData);

            var adapter = new CronicalConditionsAdapter();
            var params = adapter.getParameters(itemData, '#E56666');
            //console.log(params);
            var preffix = 'canvas_12_custom_';
            //console.log(params);
            //Start graph
            drawComplainGraph(params, id, preffix);
            $.post(_api_urls[_api_env].complains_post, {
                id_complaint: id
            });
            if (addedComplains.length == 5) {
                $('#complains_adder_container') .hide();
            }
        }
    }
}
function drawBloodDrops(data, user_data) {
    var content,
    blood,
    height;
    var user_type = user_data.id || 0;

    for (var i in data) {
        blood = data[i];
        var heightPercentage = blood.percentage;
        if (heightPercentage < 10) heightPercentage = 8;
        //height = (blood.percentage*130)/100;
        height = (heightPercentage * 130) / 100;
        content = '';
        content = $('#blood_template') .html();
        content = content.replace(/\[\[name\]\]/g, blood.name);
        content = content.replace(/\[\[percentage\]\]/g, blood.percentage);
        content = content.replace(/\[\[id\]\]/g, blood.id);
        content = content.replace(/\[\[height\]\]/g, 0);
        $('#chose_type') .append(content);
        $('#blood_type_' + blood.id + ' .porcent_div') .delay(300) .animate({
            height: height + 'px'
        }, 300);
    }
    $('#chose_type li') .click(function (event) {
        event.preventDefault();
        $('#chose_type li') .removeClass('active');
        $(this) .addClass('active');
        var typeId = $(this) .attr('data-id');
        $.post(_api_urls[_api_env].blood_post, {
            id_blood_type: typeId
        });
    });
    $('#chose_type #blood_type_' + user_type).addClass("active");
}
function drawSleepGraph(data, data_user) {
    var maxValue = 0;
    for (var i in data.days) {
        if (data.days[i].hours > maxValue) maxValue = data.days[i].hours;
    }
    for (var i in data_user.days) {
        if (data_user.days[i].hours > maxValue) maxValue = data_user.days[i].hours;
    }
    maxValue = Math.ceil(maxValue);
    var adapter = new SleepAdapter();
    var result = adapter.getParameters(data, data_user, 684, maxValue, [
        2,
        4,
        6,
        8,
        10,
        12,
        14,
        16,
        18,
        20,
        22,
        24
    ]);
    //console.log(result);
    var r_14_1 = Raphael('canvas_14_1', 1103, 767);
    doubleAxisParams2 = {
        axis: 'both',
        barsAxis: 'x',
        drawAxis: true,
        drawLabels: true,
        rotateBarLabels: false,
        elements: result.elements,
        xAxis: {
            length: 1103,
            'stroke-width': 2,
            color: '#F1F2F2',
            labelsType: 'custom_bubbles',
            name: 'Day',
            labels: result.xLabels
        },
        yAxis: {
            length: 750,
            'stroke-width': 0,
            name: 'h',
            labels: result.yLabels
        },
        centerx: 30,
        centery: 743,
        canvasSize: [
            1093,
            767
        ]
    }
    doubleAxisBars2 = new EdBarChart(r_14_1, doubleAxisParams2);
    doubleAxisBars2.draw();
    $('#step_fourteen .bloq.left .number_stat h2') .html(pad(data.avg_hours, 2));
    $('#step_fourteen .bloq.right .number_stat h2') .html(pad(data_user.avg_hours, 2));
}
function drawGenomicsTraits(data, user_data) {
    $('#genomic_traits_container') .html('');
    var c = 0;
    itemsHtml = '';
    var finalData = [
    ];
    var first = true;
    for (var i in data) {
        var itemHtml = $('#genomics_traits_graph_template') .html();
        itemHtml = itemHtml.replace(/\[\[canvas_id\]\]/g, data[i].id);
        itemHtml = itemHtml.replace(/\[\[center_text\]\]/g, data[i].name);
        if (first === true) {
            first = false;
            //console.log('REPLACE FIRST TRUE');
            itemHtml = itemHtml.replace(/\[\[hint_style\]\]/g, '');
        } else {
            //console.log('REPLACE FIRST FALSE');
            itemHtml = itemHtml.replace(/\[\[hint_style\]\]/g, 'display:none;');
        }
        if(user_data.length > 0){
	        for (var j in user_data) {
	            if (user_data[j].id == data[i].id) {
	                if (user_data[j].value == data[i].values[0]) {
	                    itemHtml = itemHtml.replace(/\[\[porcent_user\]\]/g, data[i].values[0].percentage);
	                    itemHtml = itemHtml.replace(/\[\[user_trait_name\]\]/g, data[i].values[0].name);
	                    itemHtml = itemHtml.replace(/\[\[porcent_global\]\]/g, data[i].values[1].percentage);
	                    itemHtml = itemHtml.replace(/\[\[global_trait_name\]\]/g, data[i].values[1].name);
	                    firstItem = {
	                        percentage: data[i].values[0].percentage,
	                        color: '#E56666'
	                    };
	                    secondItem = {
	                        percentage: data[i].values[1].percentage,
	                        color: '#7737C7'
	                    };
	                } else {
	                    itemHtml = itemHtml.replace(/\[\[porcent_user\]\]/g, data[i].values[1].percentage);
	                    itemHtml = itemHtml.replace(/\[\[user_trait_name\]\]/g, data[i].values[1].name);
	                    itemHtml = itemHtml.replace(/\[\[porcent_global\]\]/g, data[i].values[0].percentage);
	                    itemHtml = itemHtml.replace(/\[\[global_trait_name\]\]/g, data[i].values[0].name);
	                    firstItem = {
	                        percentage: data[i].values[0].percentage,
	                        color: '#7737C7'
	                    };
	                    secondItem = {
	                        percentage: data[i].values[1].percentage,
	                        color: '#E56666'
	                    };
	                }
	            }
	        }
        }else{
            itemHtml = itemHtml.replace(/\[\[porcent_user\]\]/g, data[i].values[1].percentage);
            itemHtml = itemHtml.replace(/\[\[user_trait_name\]\]/g, data[i].values[1].name);
            itemHtml = itemHtml.replace(/\[\[porcent_global\]\]/g, data[i].values[0].percentage);
            itemHtml = itemHtml.replace(/\[\[global_trait_name\]\]/g, data[i].values[0].name);
            firstItem = {
                percentage: data[i].values[0].percentage,
                color: '#7737C7'
            };
            secondItem = {
                percentage: data[i].values[1].percentage,
                color: '#E56666'
            };
        }
        if (c === 0) {
            itemsHtml += '<div class="container_graphs">' + itemHtml;
            c++;
        } else if (c % 2 === 0) {
            itemsHtml += itemHtml + '<div class="divisor"></div></div>';
            c = 0;
        } else {
            itemsHtml += itemHtml;
            c++;
        }
        var finalDataItem = {
            firstItem: firstItem,
            secondItem: secondItem,
            name: data[i].name,
            id: data[i].id
        }
        finalData.push(finalDataItem);
    }
    $('#genomic_traits_container') .html(itemsHtml);
    //console.log('FINAL DATA ARRAY');
    //console.log(finalData);
    for (var i in finalData) {
        //console.log('final data looping '+i);
        //console.log('final data looping');
        var elements = [
            {
                percentage: finalData[i].firstItem.percentage,
                color: finalData[i].firstItem.color,
                text: ''
            },
            {
                percentage: finalData[i].secondItem.percentage,
                color: finalData[i].secondItem.color,
                text: ''
            }
        ]
        var r = Raphael('genomics_trait_canvas_' + finalData[i].id, 310, 310);
        var animatedPie = new EdAnimatedPie(r, elements, {
            animationTime: 900,
            easing: '<',
            useAnimationDelay: false,
            lineWidth: 55,
            fontSize: 20,
            centerx: 155,
            centery: 155,
            radius: 122,
            borderColor: '#F7F2ED',
            borderMargin: 0,
            drawReferences: false,
            drawCenterImage: false,
            drawCenterText: true,
            bubbleColor: '#3F4B5B',
            centerText: {
                color: '#5B6D7F',
                size: '26',
                font: 'Omnes-Semibold',
                text: '',
                xOffset: [
                    0,
                    0
                ],
                unit: '',
                unitFont: 'Omnes-Semibold',
                unitSize: 30,
                unitOffset: [
                    45,
                    30
                ],
                unitOffsetTop: 5
            }
        });
        animatedPie.draw();
    }
}
function drawGenomicsDrugs(data, user_data) {
    var section = 'alcohol';
    for (i = 0; i < 2; i++) {
        if (i == 1) section = 'pills';
        for (j = 1; j <= 3; j++) {
            var perc = data[i].values[j - 1].percentage;
            var name = data[i].values[j - 1].name;
            var id = data[i].id;
            var pxWidth = (perc * 620) / 100;
            var selectorStr = '.container_data.' + section + ' .block.right .' + section + '_' + j;
            $(selectorStr) .attr('data-name', name);
            $(selectorStr + ' p') .html(name);
            $(selectorStr + ' .porcent_data') .css('width', pxWidth + 'px')
            $(selectorStr + ' .porcent_text') .html('<p>' + perc + '<strong>%</strong></p>');
        }
    }
    for (var z in user_data) {
        $('div[data-name="' + user_data[z].value + '"]') .addClass('active');
    }
}
function drawGenomicsRisks(data, user_data) {

	if (user_data.length > 0){
		$('#step_nineteen .pages_container') .html('');
	    for (var i in data) {
	        itemHtml = $('#genomic_risks_item_template') .html();
	        itemHtml = itemHtml.replace(/\[\[name\]\]/g, data[i].name);
	        itemHtml = itemHtml.replace(/\[\[global_percent\]\]/g, data[i].percentage);
	        for (var j in user_data) {
	            if (data[i].id == user_data[j].id) {
	                itemHtml = itemHtml.replace(/\[\[user_percent\]\]/g, user_data[j].percentage);
	            }
	        }
	        $('#step_nineteen .pages_container') .append(itemHtml);
	    }
	}else{
		$('#step_nineteen').hide();
	}



}
function deleteUserData(url, param, value, callback) {
    $.ajax({
        url: url + '?' + param + '=' + value,
        //data: param+'='+value,
        type: 'DELETE',
        success: function (result) {
            callback(result);
        }
    });
}
function deleteUserComplain(id) {
    $('.user_complain[data-id=' + id + ']') .remove();
    for (var i in addedComplains) {
        if (addedComplains[i].id == id) {
            addedComplains.splice(i, 1);
        }
    }
    deleteUserData(_api_urls[_api_env].complains_delete, 'id_complaint', id, function () {
    });
    $('#complains_adder_container') .show();
}
window.onload = function () {
    /*********** PIE CHARTS *******************/
    $.getJSON(_api_urls[_api_env].social_reach, function (data) {
        //console.log(data);
        drawSocialGraph(data);
    });
    $.getJSON(_api_urls[_api_env].share, function (data) {
        drawShareGraphs(data);
    });
    $.getJSON(_api_urls[_api_env].education, function (data) {
        drawEducationGraph(data);
    });
    $.getJSON(_api_urls[_api_env].work, function (data) {
        //console.log('WORK!!!!');
        drawWorkGraph(data);
    });
    $.getJSON(_api_urls[_api_env].exercise, function (data) {
        drawExerciseGraphs(data);
    });
    $.getJSON(_api_urls[_api_env].steps, function (data) {
        drawStepsGraph(data);
    });
    $.getJSON(_api_urls[_api_env].miles, function (data) {
        //console.log('MILES!');
        drawMilesGraph(data);
    });
    $.getJSON(_api_urls[_api_env].hours, function (data) {
        //console.log('HOURS!');
        drawHoursGraph(data);
    });
    $('.global_nutrient_data .block.right') .html('');
    $('.user_nutrient_data .block.right') .html('');
    $.getJSON(_api_urls[_api_env].nutrients, function (data) {
        drawNutrientProportionGraph(data);
    });
    $.getJSON(_api_urls[_api_env].weight, function (data) {
        //console.log('WEIGHT!');
        $('.weight_values .man .value') .html(Math.round(data.global_data.men.value));
        $('.weight_values .woman .value') .html(Math.round(data.global_data.women.value));
        $('#weight_number') .html(data.user_data.value);
    });
    $.getJSON(_api_urls[_api_env].height, function (data) {
        //console.log('WEIGHT!');
        $('.height_values .man .value') .html(Math.round(data.global_data.men.value * 100)/100);
        $('.height_values .woman .value') .html(Math.round(data.global_data.women.value * 100)/100);
        //console.log('HEIGHT USER: '+data.user_data.value);
        $('#height_number') .html(data.user_data.value);
    });
    $.getJSON(_api_urls[_api_env].bmi, function (data) {
        //console.log('WEIGHT!');
        $('.bmi_values .man .value') .html(data.global_data.men.value);
        $('.bmi_values .woman .value') .html(data.global_data.women.value);
    });
    $.getJSON(_api_urls[_api_env].user_exercise, function (data) {
        for (var i = 1; i <= data.length; i++) {
            $($('.you_cards ul li') [i]) .html('<p><span>' + data[i - 1].title + '</span><br />' + data[i - 1].message + '</p>');
        }
    });
    doCronicalConditionsSection();
    $.getJSON(_api_urls[_api_env].cronical_conditions_list, function (data) {
        cronicalsList = data;
        setupAddCronicals(data);
    });
    $.getJSON(_api_urls[_api_env].complains_user, function (user_data) {
        $.getJSON(_api_urls[_api_env].complains_top5, function (data) {
            for (var i in data) {
                var num = parseInt(i) + 1;
                drawComplainsTop5Item(data[i], num);
            }
        });
        for (var j in user_data) {
            addNewComplain(user_data[j].id, user_data[j].name, user_data);
        }
    });
    $.getJSON(_api_urls[_api_env].complains_list, function (data) {
        complainsList = data;
        createComplainsAutocompleter(data);
    });
    $.getJSON(_api_urls[_api_env].blood_list, function (data) {
        $.getJSON(_api_urls[_api_env].blood_user, function (data_user) {
            drawBloodDrops(data, data_user);
        });
    });
    $.getJSON(_api_urls[_api_env].sleep_global, function (data) {
        $.getJSON(_api_urls[_api_env].sleep_user, function (data_user) {
            //console.log('STEPS!');
            drawSleepGraph(data, data_user);
        });
    });
    $.getJSON(_api_urls[_api_env].emotions_user, function (user_data) {
        $.getJSON(_api_urls[_api_env].emotions_top5, function (data) {
            for (var i in data) {
                var num = parseInt(i) + 1;
                drawEmotionsGraph(data[i], num, user_data);
            }
        });
    });
    $.getJSON(_api_urls[_api_env].emotions_list, function (data) {
        emotionsList = data;
        setupAddEmotions(data);
    });
    $.getJSON(_api_urls[_api_env].mood_global, function (data) {
        $.getJSON(_api_urls[_api_env].mood_user, function (data_user) {
            $('#mood_2 .ui-slider-handle') .html('<span>' + data.mood_avg + '</span>');
            $('#mood_1 .ui-slider-handle') .html('<span>' + data_user.mood_avg + '</span>');
            $('#mood_1') .slider('option', 'value', data_user.mood_avg);
            $('#mood_2') .slider('option', 'value', data.mood_avg);

            // FIXME: Use CSS classes
            if(data.mood_avg < data_user.mood_avg)
                $('#mood_2').css({ "z-index": 1000 })
            else
                $('#mood_1').css({ "z-index": 1000 })
        });
    });
    $.getJSON(_api_urls[_api_env].genomics_traits, function (data) {
        $.getJSON(_api_urls[_api_env].genomics_traits_user, function (user_data) {
            drawGenomicsTraits(data, user_data);
        });
    });
    $.getJSON(_api_urls[_api_env].genomics_drugs, function (data) {
        $.getJSON(_api_urls[_api_env].genomics_drugs_user, function (user_data) {
            drawGenomicsDrugs(data, user_data);
        });
    });
    $.getJSON(_api_urls[_api_env].genomics_risks, function (data) {
        $.getJSON(_api_urls[_api_env].genomics_risks_user, function (user_data) {
            //console.log('GENOMIC RISKS');
            //console.log(data);
            //console.log(user_data);
            drawGenomicsRisks(data, user_data);
        });
    });
};
$(document) .ready(function () {
    $('.delete_stat') .click(function () {
        //$('#complains_adder_container').hide();
        $('#complains_adder_container') .removeClass('active');
        return false;
    });
    $('.user_complain') .on('click', function () {
        deleteUserComplain($(this) .attr('data-id'));
        $('#complains_adder_container') .click();
    });
    $('#complains_top5 li') .on('click', function () {
        addNewComplain($(this) .attr('data-id'), $(this) .attr('data-name'), complainsList
        );
    });
    $('#age_select_value') .jStepper({
        minValue: 0,
        maxValue: 60,
        allowDecimals: false
    });
    $('#your_lvl_c li') .click(function (event) {
        var pos = $(this) .attr('ref');
        //line = animatedQuarterPie.lines[pos];
        for (var i in animatedQuarterPie.lines) {
            line = animatedQuarterPie.lines[i];
            if (pos == i) {
                line.animate({
                    'stroke': '#E56666'
                }, 500);
            } else {
                //line.animate({"stroke": animatedQuarterPie.colors[i]}, 500);
                line.animate({
                    'stroke': '#7737c7'
                }, 500);
            }
        }
        $.ajax({
            dataType: 'json',
            type: 'POST',
            url: _api_urls[_api_env].education_post,
            data: {
                education_level: animatedQuarterPie.elements[pos].server_key
            },
            success: function (data) {
                drawEducationGraph(data);
            }
        });
    });
    $('#age_select_form') .submit(function () {
        //console.log('form submitted!');
        var age = $('#age_select_value') .val();
        $('#canvas_4_1') .html('');
        $.ajax({
            dataType: 'json',
            type: 'POST',
            url: _api_urls[_api_env].work_post,
            data: {
                working_experience: age
            },
            success: function (data) {
                drawWorkGraph(data);
            }
        });
        return false;
    });
    $('#mood_1') .on('slidestop', function (event, ui) {
        $.ajax({
            dataType: 'json',
            type: 'POST',
            url: _api_urls[_api_env].mood_post,
            data: {
                mood_avg: $('#mood_1') .slider('value')
            },
            success: function (data) {
            }
        });
    });
    $('.close_cronical_card') .on('click', function () {
        $(this) .parent() .remove();
        var id = $(this) .parent() .attr('data-id');
        //console.log('DELETING CRONICAL ID: '+id);
        deleteUserData(_api_urls[_api_env].cronical_conditions_delete, $(this) .parent() .attr('data-param'), id, function (result) {
        });
        for (var i in cronicalGraphs) {
            //console.log('looping cronical graphs: '+i);
            if (i == id) {
                //console.log('found graph to deanimate!');
                var graph = cronicalGraphs[i];
                graph.lines[0].animate({
                    'stroke': '#7737C7'
                }, 500);
                graph.texts[0].animate({
                    'fill': '#7737C7'
                }, 500);
                graph.texts[1].animate({
                    'fill': '#7737C7'
                }, 500);
            }
        }
        return false;
    });
    $('.close_emotion_card') .on('click', function () {
        $(this) .parent() .remove();
        var id = $(this) .parent() .attr('data-id');
        //console.log('DELETING EMOTION ID: '+id);
        deleteUserData(_api_urls[_api_env].emotions_delete, $(this) .parent() .attr('data-param'), id, function (result) {
        });
        for (var i in emotionGraphs) {
            //console.log('looping emotion graphs: '+i);
            if (i == id) {
                //console.log('found emotion graph to deanimate!');
                var graph = emotionGraphs[i];
                graph.lines[0].animate({
                    'stroke': '#7737C7'
                }, 500);
                graph.texts[0].animate({
                    'fill': '#7737C7'
                }, 500);
                graph.texts[1].animate({
                    'fill': '#7737C7'
                }, 500);
            }
        }
        return false;
    });
});



var app = angular.module('app', []);

app.controller('weightHeightCtrl', function ($scope, $http, $sce) {

    $scope.height = 5;
    $scope.mass = 112;
    $scope.bmi = 0;

    var calculateBMI = function () {
        $scope.bmi = ($scope.mass/($scope.height*$scope.height*144))*703;
    }
    calculateBMI();

    $('#weight_slider').on('slidestop', function (event, ui) {
        $.ajax({
            dataType: 'json',
            type: 'POST',
            url: _api_urls[_api_env].weight,
            data: {
                unit: 'Lbs',
                value: $('#weight_slider') .slider('value')
            }
        });
        $scope.mass = $('#weight_slider').slider('value');
        $scope.$apply(calculateBMI);
    });
    $('#height_slider').on('slidestop', function (event, ui) {
        $.ajax({
            dataType: 'json',
            type: 'POST',
            url: _api_urls[_api_env].height,
            data: {
                unit: 'Ft',
                value: $('#height_slider') .slider('value')
            }
        });
        $scope.height = $('#height_slider') .slider('value');
        $scope.$apply(calculateBMI);
    });

});
